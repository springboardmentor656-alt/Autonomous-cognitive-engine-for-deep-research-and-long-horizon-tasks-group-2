def write_file(state, filename, content):
    state["files"][filename] = content
    return filename


def read_file(state, filename):
    return state["files"].get(filename, "")


def ls(state):
    return list(state["files"].keys())
