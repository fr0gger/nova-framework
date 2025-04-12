"""
NOVA: The Prompt Pattern Matching
Author: Thomas Roccia 
twitter: @fr0gger_
License: MIT License
Version: 1.0.0
Description: Core matcher implementation for Nova rules
"""

from typing import Dict, List, Tuple, Optional, Any, Set, Callable
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

    def _analyze_condition(self, condition: str) -> Dict[str, Set[str]]:
        """
        Analyze the rule condition to determine which patterns need to be evaluated.
        
        Args:
            condition: The rule condition
            
        Returns:
            Dictionary with sets of variable names needed for each pattern type
        """
        needed_patterns = {
            'keywords': set(),
            'semantics': set(),
            'llm': set(),
            'section_wildcards': set()
        }
        
        # Check for section wildcards
        for section in ['keywords', 'semantics', 'llm']:
            if f"{section}.*" in condition:
                needed_patterns['section_wildcards'].add(section)
                
        # Check for "any of" section wildcards
        for section in ['keywords', 'semantics', 'llm']:
            if f"any of {section}.*" in condition:
                needed_patterns['section_wildcards'].add(section)

        # Check for direct variable references with section prefixes
        for section in ['keywords', 'semantics', 'llm']:
            # Exact references: "section.$var"
            pattern = rf'{section}\.\$([a-zA-Z0-9_]+)(?!\*)'
            for match in re.finditer(pattern, condition):
                var_name = f"${match.group(1)}"
                needed_patterns[section].add(var_name)
                
            # Wildcard references: "section.$var*"
            wildcard_pattern = rf'{section}\.\$([a-zA-Z0-9_]+)\*'
            for match in re.finditer(wildcard_pattern, condition):
                prefix = match.group(1)
                # Add all matching variables to needed patterns
                for var_name in getattr(self.rule, section, {}):
                    if var_name[1:].startswith(prefix):  # Remove $ from var name
                        needed_patterns[section].add(var_name)
        
        # Check for standalone variables ($var)
        var_pattern = r'(?<![a-zA-Z0-9_\.])(\$[a-zA-Z0-9_]+)(?!\*)'
        for match in re.finditer(var_pattern, condition):
            var_name = match.group(1)
            
            # Determine which section this variable belongs to
            if var_name in self.rule.keywords:
                needed_patterns['keywords'].add(var_name)
            elif var_name in self.rule.semantics:
                needed_patterns['semantics'].add(var_name)
            elif var_name in self.rule.llms:
                needed_patterns['llm'].add(var_name)
        
        # Check for "any of" wildcards
        any_of_pattern = r'any\s+of\s+\(\$([a-zA-Z0-9_]+)\*\)'
        for match in re.finditer(any_of_pattern, condition):
            prefix = match.group(1)
            
            # Add all matching variables from all sections
            for section, patterns in [
                ('keywords', self.rule.keywords),
                ('semantics', self.rule.semantics),
                ('llm', self.rule.llms)
            ]:
                for var_name in patterns:
                    if var_name[1:].startswith(prefix):
                        needed_patterns[section].add(var_name)
        
        return needed_patterns
        
    def check_prompt(self, prompt: str) -> Dict[str, Any]:
        """
        Check if a prompt matches the rule.
        
        Args:
            prompt: The prompt text to check
            
        Returns:
            Dictionary containing match results and details
        """
        # Extract variables needed based on the condition
        condition = self.rule.condition
        needed_patterns = self._analyze_condition(condition)
        
        # Track all evaluation results for debugging
        all_keyword_matches = {}
        all_semantic_matches = {}
        all_semantic_scores = {}
        all_llm_matches = {}
        all_llm_scores = {}
        
        # Dictionary to hold evaluation functions for lazy evaluation
        lazy_evaluations = {}
        
        # Initialize filtered dictionaries to hold results needed for condition evaluation
        keyword_matches = {}
        semantic_matches = {}
        llm_matches = {}
        
        # ------ LAZY PATTERN EVALUATION ------
        
        # Set up lazy evaluation functions for keywords
        for key, pattern in self.rule.keywords.items():
            # Only include if explicitly needed by condition or section wildcard is used
            if key in needed_patterns['keywords'] or 'keywords' in needed_patterns['section_wildcards']:
                lazy_evaluations[('keywords', key)] = lambda p=pattern, k=key: self.keyword_evaluator.evaluate(p, prompt, k)
        
        # Set up lazy evaluation functions for semantics
        for key, pattern in self.rule.semantics.items():
            # Only include if explicitly needed by condition or section wildcard is used
            if key in needed_patterns['semantics'] or 'semantics' in needed_patterns['section_wildcards']:
                lazy_evaluations[('semantics', key)] = lambda p=pattern: self.semantic_evaluator.evaluate(p, prompt)
        
        # Set up lazy evaluation functions for LLMs
        for key, pattern in self.rule.llms.items():
            # Only include if explicitly needed by condition or section wildcard is used
            if key in needed_patterns['llm'] or 'llm' in needed_patterns['section_wildcards']:
                temperature = pattern.threshold
                lazy_evaluations[('llm', key)] = lambda p=pattern, t=temperature: self.llm_evaluator.evaluate_prompt(p.pattern, prompt, temperature=t)
        
        # First evaluate only the patterns that are directly referenced in the condition
        # (We'll do the wildcard evaluations on demand during condition evaluation)
        for section, var_name in [
            ('keywords', name) for name in needed_patterns['keywords']
        ] + [
            ('semantics', name) for name in needed_patterns['semantics']
        ] + [
            ('llm', name) for name in needed_patterns['llm']
        ]:
            eval_key = (section, var_name)
            if eval_key in lazy_evaluations:
                try:
                    if section == 'keywords':
                        result = lazy_evaluations[eval_key]()
                        all_keyword_matches[var_name] = result
                        keyword_matches[var_name] = result
                    elif section == 'semantics':
                        matched, score = lazy_evaluations[eval_key]()
                        all_semantic_matches[var_name] = matched
                        all_semantic_scores[var_name] = score
                        semantic_matches[var_name] = matched
                    elif section == 'llm':
                        matched, confidence, details = lazy_evaluations[eval_key]()
                        all_llm_matches[var_name] = matched
                        all_llm_scores[var_name] = confidence
                        llm_matches[var_name] = matched
                except Exception as e:
                    print(f"Error evaluating {section}.{var_name}: {str(e)}")
                    # Default to False on error
                    if section == 'keywords':
                        all_keyword_matches[var_name] = False
                        keyword_matches[var_name] = False
                    elif section == 'semantics':
                        all_semantic_matches[var_name] = False
                        all_semantic_scores[var_name] = 0.0
                        semantic_matches[var_name] = False
                    elif section == 'llm':
                        all_llm_matches[var_name] = False
                        all_llm_scores[var_name] = 0.0
                        llm_matches[var_name] = False
        
        # Process section wildcards if needed
        for section in needed_patterns['section_wildcards']:
            if section == 'keywords' and not all_keyword_matches:
                # Only evaluate all keywords if needed and not already evaluated
                for key, pattern in self.rule.keywords.items():
                    if key not in all_keyword_matches:
                        try:
                            result = self.keyword_evaluator.evaluate(pattern, prompt, key)
                            all_keyword_matches[key] = result
                        except Exception:
                            all_keyword_matches[key] = False
            
            elif section == 'semantics' and not all_semantic_matches:
                # Only evaluate all semantics if needed and not already evaluated
                for key, pattern in self.rule.semantics.items():
                    if key not in all_semantic_matches:
                        try:
                            matched, score = self.semantic_evaluator.evaluate(pattern, prompt)
                            all_semantic_matches[key] = matched
                            all_semantic_scores[key] = score
                        except Exception:
                            all_semantic_matches[key] = False
                            all_semantic_scores[key] = 0.0
            
            elif section == 'llm' and not all_llm_matches:
                # Only evaluate all LLM patterns if needed and not already evaluated
                for key, pattern in self.rule.llms.items():
                    if key not in all_llm_matches:
                        try:
                            temperature = pattern.threshold
                            matched, confidence, details = self.llm_evaluator.evaluate_prompt(pattern.pattern, prompt, temperature=temperature)
                            all_llm_matches[key] = matched
                            all_llm_scores[key] = confidence
                        except Exception:
                            all_llm_matches[key] = False
                            all_llm_scores[key] = 0.0
        
        # Evaluate condition if provided
        has_match = False
        condition_result = None
        
        if condition:
            # Make sure eval_condition gets all variables that might be needed by wildcards
            if 'keywords' in needed_patterns['section_wildcards']:
                keyword_matches.update(all_keyword_matches)
            if 'semantics' in needed_patterns['section_wildcards']:
                semantic_matches.update(all_semantic_matches)
            if 'llm' in needed_patterns['section_wildcards']:
                llm_matches.update(all_llm_matches)
                
            # Use the condition evaluator with filtered match types
            condition_result = evaluate_condition(
                condition, 
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
                'condition': condition,
                'condition_result': condition_result,
                'all_keyword_matches': all_keyword_matches,
                'all_semantic_matches': all_semantic_matches,
                'all_llm_matches': all_llm_matches
            }
        }
        
        return results