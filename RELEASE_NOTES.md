# Nova Hunting v0.1.2 Release Notes

## Package Rename
- **Changed**: Package renamed from nova-framework to nova-hunting
- **Updated**: Version to 0.1.2

## Major Features

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
