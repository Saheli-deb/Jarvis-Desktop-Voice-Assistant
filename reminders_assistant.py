import os
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
import threading
import time
from plyer import notification
import webbrowser
from advanced_notifications import get_notification_system

load_dotenv()

# Reminders storage
REMINDERS_FILE = "reminders.json"
TODO_FILE = "todo_list.json"

# Advanced notification system
notification_system = get_notification_system()

# Notification thread
notification_thread = None
stop_notifications = False

def show_notification(title, message, duration=10):
    """Show a desktop notification using advanced system"""
    try:
        notification_system.show_advanced_notification(
            title=title,
            message=message,
            notification_type="reminder",
            duration=duration,
            sound=True
        )
        print(f"🔔 Advanced Notification: {title} - {message}")
    except Exception as e:
        print(f"❌ Failed to show notification: {e}")

def check_due_items():
    """Check for due reminders and todos and show advanced notifications"""
    global stop_notifications
    
    while not stop_notifications:
        try:
            # Check reminders
            reminders = load_reminders()
            todos = load_todos()
            now = datetime.now()
            
            for reminder in reminders:
                if not reminder['completed'] and reminder['due_date']:
                    due_date = datetime.fromisoformat(reminder['due_date'])
                    # Check if due within the next minute
                    if due_date <= now and due_date > now - timedelta(minutes=1):
                        notification_system.show_reminder_notification(reminder)
            
            # Check todos (for todos with due dates)
            for todo in todos:
                if not todo['completed'] and todo.get('due_date'):
                    due_date = datetime.fromisoformat(todo['due_date'])
                    if due_date <= now and due_date > now - timedelta(minutes=1):
                        notification_system.show_todo_notification(todo)
            
            # Sleep for 30 seconds before next check
            time.sleep(30)
            
        except Exception as e:
            print(f"❌ Error in notification thread: {e}")
            time.sleep(60)  # Wait longer on error

def start_notification_service():
    """Start the background notification service"""
    global notification_thread, stop_notifications
    stop_notifications = False
    notification_thread = threading.Thread(target=check_due_items, daemon=True)
    notification_thread.start()
    print("🔔 Notification service started")

def stop_notification_service():
    """Stop the background notification service"""
    global stop_notifications
    stop_notifications = True
    print("🔔 Notification service stopped")

def load_reminders():
    """Load reminders from JSON file"""
    if os.path.exists(REMINDERS_FILE):
        with open(REMINDERS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_reminders(reminders):
    """Save reminders to JSON file"""
    with open(REMINDERS_FILE, 'w') as f:
        json.dump(reminders, f, indent=2)

def load_todos():
    """Load todo items from JSON file"""
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE, 'r') as f:
            return json.load(f)
    return []

def save_todos(todos):
    """Save todo items to JSON file"""
    with open(TODO_FILE, 'w') as f:
        json.dump(todos, f, indent=2)

def add_reminder(title, due_date=None, priority="medium", description=""):
    """Add a new reminder with notification support"""
    reminders = load_reminders()
    
    # Parse due date if provided
    due_datetime = None
    if due_date:
        try:
            if '/' in due_date:
                due_datetime = datetime.strptime(due_date, '%m/%d/%Y')
            elif '-' in due_date:
                due_datetime = datetime.strptime(due_date, '%Y-%m-%d')
            else:
                due_datetime = datetime.now()
        except ValueError:
            print("❌ Invalid date format. Use MM/DD/YYYY")
            return False
    
    new_reminder = {
        'id': len(reminders) + 1,
        'title': title,
        'due_date': due_datetime.isoformat() if due_datetime else None,
        'priority': priority.lower(),
        'description': description,
        'completed': False,
        'created': datetime.now().isoformat()
    }
    
    reminders.append(new_reminder)
    save_reminders(reminders)
    print(f"✅ Reminder added: {title}")
    if due_datetime:
        print(f"   📅 Due: {due_datetime.strftime('%B %d, %Y')}")
        print(f"   🔔 Notification will appear when due")
    print(f"   ⚡ Priority: {priority}")
    return True

def add_todo(title, priority="medium", description="", due_date=None):
    """Add a new todo item with optional due date"""
    todos = load_todos()
    
    # Parse due date if provided
    due_datetime = None
    if due_date:
        try:
            if '/' in due_date:
                due_datetime = datetime.strptime(due_date, '%m/%d/%Y')
            elif '-' in due_date:
                due_datetime = datetime.strptime(due_date, '%Y-%m-%d')
            else:
                due_datetime = datetime.now()
        except ValueError:
            print("❌ Invalid date format. Use MM/DD/YYYY")
            return False
    
    new_todo = {
        'id': len(todos) + 1,
        'title': title,
        'priority': priority.lower(),
        'description': description,
        'due_date': due_datetime.isoformat() if due_datetime else None,
        'completed': False,
        'created': datetime.now().isoformat()
    }
    
    todos.append(new_todo)
    save_todos(todos)
    print(f"✅ Todo added: {title}")
    if due_datetime:
        print(f"   📅 Due: {due_datetime.strftime('%B %d, %Y')}")
        print(f"   🔔 Notification will appear when due")
    print(f"   ⚡ Priority: {priority}")
    return True

