"""
Ambiguity Analyzer for FST Transliteration
Student 1 - Module 1 Enhancement

This module analyzes and reports transliteration ambiguities in the FST system.
Ambiguity occurs when multiple valid paths exist through the FST for a given input,
resulting in different possible transliterations.

Theoretical Background:
    Non-deterministic FSTs can have multiple paths from initial to final states
    for the same input. This is common in transliteration due to:
    1. Overlapping rules (e.g., "th" vs "t" + "h")
    2. Alternative representations (e.g., "a" can be initial or medial vowel)
    3. Context-free rule application
    
    Mathematically: For input w, if |{δ*(q0, w)}| > 1, then w is ambiguous
    where δ* is the extended transition function.

Usage:
    python ambiguity_analyzer.py
    
    Or programmatically:
        from ambiguity_analyzer import analyze_ambiguity, find_conflicts
        
        ambiguities = analyze_ambiguity("mama gedara")
        conflicts = find_conflicts()
"""

import json
import os
import sys
from typing import Dict, List, Tuple, Set
from collections import defaultdict

# Add parent directory to path for module1 import
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from module1 import transliterate_nbest, transliterate
except ImportError as e:
    print(f"Error: Could not import module1. Make sure build_fst.py has been run.")
    print(f"Details: {e}")
    sys.exit(1)


