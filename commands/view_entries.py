from datetime import datetime, timedelta
from termcolor import cprint
from utils.date_utils import get_week_start_date

def view_weekly_entries_command(clockify):
    """View time entries for a specific week"""
    # Get the start date of the week using the utility function
    start_date = get_week_start_date()
    
    end_date = start_date + timedelta(days=6)
    entries = clockify.get_time_entries(start_date, end_date)
    
    cprint(f"\nTime entries for week of {start_date.strftime('%Y-%m-%d')}:", "cyan")
    cprint("=" * 50, "white")
    
    for entry in entries:
        entry_date = datetime.fromisoformat(entry['timeInterval']['start'].replace('Z', '+00:00'))
        start_time = datetime.fromisoformat(entry['timeInterval']['start'].replace('Z', '+00:00'))
        end_time = datetime.fromisoformat(entry['timeInterval']['end'].replace('Z', '+00:00'))
        cprint(f"\n{entry_date.strftime('%A, %Y-%m-%d')}:", "cyan")
        cprint(f"Description: {entry['description']}", "white")
        cprint(f"Time: {start_time.strftime('%I:%M %p')} - {end_time.strftime('%I:%M %p')}", "white")
        if 'projectId' in entry:
            project = clockify.get_project_name(entry['projectId'])
            cprint(f"Project: {project}", "white")
        if 'taskId' in entry:
            task = clockify.get_project_tasks(entry['projectId'])
            task_name = next((t['name'] for t in task if t['id'] == entry['taskId']), 'Unknown Task')
            cprint(f"Task: {task_name}", "white")
        cprint("-" * 30, "white") 