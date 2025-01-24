import tkinter as tk
from tkinter import ttk, messagebox
import openai
from deep_translator import GoogleTranslator
import pyttsx3
from dotenv import load_dotenv
import os
import pyperclip

class ConfigDialog:
   def __init__(self, parent):
       self.dialog = tk.Toplevel(parent)
       self.dialog.title("API-konfiguration")
       
       ttk.Label(self.dialog, text="OpenAI API-nyckel:").pack(pady=5)
       self.api_key = ttk.Entry(self.dialog, width=50)
       self.api_key.pack(pady=5)
       
       ttk.Button(self.dialog, text="Spara", command=self.save).pack(pady=10)
       
   def save(self):
       with open('.env', 'w') as f:
           f.write(f'OPENAI_API_KEY={self.api_key.get()}')
       self.dialog.destroy()

class Skrivare:
   def __init__(self):
       self.window = tk.Tk()
       self.window.title("Skrivhjälp")
       self.window.geometry("800x600")
       
       self.setup_api()
       self.setup_ui()
       self.setup_tts()
       
   def setup_api(self):
       load_dotenv()
       if not os.getenv('OPENAI_API_KEY'):
           self.show_config_dialog()
       openai.api_key = os.getenv('OPENAI_API_KEY')
       
   def setup_tts(self):
       self.engine = pyttsx3.init()
       voices = self.engine.getProperty('voices')
       self.engine.setProperty('voice', voices[0].id)
       
   def setup_ui(self):
       main_frame = ttk.Frame(self.window, padding="10")
       main_frame.grid(sticky="nsew")
       
       # Input section
       ttk.Label(main_frame, text="Original text:").grid(row=0, column=0, sticky="w")
       self.input_text = tk.Text(main_frame, height=8)
       self.input_text.grid(row=1, column=0, columnspan=2, sticky="nsew")
       
       # Processed text section
       ttk.Label(main_frame, text="Processed text:").grid(row=2, column=0, sticky="w")
       self.output_text = tk.Text(main_frame, height=8)
       self.output_text.grid(row=3, column=0, columnspan=2, sticky="nsew")
       
       # Translation section
       ttk.Label(main_frame, text="Target language:").grid(row=4, column=0, sticky="w")
       self.lang_select = ttk.Combobox(main_frame, values=["en", "es", "fr", "de"])
       self.lang_select.set("en")
       self.lang_select.grid(row=4, column=1, sticky="w")
       
       self.translated_text = tk.Text(main_frame, height=8)
       self.translated_text.grid(row=5, column=0, columnspan=2, sticky="nsew")
       
       # Buttons
       button_frame = ttk.Frame(main_frame)
       button_frame.grid(row=6, column=0, columnspan=2, pady=10)
       
       ttk.Button(button_frame, text="Process", command=self.process_text).pack(side=tk.LEFT, padx=5)
       ttk.Button(button_frame, text="Read", command=self.speak_text).pack(side=tk.LEFT, padx=5)
       ttk.Button(button_frame, text="Translate", command=self.translate_text).pack(side=tk.LEFT, padx=5)
       ttk.Button(button_frame, text="Copy", command=self.copy_to_clipboard).pack(side=tk.LEFT, padx=5)
       
       # Configure grid weights
       self.window.grid_rowconfigure(0, weight=1)
       self.window.grid_columnconfigure(0, weight=1)
       main_frame.grid_columnconfigure(1, weight=1)
       
   def show_config_dialog(self):
       ConfigDialog(self.window)
       
   def process_text(self):
       try:
           response = openai.ChatCompletion.create(
               model="gpt-4",
               messages=[
                   {"role": "system", "content": "Korrigera och förbättra följande text som kan vara skriven av en dyslektiker:"},
                   {"role": "user", "content": self.input_text.get("1.0", "end-1c")}
               ]
           )
           self.output_text.delete("1.0", tk.END)
           self.output_text.insert("1.0", response.choices[0].message.content)
       except openai.error.OpenAIError as e:
           messagebox.showerror("Error", f"OpenAI error: {str(e)}")
       except Exception as e:
           messagebox.showerror("Error", f"Unexpected error: {str(e)}")

   def translate_text(self):
       try:
           translator = GoogleTranslator(target=self.lang_select.get())
           translated = translator.translate(self.output_text.get("1.0", "end-1c"))
           self.translated_text.delete("1.0", tk.END)
           self.translated_text.insert("1.0", translated)
       except Exception as e:
           messagebox.showerror("Error", f"Translation error: {str(e)}")

   def speak_text(self):
       try:
           self.engine.say(self.output_text.get("1.0", "end-1c"))
           self.engine.runAndWait()
       except Exception as e:
           messagebox.showerror("Error", f"Text-to-speech error: {str(e)}")
           
   def copy_to_clipboard(self):
       pyperclip.copy(self.output_text.get("1.0", "end-1c"))
       messagebox.showinfo("Success", "Text copied to clipboard")

   def run(self):
       self.window.mainloop()

if __name__ == "__main__":
   app = Skrivare()
   app.run()