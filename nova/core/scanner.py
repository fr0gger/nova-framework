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
        
        # Initialize matchers for provided rules
        for rule in self.rules:
            self._matchers[rule.name] = NovaMatcher(rule)
    
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
            
        self.rules.append(rule)
        self._matchers[rule.name] = NovaMatcher(rule)
    
    def add_rules(self, rules: List[NovaRule]) -> None:
        """
        Add multiple rules to the scanner.
        
        Args:
            rules: List of NovaRule objects to add
            
        Raises:
            ValueError: If any rule has a duplicate name
        """
        for rule in rules:
            self.add_rule(rule)
    
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