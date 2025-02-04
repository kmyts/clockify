from termcolor import cprint

def list_projects_command(clockify):
    """List all available projects"""
    cprint("\nAvailable Projects:", "cyan")
    projects = clockify.get_projects()
    for project in projects:
        cprint(f"- {project['name']} (ID: {project['id']})", "white")
    return projects 