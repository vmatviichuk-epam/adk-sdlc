# Export the orchestrator agent as the main agent
from .agent import orchestrator_agent

# Also export it as root_agent for ADK CLI compatibility
root_agent = orchestrator_agent

# This makes the agents automatically loaded when using 'adk run .'
__all__ = ['orchestrator_agent', 'root_agent']