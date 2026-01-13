# graph/graph.py

from agent.planner import plan_task

def build_graph():
    """
    Builds a simple agent graph for LangSmith experiments.
    Invoking the graph generates TODO steps for a task.
    """
    # The 'invoke' method simulates the agent receiving a state with messages
    def invoke(self, state):
        """
        state: dict with "messages" key (list of {"role": ..., "content": ...})
        Returns a dict with "todos" key containing list of steps
        """
        user_input = state.get("messages", [{}])[0].get("content", "")
        todos = plan_task(user_input)
        return {"todos": todos}

    return type("AgentGraph", (), {"invoke": invoke})()




