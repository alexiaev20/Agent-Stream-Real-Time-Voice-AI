import threading
import speech_recognition as sr
import time
from app.utils import get_logger  
from app.config import Config    

logger = get_logger(__name__)

class AudioManager:
    def __init__(self, update_callback):
        self.update_callback = update_callback
        self.recognizer = sr.Recognizer()
        self.is_listening = False
        
        # Usa as configurações do Config.py
        self.device_index = self._find_vb_cable_index()
        self.microphone = sr.Microphone(device_index=self.device_index)
        
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.energy_threshold = Config.ENERGY_THRESHOLD 

    def _find_vb_cable_index(self):
        """Busca o driver VB-CABLE para capturar o áudio da chamada."""
        try:
            logger.info("Buscando dispositivos de áudio...")
            names = sr.Microphone.list_microphone_names()
            for index, name in enumerate(names):
                # Busca drivers de loopback
                if any(x in name for x in ["CABLE Output", "VB-Audio", "Mixagem Estéreo", "Stereo Mix"]):
                    logger.info(f"Dispositivo de Captura encontrado: {name} (Index: {index})")
                    return index
            
            logger.warning("VB-CABLE não encontrado. O sistema usará o microfone padrão.")
            return None
        except Exception as e:
            logger.error(f"Erro ao listar dispositivos de áudio: {e}")
            return None

    def start_listening(self):
        self.is_listening = True
        threading.Thread(target=self._listen_loop, daemon=True).start()

    def _listen_loop(self):
        try:
            with self.microphone as source:
                # Ajuste de ruído 
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                logger.info("Escutando áudio do sistema (via VB-CABLE/Loopback)...")
                
                while self.is_listening:
                    try:
                        audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=15)
                        
                        try:
                            text = self.recognizer.recognize_google(audio, language=Config.LANGUAGE)
                            
                            if text:
                                logger.info(f"Transcrição detectada: {text[:50]}...")
                                self.update_callback(text)
                                
                        except sr.UnknownValueError:
                            # Silêncio ou áudio não reconhecido
                            pass 
                        except sr.RequestError as e:
                            logger.error(f"Erro no serviço de transcrição do Google: {e}")

                    except sr.WaitTimeoutError:
                        continue 
                    except Exception as e:
                        logger.error(f"Erro no loop de captura: {e}")
                        time.sleep(1)
        except Exception as e:
            logger.error(f"Falha crítica ao acessar o microfone: {e}")

    def stop_listening(self):
        self.is_listening = False
        logger.info("Captura de áudio encerrada.")