def list_reminders(show_completed=False):
    """List all reminders"""
    reminders = load_reminders()
    if not reminders:
        print("📅 No reminders found.")
        return []
    
    # Sort by priority and due date
    priority_order = {"high": 1, "medium": 2, "low": 3}
    reminders.sort(key=lambda x: (priority_order.get(x['priority'], 4), x['due_date'] or '9999'))
    
    if not show_completed:
        reminders = [r for r in reminders if not r['completed']]
    
    if not reminders:
        print("📅 No active reminders found.")
        return []
    
    print(f"\n📅 Reminders ({len(reminders)} items):")
    print("=" * 50)
    
    for reminder in reminders:
        status = "✅" if reminder['completed'] else "⏰"
        priority_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(reminder['priority'], "⚪")
        
        print(f"{status} {priority_icon} {reminder['title']}")
        if reminder['due_date']:
            due_date = datetime.fromisoformat(reminder['due_date'])
            print(f"   📅 Due: {due_date.strftime('%B %d, %Y')}")
        if reminder['description']:
            print(f"   📝 {reminder['description']}")
        print("-" * 30)
    
    return reminders

def list_todos(show_completed=False):
    """List all todo items"""
    todos = load_todos()
    if not todos:
        print("📋 No todo items found.")
        return []
    
    # Sort by priority
    priority_order = {"high": 1, "medium": 2, "low": 3}
    todos.sort(key=lambda x: priority_order.get(x['priority'], 4))
    
    if not show_completed:
        todos = [t for t in todos if not t['completed']]
    
    if not todos:
        print("📋 No active todo items found.")
        return []
    
    print(f"\n📋 Todo List ({len(todos)} items):")
    print("=" * 50)
    
    for todo in todos:
        status = "✅" if todo['completed'] else "⏳"
        priority_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(todo['priority'], "⚪")
        
        print(f"{status} {priority_icon} {todo['title']}")
        if todo['description']:
            print(f"   📝 {todo['description']}")
        print("-" * 30)
    
    return todos

def mark_reminder_complete(reminder_id):
    """Mark a reminder as complete"""
    reminders = load_reminders()
    for reminder in reminders:
        if reminder['id'] == reminder_id:
            reminder['completed'] = True
            save_reminders(reminders)
            print(f"✅ Marked reminder as complete: {reminder['title']}")
            return True
    print(f"❌ Reminder with ID {reminder_id} not found.")
    return False

def mark_todo_complete(todo_id):
    """Mark a todo item as complete"""
    todos = load_todos()
    for todo in todos:
        if todo['id'] == todo_id:
            todo['completed'] = True
            save_todos(todos)
            print(f"✅ Marked todo as complete: {todo['title']}")
            return True
    print(f"❌ Todo with ID {todo_id} not found.")
    return False

def delete_reminder(reminder_id):
    """Delete a reminder"""
    reminders = load_reminders()
    for i, reminder in enumerate(reminders):
        if reminder['id'] == reminder_id:
            deleted_reminder = reminders.pop(i)
            save_reminders(reminders)
            print(f"✅ Deleted reminder: {deleted_reminder['title']}")
            return True
    print(f"❌ Reminder with ID {reminder_id} not found.")
    return False

def delete_todo(todo_id):
    """Delete a todo item"""
    todos = load_todos()
    for i, todo in enumerate(todos):
        if todo['id'] == todo_id:
            deleted_todo = todos.pop(i)
            save_todos(todos)
            print(f"✅ Deleted todo: {deleted_todo['title']}")
            return True
    print(f"❌ Todo with ID {todo_id} not found.")
    return False

def get_overdue_reminders():
    """Get reminders that are overdue"""
    reminders = load_reminders()
    today = datetime.now().date()
    overdue = []
    
    for reminder in reminders:
        if reminder['due_date'] and not reminder['completed']:
            due_date = datetime.fromisoformat(reminder['due_date']).date()
            if due_date < today:
                overdue.append(reminder)
    
    return overdue

def test_notification():
    """Test the advanced notification system"""
    notification_system.test_notification_system()

# Setup instructions
SETUP_INSTRUCTIONS = '''
=== REMINDERS & TODO ASSISTANT ===

This assistant helps you manage reminders and todo items.
No external setup required!

Features:
✅ Add reminders with due dates and priorities
✅ Add todo items with priorities
✅ Desktop notifications when items are due
✅ Mark items as complete
✅ Delete items
✅ List overdue reminders
✅ Persistent storage (JSON files)

Usage:
- "add reminder" - Add new reminder
- "add todo" - Add new todo item
- "list reminders" - Show all reminders
- "list todos" - Show all todos
- "mark reminder complete" - Mark reminder as done
- "mark todo complete" - Mark todo as done
- "test notification" - Test notification system

Notifications:
🔔 Desktop notifications will appear when reminders/todos are due
🔔 Notifications show title, priority, and description
🔔 Background service runs automatically
'''

if __name__ == "__main__":
    print(SETUP_INSTRUCTIONS)
    # Start notification service
    start_notification_service()
    # Example usage:
    # add_reminder("Pay bills", "12/25/2024", "high", "Electricity and water bills")
    # add_todo("Buy groceries", "medium", "Milk, bread, eggs")
    # list_reminders()
    # list_todos()
    # test_notification() 