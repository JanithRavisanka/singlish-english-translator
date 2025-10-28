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

import pynini
import json
import os

def build_fst():
    """Build and compile the FST from singlish_rules.json."""
    
    # Get the path to singlish_rules.json (in parent directory)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    rules_path = os.path.join(script_dir, '..', 'singlish_rules.json')
    
    print("Building FST from singlish_rules.json...")
    
    # 1. Read singlish_rules.json
    with open(rules_path, 'r', encoding='utf-8') as f:
        rules_dict = json.load(f)
    
    print(f"Loaded {len(rules_dict)} transliteration rules")
    
    # 2. Convert JSON dictionary to list of (sinlish, sinhala) tuples
    # Important: Rules are already ordered longest to shortest in the JSON
    rules_list = [(k, v) for k, v in rules_dict.items()]
    
    # 3. Create FST using string_map and make it handle greedily
    print("Creating FST with pynini.string_map...")
    # Create the base transducer
    fst = pynini.string_map(rules_list)
    
    # Create a closure to match any sequence of rules (greedy longest match)
    fst = pynini.closure(fst)
    
    # 4. Optimize the FST
    print("Optimizing FST...")
    fst.optimize()
    
    # 5. Write the compiled FST to disk
    output_path = os.path.join(script_dir, "transliterate.fst")
    print(f"Writing FST to {output_path}...")
    fst.write(output_path)
    
    print("✓ FST compilation complete!")
    print(f"  Output: {output_path}")
    print(f"  Rules: {len(rules_dict)}")

if __name__ == "__main__":
    try:
        build_fst()
    except FileNotFoundError as e:
        print(f"Error: Could not find singlish_rules.json")
        print(f"Make sure the file exists in the parent directory.")
        print(f"Details: {e}")
    except Exception as e:
        print(f"Error building FST: {e}")
        import traceback
        traceback.print_exc()
