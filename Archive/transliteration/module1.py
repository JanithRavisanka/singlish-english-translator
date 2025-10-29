"""
Module 1: FST Transliteration Engine - Runtime API
Student 1

This module provides the transliterate() function that converts Singlish
(Roman script) to Sinhala script using a pre-compiled FST.

The module includes preprocessing to handle:
- Case normalization (uppercase to lowercase)
- Punctuation preservation
- Number handling
- Input validation

Usage:
    from module1 import transliterate
    sinhala = transliterate("mama gedara yanawa")
    # Also handles: "Mama gedara yanawa!" → "මම ගෙදර යනවා!"
"""

import pynini
import os
from preprocess import preprocess, postprocess
from fuzzy_matcher import FuzzyMatcher

# Initialize fuzzy matcher once at module level
_fuzzy_matcher = None

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

def transliterate(sinlish_text: str, verbose: bool = False, spell_check: bool = True) -> str:
    """
    Transliterate Singlish (Roman script) to Sinhala script with preprocessing.
    
    This function uses a pre-compiled Finite-State Transducer (FST) to 
    convert Singlish text to Sinhala script. The FST applies the longest-match
    rule, ensuring that whole words are matched before syllables, and syllables
    before individual characters.
    
    Preprocessing Pipeline:
    1. Normalize text (lowercase, whitespace cleaning)
    2. Extract and preserve punctuation
    3. Handle numbers separately
    4. Validate input
    5. (Optional) Apply fuzzy matching for spelling corrections
    
    Args:
        sinlish_text: Input text in Singlish (Roman script)
                     Example: "Mama gedara yanawa!" or "mama gedra yanawa" (with typo)
        verbose: If True, print preprocessing warnings and corrections (default: False)
        spell_check: If True, attempt to correct spelling mistakes using fuzzy matching
                     (default: True)
        
    Returns:
        Transliterated text in Sinhala script with punctuation/numbers restored
        Example: "මම ගෙදර යනවා!"
        
    Raises:
        Exception: If the FST cannot transliterate the input
    """
    global _fuzzy_matcher
    
    if not sinlish_text:
        return ""
    
    try:
        # Step 1: Preprocess the input
        preprocessed_text, metadata = preprocess(sinlish_text)
        
        # Step 1.5: Apply spell checking if enabled
        if spell_check:
            # Initialize fuzzy matcher lazily (only when needed)
            if _fuzzy_matcher is None:
                _fuzzy_matcher = FuzzyMatcher(min_word_length=3, min_similarity=0.65)
            
            # Attempt to correct spelling mistakes
            corrected_text, corrections = _fuzzy_matcher.correct_text(
                preprocessed_text, 
                verbose=verbose
            )
            
            # Update metadata with corrections
            if corrections:
                metadata['spell_corrections'] = corrections
                if verbose:
                    print(f"Spell corrections applied:")
                    for corr in corrections:
                        print(f"  '{corr['original']}' → '{corr['corrected']}' "
                              f"(confidence: {corr['confidence']:.2f})")
                preprocessed_text = corrected_text
        
        # Show warnings if verbose mode
        if verbose and metadata['warnings']:
            for warning in metadata['warnings']:
                print(f"Warning: {warning}")
        
        # Step 2: Apply the FST to the preprocessed text
        # Compose the input string with the FST and get the shortest path
        input_fst = pynini.accep(preprocessed_text)
        output_fst = input_fst @ _fst
        result = pynini.shortestpath(output_fst).string()
        
        # Step 3: Postprocess to restore punctuation and numbers
        final_result = postprocess(result, metadata)
        
        return final_result
        
    except Exception as e:
        # If transliteration fails, provide helpful error message
        raise Exception(
            f"Failed to transliterate '{sinlish_text}'\n"
            f"This may be because the input contains characters not in singlish_rules.json\n"
            f"Original error: {e}"
        )


# For testing/debugging
if __name__ == "__main__":
    # Test cases showing preprocessing capabilities
    test_inputs = [
        "mama gedara yanawa",           # Normal
        "Mama gedara yanawa",           # Uppercase
        "mama  gedara   yanawa",        # Extra spaces
        "mama gedara yanawa!",          # With punctuation
        "eyala 5 potha kiyawanawa",     # With numbers
        "OYA bath kanawa?"              # Mixed case + punctuation
    ]
    
    print("Testing transliteration with preprocessing:")
    print("=" * 60)
    for text in test_inputs:
        try:
            result = transliterate(text, verbose=True)
            print(f"  Input:  {repr(text)}")
            print(f"  Output: {repr(result)}")
            print()
        except Exception as e:
            print(f"  Input:  {repr(text)}")
            print(f"  ERROR: {e}")
            print()
