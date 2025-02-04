import os
from datetime import datetime, timedelta
import requests
import random

class ClockifyAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://api.clockify.me/api/v1'
        self.headers = {
            'X-Api-Key': self.api_key,
            'Content-Type': 'application/json'
        }
        self.workspace_id = self._get_workspace_id()

    def _get_workspace_id(self):
        """Get the user's workspace ID"""
        response = requests.get(
            f'{self.base_url}/workspaces',
            headers=self.headers
        )
        return response.json()[0]['id']

    def get_projects(self):
        """Fetch all projects in the workspace"""
        response = requests.get(
            f'{self.base_url}/workspaces/{self.workspace_id}/projects',
            headers=self.headers
        )
        return response.json()

    def create_time_entry(self, project_id, description, start_time=None, end_time=None):
        """Create a new time entry"""
        if start_time is None:
            start_time = datetime.utcnow().isoformat() + 'Z'
        
        if end_time is None:
            end_time = datetime.utcnow().isoformat() + 'Z'

        data = {
            "start": start_time,
            "end": end_time,
            "projectId": project_id,
            "description": description
        }

        response = requests.post(
            f'{self.base_url}/workspaces/{self.workspace_id}/time-entries',
            headers=self.headers,
            json=data
        )
        return response.json()

    def has_entry_for_date_project(self, project_id, date):
        """Check if there's already an entry for the given project and date"""
        start_date = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = date.replace(hour=23, minute=59, second=59, microsecond=999999)
        
        entries = self.get_time_entries(start_date, end_date)
        
        for entry in entries:
            if entry.get('projectId') == project_id:
                return True
        return False

    def create_workday_entry(self, project_id, description, date=None, task_id=None):
        """Create a time entry for a standard 8-hour workday"""
        if date is None:
            date = datetime.now()
        
        # Check for existing entry
        if self.has_entry_for_date_project(project_id, date):
            return {"error": "Entry already exists"}
        
        # Randomize start time between 7:00 AM and 9:00 AM
        random_hours = random.randint(0, 2)  # 0-2 hours after 7 AM
        # Round minutes to nearest quarter (0, 15, 30, 45)
        random_minutes = random.randint(0, 3) * 15
        
        # Set start time to the randomized time
        start_time = date.replace(
            hour=7 + random_hours,
            minute=random_minutes,
            second=0,
            microsecond=0
        )
        # Set end time to 8 hours after start time
        end_time = start_time + timedelta(hours=8)

        data = {
            "start": start_time.isoformat() + 'Z',
            "end": end_time.isoformat() + 'Z',
            "projectId": project_id,
            "description": description
        }
        
        if task_id:
            data["taskId"] = task_id

        response = requests.post(
            f'{self.base_url}/workspaces/{self.workspace_id}/time-entries',
            headers=self.headers,
            json=data
        )
        return response.json()

    def get_time_entries(self, start_date, end_date):
        """Get time entries for a specific date range"""
        start_str = start_date.replace(hour=0, minute=0, second=0).isoformat() + 'Z'
        end_str = end_date.replace(hour=23, minute=59, second=59).isoformat() + 'Z'
        
        params = {
            'start': start_str,
            'end': end_str,
        }
        
        response = requests.get(
            f'{self.base_url}/workspaces/{self.workspace_id}/user/{self._get_user_id()}/time-entries',
            headers=self.headers,
            params=params
        )
        return response.json()

    def _get_user_id(self):
        """Get the current user's ID"""
        response = requests.get(
            f'{self.base_url}/user',
            headers=self.headers
        )
        return response.json()['id']

    def get_project_name(self, project_id):
        """Get project name by ID"""
        response = requests.get(
            f'{self.base_url}/workspaces/{self.workspace_id}/projects/{project_id}',
            headers=self.headers
        )
        return response.json()['name']

    def get_project_tasks(self, project_id):
        """Fetch all tasks for a project"""
        response = requests.get(
            f'{self.base_url}/workspaces/{self.workspace_id}/projects/{project_id}/tasks',
            headers=self.headers
        )
        return response.json()

    def delete_time_entry(self, entry_id):
        """Delete a time entry by ID"""
        response = requests.delete(
            f'{self.base_url}/workspaces/{self.workspace_id}/time-entries/{entry_id}',
            headers=self.headers
        )
        return response.status_code == 204

    def delete_time_entries(self, start_date, end_date):
        """Delete all time entries in a date range"""
        entries = self.get_time_entries(start_date, end_date)
        deleted_count = 0
        
        for entry in entries:
            if self.delete_time_entry(entry['id']):
                deleted_count += 1
                
        return deleted_count 