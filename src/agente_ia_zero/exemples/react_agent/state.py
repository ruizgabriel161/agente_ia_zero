from typing import Annotated, Sequence, TypedDict
from langgraph.graph.message import BaseMessage, add_messages


class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
