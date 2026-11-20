# Resumo de biografias com LangChain e LCEL

Este projeto recebe um texto biográfico, pede a um modelo de linguagem um resumo
de até 100 palavras e três fatos importantes, e mostra a resposta no terminal.
O exemplo de entrada está em `main.py`. O provedor do modelo é escolhido por
variáveis de ambiente.

## Como executar

Requisitos: Python 3.12 ou superior e [uv](https://docs.astral.sh/uv/).

```powershell
uv sync
Copy-Item .env.example .env
```

Edite `.env` para escolher o provedor e preencher a chave necessária. Para usar
o Ollama, que é o padrão, mantenha o servidor local em execução e baixe o modelo:

```powershell
ollama pull llama3.2
uv run python main.py
```

O programa imprime `Modelo em uso: ...` e, em seguida, o resumo. O arquivo
`.env` é ignorado pelo Git; `.env.example` contém somente valores de exemplo.

| `LLM_PROVIDER` | Configuração necessária | Modelo padrão | Como trocar o modelo |
| --- | --- | --- | --- |
| `ollama` (padrão) | Servidor Ollama e modelo baixado | `llama3.2` | `OLLAMA_MODEL` |
| `openai` | `OPENAI_API_KEY` | `gpt-4o-mini` | `OPENAI_MODEL` |
| `google` | `GOOGLE_API_KEY` | `gemini-3.8-flash` | `GOOGLE_MODEL` |

`OLLAMA_BASE_URL` permite apontar para outro servidor Ollama. Para os provedores
remotos, configure a chave correspondente no `.env`. A função
`create_chat_model()` lê `LLM_PROVIDER` e cria `ChatOllama`, `ChatOpenAI` ou
`ChatGoogleGenerativeAI`. Um valor desconhecido gera um erro explícito.

## Conceitos aplicados

### LCEL: composição da cadeia

**LCEL** significa *LangChain Expression Language*. É a forma de compor
componentes executáveis do LangChain, chamados *Runnables*. O operador `|`
passa a saída de uma etapa para a próxima. Neste projeto:

```python
chain = prompt | llm | StrOutputParser()
summary = chain.invoke({"information": information})
```

1. `prompt` recebe o dicionário com `information` e produz mensagens para o chat.
2. `llm` envia essas mensagens ao modelo escolhido e recebe uma resposta.
3. `StrOutputParser()` extrai o texto da resposta, para que a função retorne `str`.

`invoke()` executa a cadeia para uma entrada. A composição mantém o prompt e o
tratamento da resposta iguais quando o provedor muda. Veja o
[exemplo oficial de cadeia e tracing](https://docs.langchain.com/langsmith/trace-with-langchain).

### ChatPromptTemplate

`ChatPromptTemplate.from_messages()` define duas mensagens no projeto: uma
mensagem `system` com as regras do resumo e uma mensagem `human` com o texto da
biografia. Na mensagem humana, `{information}` é um campo do template. O valor
passado a `chain.invoke({"information": information})` preenche esse campo em
cada execução. Assim, as instruções ficam separadas dos dados fornecidos ao
modelo. Consulte a [referência de ChatPromptTemplate](https://reference.langchain.com/python/langchain-core/prompts/chat/ChatPromptTemplate).

### Modelo e parser de saída

Os três provedores implementam a interface de modelo de chat usada pela cadeia.
Por isso, `create_chat_model()` pode trocar o objeto `llm` sem reescrever o
prompt. A configuração usa temperatura `0` e limita a geração a 500 tokens;
esses parâmetros orientam a geração, mas não garantem que o texto tenha
exatamente 100 palavras ou três fatos. `StrOutputParser` devolve texto simples,
sem validar a estrutura do Markdown produzido.

## Observabilidade com LangSmith

[LangSmith](https://docs.langchain.com/langsmith/trace-with-langchain) registra
*traces* das execuções: entrada, etapas do prompt e do modelo, saída e dados de
execução. Como o projeto usa LangChain, o tracing pode ser ativado por variáveis
de ambiente, sem alterar `main.py`.

1. Crie uma chave de API no LangSmith.
2. Escolha o destino das traces conforme o tipo da sua workspace.
3. Preencha os valores no `.env`, ative `LANGSMITH_TRACING=true` e execute o programa.

Para uma **workspace baseada em agentes**, crie primeiro um agente de
observabilidade no LangSmith e use o ID real e um ambiente desse agente:

```dotenv
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=sua-chave
LANGSMITH_AGENT_ID=id-real-do-agente
LANGSMITH_AGENT_ENVIRONMENT=local
```

Para uma **workspace baseada em projetos** ou uma instalação própria, use o
nome de um projeto no lugar das duas variáveis de agente:

```dotenv
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=sua-chave
LANGSMITH_PROJECT=langchain-summarizetext-lcel
```

Não configure `LANGSMITH_PROJECT` e `LANGSMITH_AGENT_ID` ao mesmo tempo. Se sua
conta estiver fora da região padrão dos EUA, configure também
`LANGSMITH_ENDPOINT` com a URL da sua região. Para desativar o envio de traces,
use `LANGSMITH_TRACING=false`. As traces podem conter o texto biográfico enviado
e a resposta do modelo; use dados adequados para esse registro. Veja o
[guia oficial de tracing com LangChain](https://docs.langchain.com/langsmith/trace-with-langchain)
e o [guia de configuração do LangSmith](https://docs.langchain.com/langsmith/observability-quickstart).

## Escopo do exemplo

`main()` contém uma biografia fixa de Nelson Mandela. Para resumir outro texto,
troque a variável `information` ou chame `summarize_information(texto)` em outro
script. O resultado depende do modelo selecionado; o projeto não verifica os
fatos da resposta depois da geração.
