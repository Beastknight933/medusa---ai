# File Reference

This document outlines the responsibility and interactions of every major Python file in the repository.

## `main.py`
**Purpose**: The central orchestrator.
**Responsibilities**:
- Initializes configuration and logging.
- Instantiates the `N8nClient`.
- Runs the infinite `assistant_loop()`.
- Routes audio input to STT, text to n8n, n8n response to TTS, and n8n actions to `Dictapp.py`.
- Catches critical exceptions to prevent hard crashes.

## `n8n_client.py`
**Purpose**: The network communication layer.
**Responsibilities**:
- Builds the JSON payload (text + system context).
- Sends `POST` requests to the configured n8n Webhook.
- Uses `@retry` from `error_handler.py` to handle network blips.
- Parses the n8n response and ensures it matches the expected contract.

## `stt.py`
**Purpose**: The ears of the assistant.
**Responsibilities**:
- Connects to the default system microphone.
- Calibrates energy thresholds for ambient noise.
- Converts audio to text using `speech_recognition`.

## `tts.py`
**Purpose**: The mouth of the assistant.
**Responsibilities**:
- Uses `edge-tts` CLI via `subprocess` to generate `.mp3` files from text.
- Initializes `pygame.mixer` for audio playback.
- Manages temporary file cleanup to prevent disk bloat.

## `Dictapp.py`
**Purpose**: The hands of the assistant.
**Responsibilities**:
- Provides `openappweb(target)` and `closeappweb(target)` functions.
- Maps common application names (like "vscode") to executable names (like "code").
- Executes `os.system()` commands to start or taskkill applications.
- Opens web browsers if the target is a URL.

## `config.py`
**Purpose**: Centralized configuration management.
**Responsibilities**:
- Loads default configurations.
- Overrides defaults with values from `config.json` (if present) or environment variables.
- Provides a `validate()` method to ensure required values (like `N8N_WEBHOOK_URL`) are present before startup.

## `error_handler.py`
**Purpose**: Unified exception management.
**Responsibilities**:
- Defines custom exceptions (`NetworkCommunicationError`, `ConfigurationError`).
- Provides the `@retry` decorator for network resilience.
- Provides the `@handle_errors` decorator used by `main.py` to ensure the continuous loop never crashes due to a random exception.
