"""
Test script for the integrated pipeline (Module 1 + Module 2)

This script validates that the pipeline correctly processes various types of inputs
and handles edge cases properly.
"""

import sys
from pipeline import translate_singlish, batch_translate

def test_basic_translations():
    """Test basic translation functionality."""
    print("\n" + "="*60)
    print("TEST 1: Basic Translations")
    print("="*60)
    
    test_cases = [
        ("mama gedara yanawa", "මම ගෙදර යනවා", "I go home"),
        ("eyala potha kiyawanawa", "එයාලා පොත කියවනවා", "they read book"),
        ("oya bath kanawa", "ඔය බත් කනවා", "you eat rice"),
    ]
    
    passed = 0
    failed = 0
    
    for singlish, expected_sinhala, expected_english_contains in test_cases:
        result = translate_singlish(singlish)
        
        if result['success'] and result['sinhala'] == expected_sinhala:
            print(f"✓ PASS: {singlish}")
            passed += 1
        else:
            print(f"✗ FAIL: {singlish}")
            print(f"  Expected Sinhala: {expected_sinhala}")
            print(f"  Got: {result['sinhala']}")
            if result['error']:
                print(f"  Error: {result['error']}")
            failed += 1
    
    print(f"\nResult: {passed} passed, {failed} failed")
    return failed == 0


def test_edge_cases():
    """Test edge cases and preprocessing."""
    print("\n" + "="*60)
    print("TEST 2: Edge Cases (Preprocessing)")
    print("="*60)
    
    test_cases = [
        ("Mama gedara yanawa", "මම ගෙදර යනවා", "Uppercase start"),
        ("MAMA GEDARA YANAWA", "මම ගෙදර යනවා", "All uppercase"),
        ("mama  gedara   yanawa", "මම ගෙදර යනවා", "Extra spaces"),
        ("mama gedara yanawa!", "මම ගෙදර යනවා!", "With punctuation"),
        ("  mama gedara yanawa  ", "මම ගෙදර යනවා", "Leading/trailing spaces"),
    ]
    
    passed = 0
    failed = 0
    
    for singlish, expected_sinhala, description in test_cases:
        result = translate_singlish(singlish)
        
        if result['success'] and result['sinhala'] == expected_sinhala:
            print(f"✓ PASS: {description}")
            passed += 1
        else:
            print(f"✗ FAIL: {description}")
            print(f"  Input: {repr(singlish)}")
            print(f"  Expected: {expected_sinhala}")
            print(f"  Got: {result['sinhala']}")
            failed += 1
    
    print(f"\nResult: {passed} passed, {failed} failed")
    return failed == 0


def test_batch_processing():
    """Test batch translation."""
    print("\n" + "="*60)
    print("TEST 3: Batch Processing")
    print("="*60)
    
    sentences = [
        "mama gedara yanawa",
        "eyala potha kiyawanawa",
        "oya bath kanawa",
        "mama iskole yanawa",
        "eyala watura bonawa"
    ]
    
    results = batch_translate(sentences)
    
    success_count = sum(1 for r in results if r['success'])
    
    print(f"Processed {len(sentences)} sentences")
    print(f"Success: {success_count}/{len(sentences)}")
    
    if success_count == len(sentences):
        print("✓ All batch translations successful")
        return True
    else:
        print("✗ Some batch translations failed")
        for i, result in enumerate(results):
            if not result['success']:
                print(f"  Failed: {sentences[i]} - {result['error']}")
        return False


def test_parse_structure():
    """Test that parse structure contains expected fields."""
    print("\n" + "="*60)
    print("TEST 4: Parse Structure Validation")
    print("="*60)
    
    result = translate_singlish("mama gedara yanawa")
    
    required_fields = ['subject', 'verb', 'object', 'raw_translation']
    missing_fields = []
    
    for field in required_fields:
        if field not in result['parse']:
            missing_fields.append(field)
    
    if not missing_fields:
        print("✓ All required parse fields present")
        print(f"  Subject: {result['parse']['subject'].get('en', 'N/A')}")
        print(f"  Verb: {result['parse']['verb'].get('en', 'N/A')}")
        print(f"  Object: {result['parse']['object'].get('en', 'N/A')}")
        print(f"  Raw Translation: {result['parse']['raw_translation']}")
        return True
    else:
        print(f"✗ Missing parse fields: {missing_fields}")
        return False


def test_error_handling():
    """Test error handling for invalid inputs."""
    print("\n" + "="*60)
    print("TEST 5: Error Handling")
    print("="*60)
    
    # Empty input
    result = translate_singlish("")
    if result['sinhala'] == "":
        print("✓ Empty input handled correctly")
        empty_ok = True
    else:
        print("✗ Empty input not handled correctly")
        empty_ok = False
    
    # Very long input
    long_input = "mama " * 100
    result = translate_singlish(long_input)
    if result['success'] or result['error']:
        print("✓ Long input handled (no crash)")
        long_ok = True
    else:
        print("✗ Long input caused issues")
        long_ok = False
    
    return empty_ok and long_ok


def main():
    """Run all pipeline tests."""
    print("\n" + "="*60)
    print("PIPELINE INTEGRATION TEST SUITE")
    print("Testing Module 1 + Module 2 Integration")
    print("="*60)
    
    tests = [
        test_basic_translations,
        test_edge_cases,
        test_batch_processing,
        test_parse_structure,
        test_error_handling
    ]
    
    results = []
    for test_func in tests:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"\n✗ Test {test_func.__name__} crashed: {e}")
            results.append(False)
    
    print("\n" + "="*60)
    print("FINAL RESULTS")
    print("="*60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("\n✅ All pipeline tests passed!")
        return 0
    else:
        print(f"\n❌ {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

