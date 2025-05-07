import os
from google.adk.agents import Agent
from dotenv import load_dotenv

# Import tools
from .tools.orchestrator_tool import (
    requirements_agent,
    implementation_agent,
    testing_agent,
    pr_agent
)

# Import prompts
from .prompt import return_instructions_orchestrator

load_dotenv()

# Create the orchestrator agent
orchestrator_agent = Agent(
    model=os.environ.get("VERTEX_MODEL", "gemini-2.0-flash"),
    name="orchestrator_agent",
    description="Agent that coordinates the workflow between all specialized agents",
    instruction=return_instructions_orchestrator(),
    tools=[
        requirements_agent,
        implementation_agent,
        testing_agent,
        pr_agent
    ]
)

# Expose the root agent
root_agent = orchestrator_agent