from datetime import datetime, timedelta
import json
import os
from commands.list_projects import list_projects_command
from commands.create_entry import create_entry_command
from commands.create_weekly_entries import create_weekly_entries_command
from commands.view_entries import view_weekly_entries_command
from commands.delete_entries import delete_weekly_entries_command
from commands.create_batch_entries import create_batch_entries_command

class TimeTrackingCommands:
    def __init__(self, clockify, openai):
        self.clockify = clockify
        self.openai = openai
        self.default_project_id = os.getenv('CLOCKIFY_DEFAULT_PROJECT_ID')
        self.default_task_id = os.getenv('CLOCKIFY_DEFAULT_TASK_ID')

    def list_projects(self):
        return list_projects_command(self.clockify)

    def create_time_entry_with_ai(self):
        return create_entry_command(self.clockify, self.openai, self.default_project_id, self.default_task_id)

    def create_weekly_entries(self):
        return create_weekly_entries_command(self.clockify, self.openai, self.default_project_id, self.default_task_id)

    def view_weekly_entries(self):
        return view_weekly_entries_command(self.clockify)

    def delete_weekly_entries(self):
        return delete_weekly_entries_command(self.clockify)

    def create_batch_entries(self):
        return create_batch_entries_command(self.clockify, self.openai, self.default_project_id, self.default_task_id) 