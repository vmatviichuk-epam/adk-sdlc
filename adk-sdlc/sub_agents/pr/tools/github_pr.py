import os
import requests
import json
import subprocess
import base64
from google.adk.tools import FunctionTool
from typing import Dict, Any, List, Optional, Union
from dotenv import load_dotenv

load_dotenv()

def create_github_pr_func(
    ticket_id: str, 
    implementation: Dict[str, Any], 
    tests: Dict[str, Any],
    pr_title: str = "",
    pr_description: str = ""
) -> Dict[str, Any]:
    """
    Creates a GitHub pull request with the implementation and test files.
    
    Args:
        ticket_id: The JIRA ticket ID associated with this PR
        implementation: The code implementation files
        tests: The test files
        pr_title: Title for the pull request (optional)
        pr_description: Description for the pull request (optional)
        
    Returns:
        A dictionary containing PR details
    """
    # Get GitHub settings from environment variables
    github_token = os.environ.get("GITHUB_TOKEN")
    github_username = os.environ.get("GITHUB_USERNAME")
    github_repo = os.environ.get("GITHUB_REPO", "ascii-art-converter")
    github_base_branch = os.environ.get("GITHUB_BASE_BRANCH", "main")
    github_org = os.environ.get("GITHUB_ORG")
    
    # If PR title is not provided, generate one from the ticket ID
    if not pr_title:
        pr_title = f"[{ticket_id}] Implement ASCII Art Converter"
    
    # If PR description is not provided, generate a basic one
    if not pr_description:
        pr_description = f"""
# {ticket_id} - ASCII Art Converter Implementation

This PR implements an ASCII art converter that can transform images into ASCII art.

## Features Implemented

- Convert PNG and JPG images to ASCII art
- Support for different ASCII character sets (simple, standard, complex)
- Save output to text files
- Preserve aspect ratio of original images

## Test Coverage

- Unit tests for all core functionality
- Edge case handling
- Test coverage for different character sets and output options

## How to Test

1. Install dependencies: `pip install -r requirements.txt`
2. Run the converter: `python -m ascii_art_converter.image_to_ascii input_image.jpg -o output.txt`
3. Run tests: `python -m pytest tests/`
"""
    
    # Extract files from implementation and tests
    impl_files = implementation.get("files", {})
    test_files = tests.get("files", {})
    
    # Combine all files
    all_files = {**impl_files, **test_files}
    
    # Check for GitHub token
    if not github_token:
        return {
            "success": False,
            "error": "GitHub token not found in environment variables",
            "message": "Please set up your GitHub credentials in the .env file"
        }
    
    # Setup branch name
    branch_name = f"feature/{ticket_id.lower()}-ascii-art-converter"
    
    # Build the request URL for GitHub MCP API
    mcp_url = "https://api.github.com/mcp"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {github_token}"
    }
    
    try:
        # First create a branch
        branch_payload = {
            "action": "create_branch",
            "parameters": {
                "owner": github_org or github_username,
                "repo": github_repo,
                "branch": branch_name,
                "from_branch": github_base_branch
            }
        }
        
        # Create the branch
        branch_response = requests.post(mcp_url, headers=headers, json=branch_payload)
        
        if not (branch_response.status_code == 200 or branch_response.status_code == 201):
            return {
                "success": False,
                "error": f"Failed to create branch: {branch_response.status_code}",
                "message": f"Error: {branch_response.text}"
            }
        
        # Now commit files to the branch
        files_list = []
        for file_path, file_content in all_files.items():
            files_list.append({
                "path": file_path,
                "content": file_content
            })
        
        # Push files payload
        push_payload = {
            "action": "push_files",
            "parameters": {
                "owner": github_org or github_username,
                "repo": github_repo,
                "branch": branch_name,
                "message": f"Implement {ticket_id} - ASCII Art Converter",
                "files": files_list
            }
        }
        
        # Push the files
        push_response = requests.post(mcp_url, headers=headers, json=push_payload)
        
        if not (push_response.status_code == 200 or push_response.status_code == 201):
            return {
                "success": False,
                "error": f"Failed to push files: {push_response.status_code}",
                "message": f"Error: {push_response.text}"
            }
        
        # Finally create the PR
        pr_payload = {
            "action": "create_pull_request",
            "parameters": {
                "owner": github_org or github_username,
                "repo": github_repo,
                "title": pr_title,
                "body": pr_description,
                "head": branch_name,
                "base": github_base_branch
            }
        }
        
        # Create the PR
        pr_response = requests.post(mcp_url, headers=headers, json=pr_payload)
        
        if not (pr_response.status_code == 200 or pr_response.status_code == 201):
            return {
                "success": False,
                "error": f"Failed to create PR: {pr_response.status_code}",
                "message": f"Error: {pr_response.text}"
            }
        
        pr_data = pr_response.json()
        return {
            "success": True,
            "pr_number": pr_data.get("number"),
            "pr_url": pr_data.get("html_url"),
            "pr_title": pr_title,
            "branch_name": branch_name,
            "files_committed": list(all_files.keys()),
            "message": f"Successfully created PR #{pr_data.get('number')} for {ticket_id}"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"Error connecting to GitHub MCP for ticket {ticket_id}"
        }

