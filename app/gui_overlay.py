import tkinter as tk

class OverlayWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Agente IA - Em Tempo Real")
        self.root.geometry("450x250+50+50") 
        self.root.attributes('-topmost', True) 
        self.root.attributes('-alpha', 0.95)
        self.root.configure(bg='#1e1e1e')
        
        self.transcript_label = tk.Label(
            root, text="Ouvindo...", bg='#1e1e1e', fg='#00d1b2', 
            wraplength=420, justify='left', font=("Segoe UI", 11, "bold")
        )
        self.transcript_label.pack(side='top', fill='x', padx=10, pady=5)
        
        self.response_text = tk.Text(
            root, height=8, bg='#2d2d2d', fg='#ffffff', bd=0, 
            font=("Consolas", 11), wrap='word', padx=10, pady=10
        )
        self.response_text.pack(side='bottom', fill='both', expand=True, padx=10, pady=5)
        self.response_text.insert('1.0', "Aguardando interação...")
        self.response_text.config(state=tk.DISABLED)
        
        self.is_new_message = True

    def update_transcription(self, text):
        self.root.after(0, lambda: self.transcript_label.config(text=f"Usuário: {text}"))
        self.root.after(0, self._prepare_new_response)

    def _prepare_new_response(self):
        self.response_text.config(state=tk.NORMAL)
        self.response_text.delete('1.0', tk.END)
        self.response_text.insert('1.0', "IA: ")
        self.response_text.config(state=tk.DISABLED)
        self.is_new_message = False

    def append_response_chunk(self, chunk, is_final):
        self.root.after(0, self._append_text, chunk)

    def _append_text(self, text):
        self.response_text.config(state=tk.NORMAL)
        self.response_text.insert(tk.END, text)
        self.response_text.see(tk.END)
        self.response_text.config(state=tk.DISABLED)
