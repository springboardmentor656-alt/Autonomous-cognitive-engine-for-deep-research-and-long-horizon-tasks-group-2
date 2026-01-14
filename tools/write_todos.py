from langchain.tools import tool
from langchain_ollama import OllamaLLM

# Initialize TinyLlama via Ollama
llm = OllamaLLM(
    model="tinyllama",
    temperature=0
)

@tool
def write_todos(task: str):
    """
    Break a task into clear, ordered TODO steps.
    """

    prompt = f"""
You are a task planning assistant.
Break the task below into clear, numbered TODO steps.
Return ONLY the list.

Task: {task}
"""

    # Call the LLM
    response = llm.invoke(prompt)

    # Parse response into structured TODOs
    todos = []
    for i, line in enumerate(response.split("\n")):
        line = line.strip()
        if line:
            todos.append({
                "id": i + 1,
                "task": line
            })

    return todos
