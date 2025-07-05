# 🚧 WORK IN PROGRESS -- PLEASE COME BACK LATER 🚧

# 🔥 Darkmailr - Ethical Social Engineering Engine

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Ollama](https://img.shields.io/badge/Ollama-Compatible-green.svg)](https://ollama.com/)

**Darkmailr** is a self-hosted, offline phishing simulation tool that uses open-source LLMs (via Ollama) to generate realistic, context-aware phishing emails for red team exercises, security awareness training, and prompt injection testing.

## 🚀 Quick Start

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama service
ollama serve &

# Download a model
ollama run mistral

# Clone and run Darkmailr
git clone https://github.com/darkmailr/darkmailr.git
cd darkmailr
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
Access at: http://localhost:5000
📸 Screenshots
Main Interface
🎯 Features

✅ Offline Operation - No data leaves your network
✅ LAN Accessible - Use from any device on your network
✅ Open Source LLMs - Powered by Ollama (Mistral, Llama, etc.)
✅ Context-Aware - Generates realistic, targeted phishing emails
✅ Export Functionality - Save results for training purposes
✅ Easy Setup - Single command installation

🛠️ Installation
Prerequisites

Ubuntu 18.04+ (or similar Linux distribution)
Python 3.9+
4GB+ RAM (for LLM models)
Network access for initial setup

Step-by-Step Installation

Install Ollama


## Project Maintainer
- [january1073](https://linktr.ee/january1073)

---

Contributions welcome! Star the repo if you find it useful:  
**https://github.com/darkmailr**
