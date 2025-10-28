"""
Complete Pipeline Evaluation Script
Integrates Module 1 (FST) + Module 2 (RBMT) + Module 3 (Post-Processor)

This is the master script that:
1. Loads the shared corpus.json
2. Runs the complete pipeline (Singlish → Sinhala → English → Post-processed)
3. Collects all hypothesis translations and reference translations
4. Calculates BLEU score using nltk
5. Generates detailed evaluation report

Usage:
    python run_evaluation.py
    python run_evaluation.py --verbose
    python run_evaluation.py --save-results
"""

import sys
import os
import json
from typing import List, Dict, Any
import argparse

# Add module directories to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'module1'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'module2'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'module3'))

try:
    from module1 import transliterate
    from module2 import translate
    from module3 import post_process
except ImportError as e:
    print(f"Error: Failed to import modules.")
    print(f"Make sure FST is built: cd module1 && python build_fst.py")
    print(f"Details: {e}")
    sys.exit(1)

try:
    # Only import specific modules we need to avoid scipy dependency issues
    from nltk.translate.bleu_score import corpus_bleu, sentence_bleu, SmoothingFunction
except ImportError as e:
    print(f"Error: nltk not installed or has compatibility issues: {e}")
    print("Please run: conda install -c conda-forge nltk")
    print("Or: pip install nltk")
    sys.exit(1)
except ValueError as e:
    # Handle scipy/numpy compatibility issues
    print(f"Warning: scipy/numpy compatibility issue: {e}")
    print("Trying fallback import...")
    try:
        # Try direct import without scipy dependencies
        from nltk.translate.bleu_score import corpus_bleu, sentence_bleu, SmoothingFunction
    except:
        print("Error: Cannot import BLEU score module.")
        print("Installing nltk via pip might resolve this:")
        print("  pip install --force-reinstall nltk")
        sys.exit(1)


