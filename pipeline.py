"""
Singlish-to-English Translation Pipeline
Integrates Module 1 (FST) and Module 2 (RBMT)

This script provides a complete pipeline that:
1. Takes Singlish text as input
2. Transliterates to Sinhala script (Module 1)
3. Translates to English (Module 2)
4. Returns structured output with intermediate results

Usage:
    python pipeline.py "mama gedara yanawa"
    
Or import as module:
    from pipeline import translate_singlish
    result = translate_singlish("mama gedara yanawa")
"""

import sys
import os
import json
from typing import Dict, Any

# Add module directories to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'module1'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'module2'))

try:
    from module1 import transliterate
    from module2 import translate
except ImportError as e:
    print(f"Error: Failed to import modules. Make sure FST is built.")
    print(f"Run: cd module1 && python build_fst.py")
    print(f"Details: {e}")
    sys.exit(1)


def translate_singlish(singlish_text: str, verbose: bool = False) -> Dict[str, Any]:
    """
    Complete pipeline: Singlish → Sinhala → English
    
    Args:
        singlish_text: Input text in romanized Singlish
        verbose: If True, print intermediate steps
        
    Returns:
        Dictionary containing:
        - input: Original Singlish text
        - sinhala: Transliterated Sinhala text
        - english: Translated English text
        - parse: Detailed parse structure from Module 2
        - success: Boolean indicating if translation succeeded
        - error: Error message if failed
    """
    result = {
        "input": singlish_text,
        "sinhala": "",
        "english": "",
        "parse": {},
        "success": False,
        "error": None
    }
    
    try:
        # Step 1: Transliterate Singlish to Sinhala (Module 1)
        if verbose:
            print(f"[Module 1] Transliterating: {singlish_text}")
        
        sinhala_text = transliterate(singlish_text, verbose=verbose)
        result["sinhala"] = sinhala_text
        
        if verbose:
            print(f"[Module 1] Result: {sinhala_text}")
        
        # Step 2: Translate Sinhala to English (Module 2)
        if verbose:
            print(f"[Module 2] Parsing: {sinhala_text}")
        
        parse_result = translate(sinhala_text)
        result["parse"] = parse_result
        result["english"] = parse_result.get("raw_translation", "")
        
        if verbose:
            print(f"[Module 2] Result: {result['english']}")
        
        result["success"] = True
        
    except Exception as e:
        result["error"] = str(e)
        result["success"] = False
        if verbose:
            print(f"[ERROR] Pipeline failed: {e}")
    
    return result


def batch_translate(singlish_sentences: list, verbose: bool = False) -> list:
    """
    Translate multiple Singlish sentences.
    
    Args:
        singlish_sentences: List of Singlish text strings
        verbose: If True, print progress
        
    Returns:
        List of result dictionaries
    """
    results = []
    for i, sentence in enumerate(singlish_sentences, 1):
        if verbose:
            print(f"\n--- Translating sentence {i}/{len(singlish_sentences)} ---")
        result = translate_singlish(sentence, verbose=verbose)
        results.append(result)
    return results


def print_result(result: Dict[str, Any], show_parse: bool = False):
    """Pretty print a translation result."""
    print("\n" + "="*60)
    print(f"Input (Singlish):  {result['input']}")
    print(f"Step 1 (Sinhala):  {result['sinhala']}")
    print(f"Step 2 (English):  {result['english']}")
    
    if show_parse and result.get('parse'):
        print(f"\nDetailed Parse:")
        print(f"  Subject: {result['parse'].get('subject', {}).get('en', 'N/A')}")
        print(f"  Verb: {result['parse'].get('verb', {}).get('en', 'N/A')}")
        print(f"  Object: {result['parse'].get('object', {}).get('en', 'N/A')}")
        print(f"  Tense: {result['parse'].get('verb', {}).get('tense', 'N/A')}")
    
    if not result['success']:
        print(f"\n❌ Error: {result['error']}")
    else:
        print(f"\n✓ Translation successful")
    print("="*60)


def run_test_corpus(verbose: bool = False):
    """Run pipeline on the full corpus for validation."""
    corpus_path = os.path.join(os.path.dirname(__file__), 'data', 'corpus.json')
    
    try:
        with open(corpus_path, 'r', encoding='utf-8') as f:
            corpus = json.load(f)
    except FileNotFoundError:
        print(f"Error: corpus.json not found at {corpus_path}")
        return
    
    print("\n" + "="*60)
    print("TESTING PIPELINE ON FULL CORPUS")
    print("="*60)
    
    success_count = 0
    fail_count = 0
    
    for item in corpus:
        singlish = item['sinlish']
        expected_sinhala = item['sinhala']
        expected_english = item['english_reference']
        
        result = translate_singlish(singlish, verbose=False)
        
        sinhala_match = result['sinhala'] == expected_sinhala
        # For English, we just check if translation succeeded (Module 3 will handle fluency)
        
        if result['success'] and sinhala_match:
            success_count += 1
            status = "✓ PASS"
        else:
            fail_count += 1
            status = "✗ FAIL"
        
        if verbose or not sinhala_match:
            print(f"\n[ID {item['id']}] {status}")
            print(f"  Input:    {singlish}")
            print(f"  Sinhala:  {result['sinhala']}")
            if not sinhala_match:
                print(f"  Expected: {expected_sinhala}")
            print(f"  English:  {result['english']}")
            print(f"  Reference: {expected_english}")
    
    print("\n" + "="*60)
    print(f"RESULTS: {success_count} passed, {fail_count} failed")
    print("="*60)
    
    return success_count, fail_count


def main():
    """CLI interface for the pipeline."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Singlish to English Translation Pipeline (Module 1 + Module 2)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python pipeline.py "mama gedara yanawa"
  python pipeline.py "eyala potha kiyawanawa" --verbose
  python pipeline.py --test
  python pipeline.py --interactive
        """
    )
    
    parser.add_argument('text', nargs='?', help='Singlish text to translate')
    parser.add_argument('-v', '--verbose', action='store_true', 
                       help='Show detailed processing steps')
    parser.add_argument('-p', '--parse', action='store_true',
                       help='Show detailed parse information')
    parser.add_argument('-t', '--test', action='store_true',
                       help='Run pipeline on full corpus')
    parser.add_argument('-i', '--interactive', action='store_true',
                       help='Interactive mode (type to translate)')
    
    args = parser.parse_args()
    
    # Test mode
    if args.test:
        run_test_corpus(verbose=args.verbose)
        return
    
    # Interactive mode
    if args.interactive:
        print("\n" + "="*60)
        print("INTERACTIVE TRANSLATION MODE")
        print("Type Singlish text to translate (or 'quit' to exit)")
        print("="*60)
        
        while True:
            try:
                singlish = input("\n> ").strip()
                if singlish.lower() in ['quit', 'exit', 'q']:
                    print("Goodbye!")
                    break
                if not singlish:
                    continue
                    
                result = translate_singlish(singlish, verbose=args.verbose)
                print_result(result, show_parse=args.parse)
                
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
        return
    
    # Single translation mode
    if args.text:
        result = translate_singlish(args.text, verbose=args.verbose)
        print_result(result, show_parse=args.parse)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

