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

## Installation

1. **Clone the repository**
   ```bash
   cd singlish-english-translator
   ```

2. **Install dependencies**
   
   **Recommended: Using Conda**
   ```bash
   conda install -c conda-forge pynini nltk
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

## Project Structure

```
singlish-english-translator/
├── README.md
├── requirements.txt
├── corpus.json                 # Shared test data
├── singlish_rules.json         # Transliteration rules (Module 1)
├── lexicon.json                # Bilingual dictionary (Module 2)
├── module1/                    # FST Transliteration Engine
│   ├── build_fst.py
│   ├── module1.py
│   ├── test_module1.py
│   └── transliterate.fst       # Generated FST model
├── module2/                    # RBMT Translation Engine
│   ├── module2.py
│   └── test_module2.py
└── module3/                    # Post-Processor & Evaluator
    ├── module3.py
    ├── test_module3.py
    ├── run_evaluation.py
    ├── human_evaluation_sheet.csv
    └── evaluation_report.md
```

## Usage

### Module 1: Build and Test FST

```bash
cd module1
python build_fst.py          # Compile the FST
python test_module1.py       # Test transliteration
```

### Module 2: Test Translation

```bash
cd module2
python test_module2.py       # Test RBMT engine
```

### Module 3: Run Full Pipeline Evaluation

```bash
cd module3
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

