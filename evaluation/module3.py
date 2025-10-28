"""
Module 3: Post-Processor & Target Language Generation
Student 3

This module provides post-processing functionality to convert the structured
dictionary output from Module 2 into fluent, grammatically correct English.

Core NLP Tasks:
1. Target Language Generation (English)
2. Morphology (verb conjugation)
3. Syntax (article insertion)
4. Error correction (punctuation, capitalization)

Usage:
    from module3 import post_process
    result = post_process(module2_output)
"""

from typing import Dict, Any, Optional


def conjugate_verb(verb_dict: Dict[str, Any], subject_dict: Dict[str, Any]) -> str:
    """
    Apply verb conjugation rules based on tense and subject.
    
    Args:
        verb_dict: Dictionary with keys 'en' (verb), 'tense'
        subject_dict: Dictionary with keys 'en' (subject), 'pos'
        
    Returns:
        Conjugated verb phrase (e.g., "am going", "is eating")
    """
    if not verb_dict or 'en' not in verb_dict:
        return ""
    
    verb = verb_dict.get('en', '')
    tense = verb_dict.get('tense', '')
    subject = subject_dict.get('en', '').lower() if subject_dict else ''
    
    # Handle present continuous tense (main case for our corpus)
    if tense == 'PRESENT_CONTINUOUS':
        # Determine auxiliary verb (am/is/are)
        if subject in ['i']:
            auxiliary = 'am'
        elif subject in ['he', 'she', 'it']:
            auxiliary = 'is'
        elif subject in ['you', 'we', 'they']:
            auxiliary = 'are'
        else:
            # Default to 'is' for singular, 'are' for plural
            auxiliary = 'is'
        
        # Add -ing to verb
        # Handle special cases
        
        # Exception list - multi-syllable words that don't double
        no_double_verbs = {'listen', 'open', 'enter', 'offer', 'visit', 'limit', 'edit'}
        
        if verb.endswith('e') and not verb.endswith('ee'):
            # come -> coming, write -> writing
            present_participle = verb[:-1] + 'ing'
        elif (verb not in no_double_verbs and
              len(verb) >= 3 and 
              verb[-1] in 'bdfgmnprst' and
              verb[-2] in 'aeiou' and 
              verb[-3] not in 'aeiou' and
              not verb.endswith('x')):  # Don't double 'x' in "fix"
            # run -> running, sit -> sitting (CVC pattern for monosyllabic words)
            present_participle = verb + verb[-1] + 'ing'
        else:
            present_participle = verb + 'ing'
        
        return f"{auxiliary} {present_participle}"
    
    # Handle simple present (if needed)
    elif tense == 'PRESENT':
        if subject in ['he', 'she', 'it']:
            # Add -s/-es
            if verb.endswith(('s', 'sh', 'ch', 'x', 'z', 'o')):
                return verb + 'es'
            elif verb.endswith('y') and len(verb) > 1 and verb[-2] not in 'aeiou':
                return verb[:-1] + 'ies'
            else:
                return verb + 's'
        return verb
    
    # Default: return base verb
    return verb


def insert_articles(words: list, parse_dict: Dict[str, Any]) -> list:
    """
    Insert articles (a, an, the) before nouns where appropriate.
    
    Args:
        words: List of words in the sentence
        parse_dict: Parse dictionary from Module 2
        
    Returns:
        List of words with articles inserted
    """
    # Words that typically don't need articles (uncountable nouns, proper nouns, locations)
    no_article_words = {
        'home', 'water', 'rice', 'bread', 'tea', 'coffee', 'milk', 'juice',
        'music', 'work', 'school', 'office', 'television', 'tv', 
        'information', 'news', 'money', 'food', 'breakfast', 'lunch', 'dinner'
    }
    
    result = []
    
    # Get object noun if present
    obj = parse_dict.get('object', {})
    obj_word = obj.get('en', '').lower() if obj else None
    
    for i, word in enumerate(words):
        result.append(word)
        
        # If this word is a noun (object) and doesn't have an article
        if word.lower() == obj_word and obj_word:
            # Check if this word should get an article
            if obj_word not in no_article_words:
                # Check if previous word is not already an article
                if not result or (len(result) >= 2 and result[-2].lower() not in ['a', 'an', 'the']):
                    # Determine article based on first letter
                    if obj_word and obj_word[0].lower() in 'aeiou':
                        # Insert 'an' before the noun
                        result.insert(-1, 'an')
                    else:
                        # Insert 'a' before the noun
                        result.insert(-1, 'a')
    
    return result


