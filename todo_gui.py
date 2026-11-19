import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from todo import load_tasks, save_tasks

# A separate window lets us add a visual interface without replacing the CLI app.
root = tk.Tk()
root.title("My To-Do List")
root.geometry("420x500")
root.configure(bg="#ffd3f3")

style = ttk.Style(root)
style.theme_use("clam")
style.configure(
    "Title.TLabel",
    background="#f4f6f8",
    foreground="#243447",
    font=("Segoe UI", 22, "bold"),
)
style.configure("Add.TButton", background="#3b82f6", foreground="white", padding=8)
style.configure("Done.TButton", background="#16a34a", foreground="white", padding=8)
style.configure("Delete.TButton", background="#dc2626", foreground="white", padding=8)

title = ttk.Label(root, text="My Tasks", style="Title.TLabel")
title.pack(pady=24)

subtitle = tk.Label(
    root,
    text="Small steps, one task at a time.",
    font=("Segoe UI", 10),
    bg="#ffffff",
    fg="#ff499e",
)
subtitle.pack(pady=(0, 12))

task_entry = tk.Entry(root, font=("Segoe UI", 12))
task_entry.pack(fill="x", padx=24, ipady=8, pady=8)

action_frame = tk.Frame(root, bg="#ffdff3")
action_frame.pack(fill="x", padx=24, pady=8)

add_button = ttk.Button(action_frame, text="Add task", style="Add.TButton")
add_button.pack(anchor="e")

task_list = tk.Listbox(
    root,
    font=("Segoe UI", 12),
    height=10,
    bg="pink",
    fg="#FDBBEE",
    selectbackground="#ffe4fd",
    selectforeground="#ff76f4",
    bd=0,
    highlightthickness=1,
    highlightbackground="#ff00e6",
)


task_list.pack(fill="both", expand=True, padx=24, pady=16)

count_label = tk.Label(
    root, text="", font=("Segoe UI", 10), bg="#f4f6f8", fg="#64748b"
)
count_label.pack(pady=(0, 8))


def refresh_tasks():
    """Reload saved tasks into the window's list."""
    task_list.delete(0, tk.END)

    tasks = load_tasks()
    remaining = sum(not task["done"] for task in tasks)
    word = "task" if remaining == 1 else "tasks"
    count_label.config(text=f"{remaining} {word} remaining")

    for index, task in enumerate(tasks):
        status = "[x]" if task["done"] else "[ ]"
        task_list.insert(tk.END, f"{status} {task['text']}")

        color = "#ffffff" if task["done"] else "#06E6FF"
        task_list.itemconfigure(index, fg=color)


def add_task_from_window():
    """Save the text-box task and refresh the list."""
    text = task_entry.get().strip()

    if not text:
        return

    tasks = load_tasks()
    tasks.append({"text": text, "done": False})
    save_tasks(tasks)
    task_entry.delete(0, tk.END)
    refresh_tasks()


def mark_selected_done():
    """Mark the selected task as done and refresh the list."""
    selection = task_list.curselection()

    if not selection:
        messagebox.showinfo("Select a task", "Click a task in the list first.")
        return

    tasks = load_tasks()
    tasks[selection[0]]["done"] = True
    save_tasks(tasks)
    refresh_tasks()


def delete_selected_task():
    """Ask before deleting the selected task."""
    selection = task_list.curselection()

    if not selection:
        messagebox.showinfo("Select a task", "Click a task in the list first.")
        return

    tasks = load_tasks()
    index = selection[0]

    if not messagebox.askyesno(
        "Delete task",
        f"Delete '{tasks[index]['text']}'?"
    ):
        return

    tasks.pop(index)
    save_tasks(tasks)
    refresh_tasks()


add_button.configure(command=add_task_from_window)
mark_button = ttk.Button(
    action_frame, text="Mark done", command=mark_selected_done, style="Done.TButton"
)
mark_button.pack(side="left")
delete_button = ttk.Button(
    action_frame, text="Delete", command=delete_selected_task, style="Delete.TButton"
)
delete_button.pack(side="left", padx=8)
task_entry.bind("<Return>", lambda event: add_task_from_window())
refresh_tasks()

root.mainloop()