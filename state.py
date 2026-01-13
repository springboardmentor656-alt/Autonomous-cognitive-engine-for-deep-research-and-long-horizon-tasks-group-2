from typing import TypedDict, List

class AgentState(TypedDict):
    task: str
    todos: List[str]
    final_output: str
