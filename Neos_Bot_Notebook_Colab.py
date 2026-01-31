import os
import sys
import time # Adicionado para controlar a pausa entre aúdio e caixas de texto
import json
import pandas as pd
import google.generativeai as genai
from gtts import gTTS
from IPython.display import Audio, display, clear_output

# --- CONFIGURAÇÃO ---
# Sua API Key
API_KEY = ""

try:
    genai.configure(api_key=API_KEY)
except:
    print("Erro: Insira uma API Key válida.")

generation_config = {
  "temperature": 0.4,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
}

# --- CARREGAMENTO RAG ---
def carregar_contexto():
    try:
        path_perfil = 'data/perfil_investidor.json'
        path_produtos = 'data/produtos_financeiros.json'
        path_transacoes = 'data/transacoes.csv'

        with open(path_perfil, 'r', encoding='utf-8') as f: perfil = json.load(f)
        with open(path_produtos, 'r', encoding='utf-8') as f: produtos = json.load(f)
        
        if os.path.exists(path_transacoes):
            df = pd.read_csv(path_transacoes)
            transacoes = df.to_string(index=False)
        else:
            transacoes = "Sem histórico."
            
        return perfil, produtos, transacoes
    except Exception as e:
        print(f"Erro ao carregar dados: {e}")
        return {}, {}, ""

perfil_user, produtos_bank, transacoes_user = carregar_contexto()

# --- SYSTEM PROMPT ---
SYSTEM_INSTRUCTION = f"""
Você é o NEOS, um Assistente Financeiro Inteligente do Bradesco.
DADOS CLIENTE: {perfil_user.get('nome')} | Perfil: {perfil_user.get('perfil_investidor')}
HISTÓRICO: {transacoes_user}
PRODUTOS APROVADOS: {json.dumps(produtos_bank, ensure_ascii=False)}

REGRAS:
1. Responda com base nos dados acima.
2. Seja direto e curto (máximo 2 frases).
3. Se perguntarem de gastos, use o histórico.
"""
# Modelo que quiser usar
model = genai.GenerativeModel(model_name="gemini-2.5-pro", generation_config=generation_config, 
                              system_instruction=SYSTEM_INSTRUCTION
                              )
chat_session = model.start_chat(history=[])

# --- FUNÇÕES COLAB ---
def falar_resposta(texto):
    """Gera o áudio e toca no navegador"""
    arquivo = 'resposta.mp3'
    # Remove arquivo anterior se existir para evitar cache
    if os.path.exists(arquivo):
        os.remove(arquivo)
        
    tts = gTTS(text=texto, lang='pt-br')
    tts.save(arquivo)
    
    # Autoplay=False é mais seguro se o input continuar travando
    display(Audio(arquivo, autoplay=True)) 

def main():
    print(f"--- NEOS INICIADO (Usuário: {perfil_user.get('nome')}) ---")
    print("Digite 'sair' para encerrar.\n")
    
    msg_inicial = f"Olá {perfil_user.get('nome')}. Analisei seus gastos. Como posso ajudar?"
    print(f"Neos: {msg_inicial}")
    falar_resposta(msg_inicial)

    while True:
        # PAUSA CRÍTICA: Espera 2 segundos para o áudio carregar e a interface desenhar
        time.sleep(2) 
        
        # O input agora deve aparecer corretamente
        entrada = input("\nVocê: ")
        
        if entrada.lower() in ['sair', 'encerrar']:
            print("Neos: Até logo!")
            break
            
        # Chama a IA
        try:
            response = chat_session.send_message(entrada)
            texto_limpo = response.text.replace("*", "")
            
            print(f"Neos: {texto_limpo}")
            falar_resposta(texto_limpo)
        except Exception as e:
            print(f"Erro na IA: {e}")

if __name__ == "__main__":
    main()
