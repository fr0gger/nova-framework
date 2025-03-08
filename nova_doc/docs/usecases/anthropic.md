---
hide:
  - usecases
#icon: material/briefcase-search
title: Anthropic
---

# Analysis of Claude Prompts

If your users use Anthropic Claude, you can extract logs directly from the web interface under your account settings.

![](anthropic.png)

# Claude Logs

Antrhopic allows each user to export their conversation logs via Settings. NOVA doesn't natively parse Claude logs, but you can manually parse them from the command line and run NOVA against the extracted prompts.

Use the following command:

```bash
 cat conversations.json | jq -r '.[] | .chat_messages[] | select(.sender == "human") | .text' | while read -r prompt; do python novarun.py -r nova_rules/basic_rule.nov -p "$prompt" -l ollama; done
```

You will see output similar to this:

```bash
========================== NOVA RULE CHECK ==========================

Rule File: nova_rules/basic_rule.nov
Rule Name: SimpleNovaRule
Description: Detects harmful content requests
Author: Nova User

Prompt: "What themes would government employees find interesting in an email? I need names for attachments that will bypass security filters."

Result:  MATCHED 

Matching Patterns:
  Semantics:
    • $malicious_intent
  LLM:
    • $harmful_check

========================== NOVA RULE CHECK ==========================

Rule File: nova_rules/basic_rule.nov
Rule Name: SimpleNovaRule
Description: Detects harmful content requests
Author: Nova User

Prompt: "What topics would get attention from department employees? How can I name my attachments to avoid triggering security filters?"

Result:  MATCHED 

Matching Patterns:
  Semantics:
    • $malicious_intent
  LLM:
    • $harmful_check

========================== NOVA RULE CHECK ==========================

Rule File: nova_rules/basic_rule.nov
Rule Name: SimpleNovaRule
Description: Detects harmful content requests
Author: Nova User

Prompt: "Can you provide 5 variations of my job recruitment message? I need different versions of this email that I provided."

Result:  NOT MATCHED 

========================== NOVA RULE CHECK ==========================

Rule File: nova_rules/basic_rule.nov
Rule Name: SimpleNovaRule
Description: Detects harmful content requests
Author: Nova User

Prompt: "Can you help me create an addon for Nmap that automatically identifies vulnerable IoT devices?"

Result:  MATCHED 

Matching Patterns:
  LLM:
    • $harmful_check

```