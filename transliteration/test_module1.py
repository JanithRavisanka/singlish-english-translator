"""
Module 1: FST Transliteration Engine - Test Script
Student 1

This script tests the transliteration function against the shared corpus.json.
It verifies that Singlish input is correctly converted to Sinhala script.

Usage:
    python test_module1.py

Expected Output:
    PASS/FAIL for each test case
    Final summary: "All tests passed!" or error count
"""

import json
import sys
import os

# Add current directory to path so we can import module1
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from module1 import transliterate
except FileNotFoundError as e:
    print("Error: transliterate.fst not found!")
    print("Please run 'python build_fst.py' first to compile the FST.")
    print(f"\nDetails: {e}")
    sys.exit(1)
except Exception as e:
    print(f"Error importing module1: {e}")
    sys.exit(1)

def test_unicode():
    """Test Unicode to ASCII conversion capabilities."""
    
    print(f"Testing Unicode Handling Features")
    print(f"=" * 60)
    print()
    
    # Test cases for Unicode conversion
    unicode_tests = [
        # (input, expected_output, test_name)
        ("mama gedära yanawa", "මම ගෙදර යනවා", "Unicode: ä → a"),
        ("café mama yanawa", "කාෆ්එ මම යනවා", "Unicode: é → e"),
        ("naïve oya iskole", "නඉවෙ ඔය ඉස්කෝලේ", "Unicode: ï → i"),
        ("résumé potha", "ර්එස්උම්එ පොත", "Unicode: é multiple"),
        ("Mama Gëdara Yanawa", "මම ගෙදර යනවා", "Unicode: ë → e"),
        ("São Paulo", "ස පඋලො", "Unicode: ã → a, au"),
        ("Schön mama", "ස්ච්ඔන් මම", "Unicode: ö → o"),
        ("mama gedara yañawa", "මම ගෙදර යනවා", "Unicode: ñ → n"),
        ("Hëllo Wörld", "හ්එල්ලො ව්ඔර්ල්ද්", "Unicode: ë, ö multiple"),
        ("CAFÉ OYA", "කාෆ්එ ඔය", "Unicode: uppercase + accent"),
    ]
    
    pass_count = 0
    fail_count = 0
    
    for input_text, expected, test_name in unicode_tests:
        try:
            actual = transliterate(input_text, spell_check=True)
            
            if actual == expected:
                print(f"✓ PASS: {test_name}")
                print(f"         Input:  {repr(input_text)}")
                print(f"         Output: {repr(actual)}")
                pass_count += 1
            else:
                print(f"✗ FAIL: {test_name}")
                print(f"  Input:    {repr(input_text)}")
                print(f"  Expected: {repr(expected)}")
                print(f"  Got:      {repr(actual)}")
                fail_count += 1
        except Exception as e:
            print(f"✗ ERROR: {test_name}")
            print(f"  Input: {repr(input_text)}")
            print(f"  Error: {e}")
            fail_count += 1
        
        print()  # Blank line between tests
    
    # Print summary
    print("=" * 60)
    print(f"Unicode Test Results")
    print(f"=" * 60)
    print(f"Total tests: {len(unicode_tests)}")
    print(f"Passed:      {pass_count} ({pass_count/len(unicode_tests)*100:.1f}%)")
    print(f"Failed:      {fail_count} ({fail_count/len(unicode_tests)*100:.1f}%)")
    print()
    
    return fail_count == 0


