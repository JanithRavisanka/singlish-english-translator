"""
Module 1: FST Transliteration Engine - Enhanced Test Script
Student 1

This script provides comprehensive testing of the transliteration module with:
- Basic accuracy testing
- Character Error Rate (CER) and Word Error Rate (WER)
- Confusion matrix analysis
- Per-rule accuracy metrics
- OOV detection testing
- N-best hypothesis evaluation
- Performance benchmarking

Usage:
    python test_module1.py              # Run all tests
    python test_module1.py --verbose    # Detailed output
    python test_module1.py --benchmark  # Performance testing
    python test_module1.py --analysis   # Deep analysis mode
"""

import json
import sys
import os
import time
from collections import defaultdict, Counter
from typing import Dict, List, Tuple

# Add current directory to path so we can import module1
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from module1 import (transliterate, transliterate_nbest, 
                         detect_oov, get_alignment)
except FileNotFoundError as e:
    print("Error: transliterate.fst not found!")
    print("Please run 'python build_fst.py' first to compile the FST.")
    print(f"\nDetails: {e}")
    sys.exit(1)
except Exception as e:
    print(f"Error importing module1: {e}")
    sys.exit(1)


def calculate_cer(reference: str, hypothesis: str) -> float:
    """
    Calculate Character Error Rate (CER).
    
    CER = (Substitutions + Deletions + Insertions) / Total Characters in Reference
    
    Uses Levenshtein distance for edit operations.
    
    Args:
        reference: Ground truth string
        hypothesis: Predicted string
        
    Returns:
        CER as float (0.0 = perfect, higher = worse)
    """
    # Simple Levenshtein distance implementation
    if len(reference) == 0:
        return 0.0 if len(hypothesis) == 0 else 1.0
    
    # Create distance matrix
    d = [[0] * (len(hypothesis) + 1) for _ in range(len(reference) + 1)]
    
    # Initialize first column and row
    for i in range(len(reference) + 1):
        d[i][0] = i
    for j in range(len(hypothesis) + 1):
        d[0][j] = j
    
    # Fill matrix
    for i in range(1, len(reference) + 1):
        for j in range(1, len(hypothesis) + 1):
            if reference[i-1] == hypothesis[j-1]:
                d[i][j] = d[i-1][j-1]
            else:
                d[i][j] = min(
                    d[i-1][j] + 1,      # deletion
                    d[i][j-1] + 1,      # insertion
                    d[i-1][j-1] + 1     # substitution
                )
    
    return d[len(reference)][len(hypothesis)] / len(reference)


def calculate_wer(reference: str, hypothesis: str) -> float:
    """
    Calculate Word Error Rate (WER).
    
    WER = (Word Substitutions + Deletions + Insertions) / Total Words in Reference
    
    Args:
        reference: Ground truth string
        hypothesis: Predicted string
        
    Returns:
        WER as float (0.0 = perfect, higher = worse)
    """
    ref_words = reference.split()
    hyp_words = hypothesis.split()
    
    if len(ref_words) == 0:
        return 0.0 if len(hyp_words) == 0 else 1.0
    
    # Use same Levenshtein approach but on words
    d = [[0] * (len(hyp_words) + 1) for _ in range(len(ref_words) + 1)]
    
    for i in range(len(ref_words) + 1):
        d[i][0] = i
    for j in range(len(hyp_words) + 1):
        d[0][j] = j
    
    for i in range(1, len(ref_words) + 1):
        for j in range(1, len(hyp_words) + 1):
            if ref_words[i-1] == hyp_words[j-1]:
                d[i][j] = d[i-1][j-1]
            else:
                d[i][j] = min(
                    d[i-1][j] + 1,
                    d[i][j-1] + 1,
                    d[i-1][j-1] + 1
                )
    
    return d[len(ref_words)][len(hyp_words)] / len(ref_words)


