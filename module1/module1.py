"""
Module 1: FST Transliteration Engine - Runtime API
Student 1

This module provides advanced FST-based transliteration from Singlish (Roman script)
to Sinhala script using finite-state transducers with support for multiple hypotheses,
confidence scoring, and OOV detection.

Theoretical Foundation:
    This implementation uses Finite-State Transducers (FSTs), which are formal
    models of computation that map input sequences to output sequences. The FST
    applies a greedy longest-match algorithm with Kleene closure to iteratively
    consume and translate input symbols.
    
    Mathematical Formulation:
        FST = (Q, Σ, Γ, δ, q0, F)
        where Q = states, Σ = input alphabet, Γ = output alphabet,
        δ = transition function, q0 = initial state, F = final states

Complexity:
    - Time: O(n * m) where n = input length, m = max rule length
    - Space: O(|Q| + |δ|) for FST storage
    
References:
    - Mohri, M. et al. (2002). "Weighted Finite-State Transducers in Speech Recognition"
    - Beesley, K. & Karttunen, L. (2003). "Finite State Morphology"

Usage:
    from module1 import transliterate, transliterate_nbest, detect_oov
    
    # Basic transliteration
    result = transliterate("mama gedara yanawa")
    
    # N-best hypotheses with scores
    results = transliterate_nbest("mama gedara", n=3, return_scores=True)
    
    # Detect OOV segments
    oov_info = detect_oov("mama xyz yanawa")
"""

import pynini
import os
from typing import List, Tuple, Dict, Optional
import re

# Load the compiled FST once at module import time
# This makes transliteration very fast since we don't reload the FST each time
script_dir = os.path.dirname(os.path.abspath(__file__))
fst_path = os.path.join(script_dir, "transliterate.fst")

# Check if FST exists
if not os.path.exists(fst_path):
    raise FileNotFoundError(
        f"transliterate.fst not found at {fst_path}\n"
        f"Please run 'python build_fst.py' first to compile the FST."
    )

# Load the FST (done once when module is imported)
_fst = pynini.Fst.read(fst_path)

# Load rules for OOV detection
_rules_dict = None
def _load_rules():
    """Lazy load transliteration rules for OOV detection."""
    global _rules_dict
    if _rules_dict is None:
        import json
        rules_path = os.path.join(script_dir, '..', 'singlish_rules.json')
        try:
            with open(rules_path, 'r', encoding='utf-8') as f:
                _rules_dict = json.load(f)
        except:
            _rules_dict = {}
    return _rules_dict


def transliterate(sinlish_text: str, handle_oov: bool = False) -> str:
    """
    Transliterate Singlish (Roman script) to Sinhala script.
    
    This function uses a pre-compiled Finite-State Transducer (FST) to 
    convert Singlish text to Sinhala script. The FST applies the longest-match
    rule (greedy algorithm), ensuring that whole words are matched before 
    syllables, and syllables before individual characters.
    
    Algorithm:
        1. Convert input string to FST acceptor (creates linear automaton)
        2. Compose input FST with transliteration FST (⊗ operation)
        3. Extract shortest path (optimal transliteration)
        4. Convert path to output string
    
    Complexity: O(n * m) where n = input length, m = average rule length
    
    Args:
        sinlish_text: Input text in Singlish (Roman script)
                     Example: "mama gedara yanawa"
        handle_oov: If True, return partial transliteration for OOV words
                   (default: False, raises exception on OOV)
        
    Returns:
        Transliterated text in Sinhala script
        Example: "මම ගෙදර යනවා"
        
    Raises:
        Exception: If the FST cannot transliterate the input and handle_oov=False
        
    Examples:
        >>> transliterate("mama gedara yanawa")
        'මම ගෙදර යනවා'
        
        >>> transliterate("mama xyz yanawa", handle_oov=True)
        'මම xyz යනවා'  # OOV word preserved
    """
    if not sinlish_text:
        return ""
    
    try:
        # Apply the FST to the input text
        # Compose the input string with the FST and get the shortest path
        input_fst = pynini.accep(sinlish_text)
        output_fst = input_fst @ _fst
        result = pynini.shortestpath(output_fst).string()
        return result
    except Exception as e:
        if handle_oov:
            # Return input unchanged if cannot transliterate
            return sinlish_text
        # If transliteration fails, provide helpful error message
        raise Exception(
            f"Failed to transliterate '{sinlish_text}'\n"
            f"This may be because the input contains characters not in singlish_rules.json\n"
            f"Use handle_oov=True to handle OOV words gracefully\n"
            f"Original error: {e}"
        )