def start_github_mcp_server() -> Dict[str, Any]:
    """
    Starts the GitHub MCP server using the run_github_mcp.sh script.
    
    Returns:
        A dictionary containing the server status
    """
    try:
        # Get the absolute path to the script
        script_path = os.path.join(os.path.dirname(__file__), "run_github_mcp.sh")
        
        # Make sure the script is executable
        subprocess.run(["chmod", "+x", script_path], check=True)
        
        # Start the server in the background
        process = subprocess.Popen([script_path], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE,
                                 start_new_session=True)
        
        # Wait a moment for the server to start
        import time
        time.sleep(2)
        
        return {
            "success": True,
            "message": "GitHub MCP server started successfully",
            "process_id": process.pid
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to start GitHub MCP server"
        }

def setup_repository(repo_url: Optional[str] = None) -> Dict[str, Any]:
    """
    Sets up the repository by downloading it and storing its information.
    
    Args:
        repo_url: The GitHub repository URL
        
    Returns:
        A dictionary containing repository setup status
    """
    try:
        # Extract owner and repo name from URL
        parts = repo_url.strip("/").split("/")
        if len(parts) < 2:
            return {
                "success": False,
                "error": "Invalid repository URL format",
                "message": "Repository URL must be in format: https://github.com/owner/repo"
            }
        
        owner = parts[-2]
        repo = parts[-1]
        
        # Store repository information in environment variables
        os.environ["GITHUB_REPO"] = repo
        os.environ["GITHUB_USER"] = owner
        os.environ["GITHUB_REPO_URL"] = repo_url
        
        # Clone the repository
        clone_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
                               "repositories", repo)
        
        # Create repositories directory if it doesn't exist
        os.makedirs(os.path.dirname(clone_dir), exist_ok=True)
        
        # Remove existing directory if it exists
        if os.path.exists(clone_dir):
            import shutil
            shutil.rmtree(clone_dir)
        
        # Clone the repository
        subprocess.run(["git", "clone", repo_url, clone_dir], check=True)
        
        return {
            "success": True,
            "message": f"Repository {repo_url} set up successfully",
            "clone_dir": clone_dir,
            "owner": owner,
            "repo": repo
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to set up repository {repo_url}"
        }

