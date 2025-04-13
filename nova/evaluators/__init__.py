"""
NOVA: The Prompt Pattern Matching
Author: Thomas Roccia 
twitter: @fr0gger_
License: MIT License
Version: 1.0.0
Description: Evaluator module initialization
"""

# Set the clean_up_tokenization_spaces parameter globally to avoid FutureWarning
import warnings
try:
    import transformers
    # Suppress the FutureWarning about clean_up_tokenization_spaces
    from transformers import tokenization_utils_base
    tokenization_utils_base.CLEAN_UP_TOKENIZATION_SPACES = True
    # Also set the parameter in the PreTrainedTokenizerBase class
    if hasattr(transformers, 'PreTrainedTokenizerBase'):
        transformers.PreTrainedTokenizerBase.clean_up_tokenization_spaces = True
except ImportError:
    warnings.warn("Transformers library not found. Some features may not be available.")

from nova.evaluators.base import BaseEvaluator, KeywordEvaluator, SemanticEvaluator, LLMEvaluator
from nova.evaluators.keywords import DefaultKeywordEvaluator
from nova.evaluators.semantics import DefaultSemanticEvaluator
from nova.evaluators.llm import OpenAIEvaluator
from nova.evaluators.condition import evaluate_condition

__all__ = [
    'BaseEvaluator',
    'KeywordEvaluator',
    'SemanticEvaluator',
    'LLMEvaluator',
    'DefaultKeywordEvaluator',
    'DefaultSemanticEvaluator',
    'OpenAIEvaluator',
    'evaluate_condition',
]