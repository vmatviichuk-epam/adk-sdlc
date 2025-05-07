# ADK SDLC Agent Instructions

## Running Agents in UI Mode

To run the agents in UI mode, use the following command:

```bash
adk web
```

This command will start the web interface for interacting with the agents. The UI mode provides a more user-friendly way to interact with the agents and monitor their progress.

## Running Agents in CLI Mode

To run the agents in CLI mode, use the following command:

```bash
adk run .
```

This command will start the agents in the command-line interface. The CLI mode allows you to interact with the agents directly in your terminal.

## Important Notes

- Make sure your virtual environment is activated before running the command
- The `adk web` command is the correct way to start the UI mode, not `python -m ascii_art_sdlc.agent --ui`
- The UI will be accessible through your web browser once the server is running

## Additional Information

- The UI mode provides a visual interface for:
  - Monitoring agent interactions
  - Viewing agent responses
  - Tracking workflow progress
  - Managing agent configurations