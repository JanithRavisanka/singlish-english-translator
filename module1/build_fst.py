"""
Module 1: FST Transliteration Engine - Build Script
Student 1

This script compiles the Singlish-to-Sinhala transliteration rules from
singlish_rules.json into an optimized FST binary file (transliterate.fst).

Usage:
    python build_fst.py

Output:
    transliterate.fst - Compiled FST model
"""

# TODO: Implement FST compilation logic
# Steps:
# 1. Read singlish_rules.json from parent directory
# 2. Convert JSON dictionary to list of (sinlish, sinhala) tuples
# 3. Create FST using pynini.string_map(rules_list)
# 4. Optimize the FST with fst.optimize()
# 5. Write to disk: fst.write("transliterate.fst")

