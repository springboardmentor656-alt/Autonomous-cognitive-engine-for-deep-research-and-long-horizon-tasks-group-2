from langchain.tools import tool
from langchain_ollama import ChatOllama

llm = ChatOllama(model="tinyllama", temperature=0)

@tool
def write_todos(text: str) -> list:
    """
    Convert text into a numbered TODO list.
    """

    prompt = f"""
Convert the following content into a numbered TODO list.
Return only numbered steps.

{text}
"""

    response = llm.invoke([
        {"role": "user", "content": prompt}
    ])

    todos = []
    for line in response.content.split("\n"):
        line = line.strip()
        if line and line[0].isdigit():
            todos.append(line)

    return todos
