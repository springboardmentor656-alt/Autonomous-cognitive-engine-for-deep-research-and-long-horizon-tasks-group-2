from typing import TypedDict, List, Dict
from langgraph.graph import StateGraph, END
from langchain_community.chat_models import ChatOllama
from tools.vfs import write_file, read_file

# -------------------------
# State Definition
# -------------------------
class AgentState(TypedDict):
    messages: List[Dict]
    todos: List[str]
    files: Dict[str, str]

# -------------------------
# LLM
# -------------------------
llm = ChatOllama(model="tinyllama", temperature=0)

# -------------------------
# Entry Node
# -------------------------
def react_entry(state: AgentState):
    user_text = state["messages"][-1]["content"]

    # Explicit long-input rule (Milestone-2 requirement)
    if len(user_text) > 400:
        summary = user_text[:400] + "..."
        write_file.invoke({
            "filename": "bmw_notes.txt",
            "content": summary
        })
        return {"messages": state["messages"], "files": state.get("files", {})}

    return {"messages": state["messages"], "files": state.get("files", {})}

# -------------------------
# Read Notes Node
# -------------------------
def read_notes(state: AgentState):
    notes = read_file.invoke({"filename": "bmw_notes.txt"})
    state["messages"].append({
        "role": "system",
        "content": f"Use these notes to create an action plan:\n{notes}"
    })
    return state

# -------------------------
# Write TODOs Node
# -------------------------
def write_todos(state: AgentState):
    prompt = (
        "Create a structured action plan based on the notes. "
        "Return only numbered TODO steps."
    )

    messages = state["messages"] + [{"role": "user", "content": prompt}]
    response = llm.invoke(messages)

    todos = [
        line.strip()
        for line in response.content.split("\n")
        if line.strip()
    ]

    return {
        "todos": todos,
        "messages": state["messages"]
    }

# -------------------------
# Graph
# -------------------------
graph = StateGraph(AgentState)

graph.add_node("react_entry", react_entry)
graph.add_node("read_notes", read_notes)
graph.add_node("write_todos", write_todos)

graph.set_entry_point("react_entry")

graph.add_edge("react_entry", "read_notes")
graph.add_edge("read_notes", "write_todos")
graph.add_edge("write_todos", END)

app = graph.compile()
