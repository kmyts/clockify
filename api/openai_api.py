from openai import OpenAI

class OpenAIAPI:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def process_work_schedule(self, schedule_text):
        prompt = f"""
        You are a software development time tracking assistant. Parse and enhance the following work schedule.
        For each entry, parse the days and enhance the work description to be more technical and professional.

        Input:
        {schedule_text}

        Rules for enhanced descriptions:
        - Keep it technical and specific to software development
        - Remove any references to days or dates
        - Keep it under 100 characters
        - Focus on the actual development task or activity
        - Use proper technical terminology
        - Maintain the core meaning of the original description

        Return the result as a JSON array of objects, each with:
        - days: array of day numbers (0=Monday, 1=Tuesday, etc)
        - original: the exact work description from input
        - enhanced: the improved technical description

        Example input:
        mon-tue: working on login page
        wed: code review
        thu-fri: writing docs

        Example output:
        [
            {{
                "days": [0, 1],
                "original": "working on login page",
                "enhanced": "Implementing user authentication and login interface"
            }},
            {{
                "days": [2],
                "original": "code review",
                "enhanced": "Performing code review and quality assessment"
            }},
            {{
                "days": [3, 4],
                "original": "writing docs",
                "enhanced": "Developing technical documentation and API references"
            }}
        ]
        """

        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.choices[0].message.content

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
