from langgraph.graph import StateGraph, END
from langsmith import traceable
from agent.state import AgentState
from tools.write_todos import write_todos

@traceable(name="tinyllama_planner_agent")
def planner_node(state: AgentState):
    user_message = state["messages"][-1]["content"]
    todos = write_todos.invoke(user_message)
    return {"todos": todos}

graph = StateGraph(AgentState)
graph.add_node("planner", planner_node)
graph.set_entry_point("planner")
graph.add_edge("planner", END)

app = graph.compile()
