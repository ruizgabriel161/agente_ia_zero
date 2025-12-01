import operator
import os
from typing import Annotated, Literal
from dataclasses import dataclass
from langgraph.graph import StateGraph, START, END

BASE_DIR = os.path.dirname(__file__)


# 1 - Defini o Estado
@dataclass
class State:
    """
    Defini o Estado dos nodes. Usado para reconstruir o caminho dos nodes.
    """

    nodes_utils: Annotated[list[str], operator.add]
    current_number: int = 0


# 2 - Definir os nodes (Função)
def first_node(state: State) -> State:
    output_state: State = State(
        nodes_utils=["A"], current_number=state.current_number
    )
    print("> first_node", f"{state=}", f"{output_state=}")
    return output_state


def second_node(state: State) -> State:
    output_state: State = State(
        nodes_utils=["B"], current_number=state.current_number
    )
    print("> second_node", f"{state=}", f"{output_state=}")
    return output_state


def thrid_node(state: State) -> State:
    output_state: State = State(
        nodes_utils=["C"], current_number=state.current_number
    )
    print("> thrid_node", f"{state=}", f"{output_state=}")
    return output_state


# Função condicional
def the_condicional(state: State) -> Literal["B", "C"]:
    if state.current_number >= 50:
        return "C"
    return "C"


# Definir o builder do grafo
builder: StateGraph[State, None, State, State] = StateGraph(State)

builder.add_node("first_node", first_node)
builder.add_node("second_node", second_node)
builder.add_node("thrid_node", thrid_node)

# Conectar os edges (ou arestas)

builder.add_edge(
    START, "first_node"
)  # no método add_edge necessáriamente precisa seguir uma ordem cronológica
builder.add_conditional_edges(
    "first_node", the_condicional, {"B": "second_node", "C": "thrid_node"}
)

builder.add_edge("second_node", END)

builder.add_edge("thrid_node", END)
# Compilar o grafo
graph = builder.compile()

graph.get_graph().draw_mermaid_png(
    output_file_path=os.path.join(BASE_DIR, "graph", "file.png")
)

# Pegar o resultado
response: dict = graph.invoke(State(nodes_utils=[]))

# resultado do grafo
print()
print(f"{response=}")
print()
