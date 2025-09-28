# Nova Framework Installation Structure - Summary

## What We Accomplished

✅ **Split dependencies into logical groups**:
- **Basic** (`requirements-basic.txt`): `requests`, `pyyaml`, `colorama` (~5MB)
- **LLM** (`requirements-llm.txt`): Basic + ML libraries (~1GB+)  
- **Dev** (`requirements-dev.txt`): LLM + testing/docs tools
- **All**: Everything included

✅ **Updated setup.py with extras_require**:
```python
extras_require={
    'llm': llm_requirements,           # Full functionality
    'dev': dev_requirements + llm_requirements,  # Development
    'docs': docs_requirements,         # Documentation only  
    'all': llm_requirements + dev_requirements + docs_requirements
}
```

✅ **Made dependencies optional in code**:
- `transformers` import handled gracefully in `__init__.py` files
- `sentence-transformers` dynamically imported in semantic evaluator
- LLM evaluators only created when available
- Graceful fallback to keyword-only matching

✅ **Updated installation commands**:
- `pip install nova-hunting` - Basic (keywords only, ~5MB)
- `pip install nova-hunting[llm]` - Full functionality (~1GB+)
- `pip install nova-hunting[dev]` - Development setup
- `pip install nova-hunting[all]` - Everything

✅ **Added comprehensive documentation**:
- Updated README.md with installation options
- Created INSTALLATION.md with detailed guide
- Explained what `mkdocs` is for (documentation generation)
- Created test script to verify basic installation

## What Dependencies Include

### Basic Installation (Core Requirements)
**Only for rules that use `keywords` section**

```yaml
# What works:
rule BasicRule {
    keywords:
        $malware = "malware"
        $regex_pattern = /hack(ing|er)/i
    condition:
        any of keywords.*
}
```

**Dependencies**: `requests`, `pyyaml`, `colorama`
**Size**: ~5MB
**Use case**: Lightweight threat detection, basic pattern matching

### LLM Installation (Full Functionality) 
**For rules with `keywords`, `semantics`, and `llm` sections**

```yaml
# What works:
rule AdvancedRule {
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

**Dependencies**: Basic + `sentence-transformers`, `transformers`, `openai`, `anthropic`
**Size**: ~1GB+ (includes ML models)
**Use case**: Advanced AI-powered threat detection

### Development Installation
**For contributing to Nova or building custom extensions**

**Dependencies**: LLM + `pytest`, `pytest-cov`, `mkdocs`, `mkdocs-material`
**Use case**: Development, testing, documentation generation

## Migration Path

Users can start small and upgrade:

1. **Start Basic**: Test Nova with simple keyword rules
2. **Upgrade to LLM**: Add semantic and LLM patterns 
3. **Add Development**: Contribute or customize Nova

## Graceful Degradation

✅ **Rules with missing dependencies**:
- Show clear warning messages
- Continue processing available pattern types
- Don't crash or fail completely

✅ **Example behavior**:
```bash
# Basic installation with semantic rule:
Warning: Rule requires semantic evaluation but sentence-transformers not available. 
Install with: pip install nova-hunting[llm]
# ... continues with keyword matching only
```

## Files Modified/Created

### Modified:
- `setup.py` - Added extras_require structure
- `requirements.txt` - Updated with installation guide
- `README.md` - Added installation options
- `nova/__init__.py` - Graceful transformers import
- `nova/evaluators/__init__.py` - Graceful transformers import  
- `nova/novarun.py` - Graceful transformers import
- `nova/core/matcher.py` - Optional evaluator handling

### Created:
- `requirements-basic.txt` - Core dependencies only
- `requirements-llm.txt` - Full functionality dependencies
- `requirements-dev.txt` - Development dependencies
- `INSTALLATION.md` - Detailed installation guide
- `test_basic_install.py` - Verification script

## Testing Results

✅ **Basic installation works**:
- Keywords and regex patterns function correctly
- Graceful warnings for missing semantic/LLM features
- Command-line tool (`novarun`) works as expected

✅ **LLM installation works**:
- All functionality available
- Semantic matching enabled
- LLM evaluation available (with API keys)

## Answer to Original Questions

1. **What else should we include in basic?** 
   - Just `requests`, `pyyaml`, `colorama` - that's sufficient for keyword/regex matching
   
2. **Advanced LLM installation includes transformers/openai/anthropic?**
   - ✅ Yes, plus `sentence-transformers` for semantic similarity
   
3. **Developer version includes pytest?**
   - ✅ Yes, plus `pytest-cov` and documentation tools
   
4. **What is mkdocs for?**
   - ✅ Documentation generation (static website). Only needed for docs work, not for using Nova.

The core dependencies are now much lighter (~5MB vs ~1GB+) while maintaining full backward compatibility!