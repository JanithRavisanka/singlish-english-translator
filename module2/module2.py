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
    performing the SOV -> SVO structural transformation in the process.
    
    This function currently handles: SUBJ, OBJ, VERB, and applies the SOV -> SVO 
    transfer rule to the 'raw_translation' field.
    """
    
    if not sinhala_text or not lexicon:
        return {"raw_translation": "", "subject": {}, "object": {}, "verb": {}, "negation": False}

    tokens: List[str] = sinhala_text.split()
    
    # Storage for structured components
    subject_info: Dict[str, Any] = {}
    object_info: Dict[str, Any] = {}
    verb_info: Dict[str, Any] = {}
    is_negated: bool = False # Negation flag
    
    # Placeholder for collecting modifiers or other complex roles later
    modifiers: List[Dict[str, Any]] = [] 
    
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
            elif role == 'OBJ':
                # Capture all object features
                object_info = {k: v for k, v in word_data.items() if k != 'role'}
            elif pos == 'VERB':
                # Capture all verb features
                verb_info = {k: v for k, v in word_data.items() if k != 'role'}
            elif role == 'NEGATION':
                is_negated = True
            elif role == 'MODIFIER':
                # Place for future development: handling adjectives/adverbs
                modifiers.append({k: v for k, v in word_data.items() if k != 'role'})
            
        else:
            # When integrating, Module 1 should ensure all tokens are Sinhala. 
            # This warning helps debug lexicon gaps.
            print(f"Module 2 WARNING: Token '{token}' not found in lexicon. This will affect output.")
            
    # 4. Translation Model (Transfer Rules): SOV -> SVO for raw_translation
    ordered_parts: List[str] = []
    
    # 1. Subject (S)
    if subject_info:
        ordered_parts.append(subject_info['en'])
    
    # 2. Verb (V) - We use the base English verb here
    if verb_info:
        ordered_parts.append(verb_info['en'])
        
    # 3. Object (O) - Place objects and modifiers after the verb
    if object_info:
        # Note: If we had a list of modifiers, we'd insert them here before the object.
        ordered_parts.append(object_info['en'])
    
    # 5. Generate Output Dictionary (The final deliverable structure for Module 3)
    translation_dict = {
        "raw_translation": " ".join(ordered_parts), 
        "subject": subject_info,
        "object": object_info,
        "verb": verb_info,
        "negation": is_negated
    }
    
    return translation_dict