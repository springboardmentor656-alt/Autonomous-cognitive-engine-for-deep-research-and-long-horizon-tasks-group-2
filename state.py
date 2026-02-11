from typing import TypedDict, List, Dict, Any


class AgentState(TypedDict):
    input: str
    todos: List[Dict[str, str]]   # [{task, status}]
    current_task: str
    files: Dict[str, str]         # virtual memory
    results: Dict[str, Any]
    final_output: str
