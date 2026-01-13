"""
ReAct reasoning loop for the Agentic AI system with Ollama LLaMA integration.
"""

from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from agent.prompts import REACT_REASON_PROMPT  # ✅ import from prompts, not from react_loop


def react_loop(task: str, todos: list):
    """
    Execute a list of TODOs step by step using a reasoning LLM (Ollama).

    Args:
        task (str): The main task description
        todos (list): List of TODO items to execute

    Returns:
        str: Combined reasoning/execution responses for all TODOs
    """

    # Initialize the Ollama model
    llm = ChatOllama(
        model="tinyllama",   # You can change to llama3 if needed
        temperature=0.2
    )

    outputs = []

    for todo in todos:
        # -----------------
        # REASON
        # -----------------
        print(f"\n🧠 Reasoning on: {todo}")

        # Format the reasoning prompt
        prompt = REACT_REASON_PROMPT.format(
            task=task,
            todo=todo
        )

        # -----------------
        # ACT (invoke LLM)
        # -----------------
        response = llm.invoke([
            HumanMessage(content=prompt)
        ])

        # -----------------
        # OBSERVE
        # -----------------
        print("👀 Observation received")
        outputs.append(response.content)

    # Combine all responses into one text block
    return "\n\n".join(outputs)


# -----------------------------
# Demo (standalone)
# -----------------------------
if __name__ == "__main__":
    task = "Build a weather app using Python and Flask"
    todos = [
        "Set up Flask project structure",
        "Create home page route",
        "Connect to weather API",
        "Display weather data on front-end"
    ]

    final_output = react_loop(task, todos)
    print("\n=== Final Combined Output ===")
    print(final_output)
