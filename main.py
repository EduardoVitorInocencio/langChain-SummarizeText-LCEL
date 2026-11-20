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


# ----------------------------------------------------------------
# Example usage of ChatOpenAI
# ----------------------------------------------------------------

def summarize_information(information: str) -> str:
    """
    Summarizes the given information about a person.

    Args:
        information (str): The information to summarize.

    Returns:
        str: The summary of the person's life and important facts.
    """
    llm = ChatOpenAI(model="gpt-4o-mini")
    summary_template = """
        Dada a seguinte informação: {information} sobre a pessoa, eu quero que crie:
        1. Um breve resumo da vida da pessoa, com no máximo 100 palavras.
        2. Uma lista de 3 fatos importantes sobre a pessoa.
    """

    prompt = ChatPromptTemplate.from_messages([
        ("system", summary_template),
        ("user", "{information}")
    ])

    chain = prompt | llm

    answer = chain.invoke({"information": information})

    print(answer.content)

def main():
    # Example information about a person
    information = """
        Nelson Rolihlahla Mandela (Mvezo, 18 de julho de 1918 – Joanesburgo, 5 de dezembro de 2013) foi um advogado, líder rebelde e presidente da África do Sul de 1994 a 1999, considerado como o mais importante líder da África Subsaariana, vencedor do Prêmio Nobel da Paz de 1993,[1] e pai da moderna nação sul-africana,[2] onde é normalmente referido como Madiba (nome do seu clã) ou "Tata" ("Pai").
        Nascido numa família de nobreza tribal, numa pequena aldeia do interior onde possivelmente viria a ocupar cargo de chefia, recusou esse destino aos 23 anos ao seguir para a capital, Joanesburgo, e iniciar sua atuação política.[3] Passando do interior rural para uma vida rebelde na faculdade, transformou-se em um jovem advogado na capital e líder da resistência não violenta da juventude, acabando como réu em um infame julgamento por traição. Foragido, tornou-se depois o prisioneiro mais famoso do mundo e, finalmente, o político mais galardoado em vida, responsável pela refundação do seu país como uma sociedade multiétnica.[4]
        Mandela passou 27 anos na prisão — inicialmente em Robben Island e, mais tarde, nas prisões de Pollsmoor e Victor Verster. Depois de uma campanha internacional, foi libertado em 1990, quando recrudescia a guerra civil em seu país. Em dezembro de 2013, foi revelado pelo The New York Times que a CIA americana foi a força decisiva para a prisão de Mandela em 1962, quando agentes americanos foram empregados para auxiliar as forças de segurança da África do Sul a localizá-lo.[5] Até 2009, ele havia dedicado 67 anos de sua vida à causa que defendeu como advogado de direitos humanos e pela qual se tornou prisioneiro de um regime de segregação racial, até ser eleito o primeiro presidente da África do Sul livre. Em sua homenagem, a Organização das Nações Unidas instituiu o Dia Internacional Nelson Mandela no dia de seu nascimento, 18 de julho, como forma de valorizar em todo o mundo a luta pela liberdade, pela justiça e pela democracia.[6]
        Mandela foi uma figura controversa durante grande parte da sua vida. Denunciado como um terrorista comunista por seus críticos,[7][8] ele acabou sendo aclamado internacionalmente por seu ativismo e recebeu mais de 250 prêmios e condecorações, incluindo o Nobel da Paz em 1993, a Medalha Presidencial da Liberdade dos Estados Unidos e a Ordem de Lenin da União Soviética. Seus críticos apontam seus traços egocêntricos e o fato de seu governo ter sido amigo de ditadores simpáticos ao Congresso Nacional Africano (CNA).[9] Foi o mais poderoso símbolo da luta contra o regime segregacionista do Apartheid, sistema racista oficializado em 1948, e modelo mundial de resistência.[1][10] No dizer de Ali Abdessalam Treki, Presidente da Assembleia Geral das Nações Unidas, "um dos maiores líderes morais e políticos de nosso tempo".[11] Recebeu a Medalha Benjamin Franklin por Serviço Público de Destaque de 2000.
    """
    summarize_information(information)


if __name__ == "__main__":
    main()
