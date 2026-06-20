# Developer Onboarding Guide

Welcome to the Medusa AI project. This guide will take you from `git clone` to a fully functioning J.A.R.V.I.S. style voice assistant.

## Prerequisites

Before starting, ensure you have the following installed:
1. **Python 3.10+**
2. **n8n** (Running locally via npm/Docker, or a Cloud instance)
3. A working microphone and speakers

## Step 1: Clone and Setup Python

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/medusa---ai.git
   cd medusa---ai
   ```

2. Create a virtual environment (Recommended):
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Step 2: Configure Environment

Copy the example configuration file to create your local environment settings:

```bash
cp .env.example .env
```

Open `.env` and verify the `N8N_WEBHOOK_URL`. If you are running n8n locally on its default port, you likely will not need to change this.

## Step 3: Setup n8n (The Brain)

Medusa AI requires n8n to process logic.

1. Open your n8n instance.
2. Go to **Workflows** -> **Import from File**.
3. Select `n8n_starter_workflow.json` from the root of this repository.
4. Open the workflow and configure the LLM node. You will need to provide an API key for your preferred provider (OpenAI, Groq, Anthropic, etc.).
5. Click **Execute Workflow** (to put it in listening mode) or **Activate** it.

*For more details on extending the workflow, see [WORKFLOW.md](WORKFLOW.md).*

## Step 4: Run the Assistant

Start the local Python client:

```bash
python main.py
```

1. You should see logs indicating the microphone is calibrating.
2. The assistant will announce it is online.
3. Speak clearly into your microphone (e.g., "Hello, who are you?").
4. The terminal will log that it heard your voice, send it to n8n, and play the response audio back to you!

## Extending the System

To safely add new functionality:
- **Do not edit `stt.py` or `tts.py`**. They are robust, isolated I/O wrappers.
- **Do not add API keys to Python**.
- **To add a new capability** (like checking the weather), open n8n, add an HTTP node to fetch the weather, and route it to your LLM. The Python script will automatically understand the response.
- **To add a new local desktop action**, add it to the n8n logic, output a unique `action` string in the JSON, and map that string to Python code inside `execute_local_action()` in `main.py`.
