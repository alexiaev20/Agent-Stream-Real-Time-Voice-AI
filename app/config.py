import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configurações centralizadas """
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
   
    MODEL_NAME = "llama-3.3-70b-versatile" 
    SYSTEM_PROMPT = "Você é um assistente técnico de TI. Responda de forma curta em português."
    # Configurações de Áudio
    LANGUAGE = 'pt-BR'
    ENERGY_THRESHOLD = 300