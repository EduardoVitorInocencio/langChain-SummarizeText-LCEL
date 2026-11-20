import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
os.environ["OLLAMA_API_KEY"] = os.getenv("OLLAMA_API_KEY")


def main():
    print("Hello from langchain-summarizetext-lcel!")


if __name__ == "__main__":
    main()
