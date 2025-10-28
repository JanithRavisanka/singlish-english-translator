"""
Module 1: Preprocessing Pipeline
Student 1

This module provides preprocessing functions to clean and normalize
input text before FST transliteration. It handles:
- Unicode to ASCII conversion (using unidecode)
- Case normalization (uppercase to lowercase)
- Whitespace cleaning
- Punctuation preservation
- Number handling
- Input validation
"""

import re
import string
from unidecode import unidecode

def unicode_to_ascii(text):
    """
    Convert Unicode characters to their closest ASCII representation.
    
    This function uses unidecode to transliterate Unicode strings to ASCII.
    Useful for handling:
    - Accented characters (é → e, ñ → n)
    - Non-Latin scripts that have romanization
    - Mixed Unicode input
    
    Args:
        text: Input string (may contain Unicode characters)
        
    Returns:
        ASCII-only string
        
    Examples:
        "café" → "cafe"
        "naïve" → "naive"
        "Москва" → "Moskva"
        "北京" → "Bei Jing"
    """
    if not text:
        return ""
    
    try:
        return unidecode(text)
    except Exception as e:
        # If unidecode fails, return original text
        print(f"Warning: Unicode conversion failed: {e}")
        return text


def normalize_text(text):
    """
    Normalize text by converting to lowercase and cleaning whitespace.
    
    Args:
        text: Input string
        
    Returns:
        Normalized string (lowercase, single spaces)
    """
    if not text:
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Replace multiple spaces/tabs/newlines with single space
    text = re.sub(r'\s+', ' ', text)
    
    # Strip leading/trailing whitespace
    text = text.strip()
    
    return text


def separate_punctuation(text):
    """
    Extract punctuation from text and store their positions.
    
    Args:
        text: Input string
        
    Returns:
        tuple: (clean_text, punctuation_map)
               punctuation_map is a list of (position, char) tuples
    """
    punctuation_map = []
    clean_chars = []
    
    for i, char in enumerate(text):
        if char in string.punctuation:
            # Store punctuation and its position relative to clean text
            punctuation_map.append((len(clean_chars), char))
        else:
            clean_chars.append(char)
    
    clean_text = ''.join(clean_chars)
    
    return clean_text, punctuation_map


def restore_punctuation(text, punctuation_map):
    """
    Restore punctuation to text based on stored positions.
    
    Args:
        text: Transliterated string
        punctuation_map: List of (position, punctuation_char) tuples
        
    Returns:
        String with punctuation restored
    """
    if not punctuation_map:
        return text
    
    result = list(text)
    
    # Insert punctuation at stored positions (in reverse to maintain positions)
    for pos, punct in reversed(punctuation_map):
        if pos <= len(result):
            result.insert(pos, punct)
        else:
            # If position is beyond text length, append at end
            result.append(punct)
    
    return ''.join(result)


def handle_numbers(text):
    """
    Extract numbers from text and store their positions.
    
    Args:
        text: Input string
        
    Returns:
        tuple: (text_without_numbers, number_map)
               number_map is a list of (position, number_string) tuples
    """
    number_map = []
    clean_chars = []
    i = 0
    
    while i < len(text):
        if text[i].isdigit():
            # Collect the full number
            number = ""
            while i < len(text) and text[i].isdigit():
                number += text[i]
                i += 1
            # Store number and its position
            number_map.append((len(clean_chars), number))
        else:
            clean_chars.append(text[i])
            i += 1
    
    clean_text = ''.join(clean_chars)
    return clean_text, number_map


def restore_numbers(text, number_map):
    """
    Restore numbers to text based on stored positions.
    
    Args:
        text: Text without numbers
        number_map: List of (position, number_string) tuples
        
    Returns:
        String with numbers restored
    """
    if not number_map:
        return text
    
    result = list(text)
    
    # Insert numbers at stored positions (in reverse to maintain positions)
    for pos, number in reversed(number_map):
        if pos <= len(result):
            # Insert each character of the number
            for char in reversed(number):
                result.insert(pos, char)
        else:
            # If position is beyond text length, append at end
            result.extend(list(number))
    
    return ''.join(result)


def validate_input(text):
    """
    Validate input text for supported characters.
    
    Args:
        text: Input string
        
    Returns:
        tuple: (is_valid, error_message)
               is_valid is True if all characters are supported
    """
    if not text:
        return False, "Empty input"
    
    # Define supported characters (lowercase letters, spaces, numbers, common punctuation)
    supported_chars = set(string.ascii_lowercase + string.digits + string.whitespace + string.punctuation)
    
    # Check each character
    unsupported = []
    for char in text.lower():
        if char not in supported_chars:
            if char not in unsupported:
                unsupported.append(char)
    
    if unsupported:
        return False, f"Unsupported characters found: {', '.join(repr(c) for c in unsupported)}"
    
    return True, ""


def preprocess(text):
    """
    Main preprocessing pipeline.
    
    This function combines all preprocessing steps:
    0. Convert Unicode to ASCII (using unidecode)
    1. Validate input
    2. Normalize text (lowercase, whitespace)
    3. Separate punctuation
    4. Handle numbers
    
    Args:
        text: Raw input string (may contain Unicode characters)
        
    Returns:
        tuple: (preprocessed_text, metadata)
               metadata is a dict containing:
               - punctuation_map: for restoring punctuation
               - number_map: for restoring numbers
               - original_text: the original input
               - ascii_converted: boolean indicating if Unicode was converted
               - warnings: list of warning messages
    """
    warnings = []
    
    # Store original
    original_text = text
    
    # Step 0: Convert Unicode to ASCII
    ascii_text = unicode_to_ascii(text)
    ascii_converted = (ascii_text != text)
    if ascii_converted:
        warnings.append(f"Unicode characters detected and converted to ASCII")
    text = ascii_text
    
    # Validate
    is_valid, error_msg = validate_input(text)
    if not is_valid:
        warnings.append(f"Validation warning: {error_msg}")
    
    # Normalize
    text = normalize_text(text)
    
    # Separate punctuation
    text, punctuation_map = separate_punctuation(text)
    
    # Handle numbers
    text, number_map = handle_numbers(text)
    
    # Create metadata
    metadata = {
        'punctuation_map': punctuation_map,
        'number_map': number_map,
        'original_text': original_text,
        'ascii_converted': ascii_converted,
        'warnings': warnings
    }
    
    return text, metadata


def postprocess(text, metadata):
    """
    Restore text to its original format using metadata.
    
    Args:
        text: Transliterated string
        metadata: Dictionary from preprocess() containing maps
        
    Returns:
        Final text with punctuation and numbers restored
    """
    # First restore numbers (they affect character positions)
    text = restore_numbers(text, metadata['number_map'])
    
    # Then restore punctuation (at the final positions)
    text = restore_punctuation(text, metadata['punctuation_map'])
    
    return text


# For testing/debugging
if __name__ == "__main__":
    # Test cases
    test_inputs = [
        "Mama gedara yanawa",
        "mama  gedara   yanawa",
        "mama gedara yanawa.",
        "eyala 5 potha kiyawanawa!",
        "OYA bath kanawa?",
    ]
    
    print("Preprocessing Test Cases:")
    print("=" * 60)
    
    for test in test_inputs:
        print(f"\nOriginal: {repr(test)}")
        preprocessed, metadata = preprocess(test)
        print(f"Preprocessed: {repr(preprocessed)}")
        print(f"Metadata: {metadata}")
        
        # Simulate transliteration (just uppercase for demo)
        transliterated = preprocessed.upper()
        
        # Postprocess
        final = postprocess(transliterated, metadata)
        print(f"After postprocess: {repr(final)}")

