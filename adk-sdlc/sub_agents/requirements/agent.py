import os
from google.adk.agents import Agent
from dotenv import load_dotenv

# Import tools
from .tools.jira_tool import get_ticket_details_tool, list_open_tickets_tool

# Import prompts
from .prompt import return_instructions_requirements_agent

load_dotenv()

# Create the requirements agent
requirements_agent = Agent(
    model=os.environ.get("VERTEX_MODEL", "gemini-1.5-pro"),
    name="requirements_agent",
    description="Agent that fetches ticket information and extracts implementation requirements",
    instruction=return_instructions_requirements_agent(),
    tools=[
        list_open_tickets_tool,
        get_ticket_details_tool
    ]
)