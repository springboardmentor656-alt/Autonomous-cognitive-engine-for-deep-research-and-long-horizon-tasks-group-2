from typing import TypedDict, List, Dict

class AgentState(TypedDict):
    messages: List[Dict]
    todos: List[Dict]
