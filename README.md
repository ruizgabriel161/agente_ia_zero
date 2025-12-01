# agente_ia_zero
## LangGraph
O LangGraph estrutura a conexão com a LLM em grafos. Dessa forma é possível definir o fluxo de execução do agente.
 
Os grafos são compostos por nodes (nós ou funções) e por edge (arestas ou condicionais) que definem a fluxo de interação com o modelo. O grafico é definido pelo State

 - **State**: é um TypedDict ou dataclass que define o estado do gráfico. É um classe que é configurada para definir quais variáveis (e seus tipos) são necessários para o gráfico funcionar.
- **Nodes**: são nós ou função que executam ações determinadas de acordo com o fluxo

- **Edge**: Determinam o caminho de exeção do fluxo.

    - **Condicional Edges**: São condições que determinam para qual node o fluxo irá percorrer

---
### Exemplo de um grafo:
![Grafo](/src/agente_ia_zero/graph/file.png)
---
### Passo a passo para definir um grafo
1.  Criar o State para definir os estado do gráfo. Nele será definido a tipagem das veriaveis. A classe State é executada o grafo é executado.  
Exemplo:

    ```python
    class tate(TypedDict):
        messages: Annotated[Sequence[BaseMessage], add_messages]

    ```

2. Criar os Nodes (nós). Por padrão é recomendado criar uma node inicial para invocar a LLM. Exemplo do node padão
    ```python
    # 2 -  Definir os nodes
    def call_llm(state: AgentState) -> AgentState:

        llm_result = llm.invoke(state["messages"])
        return {"messages": [llm_result]}

    ```
3. Definir o buider (StateGraph), é um método construtor que inicia o grafo, executando o State. Os Parâmetros usados pelo StateGraph são:
    - **state_schema** (Obrigatório): É o State definido que vai carregar o grafico e garantir que os nodes retornem esse stado. Nesse caso a classe State definida inicialmente.
        ```python
        state_schema=State
        ```

    - **context_schema** (opcional): São informações globais, configuração dinamicas ou estáticas, parâmetros de ambiente.Exemplo:
        ```python
        class Context(TypedDict):
            temperature: float
            max_tokens: int
        ```

    - **input_schema** (opcional): Usado para validar a entrada dos dados no gráfico pelo invoke. se não for passado, ele assume por default o State passado no state_schema.
        ```
        input_schema=AgentState
        ``` 
    - **output_schema** (Opcional): É o formato que o grafo vai retonar após ser executado. Igualmente ao input_schema se não for passado assume o State passado no state_schema.
        ```python
        output_schema=AgentState
        ```
4. Adicionar os nodes e as edges ao buider.
    ```python
    # 4 - Adiconar nodes ao grafico
    buider.add_node("call_llm", call_llm)  # Cria um node (Nós) Fuções de execuções
    buider.add_edge(
        START, "call_llm"
    )  # Cria os edge (arestas) caminhos de execução
    buider.add_edge("call_llm", END)
    ```

5. Definir checkpoint para garantir que a llm carregue o contexto. E não tenha aminésia. No caso abaixo salva a conversa na memémoria RAM.
    ``` python
    checkpointer = (InMemorySaver())  # Variavel para criar um checkpoint e salvar o histórico
    ```
6. Compilar o grafico.
    ```python
    graph = buider.compile(checkpointer=checkpointer)
    ```
7. Criar o config para salvar as thread das conversas.
    ```python
    config = RunnableConfig(
        configurable={"thread_id": 1}
    )  # Runnable Config defini a configuração da thread para salvar o histórico
    ```
---
## Tools em agentes
Tools são função que a LLM sugere ao código ser chamada. A partir dai o codigo executa a função e retorna o resultado para a LLM. Segue o passo a passo para inserir tools no projeto:

1. Para criar tools basta criar uma lista de funções. Exemplo:

    ```python
    TOOLS: list[BaseTool] = [multiply, divide, subtraction, sum]
    ```
2. Após a criação da lista, deve-se criar um dicionário como o nome da função como chave e a função como valor. Ela é essencial para que o State consiga chama-la.
    ```python
    TOOLS_BY_NAME: dict[str, BaseTool] = {tool.name: tool for tool in TOOLS}
    ```
3. No node inicial deve-se chamar o método bind_tools para modificar o output da LLM e fazê-lo retornar o tool_call.
    ``` python
    llm_with_tools = load_llm().bind_tools(TOOLS)
    ```
4. Construir um node de tools para chamar as função. No exemplo abaixo mostra como a node consegue chamar as tools functions.
    ``` python
    def tool_node(state: State) -> State:
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
    ```
5. Criar uma função de rota para definir quando chamará o tool_node ou ir para o fim ou para outro node.
    ```python
    def router(state: State) -> Literal['tool_node', '__end__']:
        llm_response = state["messages"][-1] # busca a resposta da llm
        if getattr(llm_response, 'tool_calls', None): # verifica se retornou a tool_call
            return 'tool_node' # caso retorne chama a tool_node
        return '__end__' # caso não exista retorne __end__
    ```

Segue abaixo um exemplo da função de buidar o grafo usando tools
``` python
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
```
