---
hide:
  - quickstart
icon: material/cog-outline
title: Installation
---

# Installing Nova

Nova is a prompt pattern matching framework designed to detect potentially harmful or problematic prompts for Large Language Models (LLMs). This guide explains how to install and configure Nova.

## Installation

Nova is available as a Python package via pip. It works with Python 3.8 and above.

### Quick Installation

```bash
pip install nova
```

This command will install Nova and its dependencies, including the novarun command-line tool which will be automatically added to your path.

### Development Installation
For development or to get the latest version, you can install directly from GitHub:

```
pip install git+https://github.com/fr0gger/nova.git
```

# Configuration
Nova requires API keys for the LLM providers you want to use. You can set these keys as environment variables:

## Setting API Keys
### OpenAI (Default)

```
# For OpenAI models (GPT-4, GPT-3.5, etc.)
export OPENAI_API_KEY="your_openai_api_key_here"
```
### Anthropic

```
# For Anthropic models (Claude, etc.)
export ANTHROPIC_API_KEY="your_anthropic_api_key_here"
```

### Azure OpenAI
```
# For Azure OpenAI Service
export AZURE_OPENAI_API_KEY="your_azure_api_key_here"
export AZURE_OPENAI_ENDPOINT="your_azure_endpoint_here"
```

### Ollama (Local Models)
For Ollama, no API key is needed as it runs locally, but you need to have Ollama installed and running:
```
# Optional: If Ollama is running on a different host or port
export OLLAMA_HOST="http://localhost:11434"
```
## Configuration File
Nova also supports loading configuration from a YAML file. Create a file named nova_config.yaml:

```yaml
# nova_config.yaml
llm:
  default: openai  # Default LLM provider
  openai:
    api_key: your_openai_api_key  # Overrides environment variable
    model: gpt-4o  # Default model to use
  anthropic:
    api_key: your_anthropic_api_key
    model: claude-3-sonnet-20240229
  azure:
    api_key: your_azure_api_key
    endpoint: your_azure_endpoint
    deployment_name: gpt-35-turbo
    api_version: 2023-05-15
  ollama:
    host: http://localhost:11434
    model: llama3
```

To use this configuration file with the Nova runner:
```
novarun -r rules.nov -p "prompt" -c nova_config.yaml
```

# Troubleshooting
## Common Installation Issues

1. Missing command-line tool: If the novarun command is not found, ensure that your Python binary directory is in your PATH. You can also run python -m nova.novarun as an alternative.
2. Dependency conflicts: If you encounter dependency conflicts, consider using a virtual environment:
```
python -m venv nova-env
source nova-env/bin/activate  # On Windows: nova-env\\Scripts\\activate
pip install nova
```

## LLM Connection Issues

1. API key errors: Ensure your API keys are correctly set in your environment variables or configuration file.
2. Ollama connection errors: If using Ollama, make sure the Ollama service is running and accessible.
3. Network issues: Check your internet connection and firewall settings if you're having trouble connecting to external LLM providers.

# Uninstallation
To remove Nova:
```
pip uninstall nova
```

# Next Steps
Once you have Nova installed, you can proceed to:

- Creating Rules: Learn how to write detection rules
- Running Nova: Start checking prompts against your rules