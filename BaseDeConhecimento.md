# Base de Conhecimento

## Dados Utilizados

O agente **Neos** utiliza uma base de dados híbrida para contextualizar suas respostas, carregada localmente em tempo de execução:

| Arquivo | Formato | Utilização no Agente |
|---------|---------|---------------------|
| `perfil_investidor.json` | JSON | Define a persona do cliente (nome, tolerância ao risco e objetivos). |
| `produtos_financeiros.json` | JSON | Catálogo de produtos aprovados para recomendação (RAG). |
| `transacoes.csv` | CSV | Histórico financeiro para análise de gastos e padrões de consumo. |

## Estratégia de Integração

### Carregamento e Injeção
Diferente de sistemas que treinam o modelo (Fine-tuning), o Neos utiliza a estratégia de **RAG (Retrieval-Augmented Generation)** via contexto. 

1. Os arquivos são lidos pelo script Python (`neos_bot.py`) no início da sessão.
2. O CSV de transações é convertido para uma string otimizada.
3. Todo o conteúdo é injetado no **System Prompt** do Google Gemini.
4. Isso garante que a IA tenha acesso "em tempo real" aos dados do cliente sem alucinar informações externas.
