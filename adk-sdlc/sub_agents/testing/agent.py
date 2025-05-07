import os
from google.adk.agents import Agent
from dotenv import load_dotenv

# Import tools
from .tools.testing_tool import generate_tests

# Import prompts
from .prompt import return_instructions_testing_agent

load_dotenv()

# Create the testing agent
testing_agent = Agent(
    model=os.environ.get("VERTEX_MODEL", "gemini-1.5-pro"),
    name="testing_agent",
    description="Agent that generates tests for code implementations",
    instruction=return_instructions_testing_agent(),
    tools=[
        generate_tests,
    ]
)