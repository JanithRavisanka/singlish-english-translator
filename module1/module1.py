"""
Module 1: FST Transliteration Engine - Runtime API
Student 1

This module provides the transliterate() function that converts Singlish
(Roman script) to Sinhala script using a pre-compiled FST.

Usage:
    from module1 import transliterate
    sinhala = transliterate("mama gedara yanawa")
"""

# TODO: Implement transliteration function
# Steps:
# 1. Load the compiled FST on module import: fst = pynini.Fst.read("transliterate.fst")
# 2. Implement transliterate(sinlish_text: str) -> str function
# 3. Use pynini.rewrite.top_rewrite(sinlish_text, fst) to apply FST
# 4. Return the resulting Sinhala string


def transliterate(sinlish_text: str) -> str:
    """
    Transliterate Sinlish (Roman script) to Sinhala script.
    
    Args:
        sinlish_text: Input text in Sinlish (Roman script)
        
    Returns:
        Transliterated text in Sinhala script
    """
    # TODO: Implement
    raise NotImplementedError("Module 1 transliterate function not yet implemented")

