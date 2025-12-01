from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph.message import Messages
from langgraph.graph import StateGraph, START, END, add_messages
from langchain.chat_models import init_chat_model
from rich import print
from rich.markdown import Markdown

llm = init_chat_model("ollama:llama3.2")


def reducer(a: Messages, b: Messages):
    """
    funcção de debug
    """

    print('>reducer', a, b)
    return add_messages(a, b)


# 1 - Definir o State
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], reducer]


# 2 -  Definir os nodes
def call_llm(state: AgentState) -> AgentState:

    print('> call_llm')

    llm_result = llm.invoke(state["messages"])
    return {"messages": [llm_result]}


# 3 - Criar o StateGraph
buider = StateGraph(
    AgentState,
    context_schema=None,
    input_schema=AgentState,
    output_schema=AgentState,
)  # esse método verifica o typedict e executa

# 4 - Adiconar nodes ao grafico
buider.add_node("call_llm", call_llm)  # Cria um node (Nós) Fuções de execuções
buider.add_edge(
    START, "call_llm"
)  # Cria os edge (arestas) caminhos de execução
buider.add_edge("call_llm", END)

# 5 - Compilar o grafo
graph = buider.compile()


if __name__ == "__main__":
    current_messages: Sequence[
        BaseMessage
    ] = []  # Variavel para armazenar menssagens anteriores

    while True:
        user_input: str = input("Digite sua menssagem?")

        if user_input.lower() in ["q", "quit"]:
            print("Tchau 👋🏻")
            print(Markdown("---"))
            break
        human_message: HumanMessage = HumanMessage(user_input)
        current_messages = [
            *current_messages,
            human_message,
        ]  # Acrescenta as menssagens anteriores
        result = graph.invoke({
            "messages": current_messages
        })  # O metodo invoke executa iniciamente a classe State verificada pelo StateGraph. Antes de executar o primeiro node
        current_messages = result[
            "messages"
        ]  # Armazenas as messagens humanas e da Ia. Coloca o result no current_messages
        print(Markdown(str(result["messages"][-1].content)))
        print(Markdown("---"))
