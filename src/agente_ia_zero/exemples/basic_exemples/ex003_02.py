from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph, START, END, add_messages
from langgraph.graph.state import RunnableConfig
from langchain.chat_models import init_chat_model
from rich import print
from rich.markdown import Markdown

llm = init_chat_model("ollama:llama3.2")


# 1 - Difinir o State
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


# 2 -  Definir os nodes
def call_llm(state: AgentState) -> AgentState:

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
checkpointer = (
    InMemorySaver()
)  # Variavel para criar um checkpoint e salvar o histórico

graph = buider.compile(checkpointer=checkpointer)
config = RunnableConfig(
    configurable={"thread_id": 1}
)  # Runnable Config defini a configuração da thread para salvar o histórico


if __name__ == "__main__":
    while True:
        user_input: str = input("Digite sua menssagem?")

        if user_input.lower() in ["q", "quit"]:
            print("Tchau 👋🏻")
            print(Markdown("---"))
            break
        human_message: HumanMessage = HumanMessage(user_input)

        result = graph.invoke(
            {"messages": [human_message]}, config=config
        )  # O metodo invoke executa iniciamente a classe State verificada pelo StateGraph. Antes de executar o primeiro node
        print(Markdown(str(result["messages"][-1].content)))
        print(Markdown("---"))
