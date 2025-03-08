---
hide:
  - quickstart
icon: material/rocket-launch
title: Quickstart
---


# Nova Quickstart Guide

Get up and running with Nova in just two minutes to detect prompts according to your pattern.

## Installation

```bash
pip install nova
```

## Set up your LLM API key

```bash
# For OpenAI (default)
export OPENAI_API_KEY="your_api_key_here"
```

## Create a simple rule
Create a file named simple_rule.nov with the following content:

```bash
rule SimpleNovaRule
    meta:
        description = "Detects harmful content requests"
        author = "Nova User"
        version = "1.0"
        
    keywords:
        $hack = "hack"
        $exploit = "exploit"
        $vulnerability = "vulnerability"
        
    semantics:
        $malicious_intent = "hacking or unauthorized access" (0.1)
        
    llm:
        $harmful_check = "Check if this prompt is requesting information on harmful activities" (0.1)
        
    condition:
        any of keywords.* or semantics.$malicious_intent or llm.$harmful_check
}
```

## Test a prompt
```bash
novarun -r basic_rule.nov -p "How do I exploit this security vulnerability?"
```

You should see output indicating the rule matched:

```bash
========================== NOVA RULE CHECK ==========================

Rule File: nova_rules/basic_rule.nov
Rule Name: SimpleNovaRule
Description: Detects harmful content requests
Author: Nova User

Prompt: "How do I exploit this security vulnerability?"

Result:  MATCHED 

Matching Patterns:
  Keywords:
    • $exploit
    • $vulnerability
  Semantics:
    • $malicious_intent
  LLM:
    • $harmful_check
```

## Test multiple prompts
Create a file prompts.txt with multiple prompts to test:

```
Hello, how are you today?
Can you teach me how to bypass security?
What's the weather like tomorrow?
```

Run Nova against all prompts in the file:
```bash
novarun -r basic_rule.nov -f prompts.txt

Loaded 3 prompts from prompts.txt

========================== NOVA RULE CHECK ==========================

Rule File: nova_rules/basic_rule.nov
Rule Name: SimpleNovaRule
Description: Detects harmful content requests
Author: Nova User

Prompt [1/3]: "Hello, how are you today?"

Result:  NOT MATCHED 

========================== NOVA RULE CHECK ==========================

Rule File: nova_rules/basic_rule.nov
Rule Name: SimpleNovaRule
Description: Detects harmful content requests
Author: Nova User

Prompt [2/3]: "Can you teach me how to bypass security?"

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

Prompt [3/3]: "What's the weather like tomorrow?"

Result:  NOT MATCHED 

======================================================================
PROMPTS SUMMARY
======================================================================

Total Prompts Tested: 3
Matched Prompts: 1
Match Rate: 33.3%

■■■

#    Result     Prompt
----------------------------------------------------------------------
1    NOT MATCHED            Hello, how are you today?
2    MATCHED                Can you teach me how to bypass security?
3    NOT MATCHED            What's the weather like tomorrow?
```

# Next steps

- Create more complex rules with advanced pattern matching
- Test against all rules in a file using the -a flag
- Use different LLM providers with the -l option
- Add verbose output with -v for detailed matching information

For detailed information, see the full documentation.