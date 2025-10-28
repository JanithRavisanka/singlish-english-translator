"""
Rule Usage Statistics and Coverage Analyzer
Student 1 - Module 1 Enhancement

Analyzes transliteration rules to identify usage patterns, coverage gaps,
unused rules, and potential conflicts. Essential for FST optimization and
linguistic analysis.

Theoretical Background:
    Rule coverage analysis determines the effectiveness of the transduction
    mapping Σ → Γ. A comprehensive rule set should maximize coverage C where:
    
    C = |transliterated_words| / |total_words|
    
    This module also computes rule frequency distributions and identifies
    underutilized rules that may indicate over-specification or data sparsity.

Usage:
    python rule_analyzer.py
    
    Or programmatically:
        from rule_analyzer import analyze_rule_usage, find_unused_rules
"""

import json
import os
import sys
from typing import Dict, List, Tuple, Set
from collections import Counter, defaultdict

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from module1 import transliterate, get_alignment
except ImportError as e:
    print(f"Error: Could not import module1")
    sys.exit(1)


def load_rules() -> Dict[str, str]:
    """Load transliteration rules from JSON."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    rules_path = os.path.join(script_dir, '..', 'singlish_rules.json')
    
    with open(rules_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_corpus() -> List[Dict]:
    """Load corpus from JSON."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    corpus_path = os.path.join(script_dir, '..', 'corpus.json')
    
    with open(corpus_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def analyze_rule_usage(corpus_path: str = None) -> Dict:
    """
    Analyze which rules are actually used in corpus transliteration.
    
    Args:
        corpus_path: Path to corpus (default: ../corpus.json)
        
    Returns:
        Dictionary with comprehensive rule usage statistics
    """
    rules = load_rules()
    corpus = load_corpus()
    
    rule_usage = Counter()
    rule_contexts = defaultdict(list)  # Track where each rule is used
    
    # Process corpus
    for item in corpus:
        sinlish = item['sinlish']
        try:
            alignment = get_alignment(sinlish)
            
            for inp, out in alignment:
                if inp in rules and rules[inp] == out:
                    rule_usage[inp] += 1
                    rule_contexts[inp].append({
                        'sentence': sinlish,
                        'context': inp,
                        'id': item['id']
                    })
        except:
            continue
    
    # Calculate statistics
    total_rules = len(rules)
    used_rules = len(rule_usage)
    unused_rules = total_rules - used_rules
    
    # Categorize rules by length
    rule_categories = {
        'single_char': 0,
        'bigrams': 0,
        'trigrams': 0,
        'words': 0
    }
    
    for rule in rules.keys():
        if len(rule) == 1:
            rule_categories['single_char'] += 1
        elif len(rule) == 2:
            rule_categories['bigrams'] += 1
        elif len(rule) == 3:
            rule_categories['trigrams'] += 1
        else:
            rule_categories['words'] += 1
    
    return {
        'total_rules': total_rules,
        'used_rules': used_rules,
        'unused_rules': unused_rules,
        'coverage_rate': round(used_rules / total_rules, 3) if total_rules > 0 else 0,
        'rule_usage': dict(rule_usage),
        'rule_contexts': dict(rule_contexts),
        'rule_categories': rule_categories,
        'most_common': rule_usage.most_common(20),
        'least_common': [(r, c) for r, c in rule_usage.items() if c == 1]
    }


def find_unused_rules() -> List[str]:
    """
    Identify rules that are never used in corpus.
    
    Returns:
        List of unused rule patterns
    """
    analysis = analyze_rule_usage()
    rules = load_rules()
    
    used_rules = set(analysis['rule_usage'].keys())
    all_rules = set(rules.keys())
    
    unused = list(all_rules - used_rules)
    unused.sort()
    
    return unused


def identify_coverage_gaps() -> Dict:
    """
    Identify character sequences in corpus that aren't covered by rules.
    
    Returns:
        Dictionary with gap analysis
    """
    rules = load_rules()
    corpus = load_corpus()
    
    # Extract all n-grams from corpus
    corpus_ngrams = defaultdict(int)
    
    for item in corpus:
        text = item['sinlish']
        # Generate all n-grams (1 to 10 characters)
        for n in range(1, min(11, len(text) + 1)):
            for i in range(len(text) - n + 1):
                ngram = text[i:i+n]
                if ngram.strip():  # Ignore pure whitespace
                    corpus_ngrams[ngram] += 1
    
    # Find gaps (ngrams not in rules)
    gaps = []
    for ngram, freq in corpus_ngrams.items():
        if ngram not in rules and ngram != ' ':
            gaps.append((ngram, freq))
    
    # Sort by frequency
    gaps.sort(key=lambda x: x[1], reverse=True)
    
    return {
        'total_gaps': len(gaps),
        'top_gaps': gaps[:20],
        'single_char_gaps': [g for g, f in gaps if len(g) == 1],
        'multi_char_gaps': [g for g, f in gaps if len(g) > 1]
    }


def generate_rule_frequency_histogram() -> Dict[str, int]:
    """
    Generate histogram of rule usage frequencies.
    
    Returns:
        Dictionary mapping frequency ranges to counts
    """
    analysis = analyze_rule_usage()
    usage = analysis['rule_usage']
    
    histogram = {
        '1': 0,        # Used once
        '2-5': 0,      # Used 2-5 times
        '6-10': 0,     # Used 6-10 times
        '11-20': 0,    # Used 11-20 times
        '21-50': 0,    # Used 21-50 times
        '50+': 0       # Used 50+ times
    }
    
    for rule, count in usage.items():
        if count == 1:
            histogram['1'] += 1
        elif count <= 5:
            histogram['2-5'] += 1
        elif count <= 10:
            histogram['6-10'] += 1
        elif count <= 20:
            histogram['11-20'] += 1
        elif count <= 50:
            histogram['21-50'] += 1
        else:
            histogram['50+'] += 1
    
    return histogram


def print_analysis_report(analysis: Dict):
    """
    Print comprehensive rule analysis report.
    
    Args:
        analysis: Output from analyze_rule_usage()
    """
    print("=" * 80)
    print("RULE USAGE ANALYSIS REPORT")
    print("=" * 80)
    
    print(f"\nOverview:")
    print(f"  Total rules defined:      {analysis['total_rules']}")
    print(f"  Rules used in corpus:     {analysis['used_rules']}")
    print(f"  Unused rules:             {analysis['unused_rules']}")
    print(f"  Coverage rate:            {analysis['coverage_rate']*100:.1f}%")
    
    print(f"\nRule Categories:")
    for category, count in analysis['rule_categories'].items():
        percentage = (count / analysis['total_rules']) * 100
        print(f"  {category:20} {count:4} ({percentage:5.1f}%)")
    
    print(f"\nMost Frequently Used Rules:")
    print("-" * 80)
    print(f"  {'Rank':<6} {'Rule':<15} {'Output':<15} {'Count':<8} {'Percentage':<10}")
    print("-" * 80)
    
    rules = load_rules()
    total_usage = sum(analysis['rule_usage'].values())
    
    for i, (rule, count) in enumerate(analysis['most_common'][:15], 1):
        output = rules.get(rule, '?')
        percentage = (count / total_usage) * 100 if total_usage > 0 else 0
        print(f"  {i:<6} {rule:<15} {output:<15} {count:<8} {percentage:5.1f}%")
    
    # Frequency histogram
    histogram = generate_rule_frequency_histogram()
    print(f"\nRule Usage Frequency Distribution:")
    print("-" * 80)
    print(f"  {'Frequency Range':<20} {'Rule Count':<15}")
    print("-" * 80)
    for freq_range, count in histogram.items():
        print(f"  {freq_range:<20} {count:<15}")
    
    # Unused rules
    unused = find_unused_rules()
    if unused:
        print(f"\nUnused Rules ({len(unused)} total):")
        print("-" * 80)
        print("  First 20 unused rules:")
        for i, rule in enumerate(unused[:20], 1):
            output = rules.get(rule, '?')
            print(f"    {i:2}. '{rule}' → '{output}'")
        if len(unused) > 20:
            print(f"    ... and {len(unused) - 20} more")
    
    # Coverage gaps
    gaps = identify_coverage_gaps()
    if gaps['total_gaps'] > 0:
        print(f"\nCoverage Gaps:")
        print("-" * 80)
        print(f"  Total uncovered sequences: {gaps['total_gaps']}")
        print(f"\n  Top 10 missing patterns (by frequency):")
        for i, (pattern, freq) in enumerate(gaps['top_gaps'][:10], 1):
            print(f"    {i:2}. '{pattern}' (appears {freq} times)")
    
    print("\n" + "=" * 80)


def recommend_rule_improvements() -> List[str]:
    """
    Generate recommendations for rule set improvement.
    
    Returns:
        List of recommendation strings
    """
    recommendations = []
    
    analysis = analyze_rule_usage()
    gaps = identify_coverage_gaps()
    unused = find_unused_rules()
    
    # Check coverage
    if analysis['coverage_rate'] < 0.7:
        recommendations.append(
            f"⚠️  Low rule coverage ({analysis['coverage_rate']*100:.1f}%). "
            f"Consider adding more rules or reviewing corpus."
        )
    
    # Check unused rules
    if len(unused) > analysis['total_rules'] * 0.3:
        recommendations.append(
            f"ℹ️  {len(unused)} rules ({len(unused)/analysis['total_rules']*100:.1f}%) "
            f"are unused. Consider removing redundant rules."
        )
    
    # Check gaps
    if gaps['single_char_gaps']:
        recommendations.append(
            f"⚠️  {len(gaps['single_char_gaps'])} single characters are not covered: "
            f"{gaps['single_char_gaps'][:5]}..."
        )
    
    # Check frequency distribution
    histogram = generate_rule_frequency_histogram()
    if histogram['1'] > analysis['used_rules'] * 0.5:
        recommendations.append(
            f"ℹ️  Many rules ({histogram['1']}) are used only once. "
            f"Corpus may be too small or rules too specific."
        )
    
    return recommendations


def main():
    """Main function for standalone execution."""
    try:
        print("Analyzing transliteration rules...\n")
        
        # Run analysis
        analysis = analyze_rule_usage()
        print_analysis_report(analysis)
        
        # Print recommendations
        recommendations = recommend_rule_improvements()
        if recommendations:
            print("\nRECOMMENDATIONS:")
            print("-" * 80)
            for rec in recommendations:
                print(f"  {rec}")
            print()
        
    except FileNotFoundError as e:
        print(f"Error: Required files not found.")
        print(f"Make sure corpus.json and singlish_rules.json exist.")
        print(f"Details: {e}")
    except Exception as e:
        print(f"Error during analysis: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