def test_spell_check():
    """Test spell checking and fuzzy matching capabilities."""
    
    print(f"Testing Spell Check Features")
    print(f"=" * 60)
    print()
    
    # Test cases for spell checking
    spell_check_tests = [
        # (input, expected_output, test_name)
        ("mama gedra yanawa", "මම ගෙදර යනවා", "Typo: gedra → gedara"),
        ("mama gedar yanawa", "මම ගෙදර යනවා", "Typo: gedar → gedara"),
        ("eyala potha kiyawanwa", "එයාලා පොත කියවනවා", "Typo: kiyawanwa → kiyawanawa"),
        ("oya baht kanawa", "ඔය බත් කනවා", "Typo: baht → bath"),
        ("mama iskol yanawa", "මම ඉස්කෝලේ යනවා", "Typo: iskol → iskole"),
        ("eyala watura bonwa", "එයාලා වතුර බොනවා", "Typo: bonwa → bonawa"),
        ("mama computr hadanawa", "මම කොම්පියුටර් හදනවා", "Typo: computr → computer"),
        ("oya telavision balanawa", "ඔය ටෙලිවිෂන් බලනවා", "Typo: telavision → television"),
    ]
    
    pass_count = 0
    fail_count = 0
    
    for input_text, expected, test_name in spell_check_tests:
        try:
            actual = transliterate(input_text, spell_check=True)
            
            if actual == expected:
                print(f"✓ PASS: {test_name}")
                print(f"         Input:  {repr(input_text)}")
                print(f"         Output: {repr(actual)}")
                pass_count += 1
            else:
                print(f"✗ FAIL: {test_name}")
                print(f"  Input:    {repr(input_text)}")
                print(f"  Expected: {repr(expected)}")
                print(f"  Got:      {repr(actual)}")
                fail_count += 1
        except Exception as e:
            print(f"✗ ERROR: {test_name}")
            print(f"  Input: {repr(input_text)}")
            print(f"  Error: {e}")
            fail_count += 1
        
        print()  # Blank line between tests
    
    # Print summary
    print("=" * 60)
    print(f"Spell Check Test Results")
    print(f"=" * 60)
    print(f"Total tests: {len(spell_check_tests)}")
    print(f"Passed:      {pass_count} ({pass_count/len(spell_check_tests)*100:.1f}%)")
    print(f"Failed:      {fail_count} ({fail_count/len(spell_check_tests)*100:.1f}%)")
    print()
    
    return fail_count == 0


def test_preprocessing():
    """Test preprocessing capabilities."""
    
    print(f"Testing Preprocessing Features")
    print(f"=" * 60)
    print()
    
    # Test cases for preprocessing
    preprocessing_tests = [
        # (input, expected_output, test_name)
        ("mama gedara yanawa", "මම ගෙදර යනවා", "Normal lowercase"),
        ("Mama gedara yanawa", "මම ගෙදර යනවා", "Uppercase start"),
        ("MAMA GEDARA YANAWA", "මම ගෙදර යනවා", "All uppercase"),
        ("mama  gedara   yanawa", "මම ගෙදර යනවා", "Extra spaces"),
        ("mama gedara yanawa!", "මම ගෙදර යනවා!", "Punctuation (!)"),
        ("mama gedara yanawa.", "මම ගෙදර යනවා.", "Punctuation (.)"),
        ("oya bath kanawa?", "ඔය බත් කනවා?", "Punctuation (?)"),
        ("eyala 5 potha kiyawanawa", "එයාලා 5 පොත කියවනවා", "With numbers"),
        ("mama   gedara  yanawa  ", "මම ගෙදර යනවා", "Leading/trailing spaces"),
    ]
    
    pass_count = 0
    fail_count = 0
    
    for input_text, expected, test_name in preprocessing_tests:
        try:
            actual = transliterate(input_text)
            
            if actual == expected:
                print(f"✓ PASS: {test_name}")
                print(f"         Input:  {repr(input_text)}")
                print(f"         Output: {repr(actual)}")
                pass_count += 1
            else:
                print(f"✗ FAIL: {test_name}")
                print(f"  Input:    {repr(input_text)}")
                print(f"  Expected: {repr(expected)}")
                print(f"  Got:      {repr(actual)}")
                fail_count += 1
        except Exception as e:
            print(f"✗ ERROR: {test_name}")
            print(f"  Input: {repr(input_text)}")
            print(f"  Error: {e}")
            fail_count += 1
        
        print()  # Blank line between tests
    
    # Print summary
    print("=" * 60)
    print(f"Preprocessing Test Results")
    print(f"=" * 60)
    print(f"Total tests: {len(preprocessing_tests)}")
    print(f"Passed:      {pass_count} ({pass_count/len(preprocessing_tests)*100:.1f}%)")
    print(f"Failed:      {fail_count} ({fail_count/len(preprocessing_tests)*100:.1f}%)")
    print()
    
    return fail_count == 0


