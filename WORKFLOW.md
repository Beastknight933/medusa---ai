# n8n Starter Workflow Guide

This repository includes a starter file (`n8n_starter_workflow.json`) designed to act as the intelligence layer for Medusa AI.

## Workflow Philosophy

The workflow is intentionally designed to be **Model-Agnostic** and **Provider-Agnostic**. You are not locked into OpenAI. The architecture relies on standardized n8n `AI Agent` patterns, allowing you to seamlessly swap in Groq, Ollama, Anthropic, or any other LLM provider supported by n8n.

## How the Workflow Operates

1. **Webhook Trigger**: Listens for POST requests at `/webhook/assistant`. It extracts the spoken `text` and system `context` from the Python client.
2. **AI Agent Node**: This is the core reasoning engine. It is configured with a custom system prompt instructing it to act as J.A.R.V.I.S.
3. **Memory Node**: Attached to the Agent to maintain conversational history across requests.
4. **Tool Router Placeholder**: Attached to the Agent. This is where you can plug in custom tools (e.g., "Get Weather", "Check Calendar").
5. **Output Parser / Formatter**: Ensures the final output from the LLM is strictly formatted as the JSON object required by the Python client (`speech`, `action`, `target`).
6. **HTTP Response**: Returns the formatted JSON back to the waiting Python script.

## Importing the Workflow

1. Open your n8n dashboard.
2. Click **Add Workflow**.
3. Click the menu `...` in the top right and select **Import from File**.
4. Select `n8n_starter_workflow.json`.

## Configuration Required

Out of the box, the workflow uses placeholder credentials. You **must** configure it before it will work.

1. Double-click the **LLM Node** (e.g., Chat OpenAI or Groq Chat Model).
2. Create or select a credential containing your API Key.
3. Select your desired model (e.g., `gpt-4o`, `llama3-70b`).

## How to Extend Functionality Safely

Because the Python script is a "Dumb Client", all feature extensions should happen *here* in n8n.

### Example: Adding Web Search
1. In n8n, drag a `Wikipedia` or `SerpAPI` Tool node onto the canvas.
2. Connect it to the "Tools" input of your AI Agent.
3. When you speak to the Python client asking a factual question, the Agent will automatically trigger the search tool, read the results, and formulate a spoken response. You do not need to write a single line of Python code.

### Example: Custom Local Actions
If you want the assistant to lock your computer:
1. Update the AI Agent prompt in n8n to know it can output an action called `lock_screen`.
2. When triggered, n8n sends `{"speech": "Locking now.", "action": "lock_screen", "target": null}`.
3. In `main.py`, simply add an `elif action == "lock_screen": os.system("rundll32.exe user32.dll,LockWorkStation")`.
