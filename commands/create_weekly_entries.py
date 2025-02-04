from datetime import datetime, timedelta
import json
from termcolor import cprint
from utils.date_utils import get_week_start_date
from utils.project_utils import select_task

def create_weekly_entries_command(clockify, openai, default_project_id, default_task_id):
    """Create time entries for a whole week"""
    from commands.list_projects import list_projects_command
    list_projects_command(clockify)
    
    project_id = input(f"\nEnter project ID for the week (press Enter for default): ")
    if not project_id:
        project_id = default_project_id
        cprint(f"Using default project ID: {project_id}", "yellow")
    
    task_id = select_task(clockify, project_id, default_task_id)
    start_date = get_week_start_date()
    work_description = input("\nEnter work description (will be enhanced daily): ")
    
    cprint("\nCreating entries for the week...", "cyan")
    for i in range(5):  # Monday to Friday
        current_date = start_date + timedelta(days=i)
        
        # Check if entry already exists
        if clockify.has_entry_for_date_project(project_id, current_date):
            cprint(f"\nSkipped: Entry already exists for {current_date.strftime('%A, %Y-%m-%d')}", "yellow")
            continue
        
        # Enhance description with day context
        day_prompt = f"{work_description} (for {current_date.strftime('%A')})"
        cprint(f"\nProcessing {current_date.strftime('%A')}...", "cyan")
        
        try:
            # Get AI enhancement
            enhanced_result = openai.enhance_work_description(day_prompt)
            enhanced_data = json.loads(enhanced_result)
            daily_description = enhanced_data['enhanced_description']
            
            # Create entry
            result = clockify.create_workday_entry(project_id, daily_description, current_date, task_id)
            if not result.get('error'):
                start_time = datetime.fromisoformat(result['timeInterval']['start'].replace('Z', '+00:00'))
                end_time = datetime.fromisoformat(result['timeInterval']['end'].replace('Z', '+00:00'))
                cprint(f"✓ Created entry for {current_date.strftime('%A, %Y-%m-%d')}", "green")
                cprint(f"  Description: {daily_description}", "white")
                cprint(f"  Time: {start_time.strftime('%I:%M %p')} - {end_time.strftime('%I:%M %p')}", "white")
            
        except json.JSONDecodeError:
            # Fallback to original description if AI enhancement fails
            result = clockify.create_workday_entry(project_id, day_prompt, current_date, task_id)
            if not result.get('error'):
                cprint(f"✓ Created entry for {current_date.strftime('%A, %Y-%m-%d')} (without enhancement)", "green")
                cprint(f"  Description: {day_prompt}", "white")
    
    cprint("\nWeekly time entries completed!", "green") 