def test_module1():
    """Run tests on the transliteration module."""
    
    # Get path to corpus.json (in data directory)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    corpus_path = os.path.join(script_dir, '..', 'data', 'corpus.json')
    
    # Load corpus
    try:
        with open(corpus_path, 'r', encoding='utf-8') as f:
            corpus = json.load(f)
    except FileNotFoundError:
        print(f"Error: Could not find corpus.json at {corpus_path}")
        print("Please ensure corpus.json exists in the data/ directory.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: corpus.json is not valid JSON: {e}")
        sys.exit(1)
    
    if not corpus:
        print("Warning: corpus.json is empty!")
        sys.exit(1)
    
    print(f"Testing Module 1 Transliteration Engine")
    print(f"=" * 60)
    print(f"Loaded {len(corpus)} test cases from corpus.json\n")
    
    pass_count = 0
    fail_count = 0
    
    # Test each item in the corpus
    for item in corpus:
        test_id = item.get('id', '?')
        sinlish = item['sinlish']
        expected = item['sinhala']
        
        try:
            actual = transliterate(sinlish)
            
            if actual == expected:
                print(f"✓ PASS [ID {test_id}]: {sinlish}")
                print(f"         → {actual}")
                pass_count += 1
            else:
                print(f"✗ FAIL [ID {test_id}]: {sinlish}")
                print(f"  Expected: {expected}")
                print(f"  Got:      {actual}")
                fail_count += 1
        except Exception as e:
            print(f"✗ ERROR [ID {test_id}]: {sinlish}")
            print(f"  Error: {e}")
            fail_count += 1
        
        print()  # Blank line between tests
    
    # Print summary
    print("=" * 60)
    print(f"Test Results Summary")
    print(f"=" * 60)
    print(f"Total tests: {len(corpus)}")
    print(f"Passed:      {pass_count} ({pass_count/len(corpus)*100:.1f}%)")
    print(f"Failed:      {fail_count} ({fail_count/len(corpus)*100:.1f}%)")
    print()
    
    if fail_count == 0:
        print("🎉 All tests passed!")
        return 0
    else:
        print(f"⚠️  {fail_count} test(s) failed.")
        print("\nTo fix failures:")
        print("1. Check the singlish_rules.json file")
        print("2. Add or fix the transliteration rules")
        print("3. Re-run 'python build_fst.py' to recompile the FST")
        print("4. Run this test script again")
        return 1

if __name__ == "__main__":
    # Run all test suites
    print("\n" + "="*60)
    print("MODULE 1 COMPREHENSIVE TEST SUITE")
    print("="*60 + "\n")
    
    # Part 1: Unicode tests
    print("\n" + "="*60)
    print("PART 1: UNICODE HANDLING TESTS")
    print("="*60 + "\n")
    unicode_passed = test_unicode()
    
    # Part 2: Spell check tests
    print("\n" + "="*60)
    print("PART 2: SPELL CHECK TESTS")
    print("="*60 + "\n")
    spell_check_passed = test_spell_check()
    
    # Part 3: Preprocessing tests
    print("\n" + "="*60)
    print("PART 3: PREPROCESSING TESTS")
    print("="*60 + "\n")
    preprocessing_passed = test_preprocessing()
    
    # Part 4: Corpus tests
    print("\n" + "="*60)
    print("PART 4: CORPUS TESTS")
    print("="*60 + "\n")
    corpus_exit_code = test_module1()
    
    # Final summary
    print("\n" + "="*60)
    print("OVERALL TEST SUMMARY")
    print("="*60)
    
    all_passed = (unicode_passed and spell_check_passed and 
                  preprocessing_passed and corpus_exit_code == 0)
    
    if all_passed:
        print("✅ All tests passed!")
        print("   • Unicode Handling: ✓")
        print("   • Spell Checking: ✓")
        print("   • Preprocessing: ✓")
        print("   • Corpus: ✓")
        sys.exit(0)
    else:
        print("❌ Some tests failed:")
        if not unicode_passed:
            print("   • Unicode Handling: ✗")
        if not spell_check_passed:
            print("   • Spell Checking: ✗")
        if not preprocessing_passed:
            print("   • Preprocessing: ✗")
        if corpus_exit_code != 0:
            print("   • Corpus: ✗")
        sys.exit(1)