def load_rules() -> Dict[str, str]:
    """Load transliteration rules from JSON file."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    rules_path = os.path.join(script_dir, '..', 'singlish_rules.json')
    
    with open(rules_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def find_rule_conflicts() -> Dict[str, List[Tuple[str, str]]]:
    """
    Detect conflicting rules that may cause ambiguity.
    
    Identifies cases where one rule is a prefix/suffix of another,
    or where multiple rules match overlapping sequences.
    
    Returns:
        Dictionary mapping input patterns to conflicting rules
        Format: {pattern: [(rule1, output1), (rule2, output2), ...]}
    
    Example:
        {
            'th': [('th', 'ත්'), ('t', 'ත්'), ('h', 'හ්')],
            'ka': [('ka', 'ක'), ('k', 'ක්'), ('a', 'අ')]
        }
    """
    rules = load_rules()
    conflicts = defaultdict(list)
    
    # Check for prefix/substring conflicts
    for rule1, output1 in rules.items():
        for rule2, output2 in rules.items():
            if rule1 != rule2:
                # Check if rule1 is a prefix of rule2 or vice versa
                if rule1.startswith(rule2) or rule2.startswith(rule1):
                    longer = rule1 if len(rule1) > len(rule2) else rule2
                    conflicts[longer].append((rule1, output1))
                    conflicts[longer].append((rule2, output2))
    
    # Remove duplicates and sort
    for pattern in conflicts:
        conflicts[pattern] = list(set(conflicts[pattern]))
        conflicts[pattern].sort(key=lambda x: len(x[0]), reverse=True)
    
    return dict(conflicts)


def analyze_word_ambiguity(word: str, n_hypotheses: int = 10) -> Dict:
    """
    Analyze a single word for transliteration ambiguity.
    
    Args:
        word: Input word to analyze
        n_hypotheses: Number of alternative hypotheses to generate
        
    Returns:
        Dictionary containing:
        - 'word': input word
        - 'is_ambiguous': whether multiple hypotheses exist
        - 'num_hypotheses': count of distinct transliterations
        - 'hypotheses': list of (transliteration, confidence) tuples
        - 'entropy': measure of ambiguity (higher = more ambiguous)
    """
    try:
        hypotheses = transliterate_nbest(word, n=n_hypotheses, return_scores=True)
        
        # Calculate entropy as measure of ambiguity
        # H = -Σ(p * log2(p)) where p is confidence score
        import math
        entropy = 0.0
        if len(hypotheses) > 1:
            total_score = sum(score for _, score in hypotheses)
            if total_score > 0:
                for _, score in hypotheses:
                    p = score / total_score
                    if p > 0:
                        entropy -= p * math.log2(p)
        
        return {
            'word': word,
            'is_ambiguous': len(set(h[0] for h in hypotheses)) > 1,
            'num_hypotheses': len(set(h[0] for h in hypotheses)),
            'hypotheses': hypotheses,
            'entropy': round(entropy, 3)
        }
    except Exception as e:
        return {
            'word': word,
            'is_ambiguous': False,
            'num_hypotheses': 0,
            'hypotheses': [],
            'entropy': 0.0,
            'error': str(e)
        }


def analyze_corpus_ambiguity(corpus_path: str = None) -> Dict:
    """
    Analyze entire corpus for ambiguity patterns.
    
    Args:
        corpus_path: Path to corpus.json (default: ../corpus.json)
        
    Returns:
        Dictionary with corpus-wide ambiguity statistics
    """
    if corpus_path is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        corpus_path = os.path.join(script_dir, '..', 'corpus.json')
    
    with open(corpus_path, 'r', encoding='utf-8') as f:
        corpus = json.load(f)
    
    total_words = 0
    ambiguous_words = 0
    word_analyses = []
    
    for item in corpus:
        sinlish = item['sinlish']
        words = sinlish.split()
        
        for word in words:
            total_words += 1
            analysis = analyze_word_ambiguity(word, n_hypotheses=5)
            
            if analysis['is_ambiguous']:
                ambiguous_words += 1
                word_analyses.append(analysis)
    
    ambiguity_rate = ambiguous_words / total_words if total_words > 0 else 0
    
    return {
        'total_words': total_words,
        'ambiguous_words': ambiguous_words,
        'ambiguity_rate': round(ambiguity_rate, 3),
        'high_ambiguity_words': sorted(word_analyses, key=lambda x: x['entropy'], reverse=True)[:10],
        'rule_conflicts': find_rule_conflicts()
    }


def print_ambiguity_report(analysis: Dict):
    """
    Pretty-print ambiguity analysis results.
    
    Args:
        analysis: Output from analyze_corpus_ambiguity()
    """
    print("=" * 70)
    print("AMBIGUITY ANALYSIS REPORT")
    print("=" * 70)
    
    print(f"\nCorpus Statistics:")
    print(f"  Total words analyzed: {analysis['total_words']}")
    print(f"  Ambiguous words: {analysis['ambiguous_words']}")
    print(f"  Ambiguity rate: {analysis['ambiguity_rate']*100:.1f}%")
    
    if analysis['high_ambiguity_words']:
        print(f"\nTop 10 Most Ambiguous Words:")
        print("-" * 70)
        for i, word_analysis in enumerate(analysis['high_ambiguity_words'], 1):
            print(f"\n{i}. Word: '{word_analysis['word']}' (Entropy: {word_analysis['entropy']:.3f})")
            print(f"   Hypotheses: {word_analysis['num_hypotheses']}")
            for j, (hyp, score) in enumerate(word_analysis['hypotheses'][:3], 1):
                print(f"      {j}. {hyp:20} (confidence: {score:.3f})")
    
    if analysis['rule_conflicts']:
        print(f"\nRule Conflicts Detected:")
        print("-" * 70)
        conflict_count = len(analysis['rule_conflicts'])
        print(f"  Total conflicting patterns: {conflict_count}")
        
        # Show first 5 conflicts
        for i, (pattern, rules) in enumerate(list(analysis['rule_conflicts'].items())[:5], 1):
            print(f"\n{i}. Pattern: '{pattern}'")
            print(f"   Conflicting rules:")
            for rule, output in rules:
                print(f"      '{rule}' → '{output}'")
        
        if conflict_count > 5:
            print(f"\n   ... and {conflict_count - 5} more conflicts")
    
    print("\n" + "=" * 70)


def main():
    """Main function for standalone execution."""
    print("Analyzing transliteration ambiguity...")
    print()
    
    # Analyze corpus
    try:
        analysis = analyze_corpus_ambiguity()
        print_ambiguity_report(analysis)
        
        # Additional interactive analysis
        print("\nInteractive Ambiguity Check:")
        print("-" * 70)
        print("Enter words to check for ambiguity (or 'quit' to exit)")
        
        while True:
            try:
                word = input("\nWord: ").strip()
                if word.lower() in ['quit', 'exit', 'q']:
                    break
                
                if not word:
                    continue
                
                result = analyze_word_ambiguity(word, n_hypotheses=10)
                
                print(f"\nAnalysis for '{word}':")
                print(f"  Ambiguous: {result['is_ambiguous']}")
                print(f"  Hypotheses: {result['num_hypotheses']}")
                print(f"  Entropy: {result['entropy']:.3f}")
                
                if result['hypotheses']:
                    print(f"\n  Top hypotheses:")
                    for i, (hyp, score) in enumerate(result['hypotheses'][:5], 1):
                        print(f"    {i}. {hyp:20} (confidence: {score:.3f})")
            
            except KeyboardInterrupt:
                print("\n\nExiting...")
                break
            except Exception as e:
                print(f"Error: {e}")
    
    except FileNotFoundError as e:
        print(f"Error: Could not find required files.")
        print(f"Make sure corpus.json and singlish_rules.json exist.")
        print(f"Details: {e}")
    except Exception as e:
        print(f"Error during analysis: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

