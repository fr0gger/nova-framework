"""
NOVA: The Prompt Pattern Matching
Author: Thomas Roccia
twitter: @fr0gger_
License: MIT License
Version: 1.0.0
Description: Semantic pattern evaluator implementations
"""

from typing import Dict, Tuple, Optional, Union
import os
from nova.core.rules import SemanticPattern
from nova.evaluators.base import SemanticEvaluator
from nova.utils.logger import get_logger

# Get logger for this module
logger = get_logger("nova.evaluators.semantics")

# Global model cache to prevent reloading models
_MODEL_CACHE = {}
_EMBEDDING_CACHE = {}
_TEXT_EMBEDDING_CACHE = {}  # Cache for text embeddings to avoid re-encoding the same text

class DefaultSemanticEvaluator(SemanticEvaluator):
    """
    Default semantic evaluator using sentence transformers.
    Performs semantic similarity matching between patterns and text.
    """
    
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):  
        """
        Initialize the semantic evaluator with a sentence transformer model.
        
        Args:
            model_name: Name of the sentence transformer model to use
        """
        self.model_name = model_name
        self.model = None
        # Use the global embedding cache instead of instance-specific cache
        
        # Lazy load the model on first use
        self._load_model()
    
    def _load_model(self) -> bool:
        """
        Load the sentence transformer model from global cache if available.
        
        Returns:
            Boolean indicating whether the model was successfully loaded
        """
        global _MODEL_CACHE
        
        # If model already loaded on this instance, return it
        if self.model is not None:
            return True
        
        # Check if model exists in global cache
        if self.model_name in _MODEL_CACHE:
            self.model = _MODEL_CACHE[self.model_name]
            return True
            
        try:
            # Import here to avoid dependency issues if not needed
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(self.model_name)

            # Explicitly set clean_up_tokenization_spaces to True to avoid the FutureWarning
            if hasattr(self.model, 'tokenizer'):
                self.model.tokenizer.clean_up_tokenization_spaces = True

            _MODEL_CACHE[self.model_name] = self.model
            return True
        except Exception as e:
            logger.warning(f"Could not load semantic model ({self.model_name}): {e}")
            logger.warning("Semantic matching will not be available.")
            return False
    
    def evaluate(self, pattern: SemanticPattern, text: str) -> Tuple[bool, float]:
        """
        Check if a semantic pattern matches the text based on similarity.
        
        Args:
            pattern: The SemanticPattern to match
            text: The text to evaluate
            
        Returns:
            Tuple of (match_success, similarity_score)
        """
        if not self._load_model():
            return False, 0.0
        
        try:
            # Import here to avoid dependency issues if not needed
            from sentence_transformers import util
            
            # Get or compute pattern embedding
            pattern_key = f"{self.model_name}:{pattern.pattern}"
            if pattern_key not in _EMBEDDING_CACHE:
                _EMBEDDING_CACHE[pattern_key] = self.model.encode(
                    [pattern.pattern], 
                    convert_to_tensor=True
                )
            
            pattern_embedding = _EMBEDDING_CACHE[pattern_key]
            
            # Get or compute text embedding
            text_key = f"{self.model_name}:{text}"
            if text_key not in _TEXT_EMBEDDING_CACHE:
                # Use a cleaner prefix to identify the cache entry
                _TEXT_EMBEDDING_CACHE[text_key] = self.model.encode([text], convert_to_tensor=True)
            
            text_embedding = _TEXT_EMBEDDING_CACHE[text_key]
            
            # Calculate similarity
            similarity = util.pytorch_cos_sim(pattern_embedding, text_embedding)
            score = float(similarity[0][0])
            
            # Check if similarity is above threshold
            return score >= pattern.threshold, score

        except Exception as e:
            logger.error(f"Error in semantic matching: {e}")
            return False, 0.0