import tkinter as tk
import threading

class OverlayWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Assistente de IA")
        # Tamanho inicial 
        self.root.geometry("400x220+50+50") 
        self.root.attributes('-topmost', True) 
        self.root.attributes('-alpha', 0.90)   # transparência
        
        # (Dark Mode)
        self.root.configure(bg='#1e1e1e')
        self.text_font = ("Segoe UI", 12)
        
        # O que o sistema ouviu
        self.transcript_label = tk.Label(
            root, 
            text="Aguardando áudio...", 
            bg='#1e1e1e', 
            fg='#9da5b4', 
            wraplength=380, 
            justify='left', 
            font=("Segoe UI", 10, "italic")
        )
        self.transcript_label.pack(side='top', fill='x', padx=10, pady=8)
        
        # O que a IA responde
        self.response_text = tk.Text(
            root, 
            height=6, 
            bg='#2d2d2d', 
            fg='#ffffff', 
            bd=0, 
            font=("Segoe UI", 11), 
            wrap='word',
            padx=10,
            pady=10
        )
        self.response_text.pack(side='bottom', fill='both', expand=True, padx=10, pady=10)
        self.response_text.insert('1.0', "IA Pronta...")
        self.response_text.config(state=tk.DISABLED)

    def update_transcription(self, text):
        self.root.after(0, self._update_transcription_gui, text)

    def _update_transcription_gui(self, text):
        self.transcript_label.config(text=f"Você disse: {text}")
        
    def update_response(self, text):
        self.root.after(0, self._update_response_gui, text)
        
    def _update_response_gui(self, text):
        self.response_text.config(state=tk.NORMAL)
        self.response_text.delete('1.0', tk.END)
        self.response_text.insert('1.0', f" IA: {text}")
        self.response_text.config(state=tk.DISABLED)