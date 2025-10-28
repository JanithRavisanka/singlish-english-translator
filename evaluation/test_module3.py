"""
Module 3: Post-Processor - Test Script
Student 3

This script tests the post_process() function with hand-crafted test cases.
Each test uses a simulated Module 2 output dictionary.

Usage:
    python test_module3.py
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from module3 import post_process


def test_post_processing():
    """Test post-processing with various input dictionaries."""
    
    print("="*70)
    print("MODULE 3: POST-PROCESSING TEST SUITE")
    print("="*70)
    print()
    
    # Test cases: (input_dict, expected_output, test_name)
    test_cases = [
        # Test 1: Basic present continuous with "I"
        (
            {
                'raw_translation': 'I go home',
                'subject': {'en': 'I', 'pos': 'PRON'},
                'verb': {'en': 'go', 'tense': 'PRESENT_CONTINUOUS'},
                'object': {'en': 'home', 'pos': 'NOUN'},
                'negation': False
            },
            "I am going home.",
            "Present continuous (I)"
        ),
        
        # Test 2: Present continuous with "they"
        (
            {
                'raw_translation': 'they read book',
                'subject': {'en': 'they', 'pos': 'PRON'},
                'verb': {'en': 'read', 'tense': 'PRESENT_CONTINUOUS'},
                'object': {'en': 'book', 'pos': 'NOUN'},
                'negation': False
            },
            "They are reading a book.",
            "Present continuous (they) + article"
        ),
        
        # Test 3: Present continuous with "you"
        (
            {
                'raw_translation': 'you eat rice',
                'subject': {'en': 'you', 'pos': 'PRON'},
                'verb': {'en': 'eat', 'tense': 'PRESENT_CONTINUOUS'},
                'object': {'en': 'rice', 'pos': 'NOUN'},
                'negation': False
            },
            "You are eating rice.",
            "Present continuous (you)"
        ),
        
        # Test 4: Verb ending in 'e'
        (
            {
                'raw_translation': 'I write email',
                'subject': {'en': 'I', 'pos': 'PRON'},
                'verb': {'en': 'write', 'tense': 'PRESENT_CONTINUOUS'},
                'object': {'en': 'email', 'pos': 'NOUN'},
                'negation': False
            },
            "I am writing an email.",
            "Verb conjugation (e-dropping) + article (an)"
        ),
        
        # Test 5: No object
        (
            {
                'raw_translation': 'I write',
                'subject': {'en': 'I', 'pos': 'PRON'},
                'verb': {'en': 'write', 'tense': 'PRESENT_CONTINUOUS'},
                'object': {},
                'negation': False
            },
            "I am writing.",
            "No object"
        ),
        
        # Test 6: Watch (CVC pattern - should NOT double)
        (
            {
                'raw_translation': 'you watch television',
                'subject': {'en': 'you', 'pos': 'PRON'},
                'verb': {'en': 'watch', 'tense': 'PRESENT_CONTINUOUS'},
                'object': {'en': 'television', 'pos': 'NOUN'},
                'negation': False
            },
            "You are watching television.",
            "Verb conjugation (watch -> watching)"
        ),
        
        # Test 7: Drink
        (
            {
                'raw_translation': 'they drink water',
                'subject': {'en': 'they', 'pos': 'PRON'},
                'verb': {'en': 'drink', 'tense': 'PRESENT_CONTINUOUS'},
                'object': {'en': 'water', 'pos': 'NOUN'},
                'negation': False
            },
            "They are drinking water.",
            "Present continuous (drink)"
        ),
        
        # Test 8: Listen
        (
            {
                'raw_translation': 'they listen music',
                'subject': {'en': 'they', 'pos': 'PRON'},
                'verb': {'en': 'listen', 'tense': 'PRESENT_CONTINUOUS'},
                'object': {'en': 'music', 'pos': 'NOUN'},
                'negation': False
            },
            "They are listening music.",
            "Present continuous (listen)"
        ),
        
        # Test 9: Fix/repair
        (
            {
                'raw_translation': 'I fix computer',
                'subject': {'en': 'I', 'pos': 'PRON'},
                'verb': {'en': 'fix', 'tense': 'PRESENT_CONTINUOUS'},
                'object': {'en': 'computer', 'pos': 'NOUN'},
                'negation': False
            },
            "I am fixing a computer.",
            "Verb with 'x' + article"
        ),
        
        # Test 10: Play
        (
            {
                'raw_translation': 'they play game',
                'subject': {'en': 'they', 'pos': 'PRON'},
                'verb': {'en': 'play', 'tense': 'PRESENT_CONTINUOUS'},
                'object': {'en': 'game', 'pos': 'NOUN'},
                'negation': False
            },
            "They are playing a game.",
            "Present continuous (play)"
        ),
    ]
    
    pass_count = 0
    fail_count = 0
    
    for input_dict, expected, test_name in test_cases:
        try:
            actual = post_process(input_dict)
            
            if actual == expected:
                print(f"✓ PASS: {test_name}")
                print(f"         Input:    {input_dict['raw_translation']}")
                print(f"         Output:   {actual}")
                pass_count += 1
            else:
                print(f"✗ FAIL: {test_name}")
                print(f"  Input:    {input_dict['raw_translation']}")
                print(f"  Expected: {expected}")
                print(f"  Got:      {actual}")
                fail_count += 1
        except Exception as e:
            print(f"✗ ERROR: {test_name}")
            print(f"  Input: {input_dict.get('raw_translation', 'N/A')}")
            print(f"  Error: {e}")
            fail_count += 1
        
        print()  # Blank line between tests
    
    # Print summary
    print("="*70)
    print(f"Test Results Summary")
    print("="*70)
    print(f"Total tests: {len(test_cases)}")
    print(f"Passed:      {pass_count} ({pass_count/len(test_cases)*100:.1f}%)")
    print(f"Failed:      {fail_count} ({fail_count/len(test_cases)*100:.1f}%)")
    print()
    
    if fail_count == 0:
        print("🎉 All tests passed!")
        return 0
    else:
        print(f"⚠️  {fail_count} test(s) failed.")
        return 1


if __name__ == "__main__":
    exit_code = test_post_processing()
    sys.exit(exit_code)
