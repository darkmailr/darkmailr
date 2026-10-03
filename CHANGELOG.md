# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-10-03

### Added
- Model selector: new "Model" section (05) in the form, populated live from
  the local Ollama instance (`get_available_models()` queries `/api/tags`)
  instead of a hardcoded `mistral`
- Sticky form state: submitted values (sender, receiver, topic, vectors,
  model) are echoed back into the form after generation or an error, instead
  of resetting
- Reset button above the Sender section to clear the form on demand
- Copy button on the generated email, with a fallback for browsers/contexts
  where `navigator.clipboard` is unavailable (e.g. plain HTTP on a LAN IP)
- Favicon and apple-touch-icon
- Separate "First name" / "Family name" fields for both Sender and Receiver
- Footer credit link

### Changed
- Full visual redesign: replaced the pink/black neon "hacker" theme with a
  professional black-and-white design matching the new darkmailr logo
- Section headers relabelled: "Sender Information" → "Sender (impersonated)",
  "Receiver Information" → "Receiver (target)", with numbered sections (01–05)
- Prompt rebuilt with a single, explicit output format and an instruction to
  generate the email exactly once, to stop some models from producing two
  drafts (header-less + headered) in one response
- Prompt now frames the request as an authorized internal red-team /
  security-awareness exercise
- Logo switched from `static/logo.jpg` to `static/darkmailr_logo.png`
- Enter key in any form field no longer implicitly submits the form — only
  an explicit click on "Generate phishing email" does
- Flask dev server now runs with `threaded=True` so one slow/stuck request
  can't block subsequent ones

### Fixed
- Request to Ollama had no timeout and could hang indefinitely; added a
  configurable `GENERATE_TIMEOUT` (180s) with a clear on-screen error instead
- Reasoning-model output (e.g. qwen3) could include raw `<think>...</think>`
  traces in the generated email; these are now stripped
- Generate button gave no feedback and could be double-clicked; it now
  disables itself and shows "Generating…" while a request is in flight

### Removed
- "⚠️ WARNING: ETHICAL USE ONLY ⚠️" banner

## [1.0.0] - 2025-07-06

### Added
- Basic Flask web application with HTML templating
- Ollama integration for local LLM-powered email generation
- LAN-accessible web UI for phishing simulation
- Email persistence to local file system
- Debian server deployment
- Ethical usage guidelines and documentation

### Security
- Offline-only operation for air-gapped security testing
- No external API dependencies or data transmission

## [0.1.0] - 2025-07-06

### Added
- Initial project structure and documentation
- Basic Ollama setup instructions
- Flask application skeleton
