import os
import threading
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

class AIEngine:
    def __init__(self, response_callback):
        self.response_callback = response_callback
        self.api_key = os.getenv("GROQ_API_KEY")
        
        if self.api_key:
            self.client = Groq(api_key=self.api_key)
        else:
            self.client = None
            
        self.model = "llama-3.3-70b-versatile"
        
        # Memória de Contexto
        self.history = [
            {"role": "system", "content": "Você é um assistente técnico de TI. Responda de forma curta em português."}
        ]

    def process_text(self, text):
        if not text or not self.client: return
        print(f"Texto recebido (Iniciando raciocínio): {text}")
        
        # Anexa o que o usuário falou na memória
        self.history.append({"role": "user", "content": text})
        
        # Mantém apenas as últimas 10 interações (evitar limite de tokens)
        if len(self.history) > 11:
            self.history = [self.history[0]] + self.history[-10:]
            
        threading.Thread(target=self._enviar_para_groq, daemon=True).start()

    def _enviar_para_groq(self):
        try:
            print("Groq processando resposta (Streaming)...")
            
            # Chama a Groq no modo stream
            stream = self.client.chat.completions.create(
                messages=self.history,
                model=self.model,
                stream=True
            )
            
            resposta_completa = ""
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    pedaco = chunk.choices[0].delta.content
                    resposta_completa += pedaco
                    # Envia o pedaço imediatamente para a GUI
                    self.response_callback(pedaco, is_final=False)
            
            # Anexa a resposta final da IA na memória para contexto futuro
            self.history.append({"role": "assistant", "content": resposta_completa})
            self.response_callback("", is_final=True)
            print("Resposta concluída!")
                
        except Exception as e:
            error_msg = f"Erro de conexão com a Groq: {e}"
            print(error_msg)
            self.response_callback(error_msg, is_final=True)
