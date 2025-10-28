"""
Fuzzy Matching Module for Spell Correction
Provides approximate string matching for handling spelling mistakes in Singlish input.

This module helps correct common typing errors by finding the closest matching
words from the transliteration rules when exact matches fail.
"""

import json
import os
from typing import List, Tuple, Optional, Dict


def levenshtein_distance(s1: str, s2: str) -> int:
    """
    Calculate the Levenshtein distance between two strings.
    
    The Levenshtein distance is the minimum number of single-character edits
    (insertions, deletions, or substitutions) required to change one word into another.
    
    Args:
        s1: First string
        s2: Second string
        
    Returns:
        Integer representing the edit distance
    """
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    
    if len(s2) == 0:
        return len(s1)
    
    previous_row = range(len(s2) + 1)
    
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            # Cost of insertions, deletions, or substitutions
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]


def similarity_score(s1: str, s2: str) -> float:
    """
    Calculate a normalized similarity score between two strings.
    
    Args:
        s1: First string
        s2: Second string
        
    Returns:
        Float between 0 and 1, where 1 is identical and 0 is completely different
    """
    if not s1 or not s2:
        return 0.0
    
    distance = levenshtein_distance(s1.lower(), s2.lower())
    max_len = max(len(s1), len(s2))
    
    return 1 - (distance / max_len)


def find_closest_match(
    word: str, 
    candidates: List[str], 
    min_similarity: float = 0.6,
    max_results: int = 1
) -> List[Tuple[str, float]]:
    """
    Find the closest matching word(s) from a list of candidates.
    
    Args:
        word: The word to match
        candidates: List of candidate words
        min_similarity: Minimum similarity threshold (0-1)
        max_results: Maximum number of results to return
        
    Returns:
        List of tuples (matched_word, similarity_score), sorted by score descending
    """
    if not word or not candidates:
        return []
    
    # Calculate similarity for all candidates
    scored_matches = []
    for candidate in candidates:
        score = similarity_score(word, candidate)
        if score >= min_similarity:
            scored_matches.append((candidate, score))
    
    # Sort by score (descending) and return top matches
    scored_matches.sort(key=lambda x: x[1], reverse=True)
    
    return scored_matches[:max_results]


def load_vocabulary() -> List[str]:
    """
    Load all words from singlish_rules.json as the vocabulary.
    
    Returns:
        List of valid Singlish words
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    rules_path = os.path.join(script_dir, '..', 'data', 'singlish_rules.json')
    
    try:
        with open(rules_path, 'r', encoding='utf-8') as f:
            rules_dict = json.load(f)
        return list(rules_dict.keys())
    except Exception as e:
        print(f"Warning: Could not load vocabulary: {e}")
        return []


class FuzzyMatcher:
    """
    Fuzzy matcher for Singlish words with spell correction.
    """
    
    def __init__(self, min_word_length: int = 3, min_similarity: float = 0.6):
        """
        Initialize the fuzzy matcher.
        
        Args:
            min_word_length: Minimum word length to attempt fuzzy matching
            min_similarity: Minimum similarity threshold for matches
        """
        self.vocabulary = load_vocabulary()
        self.min_word_length = min_word_length
        self.min_similarity = min_similarity
        
        # Create a word length index for faster matching
        self.word_by_length: Dict[int, List[str]] = {}
        for word in self.vocabulary:
            length = len(word)
            if length not in self.word_by_length:
                self.word_by_length[length] = []
            self.word_by_length[length].append(word)
    
    def find_correction(self, word: str, verbose: bool = False) -> Optional[Tuple[str, float]]:
        """
        Find the best spelling correction for a word.
        
        Args:
            word: Word to correct
            verbose: If True, print matching details
            
        Returns:
            Tuple of (corrected_word, confidence_score) or None if no good match
        """
        if len(word) < self.min_word_length:
            return None
        
        # Look at words with similar lengths (±2)
        target_length = len(word)
        candidates = []
        
        for length in range(max(1, target_length - 2), target_length + 3):
            if length in self.word_by_length:
                candidates.extend(self.word_by_length[length])
        
        # If no candidates in similar lengths, use all vocabulary
        if not candidates:
            candidates = self.vocabulary
        
        matches = find_closest_match(word, candidates, self.min_similarity, max_results=1)
        
        if matches:
            corrected_word, score = matches[0]
            if verbose:
                print(f"  Fuzzy match: '{word}' → '{corrected_word}' (confidence: {score:.2f})")
            return corrected_word, score
        
        return None
    
    def correct_text(self, text: str, verbose: bool = False) -> Tuple[str, List[Dict]]:
        """
        Attempt to correct spelling mistakes in text.
        
        Args:
            text: Input text to correct
            verbose: If True, print correction details
            
        Returns:
            Tuple of (corrected_text, corrections_list)
            corrections_list contains dicts with 'original', 'corrected', 'confidence'
        """
        words = text.split()
        corrected_words = []
        corrections = []
        
        for word in words:
            # Try to find a correction
            result = self.find_correction(word, verbose=verbose)
            
            if result:
                corrected_word, confidence = result
                # Only apply correction if confidence is high enough and words differ
                if confidence >= self.min_similarity and corrected_word != word:
                    corrected_words.append(corrected_word)
                    corrections.append({
                        'original': word,
                        'corrected': corrected_word,
                        'confidence': confidence
                    })
                else:
                    corrected_words.append(word)
            else:
                corrected_words.append(word)
        
        return ' '.join(corrected_words), corrections


def test_fuzzy_matcher():
    """Test the fuzzy matcher with common spelling mistakes."""
    print("="*70)
    print("FUZZY MATCHING TEST")
    print("="*70)
    
    matcher = FuzzyMatcher(min_similarity=0.6)
    
    test_cases = [
        ("mama gedra yanawa", "gedra → gedara"),  # missing 'a'
        ("mama gedar yanawa", "gedar → gedara"),  # missing 'a' at end
        ("eyala potha kiyawanwa", "kiyawanwa → kiyawanawa"),  # missing 'a'
        ("oya baht kanawa", "baht → bath"),  # 'h' and 't' swapped
        ("mama iskol yanawa", "iskol → iskole"),  # missing 'e'
        ("eyala watura bonwa", "bonwa → bonawa"),  # missing 'a'
        ("oya telavision balanawa", "telavision → television"),  # typo
        ("mama computr hadanawa", "computr → computer"),  # missing 'e'
    ]
    
    print("\nTesting common spelling mistakes:\n")
    
    for text, description in test_cases:
        print(f"Input:  {text}")
        print(f"Expect: {description}")
        corrected, corrections = matcher.correct_text(text, verbose=False)
        print(f"Output: {corrected}")
        if corrections:
            for corr in corrections:
                print(f"  ✓ Corrected: {corr['original']} → {corr['corrected']} "
                      f"(confidence: {corr['confidence']:.2f})")
        else:
            print("  No corrections applied")
        print()


if __name__ == "__main__":
    test_fuzzy_matcher()

