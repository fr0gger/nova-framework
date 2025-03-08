"""
NOVA: The Prompt Pattern Matching
Author: Thomas Roccia 
twitter: @fr0gger_
License: MIT License
Version: 1.0.0
Description: Core matcher implementation for Nova rules
"""

from typing import Dict, List, Tuple, Optional, Any
import re

from nova.core.rules import NovaRule, KeywordPattern, SemanticPattern, LLMPattern
from nova.evaluators.keywords import DefaultKeywordEvaluator
from nova.evaluators.semantics import DefaultSemanticEvaluator
from nova.evaluators.llm import OpenAIEvaluator
from nova.evaluators.condition import evaluate_condition


class NovaMatcher:
    """
    Matcher for Nova rules.
    Evaluates text against rules using different pattern types.
    """
    
    def __init__(self, 
                 rule: NovaRule,
                 keyword_evaluator: Optional[DefaultKeywordEvaluator] = None,
                 semantic_evaluator: Optional[DefaultSemanticEvaluator] = None,
                 llm_evaluator: Optional[OpenAIEvaluator] = None):
        """
        Initialize the matcher with a rule and optional custom evaluators.
        
        Args:
            rule: The NovaRule to match against
            keyword_evaluator: Custom keyword evaluator (uses DefaultKeywordEvaluator if None)
            semantic_evaluator: Custom semantic evaluator (uses DefaultSemanticEvaluator if None)
            llm_evaluator: Custom LLM evaluator (uses OpenAIEvaluator if None)
        """
        self.rule = rule
        
        # Initialize evaluators
        self.keyword_evaluator = keyword_evaluator or DefaultKeywordEvaluator()
        self.semantic_evaluator = semantic_evaluator or DefaultSemanticEvaluator()
        self.llm_evaluator = llm_evaluator or OpenAIEvaluator()
        
        # Pre-compile keyword patterns for performance
        self._precompile_patterns()
    
    def _precompile_patterns(self):
        """Pre-compile regex patterns for better performance."""
        for key, pattern in self.rule.keywords.items():
            if pattern.is_regex:
                self.keyword_evaluator.compile_pattern(key, pattern)
    
    def check_prompt(self, prompt: str) -> Dict[str, Any]:
        """
        Check if a prompt matches the rule.
        
        Args:
            prompt: The prompt text to check
            
        Returns:
            Dictionary containing match results and details
        """
        # Get all keyword matches for debugging
        all_keyword_matches = {}
        for key, pattern in self.rule.keywords.items():
            all_keyword_matches[key] = self.keyword_evaluator.evaluate(pattern, prompt, key)
        
        # Get all semantic matches for debugging
        all_semantic_matches = {}
        all_semantic_scores = {}
        for key, pattern in self.rule.semantics.items():
            matched, score = self.semantic_evaluator.evaluate(pattern, prompt)
            all_semantic_matches[key] = matched
            all_semantic_scores[key] = score
        
        # Get all LLM matches for debugging
        all_llm_matches = {}
        all_llm_scores = {}
        for key, pattern in self.rule.llms.items():
            # Use the pattern's threshold as the temperature parameter
            temperature = pattern.threshold
            matched, confidence, details = self.llm_evaluator.evaluate_prompt(pattern.pattern, prompt, temperature=temperature)
            all_llm_matches[key] = matched  # Don't compare confidence to threshold anymore
            all_llm_scores[key] = confidence
        
        # For the condition evaluation, only use variables explicitly referenced
        condition = self.rule.condition
        
        # Extract variables directly referenced in the condition
        keyword_matches = {}
        semantic_matches = {}
        llm_matches = {}
        
        # Check for direct variable references with wildcards (section.$var*)
        for section, var_dict, target_dict in [
            ('keywords', all_keyword_matches, keyword_matches),
            ('semantics', all_semantic_matches, semantic_matches),
            ('llm', all_llm_matches, llm_matches)
        ]:
            # Match exact references like "section.$var"
            pattern = rf'{section}\.\$([a-zA-Z0-9_]+)(?!\*)'
            for match in re.finditer(pattern, condition):
                var_name = f"${match.group(1)}"
                if var_name in var_dict:
                    target_dict[var_name] = var_dict[var_name]
                    
            # Match wildcard references like "section.$var*"
            wildcard_pattern = rf'{section}\.\$([a-zA-Z0-9_]+)\*'
            for match in re.finditer(wildcard_pattern, condition):
                prefix = match.group(1)
                # Add all variables matching this prefix
                for var, value in var_dict.items():
                    if var[1:].startswith(prefix):  # Remove $ from var name
                        target_dict[var] = value
        
        # Check for standalone variables ($var)
        var_pattern = r'(?<![a-zA-Z0-9_\.])(\$[a-zA-Z0-9_]+)(?!\*)'
        for match in re.finditer(var_pattern, condition):
            var_name = match.group(1)
            
            # Skip if it's already handled as a section.$ reference
            if any(var_name in d for d in [keyword_matches, semantic_matches, llm_matches]):
                continue
                
            # Try to find where this variable is defined
            if var_name in all_keyword_matches:
                keyword_matches[var_name] = all_keyword_matches[var_name]
            elif var_name in all_semantic_matches:
                semantic_matches[var_name] = all_semantic_matches[var_name]
            elif var_name in all_llm_matches:
                llm_matches[var_name] = all_llm_matches[var_name]
        
        # Handle "any of" wildcards if present
        any_of_pattern = r'any\s+of\s+\(\$([a-zA-Z0-9_]+)\*\)'
        for match in re.finditer(any_of_pattern, condition):
            prefix = match.group(1)
            
            # Add variables matching this prefix from all sections
            for var, value in all_keyword_matches.items():
                if var[1:].startswith(prefix):  # Remove $ from var name
                    keyword_matches[var] = value
                    
            for var, value in all_semantic_matches.items():
                if var[1:].startswith(prefix):
                    semantic_matches[var] = value
                    
            for var, value in all_llm_matches.items():
                if var[1:].startswith(prefix):
                    llm_matches[var] = value
        
        # Process section wildcards (keywords.*, semantics.*, llm.*)
        if "keywords.*" in condition:
            keyword_matches.update(all_keyword_matches)
        if "semantics.*" in condition:
            semantic_matches.update(all_semantic_matches)
        if "llm.*" in condition:
            llm_matches.update(all_llm_matches)
        
        # Evaluate condition if provided
        has_match = False
        condition_result = None
        
        if self.rule.condition:
            # Use the condition evaluator with filtered match types
            condition_result = evaluate_condition(
                self.rule.condition, 
                keyword_matches, 
                semantic_matches, 
                llm_matches
            )
            has_match = condition_result
        else:
            # Fall back to original behavior if no condition is specified
            has_match = any(keyword_matches.values()) or any(semantic_matches.values()) or any(llm_matches.values())
        
        # Build results with matching variables only
        results = {
            'matched': has_match,
            'rule_name': self.rule.name,
            'meta': self.rule.meta,
            'matching_keywords': {k: v for k, v in keyword_matches.items() if v},
            'matching_semantics': {k: v for k, v in semantic_matches.items() if v},
            'matching_llm': {k: v for k, v in llm_matches.items() if v},
            'semantic_scores': all_semantic_scores,
            'llm_scores': all_llm_scores,
            'debug': {
                'condition': self.rule.condition,
                'condition_result': condition_result,
                'all_keyword_matches': all_keyword_matches,
                'all_semantic_matches': all_semantic_matches,
                'all_llm_matches': all_llm_matches
            }
        }
        
        return results