"""
NOVA: The Prompt Pattern Matching
Author: Thomas Roccia 
twitter: @fr0gger_
License: MIT License
Version: 1.0.0
Description: Main Nova framework package initialization
"""

__version__ = "1.0.0"

# Set the clean_up_tokenization_spaces parameter globally to avoid FutureWarning
import warnings
try:
    import transformers
    # Suppress the FutureWarning about clean_up_tokenization_spaces
    if hasattr(transformers, 'tokenization_utils_base'):
        transformers.tokenization_utils_base.CLEAN_UP_TOKENIZATION_SPACES = True
    # Also set the parameter in the PreTrainedTokenizerBase class
    if hasattr(transformers, 'PreTrainedTokenizerBase'):
        transformers.PreTrainedTokenizerBase.clean_up_tokenization_spaces = True
except ImportError:
    # Transformers not available - that's OK for basic keyword matching
    pass

from nova.core.rules import (
    KeywordPattern,
    SemanticPattern,
    LLMPattern,
    NovaRule
)
from nova.core.matcher import NovaMatcher
from nova.core.parser import NovaParser

__all__ = [
    'KeywordPattern',
    'SemanticPattern',
    'LLMPattern',
    'NovaRule',
    'NovaMatcher',
    'NovaParser',
]