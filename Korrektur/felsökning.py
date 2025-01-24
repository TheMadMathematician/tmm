import openai

key = "sk-proj-yyhuWMFpsL-tUGbvoKefm-ArTWveiCqa1gwl12nkuBCRe1yYrQ88TC7uWT3BlbkFJqHs_kWhUUUYNePObjOuD-Pw5z9xwc0Z1ldK2P5PXeKbzMVnlyaShcz2RQA"

try:
    client = openai.OpenAI(api_key = key)
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": "Comment on hello world"}],
        model="text-davinci-003",
        max_tokens=5
    )
    print(response.choices[0].text.strip())
except Exception as e:
    print(f"An error occurred: {e}")
