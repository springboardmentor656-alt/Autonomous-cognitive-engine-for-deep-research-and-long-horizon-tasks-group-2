from agent.react_agent import app

print("\n=== Deep Agent (TinyLlama TODO Planner) ===")
print("Type a task to break into TODOs")
print("Type 'exit' to quit\n")

while True:
    user_input = input("You > ")
    if user_input.lower() == "exit":
        break

    state = {
        "messages": [{"role": "user", "content": user_input}],
        "todos": []
    }

    result = app.invoke(state)

    print("\nGenerated TODO Steps:\n")
    for todo in result["todos"]:
        print(f"{todo['id']}. {todo['task']}")
    print("\n-----------------------------\n")
