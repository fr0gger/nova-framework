#!/usr/bin/env python3
"""
Test script to verify Nova works with basic installation (keywords only)
"""

import sys
from nova.core.parser import NovaParser
from nova.core.matcher import NovaMatcher

def test_basic_functionality():
    """Test basic keyword matching without LLM/semantic dependencies."""
    
    # Define a simple rule that only uses keywords
    rule_text = """
    rule BasicKeywordRule
    {
        meta:
            description = "Basic keyword matching test"
            author = "Test Suite"
        
        keywords:
            $hack = "hack"
            $exploit = "exploit"
            $malware = "malware"
        
        condition:
            any of keywords.*
    }
    """
    
    # Parse the rule
    parser = NovaParser()
    try:
        rule = parser.parse(rule_text)
        print(f"✓ Rule parsed successfully: {rule.name}")
    except Exception as e:
        print(f"✗ Failed to parse rule: {e}")
        return False
    
    # Create matcher
    try:
        matcher = NovaMatcher(rule)
        print("✓ Matcher created successfully")
    except Exception as e:
        print(f"✗ Failed to create matcher: {e}")
        return False
    
    # Test positive case
    test_prompt = "How can I hack into this system?"
    try:
        result = matcher.check_prompt(test_prompt)
        if result['matched']:
            print(f"✓ Positive test passed: '{test_prompt}' matched")
        else:
            print(f"✗ Positive test failed: '{test_prompt}' should have matched")
            return False
    except Exception as e:
        print(f"✗ Error during positive test: {e}")
        return False
    
    # Test negative case
    test_prompt = "How can I improve my programming skills?"
    try:
        result = matcher.check_prompt(test_prompt)
        if not result['matched']:
            print(f"✓ Negative test passed: '{test_prompt}' did not match")
        else:
            print(f"✗ Negative test failed: '{test_prompt}' should not have matched")
            return False
    except Exception as e:
        print(f"✗ Error during negative test: {e}")
        return False
    
    return True

def test_semantic_graceful_fallback():
    """Test that rules with semantic patterns fail gracefully when dependencies missing."""
    
    rule_text = """
    rule SemanticRule
    {
        meta:
            description = "Rule with semantic patterns"
            author = "Test Suite"
        
        keywords:
            $hack = "hack"
        
        semantics:
            $malicious = "malicious intent" (0.5)
        
        condition:
            keywords.$hack or semantics.$malicious
    }
    """
    
    parser = NovaParser()
    try:
        rule = parser.parse(rule_text)
        print(f"✓ Semantic rule parsed successfully: {rule.name}")
    except Exception as e:
        print(f"✗ Failed to parse semantic rule: {e}")
        return False
    
    # Create matcher - should work but warn about missing semantic evaluator
    try:
        matcher = NovaMatcher(rule)
        print("✓ Semantic matcher created (may have warnings)")
    except Exception as e:
        print(f"✗ Failed to create semantic matcher: {e}")
        return False
    
    # Test - should still work for keyword matching
    test_prompt = "How to hack this?"
    try:
        result = matcher.check_prompt(test_prompt)
        if result['matched']:
            print(f"✓ Semantic fallback test passed: keyword matching still works")
        else:
            print(f"✗ Semantic fallback test failed: keyword matching should still work")
            return False
    except Exception as e:
        print(f"✗ Error during semantic fallback test: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("Testing Nova Basic Installation...")
    print("=" * 50)
    
    success = True
    
    print("\n1. Testing basic keyword functionality...")
    if not test_basic_functionality():
        success = False
    
    print("\n2. Testing graceful fallback for semantic patterns...")
    if not test_semantic_graceful_fallback():
        success = False
    
    print("\n" + "=" * 50)
    if success:
        print("✓ All tests passed! Basic installation is working correctly.")
        sys.exit(0)
    else:
        print("✗ Some tests failed. Check the output above.")
        sys.exit(1)