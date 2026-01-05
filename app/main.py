import tkinter as tk
import os
import sys
from dotenv import load_dotenv


load_dotenv()


current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from audio_manager import AudioManager
from ai_engine import AIEngine
from gui_overlay import OverlayWindow

def main():
    # Validação de segurança 
    if not os.getenv("GROQ_API_KEY"):
        print(" ERRO: GROQ_API_KEY ")
       
    #  (Tkinter)
    root = tk.Tk()
    app = OverlayWindow(root)

    # 2. Quando a Groq responder, aparece na janelinha
    def ao_receber_resposta_ia(texto_ia):
        app.update_response(texto_ia)
    
    
    ai_engine = AIEngine(ao_receber_resposta_ia)

    # Quando o Gemini terminar de ouvir, manda para a Groq
    def ao_transcrever_audio(texto_ouvido):
        #
        app.update_transcription(texto_ouvido)
        # 
        ai_engine.process_text(texto_ouvido)

    #  o ouvido 
    audio_manager = AudioManager(ao_transcrever_audio)

    print(" Iniciando captura de áudio ...")
    audio_manager.start_listening()

    print(" Abrindo o Agente...")
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\n Encerrando sistema...")
    finally:
        audio_manager.stop_listening()
        sys.exit(0)

if __name__ == "__main__":
    main()