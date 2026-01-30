# Neos
Neos Minha Resolução do Bootcamp em parceria com a DIO e Bradesco!

---

## Caso de Uso

### Problema
Clientes do banco frequentemente têm dificuldade em visualizar a relação entre seus gastos diários e suas metas de longo prazo, resultando em falta de planejamento e escolhas de investimento inadequadas ao seu perfil real.

### Solução
O **Neos** atua como um planejador financeiro centralizado que cruza dados históricos de transações (CSV) com o perfil do investidor (JSON). Ele oferece insights proativos sobre hábitos de consumo e recomenda produtos financeiros de forma hiper-personalizada, utilizando IA Generativa para interpretar linguagem natural.

### Público-Alvo
Clientes correntistas do segmento Varejo e Exclusive que buscam organizar suas finanças e iniciar investimentos, mas carecem de consultoria humana dedicada.

---

## Persona e Tom de Voz

### Nome do Agente
**Neos** (do grego *neos*, novo/jovem - simbolizando novos começos financeiros).

### Personalidade
Analítico, seguro e proativo. O Neos não apenas responde, ele educa. Ele atua como um "Sócio" das finanças do cliente, celebrando conquistas e alertando sobre desvios.

### Tom de Comunicação
Profissional, porém acessível. Evita "bancadês" (jargões complexos) desnecessários, traduzindo conceitos para a realidade do cliente.

### Exemplos de Linguagem
- **Saudação:** "Olá, João. Analisei seus últimos gastos e tenho uma sugestão para sua meta de viagem."
- **Erro:** "Não localizei essa informação nos seus dados atuais. Gostaria que eu buscasse outra referência?"
- **Sucesso:** "Perfeito. Com esse aporte, sua previsão de atingir a meta caiu para 18 meses."

---

## Arquitetura

### Diagrama Simplificado

```mermaid
flowchart TD
    A[Voz do Cliente] -->|SpeechRecognition| B[Texto]
    B --> C[Orquestrador Python]
    C -->|Carrega| D[Base de Conhecimento JSON/CSV]
    D --> C
    C -->|Contexto + Prompt| E[Google Gemini API]
    E -->|Resposta Gerada| C
    C -->|gTTS| F[Resposta em Áudio]
```

## Link

Link: 



