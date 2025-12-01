from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, START, END, add_messages
from langchain.chat_models import init_chat_model

# 0 - Iniciar a llm
llm = init_chat_model("ollama:llama3.2")


# 1 - Definir o State
class AgenteState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


# 2 - Definir os nodes
def call_llm(arg):
    pass


# 3 - Definir Condicional
# 4 - Setar o buider
# 5 - conectar os edges
# 7 -  compilar o grafico
# 8 Saída
