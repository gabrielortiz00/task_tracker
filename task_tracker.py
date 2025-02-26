from flask import Flask, render_template, request, redirect, url_for
import json
import requests
from datetime import datetime

app = Flask(__name__)

# Pushover credentials (Replace with your real keys)
USER_KEY = "unpptgs51i26wwt3v7emycy7mpbqcq"
API_TOKEN = "ahk38b73rpjuphfxjgpcbrikrypbg4"

TASKS_FILE = "tasks.json"

def load_tasks():
    """Load tasks from JSON file."""
    try:
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_tasks(tasks):
    """Save tasks to JSON file."""
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

@app.route("/")
def index():
    tasks = load_tasks()
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add_task():
    """Add a new task."""
    description = request.form.get("description")
    due_date = request.form.get("due_date")

    if description and due_date:
        tasks = load_tasks()
        tasks.append({"description": description, "due_date": due_date, "completed": False})
        save_tasks(tasks)

    return redirect(url_for("index"))

@app.route("/complete/<int:task_id>")
def complete_task(task_id):
    """Mark a task as completed."""
    tasks = load_tasks()
    if 0 <= task_id < len(tasks):
        tasks[task_id]["completed"] = True
        save_tasks(tasks)
    return redirect(url_for("index"))

@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    """Delete a task."""
    tasks = load_tasks()
    if 0 <= task_id < len(tasks):
        del tasks[task_id]
        save_tasks(tasks)
    return redirect(url_for("index"))

def send_daily_notification():
    """Send daily notification with pending tasks."""
    tasks = load_tasks()
    pending_tasks = [task for task in tasks if not task["completed"]]

    if not pending_tasks:
        message = "🎉 No pending tasks today! Enjoy your day!"
    else:
        message = "📌 Daily Tasks:\n" + "\n".join(f"- {task['description']} (Due: {task['due_date']})" for task in pending_tasks)

    requests.post("https://api.pushover.net/1/messages.json", data={
        "token": API_TOKEN,
        "user": USER_KEY,
        "message": message,
        "title": "Daily Task Reminder"
    })
    print("Daily notification sent!")

if __name__ == "__main__":
    app.run(debug=True)
