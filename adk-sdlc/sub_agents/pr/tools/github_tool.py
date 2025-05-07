import os
from typing import Dict, Any, List, Optional
from google.adk.tools import FunctionTool

# Mock data for GitHub operations
MOCK_REPOSITORIES = {
    "vmatviichuk-epam/ascii-art-generator": {
        "issues": [
            {
                "number": 1,
                "title": "Implement basic ASCII art conversion",
                "body": "Create a function to convert images to ASCII art",
                "state": "open",
                "labels": ["enhancement"]
            },
            {
                "number": 2,
                "title": "Add color support",
                "body": "Add support for colored ASCII art output",
                "state": "open",
                "labels": ["feature"]
            }
        ],
        "branches": ["main", "develop"]
    }
}

def start_github_mcp_server() -> Dict[str, Any]:
    """Dummy function to simulate starting GitHub MCP server"""
    return {
        "status": "success",
        "message": "GitHub MCP server started successfully",
        "pid": 12345
    }

def setup_repository(repo_url: Optional[str] = None) -> Dict[str, Any]:
    """Dummy function to simulate setting up a GitHub repository"""
    if not repo_url:
        return {"status": "error", "message": "Repository URL is required"}
    
    # Extract owner and repo name from URL
    parts = repo_url.strip("/").split("/")
    if len(parts) < 2:
        return {"status": "error", "message": "Invalid repository URL format"}
    
    owner = parts[-2]
    repo = parts[-1]
    repo_key = f"{owner}/{repo}"
    
    if repo_key not in MOCK_REPOSITORIES:
        MOCK_REPOSITORIES[repo_key] = {
            "issues": [],
            "branches": ["main"]
        }
    
    return {
        "status": "success",
        "message": f"Repository {repo_key} setup successfully",
        "owner": owner,
        "repo": repo
    }

def list_open_issues(repo_url: Optional[str] = None) -> Dict[str, Any]:
    """Dummy function to list open issues"""
    if not repo_url:
        return {"status": "error", "message": "Repository URL is required"}
    
    parts = repo_url.strip("/").split("/")
    if len(parts) < 2:
        return {"status": "error", "message": "Invalid repository URL format"}
    
    repo_key = f"{parts[-2]}/{parts[-1]}"
    if repo_key not in MOCK_REPOSITORIES:
        return {"status": "error", "message": "Repository not found"}
    
    issues = MOCK_REPOSITORIES[repo_key]["issues"]
    open_issues = [issue for issue in issues if issue["state"] == "open"]
    
    return {
        "status": "success",
        "message": f"Found {len(open_issues)} open issues",
        "issues": open_issues
    }

def get_issue_details(issue_number: int) -> Dict[str, Any]:
    """Dummy function to get issue details"""
    for repo in MOCK_REPOSITORIES.values():
        for issue in repo["issues"]:
            if issue["number"] == issue_number:
                return {
                    "status": "success",
                    "message": f"Found issue #{issue_number}",
                    "issue": issue
                }
    
    return {
        "status": "error",
        "message": f"Issue #{issue_number} not found"
    }

def create_github_pr_func(
    title: str,
    body: str,
    head: str,
    base: str = "main",
    repo_url: Optional[str] = None
) -> Dict[str, Any]:
    """Dummy function to create a GitHub PR"""
    if not repo_url:
        return {"status": "error", "message": "Repository URL is required"}
    
    parts = repo_url.strip("/").split("/")
    if len(parts) < 2:
        return {"status": "error", "message": "Invalid repository URL format"}
    
    repo_key = f"{parts[-2]}/{parts[-1]}"
    if repo_key not in MOCK_REPOSITORIES:
        return {"status": "error", "message": "Repository not found"}
    
    # Generate a mock PR number
    pr_number = len(MOCK_REPOSITORIES[repo_key]["issues"]) + 1
    
    return {
        "status": "success",
        "message": f"Created PR #{pr_number}",
        "pr": {
            "number": pr_number,
            "title": title,
            "body": body,
            "head": head,
            "base": base,
            "state": "open"
        }
    }

# Create FunctionTool instances
start_github_mcp_server_tool = FunctionTool(start_github_mcp_server)
setup_repository_tool = FunctionTool(setup_repository)
list_open_issues_tool = FunctionTool(list_open_issues)
get_issue_details_tool = FunctionTool(get_issue_details)
create_github_pr_tool = FunctionTool(create_github_pr_func)