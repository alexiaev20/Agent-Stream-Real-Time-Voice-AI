
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

try:
    print("Listando modelos disponíveis:")
    for m in client.models.list_models():
        print(f"- {m.name}")
except Exception as e:
    print(f"Erro ao listar modelos: {e}")
