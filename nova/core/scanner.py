"""
NOVA: The Prompt Pattern Matching
Author: Thomas Roccia
twitter: @fr0gger_
License: MIT License
Version: 1.0.0
Description: Scanner for checking prompts against multiple Nova rules
"""

from typing import List, Dict, Any, Optional
from nova.core.matcher import NovaMatcher
from nova.core.rules import NovaRule
from nova.evaluators.llm import OpenAIEvaluator, LLMEvaluator
from nova.utils.logger import get_logger

# Get logger for this module
logger = get_logger("nova.scanner")

class NovaScanner:
    """
    Scanner that checks prompts against multiple Nova rules.
    """
    
    def __init__(self, rules: List[NovaRule] = None):
        """
        Initialize the scanner with a list of rules.
        
        Args:
            rules: List of NovaRule objects to check against (optional)
        """
        self.rules = rules or []
        self._matchers = {}
        self._llm_evaluator = None
        
        # Check if any rules need LLM evaluation and create a single shared evaluator if needed
        if self.rules:
            self._initialize_evaluators()
            
        # Initialize matchers for provided rules
        for rule in self.rules:
            self._create_matcher(rule)
    
    def _initialize_evaluators(self):
        """Initialize evaluators based on rule needs."""
        # Check if any rule needs LLM evaluation
        needs_llm = any(self._rule_needs_llm(rule) for rule in self.rules)
        
        # Create LLM evaluator only if needed
        if needs_llm:
            logger.info("Creating single shared LLM evaluator for all rules...")
            self._llm_evaluator = OpenAIEvaluator()
    
    def _rule_needs_llm(self, rule: NovaRule) -> bool:
        """Check if a rule requires LLM evaluation."""
        if rule.llms:
            return True
        if rule.condition and 'llm.' in rule.condition.lower():
            return True
        return False
    
    def _create_matcher(self, rule: NovaRule) -> NovaMatcher:
        """Create a matcher for a rule, with shared evaluators."""
        # Create matcher with shared LLM evaluator if one exists
        matcher = NovaMatcher(
            rule=rule,
            llm_evaluator=self._llm_evaluator,
            # Don't create a new LLM evaluator if we didn't create one already
            create_llm_evaluator=self._llm_evaluator is None
        )
        self._matchers[rule.name] = matcher
        return matcher
    
    def add_rule(self, rule: NovaRule) -> None:
        """
        Add a single rule to the scanner.
        
        Args:
            rule: NovaRule object to add
            
        Raises:
            ValueError: If a rule with the same name already exists
        """
        if rule.name in self._matchers:
            raise ValueError(f"Rule with name '{rule.name}' already exists")
            
        # Check if we need to create LLM evaluator (if we don't already have one)
        if self._llm_evaluator is None and self._rule_needs_llm(rule):
            logger.info("Creating LLM evaluator for newly added rule that requires it...")
            self._llm_evaluator = OpenAIEvaluator()
        
        self.rules.append(rule)
        self._create_matcher(rule)
    
    def add_rules(self, rules: List[NovaRule]) -> None:
        """
        Add multiple rules to the scanner.
        
        Args:
            rules: List of NovaRule objects to add
            
        Raises:
            ValueError: If any rule has a duplicate name
        """
        # Check if any of the new rules need LLM (if we don't already have one)
        if self._llm_evaluator is None and any(self._rule_needs_llm(rule) for rule in rules):
            logger.info("Creating LLM evaluator for newly added rules that require it...")
            self._llm_evaluator = OpenAIEvaluator()
        
        for rule in rules:
            if rule.name in self._matchers:
                raise ValueError(f"Rule with name '{rule.name}' already exists")
            
            self.rules.append(rule)
            self._create_matcher(rule)
    
    def scan(self, prompt: str) -> List[Dict[str, Any]]:
        """
        Scan a prompt against all loaded rules.
        
        Args:
            prompt: The prompt text to scan
            
        Returns:
            List of match results for rules that matched
        """
        results = []
        
        for rule in self.rules:
            matcher = self._matchers[rule.name]
            result = matcher.check_prompt(prompt)
            
            if result['matched']:
                results.append(result)
        
        return results
    
    def scan_with_details(self, prompt: str) -> Dict[str, Any]:
        """
        Scan a prompt and return detailed results for all rules.
        
        Args:
            prompt: The prompt text to scan
            
        Returns:
            Dictionary with comprehensive scan results
        """
        all_matches = []
        all_results = {}
        
        for rule in self.rules:
            matcher = self._matchers[rule.name]
            result = matcher.check_prompt(prompt)
            
            # Add to matches list if matched
            if result['matched']:
                all_matches.append({
                    'rule_name': rule.name,
                    'meta': rule.meta
                })
            
            # Store full result for reference
            all_results[rule.name] = result
        
        return {
            'prompt': prompt,
            'matched_any': len(all_matches) > 0,
            'matches': all_matches,
            'match_count': len(all_matches),
            'scanned_rules': len(self.rules),
            'detailed_results': all_results
        }
    
    def get_rule_names(self) -> List[str]:
        """
        Get names of all loaded rules.
        
        Returns:
            List of rule names
        """
        return [rule.name for rule in self.rules]
    
    def clear_rules(self) -> None:
        """Clear all loaded rules."""
        self.rules = []
        self._matchers = {}
        # Also clear the LLM evaluator since we don't need it anymore
        self._llm_evaluator = None