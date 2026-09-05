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
    if not os.getenv("GROQ_API_KEY"):
        print(" ERRO: GROQ_API_KEY não definida.")
       
    root = tk.Tk()
    app = OverlayWindow(root)

    # Callback alterado para streaming
    def ao_receber_chunk(chunk, is_final):
        app.append_response_chunk(chunk, is_final)
    
    ai_engine = AIEngine(ao_receber_chunk)

    def ao_transcrever_audio(texto_ouvido):
        app.update_transcription(texto_ouvido)
        ai_engine.process_text(texto_ouvido)

    audio_manager = AudioManager(ao_transcrever_audio)

    print(" Iniciando Sistema Voice AI...")
    audio_manager.start_listening()

    try:
        root.mainloop()
    except KeyboardInterrupt:
        print(" Encerrando...")
    finally:
        audio_manager.stop_listening()
        sys.exit(0)

if __name__ == "__main__":
    main()
