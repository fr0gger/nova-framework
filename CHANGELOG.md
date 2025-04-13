# NOVA Framework Changelog

## [1.1.0] - 2025-04-13

### Performance Optimizations

#### LLM Evaluator Optimization
- **Added**: LLM evaluator sharing across rules in `NovaScanner` class
- **Fixed**: Excessive creation of LLM evaluators when processing multiple rules
- **Improved**: Performance by creating only one LLM evaluator per scanning session
- **Added**: Lazy initialization of LLM evaluator only when rules need it
- **Improved**: Resource utilization by reusing API connections across rules

#### Groq Cloud Support
- **Added**: New `GroqEvaluator` class for using Groq Cloud's ultra-fast LLM API
- **Added**: Support for Groq's LLM models including llama-3.3-70b-versatile
- **Added**: Groq-specific temperature handling (0 gets converted to 1e-8)
- **Updated**: `get_validated_evaluator()` to accept 'groq' as a valid LLM type
- **Improved**: Documentation for setting up and using Groq Cloud with NOVA

#### Code Changes
- **Modified**: `scanner.py` to maintain a single shared LLM evaluator
- **Added**: `_initialize_evaluators()` method to analyze rules before creating resources
- **Added**: `_rule_needs_llm()` helper method to determine if a rule needs LLM evaluation
- **Improved**: `_create_matcher()` method to pass shared evaluators to matchers
- **Modified**: `clear_rules()` method to also clear shared evaluators
- **Updated**: `novarun.py` command-line tool to use the optimized approach
- **Updated**: `test.py` to create a single matcher instance and reuse it for multiple rules
- **Removed**: Separate `OptimizedScanner` implementation in favor of core integration

#### Bug Fixes
- **Fixed**: Invalid regex pattern validation in the parser
- **Added**: Proper error handling for malformed regex patterns

### Profiling Results
- Identified that ~95% of execution time was spent in network operations
- LLM API calls were accounting for ~93% of total execution time
- The optimization significantly reduces this overhead by reusing connections

### Documentation
- Added detailed comments explaining the LLM evaluator optimization approach
- Created test file demonstrating proper usage of the optimization
- Added documentation for using Groq Cloud with NOVA framework

### Removed
- `optimized_scanner.py` - Functionality now integrated into core `NovaScanner`
- `optimized_matcher.py` - No longer needed with core optimization
- `optimized_test.py` - Replaced by integrated test in test directory
- `test_optimized_scanner.py` - Replaced by `test_scanner_optimization.py`

### Migration Notes
- Existing code using `NovaScanner` will automatically benefit from this optimization
- No API changes required - the optimization is transparent to users
- Performance will be significantly improved for workloads with multiple rules using LLM evaluation
- To use Groq Cloud, set the `GROQ_API_KEY` environment variable and specify `llm_type="groq"` when creating evaluators