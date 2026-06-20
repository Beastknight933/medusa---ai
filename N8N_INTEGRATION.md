# n8n Integration Contract

This document defines the communication contract between the Medusa AI Python client and your n8n workflows.

## Webhook Endpoint

By default, the Python client will make a POST request to:
`http://localhost:5678/webhook/assistant`

*(This is configurable via `N8N_WEBHOOK_URL`)*

## The Request Format

When you speak, the Python client transcribes your voice and sends the following JSON payload to the webhook:

```json
{
  "text": "The exact transcribed string of what you said",
  "context": {
    "timestamp": "2026-06-20T12:00:00.000000",
    "system": "Windows",
    "assistant_name": "J.A.R.V.I.S."
  }
}
```

### Request Behavior
- **Method**: POST
- **Timeout**: The client enforces a 15-second timeout to prevent indefinite hanging. Ensure your n8n workflow resolves within this window.
- **Authentication**: Currently, no default authentication headers are sent, but `n8n_client.py` can be easily modified to include bearer tokens if your webhook requires them.

## The Response Format

Your n8n workflow **MUST** respond with an HTTP node formatted as JSON. The Python client explicitly expects three keys:

```json
{
  "speech": "Text for the local TTS engine to speak aloud",
  "action": "open_app", 
  "target": "chrome"
}
```

### Response Fields Detailed

| Field | Type | Description | Required |
| :--- | :--- | :--- | :--- |
| `speech` | String | What the assistant should say. | Yes (can be an empty string) |
| `action` | String / Null | The local OS action to perform. Valid options are `"open_app"` or `"close_app"`. | No (Use `null` if no action is needed) |
| `target` | String / Null | The application to target (e.g. `"chrome"`, `"vscode"`, `"notepad"`). | No (Use `null` if no action is needed) |

### Example 1: Simple Conversation
**Request**: `{"text": "Hello, how are you?"}`
**Response**:
```json
{
  "speech": "I am functioning perfectly, sir.",
  "action": null,
  "target": null
}
```

### Example 2: Action Trigger
**Request**: `{"text": "Please open Spotify."}`
**Response**:
```json
{
  "speech": "Opening Spotify now.",
  "action": "open_app",
  "target": "spotify"
}
```

## Error Handling

If n8n is offline, returns a 500 error, or times out, the Python client will retry up to 3 times (with exponential backoff). If it still fails, it will raise a `NetworkCommunicationError`, catch it, and audibly inform you that the connection is down, preventing the application from crashing.
