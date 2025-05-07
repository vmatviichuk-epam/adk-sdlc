from google.adk.tools import FunctionTool
from typing import Dict, Any, List
import json

def generate_requirements(ticket_id: str) -> Dict[str, Any]:
    """
    Analyzes a JIRA ticket and extracts structured requirements.
    
    Args:
        ticket_id: The JIRA ticket ID to analyze
        
    Returns:
        A dictionary containing the structured requirements
    """
    try:
        # This would normally fetch ticket details from JIRA
        # For now, we'll return mock data based on the ticket ID
        
        requirements_data = {}
        
        # Different mock data based on ticket ID
        if ticket_id == "FAKE-7":
            requirements_data = {
                "ticket": {
                    "id": "FAKE-7",
                    "summary": "Add 100% unit test coverage for both ascii_converter.py and ascii_art.py classes",
                    "description": "As a developer, I want to have 100% test coverage for both ascii_converter.py and ascii_art.py classes.",
                    "status": "Open"
                },
                "requirements": [
                    "Write unit tests for all methods in ascii_converter.py",
                    "Write unit tests for all methods in ascii_art.py",
                    "Ensure test coverage is at 100% for both files",
                    "Mock any external dependencies",
                    "Test edge cases like empty images, very large images, etc."
                ],
                "priority": "Medium",
                "acceptance_criteria": [
                    "All methods in ascii_converter.py have associated tests",
                    "All methods in ascii_art.py have associated tests",
                    "Test coverage report shows 100% coverage",
                    "CI/CD pipeline passes all tests"
                ]
            }
        elif ticket_id == "ASCII-123":
            requirements_data = {
                "ticket": {
                    "id": "ASCII-123",
                    "summary": "Implement RGB color support",
                    "description": "As a user, I want to be able to use RGB colors in my ASCII art, so I can create more colorful and visually appealing outputs.",
                    "status": "Open"
                },
                "requirements": [
                    "Add support for RGB color mapping of ASCII characters",
                    "Create a color palette selection option",
                    "Allow exporting colored ASCII art as HTML",
                    "Add a preview feature to see colors in real-time"
                ],
                "priority": "Medium",
                "acceptance_criteria": [
                    "User can specify RGB colors for ASCII output",
                    "Output can be viewed with colors in the application",
                    "HTML export preserves the color information"
                ]
            }
        elif ticket_id == "ASCII-124":
            requirements_data = {
                "ticket": {
                    "id": "ASCII-124",
                    "summary": "Add export to PDF feature",
                    "description": "As a user, I want to export my ASCII art to PDF format, so I can easily share and print high-quality versions of my creations.",
                    "status": "In Progress"
                },
                "requirements": [
                    "Add a PDF export option",
                    "Ensure fonts are embedded properly in the PDF",
                    "Allow setting page size and margins",
                    "Add an option to include metadata (title, author, etc.)"
                ],
                "priority": "Medium",
                "acceptance_criteria": [
                    "User can export ASCII art as PDF",
                    "PDF output preserves exact character spacing and alignment",
                    "PDF includes customizable metadata"
                ]
            }
        elif ticket_id == "CRM-5":
            requirements_data = {
                "ticket": {
                    "id": "CRM-5",
                    "summary": "Fix scrolling in large images",
                    "description": "As a user, I experience scrolling issues when working with large images. This needs to be fixed for better usability.",
                    "status": "Open"
                },
                "requirements": [
                    "Optimize scrolling performance for large images",
                    "Add scrollbar indicators",
                    "Implement smooth scrolling",
                    "Add a mini-map navigation option for very large images"
                ],
                "priority": "High",
                "acceptance_criteria": [
                    "Scrolling is smooth with images of any size",
                    "Scrollbars show current position within large images",
                    "Mini-map helps with navigation in very large images"
                ]
            }
        elif ticket_id == "CRM-6":
            requirements_data = {
                "ticket": {
                    "id": "CRM-6",
                    "summary": "Add dark mode support",
                    "description": "As a user, I want the application to have a dark mode option, so that I can reduce eye strain when working in low-light environments.",
                    "status": "Ready for Review"
                },
                "requirements": [
                    "Add a toggle to switch between light and dark mode",
                    "Implement dark color scheme for all UI components",
                    "Remember user preference between sessions",
                    "Automatically detect system dark mode setting"
                ],
                "priority": "Medium",
                "acceptance_criteria": [
                    "Dark mode can be toggled on/off",
                    "All UI elements have appropriate dark mode colors",
                    "Application remembers user's theme preference",
                    "Theme automatically matches system settings by default"
                ]
            }
        elif ticket_id == "FAKE-9":
            requirements_data = {
                "ticket": {
                    "id": "FAKE-9",
                    "summary": "Write a function that will inverse a string",
                    "description": "As a developer, I need a utility function that will invert a string (reverse its characters).",
                    "status": "Open"
                },
                "requirements": [
                    "Create a function that takes a string input and returns the reversed string",
                    "Handle empty strings and single-character strings properly",
                    "Ensure Unicode characters are handled correctly",
                    "Implement the function efficiently (O(n) time complexity)",
                    "Write comprehensive unit tests for the function"
                ],
                "priority": "Low",
                "acceptance_criteria": [
                    "Function correctly reverses any input string",
                    "Edge cases are handled properly",
                    "Tests cover all required functionality"
                ]
            }
        else:
            # Default mock data for unknown ticket IDs
            requirements_data = {
                "ticket": {
                    "id": ticket_id,
                    "summary": "Unknown ticket",
                    "description": "This ticket ID does not exist in the mock data.",
                    "status": "Unknown"
                },
                "requirements": [
                    "Please use one of the available mock ticket IDs"
                ],
                "priority": "Unknown",
                "acceptance_criteria": []
            }
        
        # Format the requirements for display
        requirements_list = ""
        for req in requirements_data['requirements']:
            requirements_list += f"- {req}\n"
            
        acceptance_list = ""
        for crit in requirements_data['acceptance_criteria']:
            acceptance_list += f"- {crit}\n"
            
        formatted_requirements = f"""
# Requirements Analysis for {requirements_data['ticket']['id']}

## Summary
{requirements_data['ticket']['summary']}

## Description
{requirements_data['ticket']['description']}

## Status
{requirements_data['ticket']['status']}

## Priority
{requirements_data['priority']}

## Requirements
{requirements_list}

## Acceptance Criteria
{acceptance_list}
"""
        
        return {
            "success": True,
            "ticket_id": ticket_id,
            "requirements": requirements_data,
            "formatted_requirements": formatted_requirements,
            "message": f"Requirements for ticket {ticket_id} analyzed successfully"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to generate requirements for ticket {ticket_id}"
        }

# Create the FunctionTool
generate_requirements_tool = FunctionTool(generate_requirements)