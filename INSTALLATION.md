# Nova Installation Guide

Nova Framework offers flexible installation options to match your specific needs and minimize dependencies.

## Installation Options

### 1. Basic Installation (`nova-hunting`)
**Best for**: Simple keyword and regex pattern matching
**Size**: ~5MB
**Dependencies**: `requests`, `pyyaml`, `colorama`

```bash
pip install nova-hunting
```

**What's included:**
- ✅ Keyword pattern matching (exact text, case-sensitive/insensitive)
- ✅ Regex pattern matching with full regex support
- ✅ Rule parsing and condition evaluation
- ✅ Command-line tool (`novarun`)
- ❌ Semantic similarity matching
- ❌ LLM-based evaluation

**Use cases:**
- Basic threat detection with known attack keywords
- Regex-based pattern matching
- Lightweight deployments
- Getting started with Nova

### 2. LLM Installation (`nova-hunting[llm]`)
**Best for**: Full Nova functionality including AI-powered matching
**Size**: ~1GB+ (includes ML models)
**Dependencies**: Basic + `sentence-transformers`, `transformers`, `openai`, `anthropic`

```bash
pip install nova-hunting[llm]
```

**What's included:**
- ✅ Everything from Basic installation
- ✅ Semantic similarity matching using sentence transformers
- ✅ LLM-based evaluation (OpenAI, Anthropic, Azure, Ollama, Groq)
- ✅ Advanced pattern detection using AI

**Use cases:**
- Advanced threat detection
- Semantic analysis of prompts
- LLM-powered pattern matching
- Production deployments requiring full functionality

### 3. Development Installation (`nova-hunting[dev]`)
**Best for**: Contributing to Nova or extending its functionality
**Size**: ~1GB+ (includes everything)
**Dependencies**: LLM + `pytest`, `pytest-cov`, `mkdocs`, `mkdocs-material`

```bash
pip install nova-hunting[dev]
```

**What's included:**
- ✅ Everything from LLM installation
- ✅ Testing framework (pytest)
- ✅ Documentation tools (MkDocs)
- ✅ Development utilities

### 4. Full Installation (`nova-hunting[all]`)
**Best for**: Complete Nova installation with all optional features
```bash
pip install nova-hunting[all]
```

## Feature Comparison

| Feature | Basic | LLM | Dev | All |
|---------|-------|-----|-----|-----|
| Keyword Matching | ✅ | ✅ | ✅ | ✅ |
| Regex Patterns | ✅ | ✅ | ✅ | ✅ |
| Semantic Similarity | ❌ | ✅ | ✅ | ✅ |
| LLM Evaluation | ❌ | ✅ | ✅ | ✅ |
| Testing Tools | ❌ | ❌ | ✅ | ✅ |
| Documentation | ❌ | ❌ | ✅ | ✅ |

## Rule Compatibility

### Basic Installation
Only supports rules with `keywords` section:

```yaml
rule BasicRule
{
    keywords:
        $malware = "malware"
        $phishing = /phish(ing|er)/i
    
    condition:
        any of keywords.*
}
```

### LLM Installation  
Supports all rule types:

```yaml
rule AdvancedRule
{
    keywords:
        $suspicious = "suspicious"
    
    semantics:
        $threat = "threatening behavior" (0.7)
    
    llm:
        $analysis = "Analyze if this is malicious" (0.8)
    
    condition:
        keywords.$suspicious and (semantics.$threat or llm.$analysis)
}
```

## Graceful Degradation

Nova is designed to handle missing dependencies gracefully:

- Rules requiring semantic matching will show warnings but still process keyword patterns
- Rules requiring LLM evaluation will show warnings but still process other pattern types
- The system continues to function with available capabilities

## Migration Path

You can start with basic installation and upgrade as needed:

1. **Start Basic**: Test Nova with keyword-only rules
2. **Upgrade to LLM**: Add semantic and LLM patterns to existing rules
3. **Add Development**: Contribute or customize Nova

```bash
# Start basic
pip install nova-hunting

# Upgrade to full functionality
pip install nova-hunting[llm]

# Add development tools
pip install nova-hunting[dev]
```

## Dependencies Explained

### What is `mkdocs` for?
`mkdocs` and `mkdocs-material` are used to generate the Nova documentation website. They're only needed if you want to:
- Build documentation locally
- Contribute to Nova documentation
- Create custom documentation for your rules

You can safely ignore these unless you're doing documentation work.

### Why are ML dependencies so large?
The `sentence-transformers` and `transformers` libraries include:
- Pre-trained language models for semantic similarity
- Tokenization libraries for text processing
- Neural network frameworks (PyTorch)

These enable Nova's AI-powered features but add significant size to the installation.