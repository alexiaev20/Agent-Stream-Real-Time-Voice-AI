# Voice AI - Real-Time Agent

Um Agente de Inteligência Artificial construído em Python, equipado com interface gráfica (Tkinter) e capacidade de escutar chamadas de áudio (via VB-CABLE), processar linguagem natural via **Groq (Llama-3.3)** em tempo real (*Streaming*) e verbalizar as respostas (*TTS*).

## ✨ Principais Funcionalidades

1. **Escuta de Baixa Latência**: O `AudioManager` escuta o áudio do sistema ou microfone cortando automaticamente os ruídos e enviando pacotes precisos.
2. **Memória Contextual (Conversação)**: O motor não analisa frases soltas. Ele carrega a lista das últimas interações, conseguindo entender contextos contínuos de um diálogo humano.
3. **Respostas em Streaming (Groq API)**: Em vez de ficar com a tela travada esperando o carregamento, a resposta é injetada sílaba por sílaba (efeito máquina de escrever) no painel flutuante, graças ao `stream=True`.
4. **Voz Sintetizada (pyttsx3)**: Paralelamente ao painel gráfico, uma Thread independente aguarda a resposta final da IA e realiza a pronúncia em voz alta nativamente (Text-to-Speech) sem travar a interface.

## 🛠 Como Executar

### 1. Pré-Requisitos
- Python 3.10+
- VB-CABLE Virtual Audio Device (Opcional, caso queira escutar áudio direto de chamadas do Discord/Teams/Meet).
- Chave de API da Groq.

### 2. Instalação
```bash
pip install -r requirements.txt
```

Crie um arquivo `.env` na raiz do projeto com sua chave:
```env
GROQ_API_KEY=sua_chave_aqui
```

### 3. Rodando o Agente
```bash
python app/main.py
```
Um painel flutuante negro e transparente aparecerá na tela, sobrepondo os demais aplicativos de forma não intrusiva. Fale no microfone e assista ao agente trabalhando.
