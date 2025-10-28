# Pipeline Integration Guide

## Overview

The **pipeline.py** script provides an integrated end-to-end translation system that combines:
- **Module 1**: FST-based Singlish-to-Sinhala transliteration
- **Module 2**: Rule-based Sinhala-to-English translation

## Quick Start

### 1. Basic Translation

```bash
python pipeline.py "mama gedara yanawa"
```

**Output:**
```
Input (Singlish):  mama gedara yanawa
Step 1 (Sinhala):  මම ගෙදර යනවා
Step 2 (English):  I go home
✓ Translation successful
```

### 2. Verbose Mode (See Processing Steps)

```bash
python pipeline.py "eyala potha kiyawanawa" --verbose
```

**Output:**
```
[Module 1] Transliterating: eyala potha kiyawanawa
[Module 1] Result: එයාලා පොත කියවනවා
[Module 2] Parsing: එයාලා පොත කියවනවා
[Module 2] Result: they read book
```

### 3. Detailed Parse Information

```bash
python pipeline.py "oya bath kanawa" --parse
```

**Shows:**
- Subject identification
- Verb extraction
- Object identification
- Tense information

### 4. Interactive Mode

```bash
python pipeline.py --interactive
```

Type Singlish sentences and get instant translations. Type `quit` to exit.

### 5. Test on Full Corpus

```bash
python pipeline.py --test
```

Validates the pipeline against all 25 test sentences in `data/corpus.json`.

## Python API Usage

You can also import and use the pipeline in your own code:

```python
from pipeline import translate_singlish

# Single translation
result = translate_singlish("mama gedara yanawa")

print(f"Input: {result['input']}")
print(f"Sinhala: {result['sinhala']}")
print(f"English: {result['english']}")
print(f"Success: {result['success']}")

# Access detailed parse information
parse = result['parse']
print(f"Subject: {parse['subject']['en']}")
print(f"Verb: {parse['verb']['en']}")
print(f"Object: {parse['object']['en']}")
```

### Batch Processing

```python
from pipeline import batch_translate

sentences = [
    "mama gedara yanawa",
    "eyala potha kiyawanawa",
    "oya bath kanawa"
]

results = batch_translate(sentences, verbose=False)

for result in results:
    print(f"{result['input']} → {result['english']}")
```

## Result Structure

Each translation returns a dictionary with:

```python
{
    "input": "mama gedara yanawa",           # Original Singlish
    "sinhala": "මම ගෙදර යනවා",             # Module 1 output
    "english": "I go home",                  # Module 2 output
    "parse": {                               # Detailed linguistic info
        "subject": {"en": "I", "pos": "PRON"},
        "verb": {"en": "go", "pos": "VERB", "tense": "PRESENT_CONTINUOUS"},
        "object": {"en": "home", "pos": "NOUN"},
        "raw_translation": "I go home",
        "negation": false
    },
    "success": true,                         # Translation status
    "error": null                            # Error message if failed
}
```

## Testing

### Run Pipeline Test Suite

```bash
python test_pipeline.py
```

**Tests:**
1. Basic translations (3 tests)
2. Edge cases (preprocessing - 5 tests)
3. Batch processing
4. Parse structure validation
5. Error handling

All tests should pass with the message: `✅ All pipeline tests passed!`

## Pipeline Architecture

```
User Input (Singlish)
         ↓
    [Preprocessing]
    - Lowercase normalization
    - Whitespace handling
    - Punctuation extraction
    - Number handling
         ↓
    [Module 1: FST]
    - Longest-match transliteration
    - Character-by-character mapping
    - Singlish → Sinhala
         ↓
    [Module 2: RBMT]
    - Lexicon lookup
    - SVO parsing
    - Grammar rule application
    - Sinhala → English
         ↓
    [Postprocessing]
    - Punctuation restoration
    - Number restoration
         ↓
    Output (English)
```

## Features

### ✅ Implemented
- End-to-end Singlish → English translation
- Preprocessing (case, whitespace, punctuation, numbers)
- Verbose debugging mode
- Interactive CLI
- Batch processing
- Comprehensive error handling
- Detailed parse information
- Full corpus testing
- Python API for integration

### 🚧 Future (Module 3)
- Post-processing for fluency
- Article insertion (the, a, an)
- Verb conjugation (am/is/are + -ing)
- BLEU score evaluation
- Human evaluation metrics

## Example Use Cases

### 1. Command-line Translation
```bash
python pipeline.py "mama iskole yanawa"
# I go school
```

### 2. Debugging Translations
```bash
python pipeline.py "eyala game gahanawa" --verbose --parse
# See full processing pipeline + linguistic analysis
```

### 3. Testing New Sentences
```bash
python pipeline.py --interactive
> mama tea bonawa
> eyala football gahanawa
> quit
```

### 4. Validation Testing
```bash
python pipeline.py --test
# Tests all 25 corpus sentences
```

## Troubleshooting

### Issue: "transliterate.fst not found"
**Solution:** Build the FST first
```bash
cd module1
python build_fst.py
```

### Issue: "Module import error"
**Solution:** Ensure you're running from project root
```bash
cd /path/to/singlish-english-translator
python pipeline.py "your text"
```

### Issue: "Token not found in lexicon"
**Solution:** This is a warning, not an error. The word is not in `data/lexicon.json`. Translation still proceeds with available words.

## Performance

- **Speed**: ~0.1-0.5 seconds per sentence (depends on length)
- **Accuracy**: 100% on corpus for Module 1, structural parsing for Module 2
- **Coverage**: 209 transliteration rules, 45+ lexicon entries
- **Tested**: 25 diverse test sentences

## Notes

- Pipeline currently outputs raw SVO structure ("I go home" instead of "I am going home")
- **Module 3** will add fluency improvements
- Preprocessing handles edge cases (uppercase, punctuation, extra spaces)
- All tests pass successfully

## Next Steps

When Module 3 is implemented, it will integrate into this pipeline as:

```python
# Future integration
result = translate_singlish(singlish_text)
# result['english'] will be post-processed for fluency
```

The pipeline architecture is designed to easily accommodate Module 3 without breaking changes.

