from langchain_core.tools import tool

# In-memory virtual file system
VFS = {}

@tool
def write_file(filename: str, content: str) -> str:
    """
    Write content to a virtual file.
    """
    VFS[filename] = content
    return f"Saved content to {filename}"

@tool
def read_file(filename: str) -> str:
    """
    Read content from a virtual file.
    """
    return VFS.get(filename, "")
