from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition

from agent.state import AgentState
from agent.planner import write_todos
from agent.filesystem import ls, write_file, read_file, edit_file
from agent.react_loop import agent_runnable


# -------------------------------------------------
# Register all tools (Milestone-1 + Milestone-2)
# -------------------------------------------------
tools = [
    write_todos,      # Milestone-1: Task planning
    ls,               # Milestone-2: List files
    write_file,       # Milestone-2: Write file
    read_file,        # Milestone-2: Read file
    edit_file         # Milestone-2: Edit file
]


# -------------------------------------------------
# Create the LangGraph StateGraph
# -------------------------------------------------
graph = StateGraph(state_schema=AgentState)


# -------------------------------------------------
# Agent node (LLM reasoning / ReAct loop)
# -------------------------------------------------
graph.add_node("agent", agent_runnable)


# -------------------------------------------------
# Tool execution node
# -------------------------------------------------
graph.add_node("tools", ToolNode(tools))


# -------------------------------------------------
# Define graph edges (control flow)
# -------------------------------------------------
graph.add_edge("tools", "agent")
graph.add_edge("agent", END) 

# NOTE: Since the current agent implementation (react_loop) returns a final string 
# and doesn't emit tool calls in a way ToolNode expects, we are routing to END for now.
# Future TODO: Implement a proper router or use tools_condition if agent emits tool_calls.



# -------------------------------------------------
# Entry point
# -------------------------------------------------
graph.set_entry_point("agent")


# -------------------------------------------------
# Compile graph (this is what you import & run)
# -------------------------------------------------
app = graph.compile()




