import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
import json
import subprocess
import webbrowser

load_dotenv()

# Calendar events storage (simple JSON file for now)
CALENDAR_FILE = "calendar_events.json"

def load_events():
    """Load events from JSON file"""
    if os.path.exists(CALENDAR_FILE):
        with open(CALENDAR_FILE, 'r') as f:
            return json.load(f)
    return []

def save_events(events):
    """Save events to JSON file"""
    with open(CALENDAR_FILE, 'w') as f:
        json.dump(events, f, indent=2)

def add_event(title, date, time, description=""):
    """Add a new calendar event"""
    events = load_events()
    
    # Parse date and time
    try:
        if isinstance(date, str):
            # Handle different date formats
            if '/' in date:
                date_obj = datetime.strptime(date, '%m/%d/%Y')
            elif '-' in date:
                date_obj = datetime.strptime(date, '%Y-%m-%d')
            else:
                date_obj = datetime.now()
        else:
            date_obj = date
            
        # Combine date and time
        if time:
            time_obj = datetime.strptime(time, '%H:%M').time()
            event_datetime = datetime.combine(date_obj.date(), time_obj)
        else:
            event_datetime = date_obj
            
    except ValueError:
        print("❌ Invalid date/time format. Use MM/DD/YYYY and HH:MM")
        return False
    
    new_event = {
        'id': len(events) + 1,
        'title': title,
        'datetime': event_datetime.isoformat(),
        'description': description,
        'created': datetime.now().isoformat()
    }
    
    events.append(new_event)
    save_events(events)
    print(f"✅ Event added: {title} on {event_datetime.strftime('%B %d, %Y at %I:%M %p')}")
    return True

def list_events(days_ahead=7):
    """List upcoming events"""
    events = load_events()
    if not events:
        print("📅 No upcoming events found.")
        return []
    
    # Sort events by datetime
    events.sort(key=lambda x: x['datetime'])
    
    upcoming_events = []
    cutoff_date = datetime.now() + timedelta(days=days_ahead)
    
    for event in events:
        event_date = datetime.fromisoformat(event['datetime'])
        if event_date >= datetime.now():
            upcoming_events.append(event)
    
    if not upcoming_events:
        print("📅 No upcoming events in the next {} days.".format(days_ahead))
        return []
    
    print(f"\n📅 Upcoming Events (next {days_ahead} days):")
    print("=" * 50)
    
    for event in upcoming_events:
        event_date = datetime.fromisoformat(event['datetime'])
        print(f"📌 {event['title']}")
        print(f"   📅 {event_date.strftime('%B %d, %Y at %I:%M %p')}")
        if event['description']:
            print(f"   📝 {event['description']}")
        print("-" * 30)
    
    return upcoming_events

def delete_event(event_id):
    """Delete an event by ID"""
    events = load_events()
    for i, event in enumerate(events):
        if event['id'] == event_id:
            deleted_event = events.pop(i)
            save_events(events)
            print(f"✅ Deleted event: {deleted_event['title']}")
            return True
    print(f"❌ Event with ID {event_id} not found.")
    return False

def get_today_events():
    """Get events for today"""
    events = load_events()
    today = datetime.now().date()
    today_events = []
    
    for event in events:
        event_date = datetime.fromisoformat(event['datetime']).date()
        if event_date == today:
            today_events.append(event)
    
    return today_events

def open_system_calendar():
    """Open the system calendar application"""
    try:
        # Try to open Windows Calendar
        subprocess.run(['start', 'ms-calendar:'], shell=True)
        print("✅ Opening Windows Calendar...")
        return True
    except Exception as e:
        print(f"❌ Failed to open system calendar: {e}")
        return False

def open_google_calendar():
    """Open Google Calendar in browser"""
    try:
        webbrowser.open('https://calendar.google.com')
        print("✅ Opening Google Calendar...")
        return True
    except Exception as e:
        print(f"❌ Failed to open Google Calendar: {e}")
        return False

def create_calendar_event_url(title, date, time, description=""):
    """Create a Google Calendar URL for adding events"""
    try:
        # Format date and time for Google Calendar URL
        if isinstance(date, str):
            if '/' in date:
                date_obj = datetime.strptime(date, '%m/%d/%Y')
            elif '-' in date:
                date_obj = datetime.strptime(date, '%Y-%m-%d')
            else:
                date_obj = datetime.now()
        else:
            date_obj = date
            
        # Format for Google Calendar URL
        date_str = date_obj.strftime('%Y%m%d')
        
        # Add time if provided
        if time:
            time_obj = datetime.strptime(time, '%H:%M')
            start_time = time_obj.strftime('%H%M')
            # End time (1 hour later by default)
            end_time = (time_obj + timedelta(hours=1)).strftime('%H%M')
            time_param = f"&dates={date_str}T{start_time}00/{date_str}T{end_time}00"
        else:
            time_param = f"&dates={date_str}/{date_str}"
        
        # Create Google Calendar URL
        event_url = f"https://calendar.google.com/calendar/render?action=TEMPLATE&text={title.replace(' ', '+')}{time_param}&details={description.replace(' ', '+')}"
        
        return event_url
    except Exception as e:
        print(f"❌ Error creating calendar URL: {e}")
        return None

def open_calendar_with_event(title, date, time, description=""):
    """Open calendar with pre-filled event details"""
    event_url = create_calendar_event_url(title, date, time, description)
    if event_url:
        try:
            webbrowser.open(event_url)
            print(f"✅ Opening Google Calendar with event: {title}")
            return True
        except Exception as e:
            print(f"❌ Failed to open calendar with event: {e}")
            return False
    return False

# Setup instructions
SETUP_INSTRUCTIONS = '''
=== CALENDAR ASSISTANT SETUP ===

This calendar assistant uses a local JSON file to store events.
No external setup required!

Features:
✅ Add events with title, date, time, and description
✅ List upcoming events
✅ Delete events
✅ Get today's events

Usage:
- "add calendar event" - Add new event
- "list calendar events" - Show upcoming events
- "today's events" - Show today's events
'''

if __name__ == "__main__":
    print(SETUP_INSTRUCTIONS)
    # Example usage:
    # add_event("Team Meeting", "12/25/2024", "14:30", "Weekly team sync")
    # list_events() 