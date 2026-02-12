from typing import TypedDict, List, Dict, Any

class AgentState(TypedDict):
    messages: List[Any]
    todos: List[Dict]
    files: Dict[str, str]

