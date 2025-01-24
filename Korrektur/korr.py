import openai
import os
from difflib import Differ

# Ange din OpenAI API-nyckel här
key = "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"

def load_text_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def save_text_to_file(file_path, text):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text)

def split_text_into_blocks(text, max_tokens=32000):
    sentences = text.split('.')
    blocks = []
    current_block = ""
    current_tokens = 0

    for sentence in sentences:
        tokens_in_sentence = len(sentence.split()) + 1  # +1 for the period
        if current_tokens + tokens_in_sentence > max_tokens:
            blocks.append(current_block)
            current_block = sentence + '.'
            current_tokens = tokens_in_sentence
        else:
            current_block += sentence + '.'
            current_tokens += tokens_in_sentence

    if current_block:  # Add any remaining text
        blocks.append(current_block)

    return blocks

def correct_text_block(text_block):
    client = openai.OpenAI(api_key = key)
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": """
            Du är en mycket noggrann och erfaren korrekturläsare och språkgranskare. Din uppgift är att korrekturläsa texten och komma med förslag på förbättringar utan att ändra på textens mening eller intention. Följ dessa instruktioner noggrant:

            1. Stavfel och felstavningar: Korrigera alla stavfel och felstavningar.
            2. Grammatik: Rätta grammatiska fel, inklusive felaktig användning av verbformer, tempus, prepositioner och subjekt-verb-överensstämmelse.
            3. Upprepade ord och redundans: Identifiera och ta bort onödiga upprepningar av ord eller fraser, samt eliminera redundanta uttryck.
            4. Onödig användning av adverb och stoppord: Försök att minimera användningen av överflödiga adverb och stoppord utan att påverka textens flöde eller betydelse.
            5. Satsstruktur och läsbarhet: Förbättra meningsbyggnad och satsstruktur där det är nödvändigt för att förbättra läsbarheten. Använd korrekta skiljetecken för att tydliggöra textens struktur.
            6. Formatering: Håll ögonen på felaktig eller inkonsekvent användning av stora och små bokstäver, samt andra formateringsfel.
            7. Ton och stil: Behåll den ursprungliga tonen och stilen i texten. Gör inte ändringar som påverkar författarens röst eller textens övergripande stil.
            8. Märkning av ändringar: Märk alla ändringar tydligt för att underlätta jämförelse med originaltexten. Använd t.ex. överstuken och rödfärgad text för föreslagna strykningar och grönfärgad text (mörkt grön för läsligheten) för föreslagna nya ord och sektioner. Helt omskriva sektioner kan färgas blåa. 

            Observera att du inte ska göra några ändringar som påverkar berättelsen, karaktärernas utveckling, ploten, eller andra kreativa aspekter av texten. Ditt fokus ska vara på att förbättra textens tekniska och språkliga aspekter.
            """},
            {"role": "user", "content": text_block}
        ],
        max_tokens=32000,
        temperature=0.5
    )

    return response.choices[0].message['content']

def highlight_differences(original_text, corrected_text):
    differ = Differ()
    diff = differ.compare(original_text.splitlines(), corrected_text.splitlines())
    highlighted_text = []
    
    for line in diff:
        if line.startswith('+ '):
            highlighted_text.append(f"<ins style='color: green;'>{line[2:]}</ins>")
        elif line.startswith('- '):
            highlighted_text.append(f"<del style='color: red;'>{line[2:]}</del>")
        else:
            highlighted_text.append(line[2:])
    
    return "\n".join(highlighted_text)

def process_text_file(input_file_path, output_file_path):
    text = load_text_from_file(input_file_path)
    blocks = split_text_into_blocks(text)
    corrected_text = ""

    for block in blocks:
        corrected_block = correct_text_block(block)
        corrected_text += corrected_block + "\n\n"

    highlighted_text = highlight_differences(text, corrected_text)
    save_text_to_file(output_file_path, highlighted_text)
    print(f"Korrekturläsningen är klar och sparad i {output_file_path}")

if __name__ == "__main__":
    input_file_path = "sample.txt"  # Ange sökvägen till din inmatningsfil
    output_file_path = "corrected_text.html"  # Ange sökvägen till din utmatningsfil
    
    process_text_file(input_file_path, output_file_path)
