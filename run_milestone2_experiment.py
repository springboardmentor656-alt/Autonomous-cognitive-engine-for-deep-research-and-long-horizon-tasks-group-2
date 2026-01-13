from dotenv import load_dotenv
load_dotenv()

from langsmith.evaluation import evaluate
from agent.react_agent import app


def agent_runner(example):
    state = {
        "messages": [{"role": "user", "content": example["input"]}],
        "todos": [],
        "files": {},
        "needs_read": False
    }

    result = app.invoke(state)

    # LangSmith expects an "output" key
    return {
        "output": result["todos"]
    }


evaluate(
    agent_runner,
    data="milestone-2-vfs",   # make sure this dataset exists in LangSmith
    experiment_prefix="milestone-2-vfs",
)

print("Evaluation complete — check LangSmith")