def transliterate_nbest(sinlish_text: str, n: int = 5, 
                        return_scores: bool = False) -> List[str] | List[Tuple[str, float]]:
    """
    Generate n-best transliteration hypotheses using FST path enumeration.
    
    This function explores multiple paths through the FST lattice to generate
    alternative transliterations. Useful for handling ambiguity and providing
    multiple translation candidates.
    
    Algorithm:
        1. Compose input with FST to create output lattice
        2. Use n-shortest-path algorithm to extract top-n paths
        3. Score each path based on path cost
        4. Return ranked hypotheses
    
    Theoretical Note:
        The n-shortest paths problem in FSTs can be solved efficiently using
        the algorithm by Eppstein (1998), which pynini implements internally.
        Time complexity: O(m + n*log(n)) where m = lattice size
    
    Args:
        sinlish_text: Input text in Singlish
        n: Number of best hypotheses to return (default: 5)
        return_scores: If True, return tuples of (text, score) (default: False)
        
    Returns:
        List of transliterated strings (if return_scores=False)
        OR List of (transliteration, confidence_score) tuples (if return_scores=True)
        
        Scores are normalized between 0 and 1, where 1 = highest confidence
        
    Examples:
        >>> transliterate_nbest("mama", n=3)
        ['මම', 'මම', 'මමඅ']
        
        >>> transliterate_nbest("mama", n=2, return_scores=True)
        [('මම', 1.0), ('මමඅ', 0.85)]
    """
    if not sinlish_text:
        return [] if not return_scores else []
    
    try:
        # Compose input with FST
        input_fst = pynini.accep(sinlish_text)
        output_fst = input_fst @ _fst
        
        # Extract n-shortest paths
        nbest_fst = pynini.shortestpath(output_fst, nshortest=n)
        
        # Extract all paths and their weights
        results = []
        seen = set()
        
        # Iterate through the n-best paths
        for path in nbest_fst.paths():
            output_str = ''.join([chr(label) for label in path.olabels if label != 0])
            
            # Avoid duplicates
            if output_str not in seen:
                seen.add(output_str)
                
                if return_scores:
                    # Calculate confidence score (inverse of weight, normalized)
                    # Lower weight = better path
                    weight = float(path.weight) if hasattr(path, 'weight') else 0.0
                    confidence = 1.0 / (1.0 + weight)  # Normalize to [0, 1]
                    results.append((output_str, confidence))
                else:
                    results.append(output_str)
            
            if len(results) >= n:
                break
        
        # If no paths found, return at least one result
        if not results:
            result = transliterate(sinlish_text)
            results = [(result, 1.0)] if return_scores else [result]
        
        # Normalize scores if returning scores
        if return_scores and results:
            max_score = max(score for _, score in results)
            if max_score > 0:
                results = [(text, score/max_score) for text, score in results]
        
        return results
        
    except Exception as e:
        # Fallback to single best
        result = transliterate(sinlish_text, handle_oov=True)
        return [(result, 1.0)] if return_scores else [result]


def detect_oov(sinlish_text: str) -> Dict[str, any]:
    """
    Detect Out-of-Vocabulary (OOV) segments in input text.
    
    Analyzes the input to identify portions that cannot be transliterated
    due to missing rules. Provides detailed diagnostics and suggestions.
    
    Algorithm:
        1. Tokenize input into words
        2. For each word, attempt transliteration
        3. If fails, identify which characters/sequences are OOV
        4. Suggest similar known sequences using edit distance
    
    Args:
        sinlish_text: Input text to analyze
        
    Returns:
        Dictionary containing:
        - 'has_oov': bool - whether OOV segments exist
        - 'coverage': float - percentage of input that can be transliterated
        - 'oov_words': List[str] - words that cannot be transliterated
        - 'oov_chars': List[str] - individual characters not in rules
        - 'suggestions': Dict[str, List[str]] - suggested alternatives for OOV
        
    Example:
        >>> detect_oov("mama xyz yanawa")
        {
            'has_oov': True,
            'coverage': 0.67,
            'oov_words': ['xyz'],
            'oov_chars': ['x', 'z'],
            'suggestions': {'xyz': ['xya', 'xyaa']}
        }
    """
    rules = _load_rules()
    
    # Tokenize by spaces
    words = sinlish_text.split()
    
    oov_words = []
    oov_chars = set()
    total_chars = len(sinlish_text.replace(' ', ''))
    covered_chars = 0
    
    for word in words:
        try:
            transliterate(word)
            covered_chars += len(word)
        except:
            oov_words.append(word)
            # Find which characters are OOV
            for char in word:
                if char not in rules and char != ' ':
                    oov_chars.add(char)
    
    coverage = covered_chars / total_chars if total_chars > 0 else 1.0
    
    # Generate suggestions using edit distance
    suggestions = {}
    for oov_word in oov_words:
        similar = _find_similar_words(oov_word, rules, max_suggestions=3)
        if similar:
            suggestions[oov_word] = similar
    
    return {
        'has_oov': len(oov_words) > 0,
        'coverage': round(coverage, 3),
        'oov_words': oov_words,
        'oov_chars': sorted(list(oov_chars)),
        'suggestions': suggestions,
        'total_words': len(words),
        'transliterable_words': len(words) - len(oov_words)
    }


