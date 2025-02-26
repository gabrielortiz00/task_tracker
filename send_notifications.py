import requests
import json
from datetime import datetime

# Pushover credentials (Replace with your real keys)
USER_KEY = "unpptgs51i26wwt3v7emycy7mpbqcq"
API_TOKEN = "ahk38b73rpjuphfxjgpcbrikrypbg4"

TASKS_FILE = "/Users/gabrielortiz/PycharmProjects/TaskTracker/tasks.json"


def load_tasks():
    """Load tasks from JSON file."""
    try:
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def send_notifications():
    """Send a notification with today's and upcoming tasks."""
    tasks = load_tasks()
    today = datetime.today().strftime("%Y-%m-%d")

    # Separate tasks into "today's tasks" and "upcoming tasks"
    today_tasks = [
        task for task in tasks
        if not task["completed"] and task["due_date"] == today
    ]

    upcoming_tasks = [
        task for task in tasks
        if not task["completed"] and datetime.strptime(task["due_date"], "%Y-%m-%d").date() > datetime.today().date()
    ]

    # Build the notification message
    message = "📌 **Today's Tasks:**\n"
    message += "\n".join(f"- {task['description']} (Due: {datetime.strptime(task['due_date'], '%Y-%m-%d').strftime('%B %d')})" for task in today_tasks) or "✅ No tasks for today!"

    message += "\n\n🔜 **Upcoming Tasks:**\n"
    message += "\n".join(f"- {task['description']} (Due: {datetime.strptime(task['due_date'], '%Y-%m-%d').strftime('%B %d')})" for task in upcoming_tasks) or "🎉 No upcoming tasks!"

    # Send the notification via Pushover
    requests.post("https://api.pushover.net/1/messages.json", data={
        "token": API_TOKEN,
        "user": USER_KEY,
        "message": message,
        "title": "Task Reminder"
    })

    print("Notification sent!")

# Run the notification function if script is executed directly
if __name__ == "__main__":
    send_notifications()


import os
print("DEBUG: Using tasks.json from:", os.path.abspath(TASKS_FILE))
