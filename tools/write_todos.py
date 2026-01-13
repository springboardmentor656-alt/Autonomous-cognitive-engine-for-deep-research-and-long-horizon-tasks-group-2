from langchain.tools import tool
from langchain_ollama import ChatOllama

llm = ChatOllama(model="tinyllama", temperature=0)

@tool
def write_todos(text: str) -> list:
    """
    Convert text into a simple TODO list.
    """
    prompt = f"""
Break the following text into a clear, numbered TODO list.
Return only the list.

{text}
"""
    response = llm.invoke(prompt)
    return response.content.split("\n")
