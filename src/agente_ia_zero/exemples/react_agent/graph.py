
from typing import Literal
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.state import CompiledStateGraph, StateGraph
from langchain_core.messages import AIMessage, ToolMessage
from langgraph.constants import END, START
from agente_ia_zero.exemples.react_agent.state import State
from agente_ia_zero.exemples.react_agent.tools import TOOLS, TOOLS_BY_NAME
from agente_ia_zero.exemples.react_agent.utils import load_llm


def call_llm(state: State) -> State:
    print('>call_llm')
    """
    Função (node) Responsável por iniciar a llm

    Arguments:
        state -- State(TypedDict[List]) é um dicionario com a lista de mensagem

    Returns:
        State - Retorna o State
    """
    llm_with_tools = load_llm().bind_tools(TOOLS)
    result = llm_with_tools.invoke(state["messages"])
    return {"messages": [result]}

def tool_node(state: State) -> State:
    print('>tool_node')
    llm_response = state["messages"][-1] # recupera o response da LLM
    if not isinstance(llm_response, AIMessage) or not getattr(
        llm_response, "tool_calls", None
    ): # condicional para verificar se existe uma tool_call no response
        return state
    call = llm_response.tool_calls[-1] # pega o valor da tool_call
    name, args, id_ = call["name"], call["args"], call["id"] # pega os nomes, argumentos e o id da resposta
    status = "success" # cria um status do tool_call

    try:
        content = TOOLS_BY_NAME[name].invoke(args) # Chama a função que a LLM sugeriu

    except Exception as e:
        content = f"Please, fix your mistake: {e}" # retorna erro caso não encontre

    tool_message = ToolMessage(
        content=content, tool_call_id=id_, status=status ## Retorna o resultado da função
    )

    return {"messages": [tool_message]} # coloca o tool_message para o state



def router(state: State) -> Literal['tool_node', '__end__']:
    print('>router')
    llm_response = state["messages"][-1] # busca a resposta da llm
    if getattr(llm_response, 'tool_calls', None): # verifica se retornou a tool_call
        return 'tool_node' # caso retorne chama a tool_node
    return '__end__' # caso não exista retorne __end__

def buid_graph() -> CompiledStateGraph[State, None, State, State]:
    """
    Buida e compila o grafo, controlando o fluxo de execução e salvando o histórico en memoria através dp checkpointer

    Returns:
        retorna a compilação do fluxo
    """
    builder = StateGraph(State)

    builder.add_node("call_llm", call_llm)
    builder.add_node("tool_node", tool_node)
    builder.add_edge(START, "call_llm")
    builder.add_edge("call_llm", END)
    builder.add_conditional_edges('call_llm', router, ['tool_node','__end__'])
    builder.add_edge('tool_node', "call_llm")

    return builder.compile(checkpointer=InMemorySaver())
