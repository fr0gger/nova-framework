---
hide:
  - home
icon: material/pyramid
title: Why Nova
---

# Why I Created NOVA  

Generative AI systems are being deployed everywhere, powering chatbots, automating tasks, and handling sensitive data. But with this rapid adoption comes an increased attack surface.  

## The Problem: Malicious Prompting is a Real Threat  
LLMs don’t operate like traditional software. Their vulnerabilities are **text-based** and can be exploited in ways security teams aren’t used to handling.  

- **Jailbreaking attempts** bypass safety mechanisms to generate harmful content.  
- **Data leakage risks** expose sensitive or proprietary information.  
- **Prompt injections** manipulate LLMs into executing unintended actions.  
- **Adversarial prompts** trick models into producing misleading or malicious outputs.  

Many security teams still rely on **manual review** or basic regex-based detection, which isn’t enough. Traditional security tools weren’t designed for **text-based AI threats**.  

## The Challenge: How Do You Detect Malicious Prompts?  

Malicious abuse of generative AI systems is inevitable. Some tools exist to prevent harmful content generation (often called guardrails), but they are not designed for **prompt hunting**.  

**NOVA fills this gap** by providing a **rule-based detection tool**, similar to **YARA**, but built specifically for **prompt matching**.  


## Why NOVA Uses a YARA-Like Structure  

YARA is the go-to tool for malware hunting, and it provides a **rule-based approach** to identifying malicious code. The reason it works so well is its **simplicity, flexibility, and pattern-matching power**. I wanted **NOVA Rules** to bring that same structured approach—but for **prompt-based threats** in AI systems.  

### Why Not Just Use YARA?  
YARA is built for **binary and text pattern matching** in files. But detecting **malicious prompts** requires different techniques:  

- **LLM prompts are dynamic**—attackers rephrase, manipulate, and obfuscate text-based threats in ways that traditional pattern matching struggles to catch.  
- **Context matters**—some prompts are only malicious in certain scenarios, requiring **semantic analysis** beyond just keyword matching.  
- **Traditional signatures are not enough**—simple rules can miss subtle manipulations, requiring a more adaptive approach.  


### NOVA’s Structure: Inspired by YARA, but Optimized for AI Prompts  
Instead of reinventing the wheel, NOVA adopts a **YARA-like rule structure** while adapting it to the unique challenges of **prompt security**:  

- **Human-readable rules** → Security teams can easily write, share, and modify detection logic.  
- **Pattern matching and AI-based detection** → Goes beyond simple regex by integrating **semantic similarity checks** and **LLM-assisted analysis** but regex ans strict keyword maching is also available.  

NOVA Rules bridge the gap between **traditional security tools** and the **new reality of LLM threats**, it gives defenders a familiar yet powerful way to **hunt, analyze, and counter malicious prompting techniques**.

 
## NOVA Rules The First Tool for Prompt Hunting  
Until now, **no dedicated tool existed** for **hunting malicious prompts**. Security teams had to rely on manual inspection, or generic AI safeguards.  
**NOVA Rules is the first of its kind**—a **structured detection system** designed specifically for **tracking, analyzing, and identifying prompt-based threats.**  

NOVA Rules combines multiple techniques for **prompt pattern matching**:  

- **Keyword Detection** → Finds specific terms or patterns using regex.  
- **Semantic Similarity** → Detects variations of attack patterns even when the wording changes.  
- **LLM Matching** → Uses AI-driven evaluation to identify threats beyond simple keyword filtering.  

If attackers are using **AI to enhance their tactics**, defenders need **AI-driven tools** to detect and counter them. **NOVA Rules is my attempt to fill that gap**, and to provide a structured, scalable way to detect **prompt-based threats** and give security teams an edge in defending AI systems.  
