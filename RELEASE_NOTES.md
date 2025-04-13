# Nova Hunting v0.1.4 Release Notes

## Version Update
- **Updated**: Version from 0.1.3 to 0.1.4

## Bug Fixes
- **Fixed**: Warning about `clean_up_tokenization_spaces` from transformers library
- **Added**: Warning filter to suppress FutureWarning messages related to tokenization spaces
- **Modified**: Multiple files to set tokenization parameters correctly

## Previous Features (v0.1.2)

### Package Rename
- **Changed**: Package renamed from nova-framework to nova-hunting
- **Updated**: Version to 0.1.2

### Performance Optimizations
- LLM evaluator sharing across rules in NovaScanner class
- Significantly improved performance by reusing LLM evaluators
- Lazy initialization of LLM resources

### Groq Cloud Support
- New GroqEvaluator class for using Groq Cloud's ultra-fast LLM API
- Support for Groq's LLM models including llama-3.3-70b-versatile

### Bug Fixes
- Invalid regex pattern validation in the parser
- Proper error handling for malformed regex patterns

For detailed changes, see the full CHANGELOG.md file.
