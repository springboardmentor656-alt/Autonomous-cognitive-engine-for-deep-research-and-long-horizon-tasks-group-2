from langsmith import traceable
from tools.planning import write_todos
from agent.vfs import VirtualFileSystem

vfs = VirtualFileSystem()

@traceable(run_type="chain", name="Task Supervisor")
def run_tasks(tasks):
    for i, task in enumerate(tasks, start=1):
        print("\n" + "=" * 40)
        print(f"Task {i}: {task}")
        print("=" * 40)

        # Step 1: Plan subtasks
        todos = write_todos(task)

        # Step 2: Save to VFS
        todo_file = f"task_{i}_todos.txt"
        vfs.write_file(todo_file, "\n".join(todos))
        print("Saved Subtasks to VFS:")
        for todo in todos:
            print(todo)

        # Step 3: Read back from VFS
        saved_todos = vfs.read_file(todo_file)
        print("\nLoaded from VFS:")
        print(saved_todos)

        # Step 4: Create final combined output
        final_file = f"task_{i}_final.txt"
        final_content = (
            f"Task: {task}\n\n"
            f"Subtasks:\n{saved_todos}\n\n"
            "Summary: Task successfully broken down and stored using context offloading."
        )
        vfs.write_file(final_file, final_content)

        print("\nFinal Output Saved to VFS:")
        print(vfs.read_file(final_file))
        print("=" * 40)
