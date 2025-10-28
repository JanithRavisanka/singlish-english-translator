"""
Module 2: RBMT Translation Engine - Runtime API
Student 2

This module provides the translate() function that converts Sinhala script
to a structured English representation using Rule-Based Machine Translation.

Usage:
    from module2 import translate
    result_dict = translate("මම ගෙදර යනවා")
"""

# TODO: Implement translation function
# Steps:
# 1. Load lexicon.json from parent directory
# 2. Implement translate(sinhala_text: str) -> dict function
# 3. Stage 1: Tokenize - Split input into word tokens
# 4. Stage 2: Lexical Analysis - Look up each token in lexicon.json
# 5. Stage 3: Syntactic Parse & Transfer - Identify S, O, V and reorder (SOV -> SVO)
# 6. Stage 4: Generate output dictionary with raw_translation and metadata


def translate(sinhala_text: str) -> dict:
    """
    Translate Sinhala script to structured English representation.
    
    Args:
        sinhala_text: Input text in Sinhala script
        
    Returns:
        Dictionary containing:
        - raw_translation: str (e.g., "I read book")
        - subject: dict (e.g., {"en": "I", "pos": "PRON"})
        - verb: dict (e.g., {"en": "read", "tense": "PRESENT_CONTINUOUS"})
        - object: dict (e.g., {"en": "book", "pos": "NOUN"})
        - negation: bool
    """
    # TODO: Implement
    raise NotImplementedError("Module 2 translate function not yet implemented")

