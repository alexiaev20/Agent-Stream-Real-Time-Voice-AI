# Agent Stream 

Este projeto é um assistente de inteligência artificial projetado para capturar áudio em tempo real (focado em chamadas/reuniões), transcrever o que está sendo dito e fornecer respostas ou sugestões inteligentes através de uma interface de overlay discreta.

O sistema utiliza a **Groq API** (Llama 3) para processamento ultra-rápido e o **Google Speech Recognition** para transcrição.

##  Funcionalidades

- **Captura de Áudio Inteligente**: Projetado para capturar áudio do sistema (ex: saídas de reuniões no Teams, Zoom, Meet) usando drivers como VB-CABLE.
- **Transcrição em Tempo Real**: Converte fala em texto instantaneamente.
- **Inteligência Artificial por Groq**: Utiliza modelos Llama 3 via Groq para gerar respostas contextuais e rápidas.
- **Interface Overlay**: Janela (sempre visível) e transparente, ideal para usar durante chamadas sem obstruir a visão.
- **Modo Escuro**: Interface moderna e agradável aos olhos.

## Tecnologias Utilizadas

- **Python 3**
- **Tkinter**: Para a interface gráfica (GUI).
- **SpeechRecognition**: Para converter áudio em texto.
- **Groq API**: Para o "cérebro" da IA.
- **Python-dotenv**: Gerenciamento de variáveis de ambiente.

## e Pré-requisitos

Antes de rodar o projeto, você precisará de:

1. **Python 3.x** instalado.
2. **Conta na Groq** e uma chave de API válida.
3. **VB-CABLE Driver** (Opcional, mas recomendado): Para que o script consiga "ouvir" o áudio que sai do seu computador (o que as outras pessoas falam na chamada). Se não tiver, ele tentará usar o microfone padrão.
   - [Baixar VB-CABLE](https://vb-audio.com/Cable/)

## Instalação

1. Clone este repositório:
   ```bash
   git clone https://github.com/seu-usuario/agent-stream.git
   cd agent-stream
   ```

2. Crie e ative um ambiente virtual (recomendado):
   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
   *Dependências principais: `requests`, `SpeechRecognition`, `python-dotenv`, `pyaudio` (necessário para o speech_recognition).*

##  Configuração

1. Crie um arquivo `.env` na raiz do projeto (use o `.env.example` como base se houver, ou crie do zero).
2. Adicione sua chave da API da Groq:

   ```env
   GROQ_API_KEY=sua_chave_aqui_gsk_...
   ```

## ▶Como Usar

1. Execute o arquivo principal:
   ```bash
   python app/main.py
   ```

2. A interface do assistente abrirá no canto da tela.
3. O sistema buscará automaticamente por dispositivos de áudio como "CABLE Output" ou "Mixagem Estéreo".
   - **Dica**: Nas configurações de som da sua chamada (Zoom/Meet), defina o dispositivo de SAÍDA (Alto-falantes) para "CABLE Input" se estiver usando o VB-Cable, para que o bot consiga ouvir a reunião.

## Estrutura do Projeto

- `app/main.py`: Ponto de entrada. Inicializa a GUI, o Gerenciador de Áudio e a IA.
- `app/audio_manager.py`: Lida com a captura de áudio e transcrição (Google SR).
- `app/ai_engine.py`: Comunicação com a API da Groq.
- `app/gui_overlay.py`: Interface gráfica flutuante.

## Notas Importantes

- O projeto foi configurado para priorizar a velocidade, usando a API da Groq.
- Certifique-se de que seu microfone ou dispositivo de áudio virtual está configurado corretamente no sistema operacional.

---

