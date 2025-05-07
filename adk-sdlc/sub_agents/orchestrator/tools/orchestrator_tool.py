from typing import Dict, Any
from google.adk.tools import FunctionTool
from ...requirements.agent import requirements_agent as req_agent
from ...implementation.agent import implementation_agent as impl_agent
from ...testing.agent import testing_agent as test_agent
from ...pr.agent import pr_agent as pr_agent_instance

def requirements_agent(task: str) -> Dict[str, Any]:
    """
    Invokes the requirements agent to process JIRA tickets and requirements.
    
    Args:
        task: Description of the task or JIRA ticket ID
        
    Returns:
        A dictionary containing the requirements analysis
    """
    try:
        # If task is "list_my_tickets", call the list_open_tickets tool
        if task == "list_my_tickets":
            response = req_agent.run({"command": "list_my_tickets"})
            return {
                "success": True,
                "tickets": response,
                "message": "Mock user stories retrieved successfully"
            }
        # If task starts with "fetch_jira_ticket", extract the ticket ID and call get_ticket_details
        elif task.startswith("fetch_jira_ticket"):
            ticket_id = task.split("ticket_id=")[1].strip()
            response = req_agent.run({"command": "fetch_jira_ticket", "ticket_id": ticket_id})
            return {
                "success": True,
                "ticket": response,
                "message": f"Mock user story {ticket_id} details retrieved successfully"
            }
        else:
            # For any other task, call the requirements agent with the task
            response = req_agent.run(task)
            return {
                "success": True,
                "requirements": response,
                "message": "Requirements analysis completed successfully"
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to analyze requirements"
        }

def implementation_agent(requirements: Dict[str, Any]) -> Dict[str, Any]:
    """
    Invokes the implementation agent to generate code based on requirements.
    
    Args:
        requirements: Dictionary containing the requirements analysis
        
    Returns:
        A dictionary containing the generated code
    """
    try:
        # Call the implementation agent with the requirements
        response = impl_agent.run(requirements)
        return {
            "success": True,
            "code": response,
            "message": "Code implementation completed successfully"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to generate implementation"
        }

def testing_agent(implementation: Dict[str, Any]) -> Dict[str, Any]:
    """
    Invokes the testing agent to generate tests for the implementation.
    
    Args:
        implementation: Dictionary containing the code implementation
        
    Returns:
        A dictionary containing the generated tests
    """
    try:
        # Call the testing agent with the implementation
        response = test_agent.run(implementation)
        return {
            "success": True,
            "tests": response,
            "message": "Test generation completed successfully"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to generate tests"
        }

def pr_agent(implementation: Dict[str, Any], tests: Dict[str, Any]) -> Dict[str, Any]:
    """
    Invokes the PR agent to create a pull request with the implementation and tests.
    
    Args:
        implementation: Dictionary containing the code implementation
        tests: Dictionary containing the generated tests
        
    Returns:
        A dictionary containing the PR details
    """
    try:
        # Call the PR agent with the implementation and tests
        response = pr_agent_instance.run({"implementation": implementation, "tests": tests})
        return {
            "success": True,
            "pr": response,
            "message": "Pull request created successfully"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to create pull request"
        }

# Create FunctionTools
requirements_agent = FunctionTool(requirements_agent)
implementation_agent = FunctionTool(implementation_agent)
testing_agent = FunctionTool(testing_agent)
pr_agent = FunctionTool(pr_agent) 