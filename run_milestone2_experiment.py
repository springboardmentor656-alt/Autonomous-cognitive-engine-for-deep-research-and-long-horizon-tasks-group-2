from dotenv import load_dotenv
load_dotenv()

from langsmith.evaluation import evaluate
from agent.react_agent import app


def agent_runner(example):
    state = {
        "messages": [{"role": "user", "content": example["input"]}],
        "todos": [],
        "files": {}
    }
    return app.invoke(state)


evaluate(
    agent_runner,
    data="difference_display",
    experiment_prefix="milestone-2-vfs",
)