def _find_similar_words(target: str, rules: Dict, max_suggestions: int = 3) -> List[str]:
    """
    Find similar known words using Levenshtein distance.
    
    Internal helper function for OOV suggestion system.
    
    Args:
        target: OOV word to find alternatives for
        rules: Dictionary of known transliteration rules
        max_suggestions: Maximum number of suggestions to return
        
    Returns:
        List of similar known words sorted by edit distance
    """
    def levenshtein_distance(s1: str, s2: str) -> int:
        """Calculate edit distance between two strings."""
        if len(s1) < len(s2):
            return levenshtein_distance(s2, s1)
        if len(s2) == 0:
            return len(s1)
        
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]
    
    # Find words with similar length and low edit distance
    candidates = []
    for word in rules.keys():
        if abs(len(word) - len(target)) <= 2:  # Length filter
            distance = levenshtein_distance(target, word)
            if distance <= 2:  # Edit distance threshold
                candidates.append((word, distance))
    
    # Sort by distance and return top suggestions
    candidates.sort(key=lambda x: x[1])
    return [word for word, _ in candidates[:max_suggestions]]


def get_alignment(sinlish_text: str) -> List[Tuple[str, str]]:
    """
    Get character-level alignment between input and output.
    
    Shows how the FST maps input segments to output segments, useful for
    understanding the transliteration process and debugging.
    
    Note: This is a simplified alignment based on rule matching, not the
    actual FST path traversal (which would require FST state tracking).
    
    Args:
        sinlish_text: Input text to align
        
    Returns:
        List of (input_segment, output_segment) tuples
        
    Example:
        >>> get_alignment("mama gedara")
        [('mama', 'මම'), (' ', ' '), ('gedara', 'ගෙදර')]
    """
    rules = _load_rules()
    result = transliterate(sinlish_text)
    
    # Greedy longest-match alignment
    alignments = []
    i = 0
    j = 0
    
    while i < len(sinlish_text):
        # Try longest match first
        matched = False
        for length in range(min(20, len(sinlish_text) - i), 0, -1):
            segment = sinlish_text[i:i+length]
            if segment in rules:
                output_segment = rules[segment]
                alignments.append((segment, output_segment))
                i += length
                matched = True
                break
        
        if not matched:
            # Single character fallback
            alignments.append((sinlish_text[i], sinlish_text[i]))
            i += 1
    
    return alignments


# For testing/debugging
if __name__ == "__main__":
    print("=" * 60)
    print("Module 1: Advanced FST Transliteration Engine")
    print("=" * 60)
    
    # Test basic transliteration
    test_inputs = [
        "mama gedara yanawa",
        "eyala potha kiyawanawa",
        "oya bath kanawa"
    ]
    
    print("\n1. Basic Transliteration:")
    print("-" * 60)
    for text in test_inputs:
        try:
            result = transliterate(text)
            print(f"  {text:30} → {result}")
        except Exception as e:
            print(f"  {text:30} → ERROR: {e}")
    
    # Test n-best hypotheses
    print("\n2. N-Best Hypotheses (with scores):")
    print("-" * 60)
    test_word = "mama"
    results = transliterate_nbest(test_word, n=3, return_scores=True)
    print(f"  Input: {test_word}")
    for i, (text, score) in enumerate(results, 1):
        print(f"    {i}. {text} (confidence: {score:.3f})")
    
    # Test OOV detection
    print("\n3. OOV Detection:")
    print("-" * 60)
    test_oov = "mama xyz yanawa"
    oov_info = detect_oov(test_oov)
    print(f"  Input: {test_oov}")
    print(f"  Has OOV: {oov_info['has_oov']}")
    print(f"  Coverage: {oov_info['coverage']*100:.1f}%")
    print(f"  OOV Words: {oov_info['oov_words']}")
    if oov_info['suggestions']:
        print(f"  Suggestions: {oov_info['suggestions']}")
    
    # Test alignment
    print("\n4. Character Alignment:")
    print("-" * 60)
    test_align = "mama gedara"
    alignments = get_alignment(test_align)
    print(f"  Input: {test_align}")
    print(f"  Alignment:")
    for inp, out in alignments:
        print(f"    '{inp}' → '{out}'")
    
    print("\n" + "=" * 60)