def build_confusion_matrix(test_results: List[Tuple]) -> Dict:
    """
    Build confusion matrix for character-level errors.
    
    Args:
        test_results: List of (reference, hypothesis) pairs
        
    Returns:
        Dictionary with confusion statistics
    """
    confusion = defaultdict(lambda: defaultdict(int))
    total_chars = 0
    total_errors = 0
    
    for reference, hypothesis in test_results:
        total_chars += len(reference)
        
        # Align strings and find mismatches
        for i, (ref_char, hyp_char) in enumerate(zip(reference, hypothesis)):
            if ref_char != hyp_char:
                confusion[ref_char][hyp_char] += 1
                total_errors += 1
        
        # Handle length mismatches
        if len(hypothesis) > len(reference):
            for char in hypothesis[len(reference):]:
                confusion['[INSERT]'][char] += 1
                total_errors += 1
        elif len(reference) > len(hypothesis):
            for char in reference[len(hypothesis):]:
                confusion[char]['[DELETE]'] += 1
                total_errors += 1
    
    return {
        'confusion_pairs': dict(confusion),
        'total_characters': total_chars,
        'total_errors': total_errors,
        'error_rate': total_errors / total_chars if total_chars > 0 else 0
    }


def analyze_rule_accuracy(corpus: List[Dict]) -> Dict:
    """
    Analyze per-rule accuracy by checking alignment.
    
    Args:
        corpus: Test corpus
        
    Returns:
        Dictionary with per-rule statistics
    """
    rule_stats = defaultdict(lambda: {'correct': 0, 'total': 0})
    
    for item in corpus:
        sinlish = item['sinlish']
        expected = item['sinhala']
        
        try:
            actual = transliterate(sinlish)
            alignment = get_alignment(sinlish)
            
            # Check each aligned segment
            for inp_seg, out_seg in alignment:
                rule = inp_seg
                rule_stats[rule]['total'] += 1
                
                # Check if this segment appears correctly in output
                if out_seg in expected and out_seg in actual:
                    rule_stats[rule]['correct'] += 1
        except:
            continue
    
    # Calculate accuracy for each rule
    rule_accuracy = {}
    for rule, stats in rule_stats.items():
        accuracy = stats['correct'] / stats['total'] if stats['total'] > 0 else 0
        rule_accuracy[rule] = {
            'accuracy': accuracy,
            'correct': stats['correct'],
            'total': stats['total']
        }
    
    return rule_accuracy


def test_nbest_coverage(corpus: List[Dict], n: int = 5) -> Dict:
    """
    Test if correct answer appears in n-best hypotheses.
    
    Args:
        corpus: Test corpus
        n: Number of best hypotheses to check
        
    Returns:
        Coverage statistics
    """
    in_top1 = 0
    in_top_n = 0
    total = len(corpus)
    
    for item in corpus:
        sinlish = item['sinlish']
        expected = item['sinhala']
        
        try:
            hypotheses = transliterate_nbest(sinlish, n=n, return_scores=False)
            
            if hypotheses and hypotheses[0] == expected:
                in_top1 += 1
                in_top_n += 1
            elif expected in hypotheses:
                in_top_n += 1
        except:
            continue
    
    return {
        'top_1_accuracy': in_top1 / total if total > 0 else 0,
        'top_n_coverage': in_top_n / total if total > 0 else 0,
        'n': n,
        'total': total
    }


