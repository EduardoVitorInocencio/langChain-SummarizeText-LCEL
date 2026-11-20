import os

from dotenv import find_dotenv, load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# ----------------------------------------------------------------
# Load environment variables from .env file
# ----------------------------------------------------------------
load_dotenv(find_dotenv())

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
os.environ["OLLAMA_API_KEY"] = os.getenv("OLLAMA_API_KEY")

# ----------------------------------------------------------------
# Example usage of PromptTemplate
# ----------------------------------------------------------------
prompt = ChatPromptTemplate.from_messages([
    ("system", "Você é um assistente especialista em {area}."),
    ("user", "{pergunta}")
])

# ----------------------------------------------------------------
# Example usage of ChatOpenAI
# ----------------------------------------------------------------
llm = ChatOpenAI(model="gpt-4o-mini")

chain = prompt | llm

answer = chain.invoke({"area": "programação", "pergunta": "O que é LangChain?"})

print(answer.content)

# def main():
#     print("Hello from langchain-summarizetext-lcel!")


# if __name__ == "__main__":
#     main()
