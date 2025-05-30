import os
from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from dotenv import load_dotenv

# Import sub-agents
from .sub_agents.requirements.agent import requirements_agent
from .sub_agents.implementation.agent import implementation_agent
from .sub_agents.testing.agent import testing_agent
from .sub_agents.pr.agent import pr_agent

# Import prompts
from .prompt import return_instructions_orchestrator

load_dotenv()

# Create the main orchestrator agent
orchestrator_agent = Agent(
    model=os.environ.get("VERTEX_MODEL", "gemini-1.5-pro"),
    name="adk_sdlc_orchestrator",
    instruction=return_instructions_orchestrator(),
    tools=[
        # Sub-agents wrapped with AgentTool
        AgentTool(agent=requirements_agent),
        AgentTool(agent=implementation_agent),
        AgentTool(agent=testing_agent),
        AgentTool(agent=pr_agent),
    ]
)

# Also expose as root_agent for ADK CLI compatibility
root_agent = orchestrator_agent