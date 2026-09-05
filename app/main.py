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
from tts_engine import TTSEngine

def main():
    if not os.getenv("GROQ_API_KEY"):
        print(" ERRO: GROQ_API_KEY não definida.")
       
    root = tk.Tk()
    app = OverlayWindow(root)
    tts = TTSEngine()
    
    # Variável para acumular o texto que será falado no final
    acumulador_fala = []

    def ao_receber_chunk(chunk, is_final):
        app.append_response_chunk(chunk, is_final)
        
        if not is_final:
            acumulador_fala.append(chunk)
        else:
            if chunk:
                acumulador_fala.append(chunk)
            # Ao finalizar, manda falar a frase inteira
            texto_completo = "".join(acumulador_fala)
            tts.speak(texto_completo)
            acumulador_fala.clear()
    
    ai_engine = AIEngine(ao_receber_chunk)

    def ao_transcrever_audio(texto_ouvido):
        app.update_transcription(texto_ouvido)
        ai_engine.process_text(texto_ouvido)

    audio_manager = AudioManager(ao_transcrever_audio)

    print(" Iniciando Sistema Voice AI (Com TTS)...")
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
