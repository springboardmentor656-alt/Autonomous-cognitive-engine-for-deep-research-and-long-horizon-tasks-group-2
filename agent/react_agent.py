from typing import TypedDict, List, Dict
from langgraph.graph import StateGraph, END
from tools.write_todos import write_todos
from tools.vfs import write_file, read_file

class AgentState(TypedDict):
    messages: List[Dict]
    todos: List[str]
    files: Dict[str, str]
    needs_read: bool

# ---------- ENTRY ----------
def react_entry(state: AgentState):
    user_text = state["messages"][-1]["content"]

    # Long prompt → write notes
    if len(user_text) > 400:
        write_file.invoke({
            "filename": "notes.txt",
            "content": user_text
        })
        state["needs_read"] = True
        return state

    # Short prompt → direct TODOs
    state["todos"] = write_todos.invoke(user_text)
    state["needs_read"] = False
    return state

# ---------- READ NOTES ----------
def read_notes(state: AgentState):
    notes = read_file.invoke({"filename": "notes.txt"})
    state["todos"] = write_todos.invoke(notes)
    return state

# ---------- ROUTER ----------
def router(state: AgentState):
    return "read_notes" if state.get("needs_read") else END

# ---------- GRAPH ----------
graph = StateGraph(AgentState)

graph.add_node("react_entry", react_entry)
graph.add_node("read_notes", read_notes)

graph.set_entry_point("react_entry")
graph.add_conditional_edges("react_entry", router)
graph.add_edge("read_notes", END)

app = graph.compile()
