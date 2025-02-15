import os
from dotenv import load_dotenv
from api.clockify_api import ClockifyAPI
from api.openai_api import OpenAIAPI
from commands.time_tracking_commands import TimeTrackingCommands
from termcolor import cprint
# Load environment variables
load_dotenv()

def main():
    # Initialize APIs
    clockify = ClockifyAPI(os.getenv('CLOCKIFY_API_KEY'))
    openai = OpenAIAPI(os.getenv('OPENAI_API_KEY'))
    
    # Initialize commands
    commands = TimeTrackingCommands(clockify, openai)
    
    while True:
        print("\n=== Time Tracking Menu ===")
        print("1. List Projects")
        print("2. Create Single Time Entry")
        cprint("3. Create Batch Time Entries", "yellow")
        print("4. View Weekly Time Entries")
        print("5. Delete Weekly Time Entries")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-7): ")
        
        if choice == "1":
            commands.list_projects()
        elif choice == "2":
            commands.create_time_entry_with_ai()
        elif choice == "3":
            commands.create_batch_entries()
        elif choice == "4":
            commands.view_weekly_entries()
        elif choice == "5":
            commands.delete_weekly_entries()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main() 