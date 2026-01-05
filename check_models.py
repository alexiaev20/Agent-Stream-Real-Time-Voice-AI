import os
from google import genai
from dotenv import load_dotenv
from app.utils import get_logger # Mantendo o padrão de logs do projeto

load_dotenv()
logger = get_logger("CheckModels")

def check_google_models():
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        logger.error("GOOGLE_API_KEY não encontrada no arquivo .env!")
        return

    try:
        client = genai.Client(api_key=api_key)
        logger.info("Conectado ao Google GenAI. Listando modelos compatíveis:")
        
        # Filtra apenas modelos que suportam 
        models = client.models.list_models()
        for m in models:
            if 'generateContent' in m.supported_generation_methods:
                print(f"  > Modelo: {m.name:30} | Status: Pronto")
                
        logger.info("Verificação concluída com sucesso.")
        
    except Exception as e:
        logger.error(f"Erro ao validar integração com Google GenAI: {e}")

if __name__ == "__main__":
    check_google_models()