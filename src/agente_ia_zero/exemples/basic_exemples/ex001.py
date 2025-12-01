import os
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, add_messages

BASE_DIR = os.path.dirname(__file__)


# 1 - Defini o Estado
class State(TypedDict):
    """
    Defini o Estado dos nodes. Usado para reconstruir o caminho dos nodes.


    Arguments:
        TypedDict -- O TypeDict é usado para forçar a tipagem em todas as chaves do dicionário
    """

    nodes_utils: Annotated[list[str], add_messages]


# 2 - Definir os nodes (Função)
def first_node(state: State) -> State:
    output_state: State = {"nodes_utils": ["A"]}
    print("> first_node", f"{state=}", f"{output_state=}")
    return output_state


def second_node(state: State) -> State:
    output_state: State = {"nodes_utils": ["B"]}
    print("> second_node", f"{state=}", f"{output_state=}")
    return output_state


# Definir o builder do grafo
builder: StateGraph[State, None, State, State] = StateGraph(State)

builder.add_node("first_node", first_node)
builder.add_node("second_node", second_node)

# Conectar os edges (ou arestas)

builder.add_edge(
    "__start__", "first_node"
)  # no método add_edge necessáriamente precisa seguir uma ordem cronológica
builder.add_edge("first_node", "second_node")
builder.add_edge("second_node", "__end__")

# Compilar o grafo
graph = builder.compile()

graph.get_graph().draw_mermaid_png(
    output_file_path=os.path.join(BASE_DIR, "graph", "file.png")
)

# Pegar o resultado
response: dict = graph.invoke({"nodes_utils": []})

# resultado do grafo
print()
print(f"{response=}")
print()