def create_branch(branch_name: str, base_branch: str = "main") -> Dict[str, Any]:
    """
    Creates a new branch in the GitHub repository.
    
    Args:
        branch_name: The name of the branch to create
        base_branch: The name of the base branch to branch from (default: main)
        
    Returns:
        A dictionary containing the branch creation status
    """
    try:
        # Get GitHub settings from environment variables
        github_token = os.environ.get("GITHUB_TOKEN")
        github_username = os.environ.get("GITHUB_USERNAME")
        github_repo = os.environ.get("GITHUB_REPO")
        github_org = os.environ.get("GITHUB_ORG")
        
        # Check for GitHub token
        if not github_token:
            return {
                "success": False,
                "error": "GitHub token not found in environment variables",
                "message": "Please set up your GitHub credentials in the .env file"
            }
            
        # Check for repo information
        if not github_repo:
            return {
                "success": False,
                "error": "GitHub repository not found in environment variables",
                "message": "Please set up the repository first using setup_repository function"
            }
        
        # Build the request URL for GitHub MCP API
        mcp_url = "http://localhost:3000/api"  # Use local GitHub MCP server
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {github_token}"
        }
        
        # Create branch payload
        owner = github_org or github_username
        branch_url = f"{mcp_url}/repo/{owner}/{github_repo}/git/refs"
        
        # Get the SHA of the base branch
        ref_url = f"{mcp_url}/repo/{owner}/{github_repo}/git/refs/heads/{base_branch}"
        ref_response = requests.get(ref_url, headers=headers)
        
        if ref_response.status_code != 200:
            return {
                "success": False,
                "error": f"Failed to get base branch reference: {ref_response.status_code}",
                "message": f"Error: {ref_response.text}"
            }
        
        base_sha = ref_response.json().get("object", {}).get("sha")
        
        # Create the new branch
        branch_payload = {
            "ref": f"refs/heads/{branch_name}",
            "sha": base_sha
        }
        
        branch_response = requests.post(branch_url, headers=headers, json=branch_payload)
        
        if branch_response.status_code not in [200, 201]:
            # If the branch already exists, this is not necessarily an error
            if "Reference already exists" in branch_response.text:
                return {
                    "success": True,
                    "branch_name": branch_name,
                    "message": f"Branch '{branch_name}' already exists, using existing branch"
                }
            return {
                "success": False,
                "error": f"Failed to create branch: {branch_response.status_code}",
                "message": f"Error: {branch_response.text}"
            }
        
        return {
            "success": True,
            "branch_name": branch_name,
            "base_branch": base_branch,
            "message": f"Successfully created branch '{branch_name}' from '{base_branch}'"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to create branch '{branch_name}': {str(e)}"
        }

