from dotenv import load_dotenv
load_dotenv()

from langgraph.graph import StateGraph, END


def write_todos(objective: str):
    tasks = objective.split(".")
    return [{"task": t.strip(), "status": "pending"} for t in tasks if t.strip()]
def write_file(state, filename, content):
    state["files"][filename] = content
    return state


def read_file(state, filename):
    return state["files"].get(filename, "")


def list_files(state):
    return list(state["files"].keys())
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from prompts import SUMMARIZER_PROMPT

llm = ChatOpenAI(model="gpt-3.5-turbo")


def summarize_node(state):
    return {
        "results": {
            "summary": f"[MOCK SUMMARY]\n{state['input']}"
        }
    }
def build_summarizer():
    graph = StateGraph(dict)
    graph.add_node("summarize", summarize_node)
    graph.set_entry_point("summarize")
    graph.add_edge("summarize", END)
    return graph.compile()


summarizer_agent = build_summarizer()
def delegate_task(agent_name: str, task_input: str):
    if agent_name == "summarizer":
        return summarizer_agent.invoke({"input": task_input})
    else:
        raise ValueError("Unknown agent")
