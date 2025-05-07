#!/bin/bash

# Configuration Variables
# JIRA Configuration
export JIRA_API_KEY="${JIRA_API_KEY:-}"  # Your JIRA API Key
export JIRA_USER="${JIRA_USER:-}"  # Your JIRA Username
export JIRA_DOMAIN="${JIRA_DOMAIN:-}"  # Your JIRA domain (e.g., your-domain.atlassian.net)

# Server Configuration
export MCP_HOST="${MCP_HOST:-0.0.0.0}"
export MCP_PORT="${MCP_PORT:-3000}"
export MCP_LOG_LEVEL="${MCP_LOG_LEVEL:-INFO}"

# Security Configuration
export MCP_ALLOWED_ORIGINS="${MCP_ALLOWED_ORIGINS:-*}"  # Comma-separated list of allowed origins
export MCP_AUTH_TOKEN="${MCP_AUTH_TOKEN:-}"  # Optional authentication token for API access

# Function to check if required variables are set
check_required_vars() {
    local missing_vars=()
    
    if [ -z "$JIRA_API_KEY" ]; then
        missing_vars+=("JIRA_API_KEY")
    fi
    
    if [ -z "$JIRA_USER" ]; then
        missing_vars+=("JIRA_USER")
    fi
    
    if [ -z "$JIRA_DOMAIN" ]; then
        missing_vars+=("JIRA_DOMAIN")
    fi
    
    if [ ${#missing_vars[@]} -ne 0 ]; then
        echo "Error: The following required variables are not set:"
        printf '%s\n' "${missing_vars[@]}"
        exit 1
    fi
}

# Function to clone or update the JIRA MCP server repository
setup_repo() {
    if [ ! -d "jira-mcp-server" ]; then
        echo "Cloning JIRA MCP server repository..."
        git clone https://github.com/atlassian/jira-mcp-server.git
    else
        echo "Updating JIRA MCP server repository..."
        cd jira-mcp-server
        git pull
        cd ..
    fi
}

# Function to build the server
build_server() {
    echo "Building JIRA MCP server..."
    cd jira-mcp-server
    go build -o jira-mcp-server ./cmd/server
    cd ..
}

# Function to start the MCP server
start_server() {
    echo "Starting JIRA MCP server..."
    echo "Host: $MCP_HOST"
    echo "Port: $MCP_PORT"
    echo "JIRA Domain: $JIRA_DOMAIN"
    
    cd jira-mcp-server
    ./jira-mcp-server \
        --host "$MCP_HOST" \
        --port "$MCP_PORT" \
        --jira-api-key "$JIRA_API_KEY" \
        --jira-user "$JIRA_USER" \
        --jira-domain "$JIRA_DOMAIN" \
        --log-level "$MCP_LOG_LEVEL" \
        --allowed-origins "$MCP_ALLOWED_ORIGINS"
}

# Main execution
echo "JIRA MCP Server Setup"
echo "----------------------"

# Check required variables
check_required_vars

# Setup and build the server
setup_repo
build_server

# Start the server
start_server