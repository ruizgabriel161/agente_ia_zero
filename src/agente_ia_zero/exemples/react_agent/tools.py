from langchain.tools import tool, BaseTool


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


@tool
def divide(a: float, b: float) -> float:
    """
    Multiply a / b and returns the llm_response

    Arguments:
        a -- :float dividend
        b -- :float divider

    Returns:
        the return float oh the equation a / b
    """
    return a / b


@tool
def sum(a: float, b: float) -> float:
    """
    Multiply a + b and returns the llm_response

    Arguments:
        a -- :float multiplicand
        b -- :float multiplier

    Returns:
        the return float oh the equation a * b
    """
    return a + b


@tool
def subtraction(a: float, b: float) -> float:
    """
    Multiply a - b and returns the llm_response

    Arguments:
        a -- :float
        b -- :float

    Returns:
        the return float oh the equation a - b
    """
    return a - b


TOOLS: list[BaseTool] = [multiply, divide, subtraction, sum]
TOOLS_BY_NAME: dict[str, BaseTool] = {tool.name: tool for tool in TOOLS}