def load_corpus(corpus_path: str) -> List[Dict[str, Any]]:
    """Load the corpus.json file."""
    try:
        with open(corpus_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Corpus file not found at {corpus_path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in corpus file: {e}")
        sys.exit(1)


def run_full_pipeline(singlish_text: str, verbose: bool = False) -> Dict[str, Any]:
    """
    Run complete pipeline: Singlish → Sinhala → English → Post-processed
    
    Returns:
        Dictionary with all intermediate results and final translation
    """
    result = {
        'input': singlish_text,
        'sinhala': '',
        'raw_translation': '',
        'final_translation': '',
        'parse': {},
        'success': False,
        'error': None
    }
    
    try:
        # Module 1: Transliterate Singlish → Sinhala
        if verbose:
            print(f"  [Module 1] Transliterating: {singlish_text}")
        sinhala = transliterate(singlish_text, verbose=False, spell_check=True)
        result['sinhala'] = sinhala
        
        # Module 2: Translate Sinhala → English (structured)
        if verbose:
            print(f"  [Module 2] Parsing: {sinhala}")
        parse_dict = translate(sinhala)
        result['parse'] = parse_dict
        result['raw_translation'] = parse_dict.get('raw_translation', '')
        
        # Module 3: Post-process to fluent English
        if verbose:
            print(f"  [Module 3] Post-processing: {result['raw_translation']}")
        final = post_process(parse_dict)
        result['final_translation'] = final
        
        if verbose:
            print(f"  [Result] {final}")
        
        result['success'] = True
        
    except Exception as e:
        result['error'] = str(e)
        result['success'] = False
        if verbose:
            print(f"  [ERROR] {e}")
    
    return result


def calculate_bleu(references: List[List[str]], hypotheses: List[List[str]]) -> Dict[str, float]:
    """
    Calculate BLEU scores at different n-gram levels.
    
    Args:
        references: List of reference translations (each as list of tokens)
        hypotheses: List of hypothesis translations (each as list of tokens)
        
    Returns:
        Dictionary with BLEU-1, BLEU-2, BLEU-3, BLEU-4 scores
    """
    # Use smoothing for cases with few matches
    smooth = SmoothingFunction()
    
    # Calculate corpus BLEU with different weights
    bleu_1 = corpus_bleu(references, hypotheses, weights=(1, 0, 0, 0), 
                         smoothing_function=smooth.method1)
    bleu_2 = corpus_bleu(references, hypotheses, weights=(0.5, 0.5, 0, 0),
                         smoothing_function=smooth.method1)
    bleu_3 = corpus_bleu(references, hypotheses, weights=(0.33, 0.33, 0.33, 0),
                         smoothing_function=smooth.method1)
    bleu_4 = corpus_bleu(references, hypotheses, weights=(0.25, 0.25, 0.25, 0.25),
                         smoothing_function=smooth.method1)
    
    return {
        'BLEU-1': bleu_1,
        'BLEU-2': bleu_2,
        'BLEU-3': bleu_3,
        'BLEU-4': bleu_4
    }


def tokenize(text: str) -> List[str]:
    """Simple whitespace tokenization (lowercase)."""
    return text.lower().strip().split()


def evaluate_corpus(corpus_path: str, verbose: bool = False, save_results: bool = False) -> Dict[str, Any]:
    """
    Run evaluation on the complete corpus.
    
    Returns:
        Dictionary with evaluation results
    """
    print("\n" + "="*70)
    print("COMPLETE PIPELINE EVALUATION")
    print("Module 1 (FST) + Module 2 (RBMT) + Module 3 (Post-Processor)")
    print("="*70 + "\n")
    
    # Load corpus
    corpus = load_corpus(corpus_path)
    print(f"Loaded {len(corpus)} sentences from corpus\n")
    
    # Storage for results
    references = []  # List of lists of tokens (one reference per sentence)
    hypotheses = []  # List of lists of tokens (one hypothesis per sentence)
    all_results = []
    
    success_count = 0
    fail_count = 0
    
    # Process each sentence
    print("Processing sentences...")
    print("-" * 70)
    
    for item in corpus:
        singlish = item['sinlish']
        reference = item['english_reference']
        
        if verbose:
            print(f"\n[ID {item['id']}]")
            print(f"  Input: {singlish}")
        
        # Run pipeline
        result = run_full_pipeline(singlish, verbose=verbose)
        
        # Store result
        result_entry = {
            'id': item['id'],
            'singlish': singlish,
            'sinhala_reference': item['sinhala'],
            'sinhala_output': result['sinhala'],
            'english_reference': reference,
            'english_hypothesis': result['final_translation'],
            'raw_translation': result['raw_translation'],
            'success': result['success'],
            'error': result.get('error')
        }
        all_results.append(result_entry)
        
        # Collect for BLEU calculation
        if result['success'] and result['final_translation']:
            references.append([tokenize(reference)])  # Wrap in list (single reference)
            hypotheses.append(tokenize(result['final_translation']))
            success_count += 1
            
            if not verbose:
                print(f"✓ [ID {item['id']:2}] {singlish[:40]}")
        else:
            fail_count += 1
            print(f"✗ [ID {item['id']:2}] {singlish[:40]} - ERROR: {result.get('error', 'Unknown')}")
    
    print("-" * 70)
    print(f"\nProcessed: {success_count} successful, {fail_count} failed\n")
    
    # Calculate BLEU scores
    if success_count > 0:
        print("Calculating BLEU scores...")
        bleu_scores = calculate_bleu(references, hypotheses)
        
        print("\n" + "="*70)
        print("EVALUATION RESULTS")
        print("="*70)
        print(f"\nCorpus Size:     {len(corpus)} sentences")
        print(f"Successful:      {success_count} ({success_count/len(corpus)*100:.1f}%)")
        print(f"Failed:          {fail_count} ({fail_count/len(corpus)*100:.1f}%)")
        print(f"\n{'Metric':<15} {'Score':<10}")
        print("-" * 70)
        for metric, score in bleu_scores.items():
            print(f"{metric:<15} {score*100:>6.2f}%")
        print("\n" + "="*70)
        
        # Save results if requested
        if save_results:
            output_file = 'evaluation_results.json'
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'corpus_size': len(corpus),
                    'successful': success_count,
                    'failed': fail_count,
                    'bleu_scores': bleu_scores,
                    'detailed_results': all_results
                }, f, indent=2, ensure_ascii=False)
            print(f"\nDetailed results saved to: {output_file}")
        
        return {
            'corpus_size': len(corpus),
            'successful': success_count,
            'failed': fail_count,
            'bleu_scores': bleu_scores,
            'results': all_results
        }
    else:
        print("\n⚠️  No successful translations to evaluate!")
        return {
            'corpus_size': len(corpus),
            'successful': 0,
            'failed': fail_count,
            'bleu_scores': {},
            'results': all_results
        }


def print_sample_translations(corpus_path: str, num_samples: int = 5):
    """Print sample translations for quick inspection."""
    corpus = load_corpus(corpus_path)
    
    print("\n" + "="*70)
    print(f"SAMPLE TRANSLATIONS (First {num_samples})")
    print("="*70 + "\n")
    
    for i, item in enumerate(corpus[:num_samples], 1):
        print(f"Example {i}:")
        print(f"  Singlish:   {item['sinlish']}")
        
        result = run_full_pipeline(item['sinlish'], verbose=False)
        
        print(f"  Sinhala:    {result['sinhala']}")
        print(f"  Reference:  {item['english_reference']}")
        print(f"  Hypothesis: {result['final_translation']}")
        print()


def main():
    """CLI interface for evaluation."""
    parser = argparse.ArgumentParser(
        description='Complete Pipeline Evaluation (Module 1 + 2 + 3)',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Show detailed processing for each sentence')
    parser.add_argument('-s', '--save-results', action='store_true',
                       help='Save detailed results to JSON file')
    parser.add_argument('--samples', type=int, default=0,
                       help='Show N sample translations and exit')
    
    args = parser.parse_args()
    
    # Get corpus path
    corpus_path = os.path.join(os.path.dirname(__file__), 'data', 'corpus.json')
    
    # Show samples if requested
    if args.samples > 0:
        print_sample_translations(corpus_path, args.samples)
        return
    
    # Run full evaluation
    evaluate_corpus(corpus_path, verbose=args.verbose, save_results=args.save_results)


if __name__ == "__main__":
    main()