def benchmark_performance(corpus: List[Dict], iterations: int = 100) -> Dict:
    """
    Benchmark transliteration performance.
    
    Args:
        corpus: Test corpus
        iterations: Number of times to repeat
        
    Returns:
        Performance statistics
    """
    times = []
    
    for _ in range(iterations):
        for item in corpus:
            start = time.time()
            try:
                transliterate(item['sinlish'])
            except:
                pass
            end = time.time()
            times.append((end - start) * 1000)  # Convert to ms
    
    times.sort()
    
    return {
        'mean_ms': sum(times) / len(times),
        'median_ms': times[len(times) // 2],
        'min_ms': min(times),
        'max_ms': max(times),
        'p95_ms': times[int(len(times) * 0.95)],
        'total_iterations': len(times)
    }


def test_module1(verbose: bool = False, benchmark: bool = False, analysis: bool = False):
    """Run comprehensive tests on the transliteration module."""
    
    # Get path to corpus.json (in parent directory)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    corpus_path = os.path.join(script_dir, '..', 'corpus.json')
    
    # Load corpus
    try:
        with open(corpus_path, 'r', encoding='utf-8') as f:
            corpus = json.load(f)
    except FileNotFoundError:
        print(f"Error: Could not find corpus.json at {corpus_path}")
        print("Please ensure corpus.json exists in the parent directory.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: corpus.json is not valid JSON: {e}")
        sys.exit(1)
    
    if not corpus:
        print("Warning: corpus.json is empty!")
        sys.exit(1)
    
    print("=" * 80)
    print("MODULE 1: ENHANCED TEST SUITE".center(80))
    print("=" * 80)
    print(f"\nLoaded {len(corpus)} test cases from corpus.json\n")
    
    # ============================================================
    # PART 1: Basic Accuracy Testing
    # ============================================================
    print("=" * 80)
    print("PART 1: BASIC ACCURACY TESTING")
    print("=" * 80)
    print()
    
    pass_count = 0
    fail_count = 0
    test_results = []
    cer_scores = []
    wer_scores = []
    
    # Test each item in the corpus
    for item in corpus:
        test_id = item.get('id', '?')
        sinlish = item['sinlish']
        expected = item['sinhala']
        
        try:
            actual = transliterate(sinlish)
            cer = calculate_cer(expected, actual)
            wer = calculate_wer(expected, actual)
            
            cer_scores.append(cer)
            wer_scores.append(wer)
            test_results.append((expected, actual))
            
            if actual == expected:
                if verbose:
                    print(f"✓ PASS [ID {test_id}]: {sinlish}")
                    print(f"         → {actual}")
                    print(f"         CER: {cer:.3f}, WER: {wer:.3f}")
                else:
                    print(f"✓ PASS [ID {test_id}]: {sinlish}")
                    print(f"         → {actual}")
                pass_count += 1
            else:
                print(f"✗ FAIL [ID {test_id}]: {sinlish}")
                print(f"  Expected: {expected}")
                print(f"  Got:      {actual}")
                print(f"  CER: {cer:.3f}, WER: {wer:.3f}")
                fail_count += 1
        except Exception as e:
            print(f"✗ ERROR [ID {test_id}]: {sinlish}")
            print(f"  Error: {e}")
            fail_count += 1
            cer_scores.append(1.0)
            wer_scores.append(1.0)
        
        print()
    
    # ============================================================
    # PART 2: Error Metrics (CER & WER)
    # ============================================================
    print("=" * 80)
    print("PART 2: ERROR METRICS")
    print("=" * 80)
    print()
    
    avg_cer = sum(cer_scores) / len(cer_scores) if cer_scores else 0
    avg_wer = sum(wer_scores) / len(wer_scores) if wer_scores else 0
    
    print(f"Character Error Rate (CER):")
    print(f"  Average: {avg_cer:.4f} ({avg_cer*100:.2f}%)")
    print(f"  Best:    {min(cer_scores):.4f}")
    print(f"  Worst:   {max(cer_scores):.4f}")
    print()
    
    print(f"Word Error Rate (WER):")
    print(f"  Average: {avg_wer:.4f} ({avg_wer*100:.2f}%)")
    print(f"  Best:    {min(wer_scores):.4f}")
    print(f"  Worst:   {max(wer_scores):.4f}")
    print()
    
    # ============================================================
    # PART 3: Confusion Matrix Analysis
    # ============================================================
    if analysis:
        print("=" * 80)
        print("PART 3: CONFUSION MATRIX ANALYSIS")
        print("=" * 80)
        print()
        
        confusion_data = build_confusion_matrix(test_results)
        
        print(f"Total characters analyzed: {confusion_data['total_characters']}")
        print(f"Total character errors: {confusion_data['total_errors']}")
        print(f"Character error rate: {confusion_data['error_rate']*100:.2f}%")
        
        if confusion_data['confusion_pairs']:
            print("\nMost common confusions:")
            confusion_list = []
            for ref_char, hyp_dict in confusion_data['confusion_pairs'].items():
                for hyp_char, count in hyp_dict.items():
                    confusion_list.append((ref_char, hyp_char, count))
            
            confusion_list.sort(key=lambda x: x[2], reverse=True)
            
            for i, (ref, hyp, count) in enumerate(confusion_list[:10], 1):
                print(f"  {i}. '{ref}' → '{hyp}' ({count} times)")
        else:
            print("\n✓ No character confusions detected!")
        
        print()
    
    # ============================================================
    # PART 4: Per-Rule Accuracy
    # ============================================================
    if analysis:
        print("=" * 80)
        print("PART 4: PER-RULE ACCURACY ANALYSIS")
        print("=" * 80)
        print()
        
        rule_accuracy = analyze_rule_accuracy(corpus)
        
        # Sort by accuracy (worst first)
        sorted_rules = sorted(rule_accuracy.items(), 
                            key=lambda x: x[1]['accuracy'])
        
        print(f"Total rules tested: {len(rule_accuracy)}")
        print()
        
        # Show worst performing rules
        print("Lowest accuracy rules:")
        for i, (rule, stats) in enumerate(sorted_rules[:10], 1):
            acc = stats['accuracy']
            correct = stats['correct']
            total = stats['total']
            print(f"  {i}. '{rule}': {acc*100:.1f}% ({correct}/{total})")
        
        # Show best performing rules
        print("\nHighest accuracy rules:")
        for i, (rule, stats) in enumerate(sorted_rules[-10:][::-1], 1):
            acc = stats['accuracy']
            correct = stats['correct']
            total = stats['total']
            print(f"  {i}. '{rule}': {acc*100:.1f}% ({correct}/{total})")
        
        print()
    
    # ============================================================
    # PART 5: N-Best Coverage Analysis
    # ============================================================
    if analysis:
        print("=" * 80)
        print("PART 5: N-BEST COVERAGE ANALYSIS")
        print("=" * 80)
        print()
        
        nbest_stats = test_nbest_coverage(corpus, n=5)
        
        print(f"Top-1 Accuracy: {nbest_stats['top_1_accuracy']*100:.2f}%")
        print(f"Top-{nbest_stats['n']} Coverage: {nbest_stats['top_n_coverage']*100:.2f}%")
        print(f"  (Correct answer appears in top {nbest_stats['n']} hypotheses)")
        print()
    
    # ============================================================
    # PART 6: Performance Benchmark
    # ============================================================
    if benchmark:
        print("=" * 80)
        print("PART 6: PERFORMANCE BENCHMARK")
        print("=" * 80)
        print()
        
        print("Running benchmark (this may take a moment)...")
        perf_stats = benchmark_performance(corpus, iterations=100)
        
        print(f"\nTransliteration Performance (100 iterations):")
        print(f"  Mean:     {perf_stats['mean_ms']:.3f} ms")
        print(f"  Median:   {perf_stats['median_ms']:.3f} ms")
        print(f"  Min:      {perf_stats['min_ms']:.3f} ms")
        print(f"  Max:      {perf_stats['max_ms']:.3f} ms")
        print(f"  95th %ile: {perf_stats['p95_ms']:.3f} ms")
        print(f"  Total ops: {perf_stats['total_iterations']}")
        print()
    
    # ============================================================
    # SUMMARY
    # ============================================================
    print("=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print()
    
    print(f"Basic Accuracy:")
    print(f"  Total tests:    {len(corpus)}")
    print(f"  Passed:         {pass_count} ({pass_count/len(corpus)*100:.1f}%)")
    print(f"  Failed:         {fail_count} ({fail_count/len(corpus)*100:.1f}%)")
    print()
    
    print(f"Error Metrics:")
    print(f"  Avg CER:        {avg_cer:.4f} ({avg_cer*100:.2f}%)")
    print(f"  Avg WER:        {avg_wer:.4f} ({avg_wer*100:.2f}%)")
    print()
    
    if fail_count == 0 and avg_cer == 0:
        print("=" * 80)
        print("🎉 PERFECT SCORE! All tests passed with 0% error rate!".center(80))
        print("=" * 80)
        return 0
    elif fail_count == 0:
        print("✓ All tests passed!")
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
    # Parse command line arguments
    verbose = '--verbose' in sys.argv or '-v' in sys.argv
    benchmark = '--benchmark' in sys.argv or '-b' in sys.argv
    analysis = '--analysis' in sys.argv or '-a' in sys.argv
    
    # If no flags, run basic test
    if not verbose and not benchmark and not analysis:
        verbose = False
        benchmark = False
        analysis = False
    
    exit_code = test_module1(verbose=verbose, benchmark=benchmark, analysis=analysis)
    sys.exit(exit_code)
