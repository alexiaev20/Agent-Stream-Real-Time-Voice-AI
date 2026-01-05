import time
from app.ai_engine import AIEngine
from app.utils import get_logger

logger = get_logger("IntegrationTest")

def meu_callback(resposta):
    """Função que será chamada quando a IA retornar a resposta."""
    print("\n" + "="*50)
    print(f"RESPOSTA DA IA: {resposta}")
    print("="*50 + "\n")

# Groq/Llama 3
try:
    engine = AIEngine(response_callback=meu_callback)

    logger.info("Iniciando teste de integração com a API...")
    pergunta = "Olá, descreva em uma frase o que é computação em nuvem."
    
    logger.info(f"Enviando pergunta: '{pergunta}'")
    engine.process_text(pergunta)

    logger.info("Aguardando processamento timeout de 10s...")
    for i in range(10, 0, -1):
        time.sleep(1)
      

except Exception as e:
    logger.error(f"Falha ao executar o teste de integração: {e}")

finally:
    logger.info("Teste finalizado.")