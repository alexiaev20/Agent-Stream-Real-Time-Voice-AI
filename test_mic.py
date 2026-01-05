from app.ai_engine import AIEngine
import time

def meu_callback(resposta):
    # Isso vai imprimir a resposta do Gemini na tela
    print(f"\n[GEMINI RESPONDEU]: {resposta}")

# Inicializa a IA 
engine = AIEngine(response_callback=meu_callback)

print("Enviando pergunta para o Gemini...")
engine.process_text("Olá, descreva em uma frase o que é computação em nuvem.")

# O programa PRECISA esperar aqui, senão ele fecha antes do Google responder
print("Aguardando resposta do Google (não feche o terminal)...")
time.sleep(10)