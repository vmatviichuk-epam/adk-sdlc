import os
from google.adk.agents import Agent
from dotenv import load_dotenv

# Import tools
from .tools.implementation_tool import generate_implementation

# Import prompts
from .prompt import return_instructions_implementation_agent

load_dotenv()

# Create the implementation agent
implementation_agent = Agent(
    model=os.environ.get("VERTEX_MODEL", "gemini-1.5-pro"),
    name="implementation_agent",
    description="Agent that generates code implementations based on requirements",
    instruction=return_instructions_implementation_agent(),
    tools=[
        generate_implementation,
    ]
)