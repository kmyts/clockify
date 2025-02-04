from termcolor import cprint

def select_task(clockify, project_id, default_task_id=None):
    """Helper function to select a task from a project"""
    tasks = clockify.get_project_tasks(project_id)
    
    if not tasks:
        return default_task_id
        
    cprint("\nAvailable Tasks:", "cyan")
    for i, task in enumerate(tasks, 1):
        is_default = task['id'] == default_task_id
        task_display = f"{i}. {task['name']} (ID: {task['id']})"
        if is_default:
            task_display += " (default)"
        cprint(task_display, "white")
    
    choice = input("\nEnter task number (press Enter to use default): ")
    
    if not choice:
        if default_task_id:
            cprint(f"Using default task ID: {default_task_id}", "yellow")
            return default_task_id
        return None
        
    try:
        task_index = int(choice) - 1
        if 0 <= task_index < len(tasks):
            return tasks[task_index]['id']
    except ValueError:
        pass
    
    cprint("Invalid selection. Using default task.", "yellow")
    return default_task_id 