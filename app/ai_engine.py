import threading
import requests
import json
from app.config import Config
from app.utils import get_logger

logger = get_logger(__name__)

class AIEngine:
    def __init__(self, response_callback):
        self.response_callback = response_callback
        self.url = "https://api.groq.com/openai/v1/chat/completions"

    def process_text(self, text):
        if not text: return
        logger.info(f"Processando áudio transcrito: {text[:50]}...")
        threading.Thread(target=self._enviar_para_groq, args=(text,), daemon=True).start()

    def _enviar_para_groq(self, texto_transcrito):
        try:
            payload = {
                "model": Config.MODEL_NAME,
                "messages": [
                    {"role": "system", "content": Config.SYSTEM_PROMPT},
                    {"role": "user", "content": texto_transcrito}
                ]
            }
            headers = {
                "Authorization": f"Bearer {Config.GROQ_API_KEY}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(self.url, headers=headers, data=json.dumps(payload), timeout=10)
            
            if response.status_code == 200:
                resposta = response.json()['choices'][0]['message']['content']
                logger.info("Resposta recebida da Groq.")
                self.response_callback(resposta)
            else:
                logger.error(f"Erro na API Groq: {response.status_code}")
        except Exception as e:
            logger.error(f"Falha na comunicação com a IA: {e}")