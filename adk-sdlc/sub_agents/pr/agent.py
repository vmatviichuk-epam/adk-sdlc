import os
from google.adk.agents import Agent
from dotenv import load_dotenv

# Import tools
from .tools.github_tool import start_github_mcp_server_tool, setup_repository_tool, create_github_pr_tool
from .prompt import return_instructions_pr_agent

load_dotenv()

# Create the PR agent
pr_agent = Agent(
    model=os.environ.get("VERTEX_MODEL", "gemini-1.5-pro"),
    name="pr_agent",
    description="Agent that interacts with GitHub repositories and creates pull requests",
    instruction=return_instructions_pr_agent(),
    tools=[
        start_github_mcp_server_tool,
        setup_repository_tool,
        create_github_pr_tool
    ]
)