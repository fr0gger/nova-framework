---
hide:
  - usecases
#icon: material/list-box-outline
title: Detecting Prompts
---

# How can you use NOVA?

NOVA was initially developed as a flexible tool for detecting and hunting prompts based on rules that define matching conditions. The goal is to identify malicious attempts, injections, or TTPs.

NOVA can detect a wide range of prompts. Some examples include:

- **Prompt Injection**: Attempts to manipulate AI models by injecting crafted inputs to override instructions or alter behavior.
- **Jailbreaking**: Exploiting AI restrictions to force responses that bypass ethical, security, or policy constraints.
- **Malicious Code Generation**: Prompts designed to generate malware, exploits, or scripts for unauthorized activities.
- **Scam or Phishing Generation**: Crafting fraudulent messages, fake emails, or social engineering content for scams.
- **Reconnaissance**: Attempts to gather intelligence, such as fingerprinting an AI’s knowledge or extracting sensitive information.
- **Bias, Toxicity, NSFW**: Prompts that elicit harmful, biased, offensive, or inappropriate content.
- **And More**: Custom rules can be created to detect other specific threats.

## How does NOVA work?

Generative AI services generate logs containing user prompts.

NOVA is particularly useful if you host your own model and want to analyze and track prompts. However, it can also work as a standalone tool on exported logs.

### Usage:

- Test a single prompt against a defined rule.
- Analyze multiple prompts with multiple rules.
- Export logs from your AI system and run them against detection rules.
- Deploy NOVA for continuous monitoring and prompt hunting on your database.