def capitalize_and_punctuate(sentence: str) -> str:
    """
    Apply capitalization and punctuation rules.
    
    Args:
        sentence: Input sentence
        
    Returns:
        Sentence with proper capitalization and punctuation
    """
    if not sentence:
        return ""
    
    # Capitalize first letter
    sentence = sentence[0].upper() + sentence[1:] if len(sentence) > 1 else sentence.upper()
    
    # Add period if not already ending with punctuation
    if not sentence.endswith(('.', '!', '?')):
        sentence += '.'
    
    return sentence


def post_process(translation_dict: Dict[str, Any]) -> str:
    """
    Main post-processing function: applies English grammar rules to generate
    fluent output from Module 2's structured dictionary.
    
    Processing pipeline:
    1. Extract components (subject, verb, object)
    2. Apply verb conjugation
    3. Insert articles
    4. Apply capitalization and punctuation
    
    Args:
        translation_dict: Output dictionary from Module 2 containing:
            - raw_translation: str
            - subject: dict with 'en', 'pos'
            - verb: dict with 'en', 'tense'
            - object: dict with 'en', 'pos'
            - negation: bool
            
    Returns:
        Fluent English sentence string
        
    Example:
        Input:  {'raw_translation': 'I go home', 
                 'verb': {'en': 'go', 'tense': 'PRESENT_CONTINUOUS'},
                 'subject': {'en': 'I'}}
        Output: "I am going home."
    """
    if not translation_dict:
        return ""
    
    # Extract components
    raw_translation = translation_dict.get('raw_translation', '')
    subject_dict = translation_dict.get('subject', {})
    verb_dict = translation_dict.get('verb', {})
    object_dict = translation_dict.get('object', {})
    negation = translation_dict.get('negation', False)
    
    if not raw_translation:
        return ""
    
    # Split into words
    words = raw_translation.split()
    
    if not words:
        return ""
    
    # Step 1: Apply verb conjugation
    if verb_dict and 'en' in verb_dict:
        verb_original = verb_dict['en']
        verb_conjugated = conjugate_verb(verb_dict, subject_dict)
        
        # Replace the verb in the word list
        if verb_original in words:
            verb_index = words.index(verb_original)
            # Remove original verb and insert conjugated form
            words.pop(verb_index)
            # Insert conjugated verb (may be multiple words like "am going")
            for i, v_word in enumerate(verb_conjugated.split()):
                words.insert(verb_index + i, v_word)
    
    # Step 2: Insert articles
    # Only insert articles for objects (nouns)
    if object_dict and 'en' in object_dict:
        words = insert_articles(words, translation_dict)
    
    # Step 3: Handle negation (if present)
    if negation and 'not' not in words:
        # Find auxiliary verb and insert 'not' after it
        for i, word in enumerate(words):
            if word in ['am', 'is', 'are', 'was', 'were', 'have', 'has', 'had']:
                words.insert(i + 1, 'not')
                break
    
    # Join words
    sentence = ' '.join(words)
    
    # Step 4: Apply capitalization and punctuation
    sentence = capitalize_and_punctuate(sentence)
    
    return sentence


# For testing/debugging
if __name__ == "__main__":
    # Test with example dictionary
    test_dict = {
        'raw_translation': 'I go home',
        'subject': {'en': 'I', 'pos': 'PRON', 'role': 'SUBJ'},
        'verb': {'en': 'go', 'pos': 'VERB', 'tense': 'PRESENT_CONTINUOUS'},
        'object': {'en': 'home', 'pos': 'NOUN', 'role': 'OBJ'},
        'negation': False
    }
    
    result = post_process(test_dict)
    print(f"Input:  {test_dict['raw_translation']}")
    print(f"Output: {result}")
    print(f"Expected: I am going home.")
