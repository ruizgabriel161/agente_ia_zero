from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph.state import RunnableConfig
from agente_ia_zero.exemples.react_agent.graph import buid_graph, CompiledStateGraph
from rich import print
from rich.prompt import Prompt
from rich.markdown import Markdown
from agente_ia_zero.exemples.react_agent.prompts import SYSTEM_PROMPT


def main() -> None:
    """
    função main para executar o fluxo
    """
    config = RunnableConfig(configurable={"thread_id": 1})
    graph = buid_graph()

    interaction(config=config, graph=graph)
  
def interaction(config: RunnableConfig, graph: CompiledStateGraph) -> None:
    #configuração do rich
    prompt: Prompt = Prompt()
    first_loop = True # variavel de controle do primeiro laço
    #inicia o loop para interações
    while True:
        user_input:str = prompt.ask('[red]User: \n')
        print(Markdown('---'))

        if user_input.lower() in ['q', 'quit', 'exit', 'sair']:
            break

        human_message: HumanMessage = HumanMessage(content=user_input)  # converte a string em ua HumanMessage
        current_loop_message = [human_message]

        if first_loop:
            current_loop_message = [SystemMessage(SYSTEM_PROMPT), human_message]
            first_loop = False

        result = graph.invoke({'messages': current_loop_message}, config=config) # O método invoke chama a Ia passando as mensagens e configurações para ela

        print('[#FFD700]Resposta: \n[/#FFD700]')
        print(Markdown(result['messages'][-1].content))
        print(Markdown('---'))
        print(result['messages'])
        print(Markdown('---'))
        pass

if __name__ == "__main__":
    main()
