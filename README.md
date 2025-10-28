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

## Module 1: Advanced Enhancements ✨

Module 1 has been significantly enhanced with advanced FST features and comprehensive documentation:

**🎯 Advanced Features:**
- ✅ N-best path generation with confidence scoring
- ✅ Out-of-Vocabulary (OOV) detection with suggestions
- ✅ Character-level alignment visualization
- ✅ Ambiguity detection and analysis
- ✅ Rule usage statistics and coverage analysis
- ✅ Interactive CLI with real-time transliteration

**📊 Analysis Tools:**
- `ambiguity_analyzer.py` - Detect and analyze transliteration ambiguities
- `rule_analyzer.py` - Comprehensive rule usage and coverage statistics
- `alignment_visualizer.py` - Multiple visualization styles (table/inline/detailed)
- `interactive_transliterator.py` - Interactive CLI interface

**📚 Comprehensive Documentation:**
- `MODULE1_REPORT.md` - 2000+ line academic technical report with FST theory
- `API_REFERENCE.md` - Complete API documentation with examples
- `ENHANCEMENTS_SUMMARY.md` - Detailed enhancement overview

**📈 Statistics:**
- Code: 269 → 4833+ lines (1696% growth)
- Test Accuracy: 100% (25/25 sentences)
- Performance: <1ms per word transliteration
- Documentation: 3000+ lines

See `module1/ENHANCEMENTS_SUMMARY.md` for complete details.

---

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

### Module 1: Advanced FST Transliteration Engine

**Basic Usage:**
```bash
cd module1
python build_fst.py          # Compile the FST
python test_module1.py       # Test transliteration (100% accuracy)
```

**Advanced Features:**
```bash
# Interactive transliterator with real-time feedback
python interactive_transliterator.py

# Analyze rule usage and coverage
python rule_analyzer.py

# Detect ambiguities in transliteration
python ambiguity_analyzer.py

# Visualize character alignments
python alignment_visualizer.py "mama gedara yanawa"
```

**Programmatic Usage:**
```python
from module1 import (transliterate, transliterate_nbest, 
                     detect_oov, get_alignment)

# Basic transliteration
result = transliterate("mama gedara yanawa")

# Get n-best alternatives with confidence scores
alternatives = transliterate_nbest("mama", n=3, return_scores=True)

# Detect out-of-vocabulary segments
oov_info = detect_oov("mama xyz yanawa")

# Get character-level alignment
alignment = get_alignment("mama gedara")
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

