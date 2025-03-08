---
hide:
  - usecases
#icon: material/briefcase-search
title: Ollama
---

# Analysis prompts from Ollama

Ollama is an open source tool that allows you to load and host multiple open source models. You can host your own ollama server and add the models you want. Ollama server listen by default on localhost: 

But you can configure your server as you want. 

# Ollama logs

By default ollama store the prompt history in the file  '~/.ollama/history'. This is file is a text file containing one prompt per lines.

You can run Nova against this file using the following command:

```bash
python novarun.py -r nova_rules/testrule.nov -f ~/.ollama/history
```

