import threading
import speech_recognition as sr
import time

class AudioManager:
    def __init__(self, update_callback):
        self.update_callback = update_callback
        self.recognizer = sr.Recognizer()
        self.is_listening = False
        
        self.device_index = self._find_vb_cable_index()
        self.microphone = sr.Microphone(device_index=self.device_index)
        
        # Otimização de Sensibilidade e Ruído
        self.recognizer.dynamic_energy_threshold = False
        self.recognizer.energy_threshold = 400 
        self.recognizer.pause_threshold = 0.8 # Tempo de silêncio para considerar que o usuário parou de falar

    def _find_vb_cable_index(self):
        try:
            print(" Encontrando dispositivo de audio...")
            for index, name in enumerate(sr.Microphone.list_microphone_names()):
                if "CABLE Output" in name or "VB-Audio" in name or "Mixagem Estéreo" in name:
                    print(f" Captura de Chamada ativa: {name} (Index: {index})")
                    return index
            print(" VB-CABLE não encontrado. Usando microfone padrão do Windows.")
            return None
        except Exception as e:
            print(f" Erro ao listar áudio: {e}")
            return None

    def start_listening(self):
        self.is_listening = True
        threading.Thread(target=self._listen_loop, daemon=True).start()

    def _listen_loop(self):
        with self.microphone as source:
            print(" Calibrando ruído ambiente...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print(" Pronto para ouvir!")
            
            while self.is_listening:
                try:
                    # phrase_time_limit força corte após 10s para não ficar ouvindo infinitamente
                    audio = self.recognizer.listen(source, timeout=2, phrase_time_limit=10)
                    
                    try:
                        text = self.recognizer.recognize_google(audio, language='pt-BR')
                        if text:
                            print(f" [Ouvido]: {text}")
                            self.update_callback(text)
                            
                    except sr.UnknownValueError:
                        pass # Silêncio ou áudio ininteligível
                    except sr.RequestError as e:
                        print(f" Erro de Conexão STT: {e}")

                except sr.WaitTimeoutError:
                    continue 
                except Exception as e:
                    print(f" Erro de hardware de áudio: {e}")
                    time.sleep(1)

    def stop_listening(self):
        self.is_listening = False
