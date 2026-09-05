import pyttsx3
import threading
import queue

class TTSEngine:
    def __init__(self):
        self.q = queue.Queue()
        self.thread = threading.Thread(target=self._worker, daemon=True)
        self.thread.start()

    def _worker(self):
        engine = pyttsx3.init()
        # Ajuste para voz em Português se possível (opcional, o OS costuma resolver)
        rate = engine.getProperty('rate')
        engine.setProperty('rate', rate - 20) 
        
        while True:
            text = self.q.get()
            if text is None:
                break
            engine.say(text)
            engine.runAndWait()
            self.q.task_done()

    def speak(self, text):
        if text.strip():
            self.q.put(text)
