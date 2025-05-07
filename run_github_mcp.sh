#!/bin/bash

# Configuration Variables
# GitHub Configuration
export GITHUB_PAT="${GITHUB_PAT:-}"  # Your GitHub Personal Access Token
export GITHUB_API_URL="${GITHUB_API_URL:-https://api.github.com}"
export GITHUB_ORG="${GITHUB_ORG:-}"  # Your GitHub Organization (if applicable)
export GITHUB_REPO="${GITHUB_REPO:-}" # Your GitHub Repository

# Server Configuration
export MCP_HOST="${MCP_HOST:-0.0.0.0}"
export MCP_PORT="${MCP_PORT:-8001}"
export MCP_LOG_LEVEL="${MCP_LOG_LEVEL:-INFO}"

# Security Configuration
export MCP_ALLOWED_ORIGINS="${MCP_ALLOWED_ORIGINS:-*}"  # Comma-separated list of allowed origins
export MCP_AUTH_TOKEN="${MCP_AUTH_TOKEN:-}"  # Optional authentication token for API access

# Function to check if required variables are set
check_required_vars() {
    local missing_vars=()
    
    if [ -z "$GITHUB_PAT" ]; then
        missing_vars+=("GITHUB_PAT")
    fi
    
    if [ ${#missing_vars[@]} -ne 0 ]; then
        echo "Error: The following required variables are not set:"
        printf '%s\n' "${missing_vars[@]}"
        exit 1
    fi
}

# Function to clone or update the GitHub MCP server repository
setup_repo() {
    if [ ! -d "github-mcp-server" ]; then
        echo "Cloning GitHub MCP server repository..."
        git clone https://github.com/github/github-mcp-server.git
    else
        echo "Updating GitHub MCP server repository..."
        cd github-mcp-server
        git pull
        cd ..
    fi
}

# Function to build the server
build_server() {
    echo "Building GitHub MCP server..."
    cd github-mcp-server
    go build -o github-mcp-server ./cmd/server
    cd ..
}

# Function to start the MCP server
start_server() {
    echo "Starting GitHub MCP server..."
    echo "Host: $MCP_HOST"
    echo "Port: $MCP_PORT"
    echo "GitHub API URL: $GITHUB_API_URL"
    
    cd github-mcp-server
    ./github-mcp-server \
        --host "$MCP_HOST" \
        --port "$MCP_PORT" \
        --github-token "$GITHUB_PAT" \
        --log-level "$MCP_LOG_LEVEL" \
        --allowed-origins "$MCP_ALLOWED_ORIGINS"
}

# Main execution
echo "GitHub MCP Server Setup"
echo "----------------------"

# Check required variables
check_required_vars

# Setup and build the server
setup_repo
build_server

# Start the server
start_server 