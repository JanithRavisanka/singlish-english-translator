import json
from typing import Dict, Any, List

# --- Constants ---
LEXICON_FILE = 'lexicon.json' 

# --- Module-level variable to hold the lexicon (Data Lookup) ---
try:
    with open(LEXICON_FILE, 'r', encoding='utf-8') as f:
        lexicon = json.load(f)
except FileNotFoundError:
    print(f"Module 2 ERROR: {LEXICON_FILE} not found. Translation will fail.")
    lexicon = {}
except json.JSONDecodeError:
    print(f"Module 2 ERROR: Could not decode {LEXICON_FILE}. Check JSON syntax.")
    lexicon = {}


def translate(sinhala_text: str) -> Dict[str, Any]:
    """
    Translates a clean Sinhala string into a structured English dictionary, 
    performing the SOV -> SVO structural transformation in the process,
    and handling Modifiers (Adjectives) and Negation.
    """
    
    if not sinhala_text or not lexicon:
        return {"raw_translation": "", "subject": {}, "object": {}, "verb": {}, "negation": False}

    tokens: List[str] = sinhala_text.split()
    
    # Storage for structured components
    subject_info: Dict[str, Any] = {}
    object_info: Dict[str, Any] = {}
    verb_info: Dict[str, Any] = {}
    is_negated: bool = False
    
    # List to hold modifiers (adjectives) and associate them with the object they precede.
    object_modifiers: List[str] = []
    
    # 2. Lexical Analysis & 3. Syntactic Parse
    for token in tokens:
        if token in lexicon:
            word_data = lexicon[token]
            role = word_data.get('role')
            pos = word_data.get('pos')
            
            # 3. Parse and Store: Assign to grammatical role
            if role == 'SUBJ':
                # Capture all subject features
                subject_info = {k: v for k, v in word_data.items() if k != 'role'} 
            elif pos == 'VERB':
                # Capture all verb features
                verb_info = {k: v for k, v in word_data.items() if k != 'role'}
            elif role == 'NEGATION':
                # Set the negation flag
                is_negated = True
            elif role == 'MODIFIER':
                # Adjectives precede the noun in Sinhala (SOV order), so we collect them here.
                object_modifiers.append(word_data['en'])
            elif role == 'OBJ':
                # Capture all object features
                object_info = {k: v for k, v in word_data.items() if k != 'role'}
                
                # Attach collected modifiers to the object they precede in the Sinhala sentence.
                if object_modifiers:
                    object_info['modifiers'] = object_modifiers
                # Reset modifiers for the next object
                object_modifiers = [] 
            
        else:
            # The warning message is useful but we must continue processing
            print(f"Module 2 WARNING: Token '{token}' not found in lexicon. This will affect output.")
            
    # 4. Implicit Verb Handling (Fix for Test ID 8)
    # If no explicit verb is found, but there is a subject and either negation or a locational object, 
    # we must assume an implicit 'to be' verb for the English SVO structure.
    # Note: The object role 'LOC' (from 'අහසෙ') or 'NEGATION' (from 'නැහැ') often implies 'to be'
    is_locational_or_negated = object_info.get('role') == 'LOC' or is_negated
    
    if not verb_info and subject_info and is_locational_or_negated:
        # Using 'be' and letting Module 3 refine the conjugation (is/am/are)
        verb_info = {
            "en": "be", 
            "pos": "VERB", 
            "tense": "PRESENT_CONTINUOUS", 
            "context": "IMPLICIT_BE" # New context tag for Module 3
        }
        # In the raw output, we use 'be' to ensure the V slot is occupied.
        # This fixes the raw output for Test 8: "they home" -> "they be home"
        ordered_parts_raw = [subject_info['en'], verb_info['en']] 
    else:
        # Standard SVO ordering for the raw output
        ordered_parts_raw = [subject_info['en']] if subject_info else []
        if verb_info:
            ordered_parts_raw.append(verb_info['en'])


    # 5. Translation Model (Transfer Rules): SOV -> SVO for raw_translation
    
    # 3. Object (O) - Add modifiers before the object noun for the raw SVO output.
    if object_info:
        # Add indefinite article 'a/an' if the feature is present in the object info
        if object_info.get('indefinite_article'):
            # Simple heuristic: use 'a' for raw, let Module 3 handle a/an rules
            ordered_parts_raw.append('a') 
        
        if 'modifiers' in object_info:
            ordered_parts_raw.extend(object_info['modifiers']) # Adds the adjective
        ordered_parts_raw.append(object_info['en']) # Adds the noun

    # 6. Generate Output Dictionary (The final deliverable structure for Module 3)
    translation_dict = {
        "raw_translation": " ".join(ordered_parts_raw), 
        "subject": subject_info,
        "object": object_info,
        "verb": verb_info,
        "negation": is_negated
    }
    
    return translation_dict

# --- TEST HARNESS (Placeholder - actual test logic is in test_module2.py) ---
if __name__ == '__main__':
    # Placeholder for local testing if needed
    pass
