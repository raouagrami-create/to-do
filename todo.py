import json
import sys
from pathlib import Path

# Keeping the data beside where you run the app makes it easy to find.
DATA_FILE = Path.cwd() / "todo.json"


def load_tasks():
    """Load saved tasks, or start with an empty list."""
    if not DATA_FILE.exists():
        return []

    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_tasks(tasks):
    """Save tasks so they are available next time."""
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=2)

def add_task(text):
    """Add a task and save the updated list."""
    tasks = load_tasks()
    tasks.append({"text": text, "done": False})
    save_tasks(tasks)
    print(f"Added: {text}")


def list_tasks():
    """Show each task's number, status, and text."""
    tasks = load_tasks()

    if not tasks:
        print("No tasks yet.")
        return

    for number, task in enumerate(tasks, start=1):
        status = "done" if task["done"] else "not done"
        print(f"{number}. [{status}] {task['text']}")

def mark_done(number):
    """Mark the numbered task as done and save it."""
    tasks = load_tasks()
    index = number - 1

    if index < 0 or index >= len(tasks):
        print("That task number doesn't exist.")
        return

    tasks[index]["done"] = True
    save_tasks(tasks)
    print(f"Marked done: {tasks[index]['text']}")


def delete_task(number):
    """Delete the numbered task and save the updated list."""
    tasks = load_tasks()
    index = number - 1

    if index < 0 or index >= len(tasks):
        print("That task number doesn't exist.")
        return

    removed = tasks.pop(index)
    save_tasks(tasks)
    print(f"Deleted: {removed['text']}")

def main():
    """Read the command and call the matching task function."""
    if len(sys.argv) < 2:
        print("Usage: python todo.py [add|list|done|delete]")
        return

    command = sys.argv[1]

    if command == "add":
        if len(sys.argv) < 3:
            print('Usage: python todo.py add "task text"')
            return

        # Join the words so task text can contain spaces.
        add_task(" ".join(sys.argv[2:]))

    elif command == "list":
        list_tasks()

    elif command in ("done", "delete"):
        if len(sys.argv) != 3:
            print(f"Usage: python todo.py {command} NUMBER")
            return

        try:
            number = int(sys.argv[2])
        except ValueError:
            print("Task number must be a whole number.")
            return

        if command == "done":
            mark_done(number)
        else:
            delete_task(number)

    else:
        print("Unknown command. Use add, list, done, or delete.")


# Run main() only when this file is started as a program.
if __name__ == "__main__":
    main()