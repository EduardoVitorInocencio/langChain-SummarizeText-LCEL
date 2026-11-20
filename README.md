# LangChain SummarizeText LCEL

Summarize a person's biography with a LangChain chat model. The provider is
selected by `LLM_PROVIDER` in your environment or `.env` file.

```powershell
uv sync
uv run python main.py
```

| `LLM_PROVIDER` | Required setup | Default model | Optional model variable |
| --- | --- | --- | --- |
| `openai` (default) | `OPENAI_API_KEY` | `gpt-4o-mini` | `OPENAI_MODEL` |
| `google` | `GOOGLE_API_KEY` | `gemini-2.5-flash` | `GOOGLE_MODEL` |
| `ollama` | Running Ollama server and downloaded model | `llama3.2` | `OLLAMA_MODEL` |

For example, add one of these selections to `.env`:

```dotenv
LLM_PROVIDER=google
GOOGLE_API_KEY=your-key
```

For local Ollama, run `ollama pull llama3.2` before using
`LLM_PROVIDER=ollama`. Set `OLLAMA_BASE_URL` if the Ollama server is not at its
default local address. An API key is not required for a local Ollama server.
