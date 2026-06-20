# Configuration Documentation

Medusa AI uses a layered configuration system. Settings can be defined in environment variables, a local `config.json` file, or fallback to sensible defaults.

## Configuration Resolution Order
1. **Environment Variables** (Highest priority)
2. **`config.json` file**
3. **Default values in `config.py`** (Lowest priority)

## Setting Up Environment Variables

Copy `.env.example` to `.env` in the root directory.

```bash
cp .env.example .env
```

## Available Settings

### Core Settings

| Variable | Default Value | Required? | Description |
| :--- | :--- | :--- | :--- |
| `N8N_WEBHOOK_URL` | `http://localhost:5678/webhook/assistant` | **YES** | The absolute URL of your n8n workflow's webhook trigger. If this is missing, the application will refuse to start. |
| `ASSISTANT_NAME` | `Ashley` | No | The name the assistant refers to itself as. Sent to n8n as context. |

### Speech-to-Text (STT) Settings

| Variable | Default Value | Required? | Description |
| :--- | :--- | :--- | :--- |
| `STT_LANGUAGE` | `en-US` | No | BCP-47 language tag for speech recognition. |
| `STT_TIMEOUT` | `8` | No | Maximum seconds to wait for speech to begin. |
| `STT_PHRASE_TIME_LIMIT` | `3` | No | Maximum seconds a phrase can last before processing. |
| `STT_ENERGY_THRESHOLD` | `300` | No | Audio level threshold for silence detection. |

### Text-to-Speech (TTS) Settings

| Variable | Default Value | Required? | Description |
| :--- | :--- | :--- | :--- |
| `TTS_VOICE` | `en-US-MichelleNeural` | No | Microsoft Edge TTS voice identifier. |
| `TTS_RATE` | `medium` | No | Speed of speech (`slow`, `medium`, `fast`). |
| `TTS_VOLUME` | `1.0` | No | Volume multiplier (0.0 to 1.0). |

### System Settings

| Variable | Default Value | Required? | Description |
| :--- | :--- | :--- | :--- |
| `LOG_LEVEL` | `INFO` | No | Defines console and file logging verbosity (`DEBUG`, `INFO`, `WARNING`, `ERROR`). |
| `LOG_FILE` | `assistant.log` | No | Path to the runtime log file. Excluded from version control. |

## Validation

When `main.py` is executed, `config.validate()` is automatically called. 
- If `N8N_WEBHOOK_URL` is completely missing, a `ConfigurationError` is raised and the app crashes intentionally to inform the user.
- If it is set to the `localhost` default, a warning is logged to remind the user to verify their n8n setup.
