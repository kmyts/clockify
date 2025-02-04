from datetime import datetime, timedelta
import json
from termcolor import cprint
from utils.date_utils import get_week_start_date
from utils.project_utils import select_task

def create_batch_entries_command(clockify, openai, default_project_id, default_task_id):
    """Create multiple time entries for different days of the week"""
    # Get project ID first (use default if empty)
    from commands.list_projects import list_projects_command
    list_projects_command(clockify)
    
    project_id = input(f"\nEnter project ID (press Enter for default): ")
    if not project_id:
        project_id = default_project_id
        cprint(f"Using default project ID: {project_id}", "yellow")
    
    # Get task ID (use default if empty)
    task_id = select_task(clockify, project_id, default_task_id)
    
    # Get the start date of the week
    start_date = get_week_start_date()
    
    cprint("\nEnter work items in natural language", "cyan")
    cprint("Examples:", "white")
    cprint("  mon-tue: Feature implementation", "white")
    cprint("  wed: Code review", "white")
    cprint("  thursday-friday: Documentation", "white")
    cprint("\nEnter your work items (Ctrl+D or empty line when done):", "yellow")
    
    lines = []
    while True:
        try:
            line = input().strip()
            if not line:
                break
            lines.append(line)
        except EOFError:
            break
    
    if not lines:
        cprint("\nNo input provided.", "yellow")
        return
        
    try:
        # Parse the schedule first
        parsed_result = openai.parse_work_schedule('\n'.join(lines))
        entries_data = json.loads(parsed_result)
        
        # Convert to our internal format and enhance descriptions in one go
        planned_entries = []
        for day_num in range(5):  # Monday to Friday
            current_date = start_date + timedelta(days=day_num)
            
            # Find description for this day
            description = None
            for entry in entries_data:
                if day_num in entry['days']:
                    description = entry['description']
                    break
            
            if description:
                # Check if entry already exists
                if clockify.has_entry_for_date_project(project_id, current_date):
                    cprint(f"\n{current_date.strftime('%A, %Y-%m-%d')}:", "red")
                    cprint("Entry already exists for this date", "red")
                    continue
                
                # Get AI enhancement for all descriptions at once
                try:
                    enhanced_result = openai.enhance_work_description(description)
                    enhanced_data = json.loads(enhanced_result)
                    enhanced_description = enhanced_data['enhanced_description']
                    
                    planned_entries.append({
                        'date': current_date,
                        'description': enhanced_description,
                        'original': description
                    })
                    
                    cprint(f"\n{current_date.strftime('%A, %Y-%m-%d')}:", "cyan")
                    cprint(f"Original: {description}", "white")
                    cprint(f"Enhanced: {enhanced_description}", "green")
                except json.JSONDecodeError:
                    cprint(f"\nError processing AI enhancement for {current_date.strftime('%A')}", "red")
                    cprint(f"Will use original: {description}", "yellow")
                    planned_entries.append({
                        'date': current_date,
                        'description': description,
                        'original': description
                    })
        
        if not planned_entries:
            cprint("\nNo entries to create (all dates may already have entries).", "yellow")
            return
        
        # Confirm creation
        confirm = input("\nCreate these entries? (y/n): ").lower()
        if confirm != 'y':
            cprint("\nOperation cancelled.", "yellow")
            return
        
        # Create entries
        created_count = 0
        for entry in planned_entries:
            result = clockify.create_workday_entry(
                project_id,
                entry['description'],
                entry['date'],
                task_id
            )
            if not result.get('error'):
                created_count += 1
                start_time = datetime.fromisoformat(result['timeInterval']['start'].replace('Z', '+00:00'))
                end_time = datetime.fromisoformat(result['timeInterval']['end'].replace('Z', '+00:00'))
                cprint(f"\n✓ Created entry for {entry['date'].strftime('%A, %Y-%m-%d')}", "green")
                cprint(f"  Time: {start_time.strftime('%I:%M %p')} - {end_time.strftime('%I:%M %p')}", "white")
        
        cprint(f"\nSuccessfully created {created_count} entries!", "green")
        
    except Exception as e:
        cprint(f"\nError processing input: {str(e)}", "red")
        return 