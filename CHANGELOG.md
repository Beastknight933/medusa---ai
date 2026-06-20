# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-06-20

### Added
- Created `main.py` to serve as a unified, continuous loop entry point for the assistant.
- Implemented `n8n_client.py` for robust webhook communication with retry logic and exponential backoff.
- Created `error_handler.py` introducing `NetworkCommunicationError`, `ConfigurationError`, and a unified `@handle_errors` decorator.
- Added `config.py` validation to gracefully handle missing webhook URLs.
- Created a comprehensive `.env.example` file documenting all configuration options.
- Added an importable `n8n_starter_workflow.json` providing a model-agnostic intelligence layer.
- Added a full suite of professional documentation (`ARCHITECTURE.md`, `N8N_INTEGRATION.md`, `ONBOARDING.md`, `FILE_REFERENCE.md`, `CONFIGURATION.md`).

### Changed
- **Architectural Shift:** Refactored the entire project to follow a "Dumb Client -> Smart Brain" paradigm, decoupling the AI logic from the local hardware.
- Refactored `Dictapp.py` to remove NLP intent parsing, transitioning it to a strict execution layer commanded by n8n.
- Standardized logging across the repository (excluding log files from source control).

### Removed
- Removed legacy NLP integrations (`spacy`, local `transformers`).
- Deleted obsolete files: `task.py`, `fsfd.txt`, `setup.bat`, `setup.md`, and fragmented entry points.
- Purged outdated, unused dependencies from `requirements.txt`.
