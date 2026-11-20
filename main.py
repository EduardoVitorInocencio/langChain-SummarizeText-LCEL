
import os

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI


# --------------------------------------------------
# Load environment variables
# --------------------------------------------------
load_dotenv()


# --------------------------------------------------
# LLM Factory
# --------------------------------------------------
def create_chat_model():
    provider = os.getenv(
        "LLM_PROVIDER", "ollama"
    ).strip().lower()

    if provider == "openai":
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError(
                "OPENAI_API_KEY is required"
            )

        return ChatOpenAI(
            model=os.getenv(
                "OPENAI_MODEL", "gpt-4o-mini"
            ),
            temperature=0,
            max_tokens=500,
        )

    if provider == "google":
        if not os.getenv("GOOGLE_API_KEY"):
            raise ValueError(
                "GOOGLE_API_KEY is required"
            )

        return ChatGoogleGenerativeAI(
            model=os.getenv(
                "GOOGLE_MODEL", "gemini-3.8-flash"
            ),
            temperature=0,
            max_output_tokens=500,
        )

    if provider == "ollama":
        return ChatOllama(
            model=os.getenv(
                "OLLAMA_MODEL", "llama3.2"
            ),
            base_url=os.getenv(
                "OLLAMA_BASE_URL",
                "http://localhost:11434"
            ),
            temperature=0,
            num_predict=500,
        )

    raise ValueError(
        f"Unsupported LLM_PROVIDER={provider!r}. "
        "Choose openai, google, or ollama."
    )


def get_model_name(llm) -> str:
    return getattr(llm, "model_name", None) or llm.model


# --------------------------------------------------
# Summarization Chain
# --------------------------------------------------
def summarize_information(information: str) -> str:
    if not information.strip():
        raise ValueError("Information cannot be empty")

    llm = create_chat_model()
    print(f"Modelo em uso: {get_model_name(llm)}")

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
            Você é um especialista em biografias.

            Com base no texto fornecido:

            1. Crie um resumo da vida da pessoa
               com no máximo 100 palavras.
            2. Liste exatamente 3 fatos importantes.
            3. Responda em português brasileiro.
            4. Não invente informações.
            5. Organize a resposta em Markdown.
            """
        ),
        (
            "human",
            "Informações sobre a pessoa:\n\n{information}"
        )
    ])

    chain = prompt | llm | StrOutputParser()

    return chain.invoke({
        "information": information
    })


# --------------------------------------------------
# Main
# --------------------------------------------------
def main():
    information = """
    Nelson Mandela nasceu em 18 de julho de 1918,
    na África do Sul.

    Foi um advogado, ativista contra o apartheid
    e líder político sul-africano.

    Passou 27 anos na prisão por sua atuação
    contra o regime de segregação racial.

    Foi libertado em 1990 e recebeu o
    Prêmio Nobel da Paz em 1993.

    Em 1994, tornou-se o primeiro presidente
    negro da África do Sul, governando até 1999.

    Mandela faleceu em 5 de dezembro de 2013.
    """

    try:
        summary = summarize_information(information)
        print("\n=== RESUMO ===\n")
        print(summary)

    except Exception as error:
        print(f"Erro ao gerar resumo: {error}")
        raise


if __name__ == "__main__":
    main()
