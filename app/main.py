import tkinter as tk
import sys
from app.audio_manager import AudioManager
from app.ai_engine import AIEngine
from app.gui_overlay import OverlayWindow
from app.config import Config
from app.utils import get_logger

logger = get_logger("Main")

def main():
    # Validação de segurança 
    if not Config.GROQ_API_KEY:
        logger.error("ERRO: GROQ_API_KEY não configurada no arquivo .env")
        sys.exit(1)

    root = tk.Tk()
    app = OverlayWindow(root)

    #  Quando a Groq responder, aparece na janelinha
    def ao_receber_resposta_ia(texto_ia):
        app.update_response(texto_ia)
    
    ai_engine = AIEngine(ao_receber_resposta_ia)

    # Quando o Gemini terminar de ouvir, manda para a Groq
    def ao_transcrever_audio(texto_ouvido):
        app.update_transcription(texto_ouvido)
        ai_engine.process_text(texto_ouvido)

    audio_manager = AudioManager(ao_transcrever_audio)
    audio_manager.start_listening()

    try:
        root.mainloop()
    except KeyboardInterrupt:
        logger.info("Encerrando Agent-Stream...")
    finally:
        audio_manager.stop_listening()
        sys.exit(0)

if __name__ == "__main__":
    main()