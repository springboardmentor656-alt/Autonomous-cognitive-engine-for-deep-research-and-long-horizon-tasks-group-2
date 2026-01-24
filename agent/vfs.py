# agent/vfs.py

from langsmith import traceable  # for tool-level tracing

class VirtualFileSystem:
    def __init__(self):
        self.files = {}

    @traceable(run_type="tool", name="List Files")
    def ls(self):
        return list(self.files.keys())

    @traceable(run_type="tool", name="Write File")
    def write_file(self, filename: str, content: str):
        self.files[filename] = content
        return f"Written {filename}."

    @traceable(run_type="tool", name="Read File")
    def read_file(self, filename: str):
        if filename not in self.files:
            return f"Error: {filename} not found."
        return self.files[filename]

    @traceable(run_type="tool", name="Edit File")
    def edit_file(self, filename: str, content: str):
        if filename not in self.files:
            return f"Error: {filename} not found."
        self.files[filename] += content
        return f"Edited {filename}."
