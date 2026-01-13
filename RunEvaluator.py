from dotenv import load_dotenv
load_dotenv()

from langsmith.evaluation import evaluate
from agent.react_agent import app

DATASET_NAME = "milestone-1-todo-eval"

def agent_runner(example):
    """
    Called by LangSmith for each dataset row.
    """
    state = {
        "messages": [
            {"role": "user", "content": example["input"]}
        ],
        "todos": []
    }

    result = app.invoke(state)

    return {
        "output": result["todos"]
    }


evaluate(
    agent_runner,
    data=DATASET_NAME
)

print("Experiment created. Check LangSmith → Experiments.")
