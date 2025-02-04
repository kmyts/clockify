from openai import OpenAI

class OpenAIAPI:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def enhance_work_description(self, description):
        prompt = f"""
        As a software development time tracking assistant, create a clear and professional description 
        of the development work. Use specific technical terms and focus on the actual development task.

        Original description: {description}
        
        Format your response as a JSON-like structure:
        {{
            "enhanced_description": "the improved description"
        }}
        
        Rules:
        - Keep it technical and specific to software development
        - Remove any references to days or dates
        - Keep it under 100 characters
        - Focus on the actual development task or activity
        - Use proper technical terminology
        - Maintain the core meaning of the original description
        
        Example:
        Input: "working on the login page"
        Output: {{"enhanced_description": "Implementing user authentication and login interface"}}
        
        Input: "fixing bugs in api"
        Output: {{"enhanced_description": "Resolving API endpoint issues and implementing bug fixes"}}
        """

        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.choices[0].message.content

    def parse_work_schedule(self, schedule_text):
        prompt = f"""
        You are a software development time tracking assistant. Parse the following work schedule into a structured format.
        Each entry should specify which days of the week (0-4 for Monday-Friday) and preserve the original work description.
        Do not modify or enhance the descriptions, just parse the schedule.
        
        Input:
        {schedule_text}
        
        Return the result as a JSON array of objects, each with:
        - days: array of day numbers (0=Monday, 1=Tuesday, etc)
        - description: the exact work description from input
        
        Example input:
        mon-tue: Implementing user authentication
        wed: Code review and fixes
        thu-fri: API documentation
        
        Example output:
        [
            {{"days": [0, 1], "description": "Implementing user authentication"}},
            {{"days": [2], "description": "Code review and fixes"}},
            {{"days": [3, 4], "description": "API documentation"}}
        ]
        """

        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.choices[0].message.content 