import json
import os
from module2 import translate # Import the core function
from module2 import LEXICON_FILE # Import the constants to ensure consistency

# --- Constants ---
script_dir = os.path.dirname(os.path.abspath(__file__))
CORPUS_FILE = os.path.join(script_dir, '..', 'data', 'corpus.json')

def run_tests():
    """Reads corpus data and tests the translate function from module2."""
    print("--- Starting Independent Test for Module 2 (RBMT) ---")
    
    if not os.path.exists(LEXICON_FILE):
        print(f"Test FAILED: Required data file {LEXICON_FILE} not found. Please create it.")
        return
        
    if not os.path.exists(CORPUS_FILE):
        print(f"Test FAILED: Corpus file {CORPUS_FILE} not found. Please create it.")
        return

    try:
        with open(CORPUS_FILE, 'r', encoding='utf-8') as f:
            test_corpus = json.load(f)
        print(f"Test data loaded successfully from {CORPUS_FILE}.")
    except Exception as e:
        print(f"ERROR loading corpus: {e}")
        return

    for item in test_corpus:
        sinhala_input = item.get('sinhala')
        if not sinhala_input:
            continue
            
        reference = item.get('english_reference', 'N/A')
        
        print(f"\n[Test ID: {item.get('id', 'N/A')}]")
        print(f"  Input (Sinhala): {sinhala_input}")
        
        output_dict = translate(sinhala_input)
        
        # Display results
        print(f"  Expected Fluent Output (For Module 3): {reference}")
        print("  Module 2 SVO Output (Raw English):", output_dict.get('raw_translation'))
        print("  Module 2 Output (Structured Dictionary):")
        print(json.dumps(output_dict, indent=4, ensure_ascii=False))
        
        # Simple status check
        if output_dict.get('subject') and output_dict.get('verb'):
            print("  STATUS: SUCCESS - Core parsing detected (SUBJ and VERB).")
        else:
            print("  STATUS: FAIL - Missing core component(s). Check lexicon/parsing logic.")

if __name__ == '__main__':
    run_tests()
