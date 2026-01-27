def ls(state):
    return list(state["files"].keys())

def write_file(state, filename: str, content: str):
    state["files"][filename] = content
    return f"File '{filename}' written successfully."

def read_file(state, filename: str):
    if filename not in state["files"]:
        return "File not found."
    return state["files"][filename]

def edit_file(state, filename: str, new_content: str):
    if filename not in state["files"]:
        return "File not found."
    state["files"][filename] = new_content
    return f"File '{filename}' updated successfully."
