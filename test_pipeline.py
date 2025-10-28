"""
Simple Complete Pipeline Test (without nltk dependency)
Tests the integration of Module 1 + Module 2 + Module 3

This script can run even if nltk has compatibility issues.
For full BLEU score calculation, use run_evaluation.py after fixing nltk.
"""

import sys
import os
import json

# Add module directories to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'transliteration'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'translation'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'evaluation'))

try:
    from module1 import transliterate
    from module2 import translate
    from module3 import post_process
except ImportError as e:
    print(f"Error: Failed to import modules.")
    print(f"Make sure FST is built: cd transliteration && python build_fst.py")
    print(f"Details: {e}")
    sys.exit(1)


def run_pipeline(singlish_text):
    """Run complete pipeline: Singlish → Sinhala → English → Post-processed"""
    try:
        # Module 1: Transliterate
        sinhala = transliterate(singlish_text, verbose=False, spell_check=True)
        
        # Module 2: Parse and translate
        parse_dict = translate(sinhala)
        
        # Module 3: Post-process
        final = post_process(parse_dict)
        
        return {
            'success': True,
            'sinhala': sinhala,
            'raw_translation': parse_dict.get('raw_translation', ''),
            'final_translation': final,
            'parse': parse_dict
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def main():
    """Test pipeline on corpus."""
    corpus_path = os.path.join(os.path.dirname(__file__), 'data', 'corpus.json')
    
    try:
        with open(corpus_path, 'r', encoding='utf-8') as f:
            corpus = json.load(f)
    except FileNotFoundError:
        print(f"Error: corpus.json not found at {corpus_path}")
        return
    
    print("\n" + "="*70)
    print("COMPLETE PIPELINE TEST (Module 1 + Module 2 + Module 3)")
    print("="*70 + "\n")
    
    print("Testing first 10 sentences...\n")
    print("-"*70)
    
    success_count = 0
    fail_count = 0
    
    for item in corpus[:10]:
        singlish = item['sinlish']
        reference = item['english_reference']
        
        result = run_pipeline(singlish)
        
        if result['success']:
            success_count += 1
            print(f"\n✓ [ID {item['id']}]")
            print(f"  Input:       {singlish}")
            print(f"  Sinhala:     {result['sinhala']}")
            print(f"  Translation: {result['final_translation']}")
            print(f"  Reference:   {reference}")
        else:
            fail_count += 1
            print(f"\n✗ [ID {item['id']}] ERROR: {result['error']}")
            print(f"  Input: {singlish}")
    
    print("\n" + "-"*70)
    print(f"\nResults: {success_count} successful, {fail_count} failed\n")
    print("="*70)
    
    # Test additional examples
    print("\n" + "="*70)
    print("ADDITIONAL TEST EXAMPLES")
    print("="*70 + "\n")
    
    test_examples = [
        "mama gedara yanawa",
        "eyala potha kiyawanawa",
        "oya bath kanawa"
    ]
    
    for singlish in test_examples:
        result = run_pipeline(singlish)
        if result['success']:
            print(f"Input:  {singlish}")
            print(f"Output: {result['final_translation']}\n")


if __name__ == "__main__":
    main()

