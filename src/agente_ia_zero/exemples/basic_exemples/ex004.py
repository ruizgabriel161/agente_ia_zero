from langchain.tools import tool, BaseTool
from langchain.chat_models import init_chat_model
from langchain_core.messages import (
    BaseMessage,
    SystemMessage,
    HumanMessage,
    AIMessage,
    ToolMessage,
)
from rich import print
from rich.markdown import Markdown


# 1 - Criar a ferramenta
@tool
def multiply(a: float, b: float) -> float:
    """
    Multiply a * b and returns the llm_response

    Arguments:
        a -- :float multiplicand
        b -- :float multiplier

    Returns:
        the return float oh the equation a * b
    """
    return a * b


llm = init_chat_model("ollama:llama3.2")


system_message = SystemMessage(
    "You are an AI assistant with access to tools, but you must NEVER call "
    "any tool unless the user explicitly requests the tool's functionality.\n\n"
    "Rules:\n"
    "- Do NOT call a tool unless the user clearly asks for it.\n"
    "- Do NOT invent tool arguments.\n"
    "- Do NOT assume the user wants a tool.\n"
    "- Do NOT call tools when the user only greets, talks, or asks general questions.\n"
    "- Only call a tool if the user explicitly says something like: "
    "'use the tool', 'call the multiply tool', 'calculate using multiply', "
    "'run the tool', or similar.\n\n"
    "If you are uncertain whether the user wants to use a tool: DO NOT CALL ANY TOOL."
)

human_message = HumanMessage("Oi, sou Gabriel. Quanto é 5x5")

messages: list[BaseMessage] = [system_message, human_message]


tools: list[BaseTool] = [multiply]

tools_by_name: dict[str, BaseTool] = {tool.name: tool for tool in tools}

llm_with_tools = llm.bind_tools(tools=tools, tool_choice="none")

llm_response: AIMessage = llm_with_tools.invoke(messages)

messages.append(llm_response)
print(Markdown("---"))

print(llm_response)

if isinstance(llm_response, AIMessage) and getattr(
    llm_response, "tool_calls", None
):
    call = llm_response.tool_calls[-1]
    name, args, id_ = call["name"], call["args"], call["id"]
    status = "success"

    try:
        content = tools_by_name[name].invoke(args)

    except Exception as e:
        content = f"Please, fix your mistake: {e}"

    tool_message = ToolMessage(
        content=content, tool_call_id=id_, status=status
    )

    messages.append(tool_message)

    llm_response: AIMessage = llm_with_tools.invoke(messages)
    messages.append(llm_response)

print(Markdown("---"))
print(messages)
print(Markdown("---"))
