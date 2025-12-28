import os
import threading
import requests
import json
from dotenv import load_dotenv

load_dotenv()

class AIEngine:
    def __init__(self, response_callback):
        self.response_callback = response_callback
        # Aqui chamo a GROQ para ser o cérebro
        self.api_key = os.getenv("GROQ_API_KEY")
        
        self.url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "llama-3.3-70b-versatile" 
        self.system_prompt = "Você é um assistente técnico de TI. Responda de forma curta em português."

    def process_text(self, text):
        if not text: return
        # Quando o Google termina de transcrever, esta função é chamada
        print(f"Texto recebido do Google: {text}")
        threading.Thread(target=self._enviar_para_groq, args=(text,), daemon=True).start()

    def _enviar_para_groq(self, texto_transcrito):
        try:
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": texto_transcrito}
                ]
            }
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            print(f"Groq processando resposta...")
            response = requests.post(self.url, headers=headers, data=json.dumps(payload))
            
            if response.status_code == 200:
                data = response.json()
                resposta_final = data['choices'][0]['message']['content']
                print(" Sucesso!")
                self.response_callback(resposta_final)
            else:
                self.response_callback(f"Erro na Groq: {response.status_code}")
                
        except Exception as e:
            self.response_callback(f"Erro de conexão: {e}")