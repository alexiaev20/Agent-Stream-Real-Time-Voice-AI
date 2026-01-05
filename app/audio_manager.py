import threading
import speech_recognition as sr
import queue
import time

class AudioManager:
    def __init__(self, update_callback):
        self.update_callback = update_callback
        self.recognizer = sr.Recognizer()
        self.is_listening = False
        
        # identifica o  VB-CABLE
        self.device_index = self._find_vb_cable_index()
        self.microphone = sr.Microphone(device_index=self.device_index)
        
        # sensibilidade de vozes de chamadas 
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.energy_threshold = 300 

    def _find_vb_cable_index(self):
        """Busca o driver VB-CABLE para capturar o áudio da chamada."""
        try:
            print(" Encontrando dispositivo de audio..")
            for index, name in enumerate(sr.Microphone.list_microphone_names()):
                if "CABLE Output" in name or "VB-Audio" in name or "Mixagem Estéreo" in name:
                    print(f" Dispositivo de Captura de Chamada encontrado: {name} (Index: {index})")
                    return index
            print(" VB-CABLE não encontrado. Usando microfone padrão.")
            return None
        except Exception as e:
            print(f" Erro ao listar dispositivos: {e}")
            return None

    def start_listening(self):
        self.is_listening = True
        threading.Thread(target=self._listen_loop, daemon=True).start()

    def _listen_loop(self):
        with self.microphone as source:
            # [função para ]gnorar ruído 
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print(" Escutando a chamada (via VB-CABLE)...")
            
            while self.is_listening:
                try:
                    # tempo de escuta
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=15)
                    
                    try:
                        text = self.recognizer.recognize_google(audio, language='pt-BR')
                        
                        if text:
                            print(f" Transcrito da Call: {text}")
                            self.update_callback(text)
                            
                    except sr.UnknownValueError:
                        pass 
                    except sr.RequestError as e:
                        print(f" Erro no Google: {e}")

                except sr.WaitTimeoutError:
                    continue 
                except Exception as e:
                    print(f" Erro no loop: {e}")
                    time.sleep(1)

    def stop_listening(self):
        self.is_listening = False