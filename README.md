# Medusa AI Assistant

![Version](https://img.shields.io/badge/version-1.0.0-blue)

A professional, lightweight, voice-activated AI assistant architecture that operates as a sensory client for an external n8n intelligence layer.

## Project Overview

Medusa AI was completely refactored to decouple the heavy processing (NLP, LLM interactions) from the local hardware. By adopting a "Dumb Client -> Smart Brain" paradigm (similar to the J.A.R.V.I.S. architecture), the local Python application serves purely as the eyes, ears, and hands, while an n8n webhook workflow handles the actual thinking.

## Core Features

- **Decoupled Architecture**: Voice processing and actions run locally; reasoning runs on n8n.
- **Provider-Agnostic Intelligence**: Since n8n is the orchestrator, you can plug in any LLM (OpenAI, Groq, Anthropic, Ollama) without changing a single line of Python code.
- **Local App Control**: Can dynamically open and close desktop applications based on commands received from n8n.
- **Fast Execution**: Removed heavy local NLP models (like spaCy and Transformers) for near-instant execution times.
- **Robust Error Handling**: Built-in retry decorators and unified exception management ensure network blips do not crash the assistant.

## Technology Stack

- **Python 3.10+** (Core Client)
- **SpeechRecognition** (Microphone Input / STT)
- **Edge-TTS** (Text-to-Speech Output)
- **Pygame** (Audio Playback)
- **Requests** (HTTP Webhook Communication)
- **n8n** (Orchestration & LLM Integration)

## Repository Structure

```text
medusa---ai/
├── main.py              # The entry point and main continuous loop
├── n8n_client.py        # Handles webhook communication with retry logic
├── Dictapp.py           # Executes local OS actions (open/close apps)
├── stt.py               # Handles microphone listening and Speech-to-Text
├── tts.py               # Handles Text-to-Speech generation and playback
├── config.py            # Centralized configuration and validation
├── error_handler.py     # Unified error handling and retry decorators
├── requirements.txt     # Python dependencies
├── .env.example         # Template for environment variables
└── docs/                # Comprehensive architectural documentation
```

## Quick Start & Installation

To get started quickly, please refer to the [ONBOARDING.md](ONBOARDING.md) guide for a step-by-step tutorial on installing the Python client and importing the n8n starter workflow.

## Documentation Reference

- **[ARCHITECTURE.md](ARCHITECTURE.md)**: Deep dive into the data flow and system design.
- **[N8N_INTEGRATION.md](N8N_INTEGRATION.md)**: The developer contract defining the exact JSON structures required.
- **[FILE_REFERENCE.md](FILE_REFERENCE.md)**: A module-by-module breakdown of the Python codebase.
- **[CONFIGURATION.md](CONFIGURATION.md)**: Documentation of all available environment variables.
- **[WORKFLOW.md](WORKFLOW.md)**: Explanation of the provided n8n starter workflow.
