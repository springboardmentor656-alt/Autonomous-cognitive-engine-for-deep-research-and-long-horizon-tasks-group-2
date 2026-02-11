from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

from langgraph.graph import StateGraph, END


from state import AgentState
from tools import write_todos, write_file, delegate_task
from prompts import SUPERVISOR_PROMPT

llm=ChatOpenAI(model="gpt-3.5-turbo")

import os



# -------- Nodes --------

def planner(state: AgentState):
    todos = write_todos(state["input"])
    return {"todos": todos}


def executor(state: AgentState):
    task = state["current_task"]

    if "summarize" in task.lower():
        result = delegate_task("summarizer", task)

        # FIX: safely extract summary
        summary = result.get("summary") or result.get("results", {}).get("summary")

        if summary:
            write_file(state, f"{task}.txt", summary)

        return {"results": result}

    return {}



def synthesizer(state: AgentState):
    combined = "\n".join(state["files"].values())
    return {
        "final_output": "[MOCK FINAL OUTPUT]\n" + combined
    }

def router(state: AgentState):
    for todo in state["todos"]:
        if todo["status"] == "pending":
            state["current_task"] = todo["task"]
            todo["status"] = "done"
            return "execute"
    return "synthesize"


# -------- Graph --------

graph = StateGraph(AgentState)

graph.add_node("plan", planner)
graph.add_node("execute", executor)
graph.add_node("synthesize", synthesizer)

graph.set_entry_point("plan")
graph.add_conditional_edges("plan", router)
graph.add_conditional_edges("execute", router)
graph.add_edge("synthesize", END)

app = graph.compile()


# -------- Run --------

if __name__ == "__main__":
    output = app.invoke({
        "input": "Summarize artificial intelligence. Summarize machine learning.",
        "todos": [],
        "current_task": "",
        "files": {},
        "results": {},
        "final_output": ""
    })

    print("\nFINAL OUTPUT:\n")
    print(output["final_output"])
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv
load_dotenv()

from state import AgentState
from tools import write_todos, write_file, delegate_task


# -------- Nodes --------

def planner(state: AgentState):
    todos = write_todos(state["input"])
    return {"todos": todos}


def executor(state: AgentState):
    task = state["current_task"]

    if "summarize" in task.lower():
        result = delegate_task("summarizer", task)
        summary = result["summary"]

        new_files = dict(state.get("files", {}))
        new_files[f"{task}.txt"] = summary

        return {
            "files": new_files,
            "results": result
        }

    return {}


def synthesizer(state: AgentState):
    combined = "\n\n".join(state.get("files", {}).values())

    return {
        "files": state.get("files", {}),
        "final_output": "[MOCK FINAL OUTPUT]\n" + combined
    }


def router(state: AgentState):
    for todo in state["todos"]:
        if todo["status"] == "pending":
            state["current_task"] = todo["task"]
            todo["status"] = "done"
            return "execute"
    return "synthesize"


# -------- Graph --------

graph = StateGraph(AgentState)

graph.add_node("plan", planner)
graph.add_node("execute", executor)
graph.add_node("synthesize", synthesizer)

graph.set_entry_point("plan")
graph.add_conditional_edges("plan", router)
graph.add_conditional_edges("execute", router)
graph.add_edge("synthesize", END)

app = graph.compile()


# -------- Run --------

if __name__ == "__main__":
    output = app.invoke({
        "input": "Summarize artificial intelligence. Summarize machine learning.",
        "todos": [],
        "current_task": "",
        "files": {},
        "results": {},
        "final_output": ""
    })

    print("\nFINAL OUTPUT:\n")
    print(output["final_output"])
