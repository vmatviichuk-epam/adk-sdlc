import os
from typing import Dict, Any, List, Optional
from google.adk.tools import FunctionTool

# Mock data for JIRA operations
MOCK_TICKETS = [
    {
        "key": "TEST-1",
        "summary": "Implement a string reverse function in Python",
        "status": "Open",
        "description": """
As a developer, I want to have a utility function that will reverse a string in Python.

Requirements:
- Create a function that takes a string input and returns the reversed string
- Handle empty strings and single-character strings properly
- Ensure Unicode characters are handled correctly
- Implement the function efficiently (O(n) time complexity)
- Write comprehensive unit tests for the function

Acceptance Criteria:
1. Function correctly reverses any input string
2. Edge cases (empty string, single character) are handled properly
3. Unicode characters are preserved correctly
4. Performance is optimal (O(n) time complexity)
5. Unit tests cover all required functionality
""",
        "type": "Story",
        "priority": "High",
        "assignee": "John Doe",
        "reporter": "Jane Smith",
        "created": "2024-05-07T10:00:00.000Z",
        "updated": "2024-05-07T10:30:00.000Z"
    },
    {
        "key": "TEST-2",
        "summary": "Implement a Python function to display current time + 1 hour",
        "status": "Open",
        "description": """
As a developer, I want to have a utility function that will display the current time plus one hour.

Requirements:
- Create a function that returns the current time plus one hour
- Use Python's datetime module for time handling
- Handle timezone considerations
- Format the output in a readable way
- Write comprehensive unit tests for the function

Acceptance Criteria:
1. Function returns current time + 1 hour correctly
2. Timezone handling is implemented properly
3. Output format is clear and readable
4. Edge cases (day/month/year boundaries) are handled correctly
5. Unit tests cover all required functionality
""",
        "type": "Story",
        "priority": "Medium",
        "assignee": "John Doe",
        "reporter": "Jane Smith",
        "created": "2024-05-07T11:00:00.000Z",
        "updated": "2024-05-07T11:15:00.000Z"
    },
    {
        "key": "TEST-3",
        "summary": "Implement a Java function to multiply two numbers",
        "status": "Open",
        "description": """
As a developer, I want to have a utility function in Java that will multiply two numbers.

Requirements:
- Create a function that takes two numbers as input and returns their product
- Handle different numeric types (int, double, etc.)
- Implement proper error handling
- Write comprehensive unit tests for the function
- Document the function with JavaDoc

Acceptance Criteria:
1. Function correctly multiplies two numbers
2. Different numeric types are handled properly
3. Error cases (null inputs, invalid numbers) are handled gracefully
4. JavaDoc documentation is complete and clear
5. Unit tests cover all required functionality
""",
        "type": "Story",
        "priority": "Medium",
        "assignee": "John Doe",
        "reporter": "Jane Smith",
        "created": "2024-05-07T12:00:00.000Z",
        "updated": "2024-05-07T12:10:00.000Z"
    }
]

def start_jira_mcp_server() -> Dict[str, Any]:
    """Dummy function to simulate starting JIRA MCP server"""
    return {
        "status": "success",
        "message": "JIRA MCP server started successfully",
        "pid": 12346
    }

def get_ticket_details(ticket_id: str) -> Dict[str, Any]:
    """Dummy function to get JIRA ticket details"""
    for ticket in MOCK_TICKETS:
        if ticket["key"] == ticket_id:
            # Extract requirements and acceptance criteria
            description = ticket["description"]
            requirements = []
            acceptance_criteria = []
            
            for line in description.split("\n"):
                if line.strip().startswith("- "):
                    requirements.append(line.strip()[2:])
                elif line.strip().startswith(str(len(acceptance_criteria) + 1) + ". "):
                    acceptance_criteria.append(line.strip()[3:])
            
            formatted_details = f"""# {ticket["key"]}: {ticket["summary"]}

**Status:** {ticket["status"]}
**Type:** {ticket["type"]}
**Priority:** {ticket["priority"]}
**Assignee:** {ticket["assignee"]}
**Reporter:** {ticket["reporter"]}

## Description
{ticket["description"]}

## Requirements
{"".join([f"- {req}\\n" for req in requirements])}

## Acceptance Criteria
{"".join([f"{i+1}. {ac}\\n" for i, ac in enumerate(acceptance_criteria)])}
"""
            
            return {
                "status": "success",
                "message": f"Found ticket {ticket_id}",
                "ticket": ticket,
                "formatted_details": formatted_details
            }
    
    return {
        "status": "error",
        "message": f"Ticket {ticket_id} not found"
    }

def list_open_tickets() -> Dict[str, Any]:
    """Dummy function to list open JIRA tickets"""
    open_tickets = [ticket for ticket in MOCK_TICKETS if ticket["status"] == "Open"]
    
    # Format tickets as markdown table
    table = "| Key | Summary | Type | Priority | Assignee |\n"
    table += "|-----|---------|------|----------|----------|\n"
    for ticket in open_tickets:
        table += f"| {ticket['key']} | {ticket['summary']} | {ticket['type']} | {ticket['priority']} | {ticket['assignee']} |\n"
    
    return {
        "status": "success",
        "message": f"Found {len(open_tickets)} open tickets",
        "tickets": open_tickets,
        "formatted_table": table
    }

# Create FunctionTool instances
start_jira_mcp_server_tool = FunctionTool(start_jira_mcp_server)
get_ticket_details_tool = FunctionTool(get_ticket_details)
list_open_tickets_tool = FunctionTool(list_open_tickets)