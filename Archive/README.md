# Singlish-to-English NLP Translator

A 3-Module NLP Pipeline to translate "Singlish" (Sinhala in Roman script) into fluent, grammatically correct English.

## Project Overview

This project implements a cascading translation system that processes Singlish input through three specialized NLP modules:

1. **Module 1: FST Transliteration Engine** - Converts Singlish to Sinhala script using Finite-State Transducers
2. **Module 2: RBMT Translation Engine** - Translates Sinhala to structured English using Rule-Based Machine Translation
3. **Module 3: Post-Processor & Evaluator** - Generates fluent English sentences and evaluates the pipeline

## System Architecture

```
Input (Singlish) 
  -> [Module 1: FST Engine] 
  -> Output (Sinhala Script)
  -> [Module 2: RBMT Engine] 
  -> Output (Structured Dict)
  -> [Module 3: Post-Processor] 
  -> Output (English Sentence)
  -> [Evaluator] 
  -> BLEU Score
```

## Key Features

### Module 1 Enhancements
- ✨ **Unicode to ASCII Conversion**: Automatically handles accented characters and non-Latin scripts using `unidecode`
- ✨ **Spell Checking**: Fuzzy matching with Levenshtein distance to correct common typos (65% similarity threshold)
- ✅ **Preprocessing Pipeline**: Case normalization, punctuation preservation, number handling
- ✅ **266 Transliteration Rules**: Comprehensive longest-match FST-based conversion

### Module 2 Features
- ✅ **68-Word Lexicon**: POS-tagged bilingual dictionary
- ✅ **SVO Parsing**: Subject-Verb-Object structure extraction
- ✅ **Tense Detection**: Identifies present continuous tense

### Integration
- ✅ **50-Sentence Corpus**: Comprehensive test coverage
- ✅ **Pipeline API**: Command-line and Python interfaces
- ✅ **100% Test Pass Rate**: All modules fully tested

## Installation

1. **Clone the repository**
   ```bash
   cd singlish-english-translator
   ```

2. **Install dependencies**
   
   **Recommended: Using Conda**
   ```bash
   conda install -c conda-forge pynini nltk
   pip install unidecode
   ```
   
   **Alternative: Using pip** (requires OpenFST installed)
   ```bash
   # On macOS
   brew install openfst
   
   # Then install Python packages
   pip install -r requirements.txt
   ```

3. **Download NLTK data** (for Module 3)
   ```python
   python -c "import nltk; nltk.download('punkt')"
   ```

4. **Install Gradio for Web UI** (optional)
   ```bash
   pip install -r requirements_ui.txt
   ```

## Project Structure

```
singlish-english-translator/
├── README.md
├── requirements.txt
├── requirements_ui.txt         # ⭐ UI dependencies
├── app.py                      # ⭐ Gradio web interface
├── pipeline.py                 # ⭐ Integrated full pipeline
├── run_evaluation.py           # ⭐ Complete evaluation with BLEU scores
├── test_pipeline.py            # Pipeline integration tests
├── data/                       # Shared data files
│   ├── corpus.json             # 50 test sentences (Singlish, Sinhala, English)
│   ├── singlish_rules.json     # 266 transliteration rules
│   └── lexicon.json            # 68-word bilingual dictionary
├── transliteration/            # Module 1: FST Transliteration Engine
│   ├── build_fst.py            # FST compiler
│   ├── module1.py              # Main transliteration module
│   ├── preprocess.py           # Preprocessing (Unicode, punctuation, numbers)
│   ├── fuzzy_matcher.py        # Spell correction engine
│   ├── test_module1.py         # Comprehensive tests (77 tests)
│   └── transliterate.fst       # Generated FST model
├── translation/                # Module 2: RBMT Translation Engine
│   ├── module2.py              # Rule-based parser
│   └── test_module2.py         # Module 2 tests
└── evaluation/                 # Module 3: Post-Processor & Evaluator
    ├── module3.py              # Post-processing rules
    ├── test_module3.py         # Module 3 tests (10 tests)
    ├── README.md               # Module 3 documentation
    ├── human_evaluation_sheet.csv
    └── evaluation_report.md    # Comprehensive evaluation findings
```

## Usage

### Quick Start: Integrated Pipeline

Translate Singlish directly to English using the integrated pipeline:

```bash
# Single translation
python pipeline.py "mama gedara yanawa"

# With detailed output
python pipeline.py "eyala potha kiyawanawa" --verbose --parse

# Interactive mode
python pipeline.py --interactive

# Test on full corpus
python pipeline.py --test

# Run pipeline test suite
python test_pipeline.py
```

**Pipeline Output:**
```
Input (Singlish):  mama gedara yanawa
Step 1 (Sinhala):  මම ගෙදර යනවා
Step 2 (English):  I go home
✓ Translation successful
```

### Web Interface (Gradio UI)

Launch the interactive web interface to see all pipeline stages visually:

```bash
python app.py
```

**Features:**
- 🌐 Interactive web UI at http://127.0.0.1:7860
- 📊 View all three pipeline stages (Sinhala, Raw English, Final English)
- 🔍 See parse details (Subject, Verb, Object, Tense)
- 💡 Click example sentences for quick testing
- ✅ Real-time translation with visual feedback

**Interface Displays:**
1. **Module 1 Output:** Sinhala script transliteration
2. **Module 2 Output:** Raw English with parse structure (SUBJ, VERB, OBJ)
3. **Module 3 Output:** Fluent, grammatically correct English

Perfect for demos, presentations, and understanding how the pipeline works!

### Module 1: Build and Test Transliteration

```bash
cd transliteration
python build_fst.py          # Compile the FST
python test_module1.py       # Test transliteration (77 tests)
```

### Module 2: Test Translation

```bash
cd translation
python test_module2.py       # Test RBMT engine
```

### Module 3: Test Post-Processing & Run Full Evaluation

```bash
cd evaluation
python test_module3.py       # Test post-processing (10 tests)
cd ..
python run_evaluation.py     # Execute end-to-end pipeline and calculate BLEU score
```

## Development Timeline

- **Week 1**: Setup & Data Collection (All modules)
- **Week 2**: Independent Module Development
- **Week 3**: Integration & Debugging
- **Week 4**: Refinement & Final Evaluation

## Team

- **Student 1**: Module 1 (FST Transliteration)
- **Student 2**: Module 2 (RBMT Translation)
- **Student 3**: Module 3 (Post-Processing & Evaluation)

## Course

NLP Machine Translation Module

## License

Academic Project - Course Assignment

