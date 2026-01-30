import os
import sys
import json
import pandas as pd
import speech_recognition as sr
import google.generativeai as genai
from gtts import gTTS
from playsound import playsound

# --- CONFIGURAÇÃO E CONSTANTES ---
# Insira sua chave da Google AI Studio aqui
API_KEY = "SUA_CHAVE_GOOGLE_AQUI" 

genai.configure(api_key=API_KEY)

# Configuração do Modelo Generativo
generation_config = {
  "temperature": 0.4,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
}

# --- CARREGAMENTO DA BASE DE CONHECIMENTO (RAG) ---
def carregar_contexto():
    """
    Carrega os dados da pasta 'data/' para compor a memória do agente.
    """
    try:
        # Caminhos dos arquivos (agora apontando para a pasta data)
        path_perfil = os.path.join('data', 'perfil_investidor.json')
        path_produtos = os.path.join('data', 'produtos_financeiros.json')
        path_transacoes = os.path.join('data', 'transacoes.csv')

        # Carregamento do Perfil
        if os.path.exists(path_perfil):
            with open(path_perfil, 'r', encoding='utf-8') as f:
                perfil = json.load(f)
        else:
            print(f"Erro: Arquivo {path_perfil} não encontrado.")
            sys.exit(1)
        
        # Carregamento dos Produtos
        if os.path.exists(path_produtos):
            with open(path_produtos, 'r', encoding='utf-8') as f:
                produtos = json.load(f)
        else:
            print(f"Erro: Arquivo {path_produtos} não encontrado.")
            sys.exit(1)
            
        # Carregamento das Transações
        if os.path.exists(path_transacoes):
            df_transacoes = pd.read_csv(path_transacoes)
            transacoes = df_transacoes.to_string(index=False)
        else:
            transacoes = "Histórico de transações não disponível."
            
        return perfil, produtos, transacoes

    except Exception as e:
        print(f"Erro crítico ao carregar base de dados: {e}")
        sys.exit(1)

# Inicializa as bases de dados na memória
perfil_user, produtos_bank, transacoes_user = carregar_contexto()

# Definição do System Prompt (Personalidade e Regras)
SYSTEM_INSTRUCTION = f"""
Você é o NEOS, um Assistente Financeiro Inteligente do Bradesco.
Seu foco é Planejamento de Metas e Saúde Financeira.

DADOS DO CLIENTE ATUAL:
- Nome: {perfil_user.get('nome', 'Cliente')}
- Perfil: {perfil_user.get('perfil_investidor', 'Não definido')}
- Objetivo: {perfil_user.get('objetivo_principal', 'Geral')}
- Renda Mensal: R$ {perfil_user.get('renda_mensal', 0)}

HISTÓRICO FINANCEIRO RECENTE:
{transacoes_user}

PRODUTOS FINANCEIROS DISPONÍVEIS (Recomende APENAS estes):
{json.dumps(produtos_bank, indent=2, ensure_ascii=False)}

DIRETRIZES DE COMPORTAMENTO:
1. Seja direto, seguro e proativo. Use linguagem acessível mas profissional.
2. Utilize os dados fornecidos (CSV/JSON) para embasar suas respostas.
3. Se o usuário perguntar sobre gastos, analise o histórico de transações.
4. Jamais invente taxas ou produtos que não estejam na lista aprovada.
5. Suas respostas devem ser curtas (máximo 3 frases) para facilitar a síntese de voz.
"""

# Inicialização do Modelo
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction=SYSTEM_INSTRUCTION
)

# Histórico de chat da sessão
chat_session = model.start_chat(history=[])

# --- FUNÇÕES DE INTERFACE (I/O) ---

def texto_para_audio(mensagem):
    """Gera áudio a partir da resposta do agente."""
    arquivo_audio = 'response.mp3'
    
    if os.path.exists(arquivo_audio):
        try:
            os.remove(arquivo_audio)
        except PermissionError:
            pass

    try:
        tts = gTTS(text=mensagem, lang='pt-br')
        tts.save(arquivo_audio)
        playsound(arquivo_audio)
        os.remove(arquivo_audio)
    except Exception as e:
        print(f"Erro no subsistema de áudio: {e}")

def ouvir_usuario():
    """Captura e transcreve o áudio do microfone."""
    recon = sr.Recognizer()
    with sr.Microphone() as source:
        recon.adjust_for_ambient_noise(source, duration=0.5)
        print("\nNeos ouvindo...")
        try:
            audio = recon.listen(source, timeout=5)
            texto = recon.recognize_google(audio, language='pt-BR')
            print(f">> Usuário: {texto}")
            return texto.lower()
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            print("Erro de conexão com serviço de reconhecimento.")
            return None

def processar_interacao(entrada_usuario):
    """Núcleo lógico de processamento."""
    if not entrada_usuario:
        return

    # Comandos de sistema
    if 'encerrar' in entrada_usuario or 'sair' in entrada_usuario:
         despedida = "Encerrando sessão. Até logo, João."
         print(f">> Neos: {despedida}")
         texto_para_audio(despedida)
         sys.exit()

    # Interação com LLM
    try:
        print("Processando resposta...")
        response = chat_session.send_message(entrada_usuario)
        texto_resposta = response.text.replace("*", "") 
        
        print(f">> Neos: {texto_resposta}")
        texto_para_audio(texto_resposta)
        
    except Exception as e:
        erro_msg = "Desculpe, tive um problema ao processar sua solicitação."
        print(f"Erro API: {e}")
        texto_para_audio(erro_msg)

# --- EXECUÇÃO PRINCIPAL ---
def main():
    boas_vindas = f"Olá, eu sou o Neos. Identifiquei que você é {perfil_user.get('nome')}. Como posso auxiliar no seu planejamento hoje?"
    print(f">> Neos: {boas_vindas}")
    texto_para_audio(boas_vindas)

    while True:
        input_usuario = ouvir_usuario()
        if input_usuario:
            processar_interacao(input_usuario)

if __name__ == "__main__":
    main()

