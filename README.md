# ADK SDLC Agent Chain

This project uses the Agent Development Kit (ADK) to create a chain of AI agents that automate the software development lifecycle for any software project.

## Architecture

The agent chain consists of the following components:

1. **Orchestrator Agent** - Coordinates the workflow between all other agents
2. **Requirements Agent** - Connects to Atlassian/JIRA via MCP to fetch ticket descriptions
3. **Implementation Agent** - Writes code based on the requirements
4. **Testing Agent** - Creates unit tests for the implementation
5. **PR Agent** - Submits code changes to GitHub using GitHub MCP

## Getting Started

### Prerequisites

- Python 3.9 or higher
- [Poetry](https://python-poetry.org/docs/#installation)
- Google Cloud account with Vertex AI enabled
- Atlassian/JIRA account with API access
- GitHub account with access to your target repository

### Setup

1. Clone this repository
2. Copy `.env.example` to `.env` and fill in your credentials
3. Install dependencies:

```bash
poetry install
```

### Running the Agent Chain

Start the agent chain with:

```bash
cd adk-sdlc
adk run .
```

Or use the ADK web interface:

```bash
cd adk-sdlc
adk web
```

Then select the ADK SDLC agent from the dropdown menu in your browser.

## Usage

Once the agent is running, you can initiate the workflow by providing a JIRA ticket ID. The agent chain will:

1. Fetch the ticket description from JIRA
2. Generate an implementation based on the requirements
3. Create unit tests for the implementation
4. Submit a pull request to your target repository

## Customization

You can customize the behavior of each agent by modifying its prompt in the respective prompt.py file.