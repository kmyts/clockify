from datetime import datetime
import json
from termcolor import cprint
from utils.project_utils import select_task

def create_entry_command(clockify, openai, default_project_id, default_task_id):
    """Create a time entry with AI-enhanced description"""
    work_description = input("\nEnter your work description: ")
    
    cprint("\nEnhancing your description with AI...", "yellow")
    enhanced_result = openai.enhance_work_description(work_description)
    
    try:
        enhanced_data = json.loads(enhanced_result)
        enhanced_description = enhanced_data['enhanced_description']
        
        cprint("\nEnhanced Description:", "cyan")
        cprint(enhanced_description, "white")
        
        use_enhanced = input("\nUse enhanced description? (y/n): ").lower() == 'y'
        final_description = enhanced_description if use_enhanced else work_description
        
        project_id = input(f"\nEnter project ID (press Enter for default): ")
        if not project_id:
            project_id = default_project_id
            cprint(f"Using default project ID: {project_id}", "yellow")
        
        task_id = select_task(clockify, project_id, default_task_id)
        
        custom_date = input("\nEnter date (YYYY-MM-DD) or press Enter for today: ")
        if custom_date:
            date = datetime.strptime(custom_date, "%Y-%m-%d")
        else:
            date = datetime.now()
        
        result = clockify.create_workday_entry(project_id, final_description, date, task_id)
        
        if result.get('error'):
            cprint(f"\nSkipped: Entry already exists for {date.strftime('%Y-%m-%d')}", "red")
        else:
            start_time = datetime.fromisoformat(result['timeInterval']['start'].replace('Z', '+00:00'))
            end_time = datetime.fromisoformat(result['timeInterval']['end'].replace('Z', '+00:00'))
            cprint("\nTime entry created successfully!", "green")
            cprint(f"Description: {final_description}", "white")
            cprint(f"Duration: 8 hours ({start_time.strftime('%I:%M %p')} - {end_time.strftime('%I:%M %p')})", "white")
            cprint(f"Date: {date.strftime('%Y-%m-%d')}", "white")
        
    except json.JSONDecodeError:
        cprint("\nError processing AI response. Using original description.", "red")
        project_id = input("\nEnter project ID: ")
        result = clockify.create_workday_entry(project_id, work_description)
        if result.get('error'):
            cprint(f"\nSkipped: Entry already exists for today", "red")
        else:
            cprint("Time entry created successfully!", "green") 