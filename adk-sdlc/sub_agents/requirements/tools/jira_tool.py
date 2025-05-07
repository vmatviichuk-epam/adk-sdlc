import os
from typing import Dict, Any, List, Optional
from google.adk.tools import FunctionTool

# Mock data for JIRA operations
MOCK_TICKETS = [
    {
        "key": "ASCII-1",
        "summary": "Implement basic ASCII art conversion",
        "status": "Open",
        "description": """
As a user, I want to convert images to ASCII art.

Requirements:
- Support PNG and JPEG formats
- Allow adjusting output size
- Support grayscale conversion

Acceptance Criteria:
1. User can upload an image
2. User can select output size
3. User can download ASCII art result
""",
        "type": "Story",
        "priority": "High",
        "assignee": "John Doe",
        "reporter": "Jane Smith",
        "created": "2024-05-07T10:00:00.000Z",
        "updated": "2024-05-07T10:30:00.000Z"
    },
    {
        "key": "ASCII-2",
        "summary": "Add color support to ASCII art",
        "status": "Open",
        "description": """
As a user, I want to generate colored ASCII art.

Requirements:
- Support RGB color output
- Allow color intensity adjustment
- Maintain readability

Acceptance Criteria:
1. ASCII art preserves original colors
2. User can adjust color intensity
3. Output is readable on both light and dark backgrounds
""",
        "type": "Story",
        "priority": "Medium",
        "assignee": "John Doe",
        "reporter": "Jane Smith",
        "created": "2024-05-07T11:00:00.000Z",
        "updated": "2024-05-07T11:15:00.000Z"
    },
    {
        "key": "ASCII-3",
        "summary": "Add export options",
        "status": "Open",
        "description": """
As a user, I want to export ASCII art in different formats.

Requirements:
- Support TXT format
- Support HTML format with styling
- Support PDF export

Acceptance Criteria:
1. User can export as plain text
2. User can export as styled HTML
3. User can export as PDF with preserved formatting
""",
        "type": "Story",
        "priority": "Low",
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