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
        self._embedding_cache: Dict[str, any] = {}  # Cache for pattern embeddings
        
        # Lazy load the model on first use
        self._load_model()
    
    def _load_model(self) -> bool:
        """
        Load the sentence transformer model.
        
        Returns:
            Boolean indicating whether the model was successfully loaded
        """
        if self.model is not None:
            return True
            
        try:
            # Import here to avoid dependency issues if not needed
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(self.model_name)
            return True
        except Exception as e:
            print(f"Warning: Could not load semantic model ({self.model_name}): {e}")
            print("Semantic matching will not be available.")
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
            pattern_key = pattern.pattern
            if pattern_key not in self._embedding_cache:
                self._embedding_cache[pattern_key] = self.model.encode(
                    [pattern.pattern], 
                    convert_to_tensor=True
                )
            
            pattern_embedding = self._embedding_cache[pattern_key]
            text_embedding = self.model.encode([text], convert_to_tensor=True)
            
            # Calculate similarity
            similarity = util.pytorch_cos_sim(pattern_embedding, text_embedding)
            score = float(similarity[0][0])
            
            # Check if similarity is above threshold
            return score >= pattern.threshold, score
            
        except Exception as e:
            print(f"Error in semantic matching: {e}")
            return False, 0.0