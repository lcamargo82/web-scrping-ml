
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

with open("models_list.txt", "w") as f:
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                f.write(f"{m.name}\n")
        print("Modelos listados em models_list.txt")
    except Exception as e:
        f.write(f"Erro: {e}")
        print(f"Erro: {e}")
