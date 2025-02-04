from datetime import datetime, timedelta
from termcolor import cprint
from utils.date_utils import get_week_start_date

def delete_weekly_entries_command(clockify):
    """Delete time entries for a specific week"""
    start_date = get_week_start_date()
    end_date = start_date + timedelta(days=6)
    
    entries = clockify.get_time_entries(start_date, end_date)
    
    if not entries:
        cprint(f"\nNo entries found for week of {start_date.strftime('%Y-%m-%d')}", "yellow")
        return
    
    cprint(f"\nEntries to be deleted for week of {start_date.strftime('%Y-%m-%d')}:", "cyan")
    cprint("=" * 50, "white")
    
    for entry in entries:
        entry_date = datetime.fromisoformat(entry['timeInterval']['start'].replace('Z', '+00:00'))
        cprint(f"\n{entry_date.strftime('%A, %Y-%m-%d')}:", "cyan")
        cprint(f"Description: {entry['description']}", "white")
        if 'projectId' in entry:
            project = clockify.get_project_name(entry['projectId'])
            cprint(f"Project: {project}", "white")
        if 'taskId' in entry:
            task = clockify.get_project_tasks(entry['projectId'])
            task_name = next((t['name'] for t in task if t['id'] == entry['taskId']), 'Unknown Task')
            cprint(f"Task: {task_name}", "white")
        cprint("-" * 30, "white")
    
    # Confirm deletion
    confirm = input("\nAre you sure you want to delete these entries? (y/n): ").lower()
    if confirm != 'y':
        cprint("\nDeletion cancelled.", "yellow")
        return
    
    # Delete entries
    deleted_count = clockify.delete_time_entries(start_date, end_date)
    cprint(f"\nSuccessfully deleted {deleted_count} entries!", "green") 