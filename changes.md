# Changes Log

## 2025-04-29
- Fixed JIRA MCP server connection issue by updating start_jira_mcp_server function to use uvx command
- Updated JIRA API token to include complete token string
- Increased server startup wait time to ensure proper initialization
- Enhanced PR agent to use default repository (https://github.com/vmatviichuk-epam/ascii-art-generator) when the user provides an empty input
- Updated orchestrator agent prompt to inform users about the default repository option

## 2025-04-28
- Added support for CRM-7 ticket to JIRA tool
- Implemented Atlassian MCP API connection with fallback to mock data
- Added JIRA integration environment variables to configuration
- Implemented GitHub MCP API for PR creation with fallback to mock data
- Added GitHub integration environment variables
- Updated orchestrator agent to accept any JIRA ticket ID format
- Removed all mock data from JIRA tool, using only real Atlassian MCP API
- Removed all mock data from GitHub PR tool, using only real GitHub MCP API
- Updated .env file to clearly mark required API credentials
- Fixed JIRA tool to use correct MCP API action 'jira_get_issue' for fetching CRM-7
- Added fallback to list available tickets when specific ticket ID isn't found
- Updated requirements agent prompt to handle fallback ticket listing feature
- Updated orchestrator prompt to display available tickets when ticket isn't found
- Registered list_my_tickets tool to enable direct ticket listing
- Enhanced requirements agent to display formatted table of available tickets
- Modified JIRA tool to use local MCP server with fallback to demo data