def make_pr(issue_number: int, title: str = "", branch_name: str = "", base_branch: str = "main", 
            files: Dict[str, str] = None, description: str = "") -> Dict[str, Any]:
    """
    Creates a pull request for the given GitHub issue.
    
    Args:
        issue_number: The GitHub issue number to reference in the PR
        title: Optional PR title (if not provided, will use issue title)
        branch_name: Optional branch name (if not provided, will create one based on issue number)
        base_branch: The base branch to target (default: main)
        files: Dictionary of files to include in the PR, with file paths as keys and content as values
        description: Optional PR description
        
    Returns:
        A dictionary containing the PR creation status
    """
    try:
        # Get GitHub settings from environment variables
        github_token = os.environ.get("GITHUB_TOKEN")
        github_repo = os.environ.get("GITHUB_REPO")
        owner = os.environ.get("GITHUB_OWNER") or os.environ.get("GITHUB_USER") or os.environ.get("GITHUB_USERNAME")
        
        # Check for GitHub token
        if not github_token:
            return {
                "success": False,
                "error": "GitHub token not found in environment variables",
                "message": "Please set up your GitHub credentials in the .env file"
            }
            
        # Check for repo information
        if not github_repo or not owner:
            return {
                "success": False,
                "error": "GitHub repository information not found in environment variables",
                "message": "Please set up the repository first using setup_repository function"
            }
        
        # Get issue details if needed for title/description
        if not title or not description:
            # Get the issue details
            issue_url = f"http://localhost:3000/api/repo/{owner}/{github_repo}/issues/{issue_number}"
            issue_response = requests.get(
                issue_url, 
                headers={"Authorization": f"Bearer {github_token}"}
            )
            
            if issue_response.status_code != 200:
                return {
                    "success": False,
                    "error": f"Failed to fetch issue: {issue_response.status_code}",
                    "message": f"Error: {issue_response.text}"
                }
            
            issue_data = issue_response.json()
            
            # Use issue title for PR title if not provided
            if not title:
                title = f"Fix #{issue_number}: {issue_data.get('title')}"
            
            # Use issue body for PR description if not provided
            if not description:
                description = f"""
## Fix for issue #{issue_number}

{issue_data.get('body', '')}

## Changes

- Implementation of the required changes to address the issue
- Added automated tests to verify functionality

Closes #{issue_number}
"""
        
        # Generate branch name if not provided
        if not branch_name:
            branch_name = f"fix-issue-{issue_number}"
        
        # Create the branch if it doesn't exist
        branch_result = create_branch(branch_name, base_branch)
        if not branch_result.get("success", False):
            return {
                "success": False,
                "error": branch_result.get("error", "Unknown error creating branch"),
                "message": branch_result.get("message", "Failed to create branch")
            }
        
        # Push files to the branch if provided
        if files:
            # Convert files dict to list of paths and contents
            files_list = []
            for file_path, file_content in files.items():
                files_list.append({
                    "path": file_path,
                    "content": file_content
                })
            
            # Push files to the branch
            commit_message = f"Fix #{issue_number}: {title}"
            files_url = f"http://localhost:3000/api/repo/{owner}/{github_repo}/contents"
            
            for file_info in files_list:
                file_path = file_info["path"]
                file_content = file_info["content"]
                
                # Check if file already exists to get its SHA
                file_check_url = f"{files_url}/{file_path}"
                file_check_params = {"ref": branch_name}
                file_check_response = requests.get(
                    file_check_url,
                    params=file_check_params,
                    headers={"Authorization": f"Bearer {github_token}"}
                )
                
                file_sha = None
                if file_check_response.status_code == 200:
                    # File exists, get its SHA
                    file_sha = file_check_response.json().get("sha")
                
                # Prepare the payload for creating/updating the file
                file_payload = {
                    "message": commit_message,
                    "content": base64.b64encode(file_content.encode()).decode(),
                    "branch": branch_name
                }
                
                # Add SHA if updating an existing file
                if file_sha:
                    file_payload["sha"] = file_sha
                
                # Create or update the file
                file_response = requests.put(
                    file_check_url,
                    headers={"Authorization": f"Bearer {github_token}", "Content-Type": "application/json"},
                    json=file_payload
                )
                
                if file_response.status_code not in [200, 201]:
                    return {
                        "success": False,
                        "error": f"Failed to push file {file_path}: {file_response.status_code}",
                        "message": f"Error: {file_response.text}"
                    }
        
        # Create the PR
        pr_url = f"http://localhost:3000/api/repo/{owner}/{github_repo}/pulls"
        pr_payload = {
            "title": title,
            "body": description,
            "head": branch_name,
            "base": base_branch
        }
        
        pr_response = requests.post(
            pr_url,
            headers={"Authorization": f"Bearer {github_token}", "Content-Type": "application/json"},
            json=pr_payload
        )
        
        if pr_response.status_code not in [200, 201]:
            return {
                "success": False,
                "error": f"Failed to create PR: {pr_response.status_code}",
                "message": f"Error: {pr_response.text}"
            }
        
        pr_data = pr_response.json()
        return {
            "success": True,
            "pr_number": pr_data.get("number"),
            "pr_url": pr_data.get("html_url"),
            "pr_title": title,
            "branch_name": branch_name,
            "files_committed": list(files.keys()) if files else [],
            "message": f"Successfully created PR #{pr_data.get('number')} for issue #{issue_number}"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to create PR for issue #{issue_number}: {str(e)}"
        }

# Create FunctionTool instances
start_github_mcp = FunctionTool(start_github_mcp_server)
setup_repository_tool = FunctionTool(setup_repository)
create_github_pr = FunctionTool(create_github_pr_func)
create_branch_tool = FunctionTool(create_branch)
make_pr_tool = FunctionTool(make_pr)