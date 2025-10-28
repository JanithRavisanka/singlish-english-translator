# Module 1 API Reference
## FST Transliteration Engine - Complete Function Documentation

**Version:** 1.0  
**Student:** Student 1  
**Last Updated:** October 2025

---

## Table of Contents

1. [Core Transliteration](#core-transliteration)
2. [Advanced Features](#advanced-features)
3. [Analysis Tools](#analysis-tools)
4. [Visualization](#visualization)
5. [Interactive Interface](#interactive-interface)
6. [Usage Examples](#usage-examples)

---

## Core Transliteration

### `transliterate(sinlish_text, handle_oov=False)`

Basic FST-based transliteration from Sinlish to Sinhala.

**Parameters:**
- `sinlish_text` (str): Input text in Romanized Sinhala
- `handle_oov` (bool, optional): If True, preserve untransliterable words. Default: False

**Returns:**
- `str`: Transliterated text in Sinhala script

**Raises:**
- `Exception`: If transliteration fails and handle_oov=False

**Complexity:** O(n × m) where n=input length, m=max rule length

**Example:**
```python
from module1 import transliterate

result = transliterate("mama gedara yanawa")
print(result)  # Output: මම ගෙදර යනවා

# Handle OOV gracefully
result = transliterate("mama xyz yanawa", handle_oov=True)
print(result)  # Output: මම xyz යනවා
```

---

## Advanced Features

### `transliterate_nbest(sinlish_text, n=5, return_scores=False)`

Generate multiple transliteration hypotheses using n-shortest paths algorithm.

**Parameters:**
- `sinlish_text` (str): Input text in Sinlish
- `n` (int, optional): Number of hypotheses to generate. Default: 5
- `return_scores` (bool, optional): Include confidence scores. Default: False

**Returns:**
- `List[str]` if return_scores=False: List of transliterations
- `List[Tuple[str, float]]` if return_scores=True: List of (transliteration, confidence) pairs

**Complexity:** O(n×m + k log k) where k=number of hypotheses

**Example:**
```python
from module1 import transliterate_nbest

# Get alternatives without scores
results = transliterate_nbest("mama", n=3)
print(results)  # ['මම', 'මමඅ', ...]

# Get alternatives with confidence scores
results = transliterate_nbest("mama", n=3, return_scores=True)
for text, score in results:
    print(f"{text}: {score:.3f}")
# Output:
#   මම: 1.000
#   මමඅ: 0.850
```

---

### `detect_oov(sinlish_text)`

Detect Out-of-Vocabulary segments and analyze coverage.

**Parameters:**
- `sinlish_text` (str): Input text to analyze

**Returns:**
- `Dict` with keys:
  - `has_oov` (bool): Whether OOV segments exist
  - `coverage` (float): Proportion of transliterable text [0-1]
  - `oov_words` (List[str]): Words that cannot be transliterated
  - `oov_chars` (List[str]): Individual OOV characters
  - `suggestions` (Dict[str, List[str]]): Suggested alternatives
  - `total_words` (int): Total word count
  - `transliterable_words` (int): Successfully transliterable words

**Complexity:** O(w × n × m) where w=number of words

**Example:**
```python
from module1 import detect_oov

info = detect_oov("mama xyz yanawa")
print(f"Has OOV: {info['has_oov']}")  # True
print(f"Coverage: {info['coverage']*100:.1f}%")  # 76.9%
print(f"OOV Words: {info['oov_words']}")  # ['xyz']
print(f"Suggestions: {info['suggestions']}")  # {'xyz': ['oya', 'eye']}
```

---

### `get_alignment(sinlish_text)`

Get character-level alignment showing rule application.

**Parameters:**
- `sinlish_text` (str): Input text

**Returns:**
- `List[Tuple[str, str]]`: List of (input_segment, output_segment) pairs

**Complexity:** O(n × m)

**Example:**
```python
from module1 import get_alignment

alignment = get_alignment("mama gedara")
for inp, out in alignment:
    print(f"'{inp}' → '{out}'")
# Output:
#   'mama' → 'මම'
#   ' ' → ' '
#   'gedara' → 'ගෙදර'
```

---

## Analysis Tools

### Ambiguity Analysis

**File:** `ambiguity_analyzer.py`

#### `analyze_word_ambiguity(word, n_hypotheses=10)`

Analyze a single word for transliteration ambiguity.

**Parameters:**
- `word` (str): Word to analyze
- `n_hypotheses` (int): Number of alternatives to check

**Returns:**
- `Dict` with keys:
  - `word` (str): Input word
  - `is_ambiguous` (bool): Multiple hypotheses exist
  - `num_hypotheses` (int): Count of distinct transliterations
  - `hypotheses` (List[Tuple[str, float]]): Alternatives with scores
  - `entropy` (float): Ambiguity measure (0=unambiguous, higher=more ambiguous)

**Example:**
```python
from ambiguity_analyzer import analyze_word_ambiguity

result = analyze_word_ambiguity("mama", n_hypotheses=5)
print(f"Ambiguous: {result['is_ambiguous']}")
print(f"Entropy: {result['entropy']:.3f}")
```

---

#### `analyze_corpus_ambiguity(corpus_path=None)`

Analyze entire corpus for ambiguity patterns.

**Parameters:**
- `corpus_path` (str, optional): Path to corpus.json

**Returns:**
- `Dict` with corpus-wide statistics

**Example:**
```python
from ambiguity_analyzer import analyze_corpus_ambiguity

analysis = analyze_corpus_ambiguity()
print(f"Ambiguity rate: {analysis['ambiguity_rate']*100:.1f}%")
```

---

#### `find_rule_conflicts()`

Detect conflicting rules that may cause ambiguity.

**Returns:**
- `Dict[str, List[Tuple[str, str]]]`: Mapping of patterns to conflicting rules

**Example:**
```python
from ambiguity_analyzer import find_rule_conflicts

conflicts = find_rule_conflicts()
for pattern, rules in conflicts.items():
    print(f"{pattern}: {rules}")
```

---

### Rule Analysis

**File:** `rule_analyzer.py`

#### `analyze_rule_usage(corpus_path=None)`

Analyze which rules are used in corpus transliteration.

**Returns:**
- `Dict` with comprehensive statistics

**Example:**
```python
from rule_analyzer import analyze_rule_usage

analysis = analyze_rule_usage()
print(f"Coverage: {analysis['coverage_rate']*100:.1f}%")
print(f"Most common rules: {analysis['most_common'][:5]}")
```

---

#### `find_unused_rules()`

Identify rules never used in corpus.

**Returns:**
- `List[str]`: Unused rule patterns

**Example:**
```python
from rule_analyzer import find_unused_rules

unused = find_unused_rules()
print(f"Unused rules: {len(unused)}")
```

---

#### `identify_coverage_gaps()`

Find character sequences not covered by rules.

**Returns:**
- `Dict` with gap analysis

**Example:**
```python
from rule_analyzer import identify_coverage_gaps

gaps = identify_coverage_gaps()
print(f"Coverage gaps: {gaps['total_gaps']}")
```

---

## Visualization

### Alignment Visualization

**File:** `alignment_visualizer.py`

#### `visualize_alignment(text, style='table')`

Create visual representation of transliteration alignment.

**Parameters:**
- `text` (str): Input text
- `style` (str): Visualization style - 'table', 'inline', or 'detailed'

**Returns:**
- `str`: Formatted alignment visualization

**Example:**
```python
from alignment_visualizer import visualize_alignment

# Table format
print(visualize_alignment("mama gedara", style='table'))

# Inline format
print(visualize_alignment("mama", style='inline'))

# Detailed with statistics
print(visualize_alignment("oya bath kanawa", style='detailed'))
```

---

#### `create_latex_alignment(text)`

Generate LaTeX code for alignment (for academic papers).

**Parameters:**
- `text` (str): Input text

**Returns:**
- `str`: LaTeX table code

**Example:**
```python
from alignment_visualizer import create_latex_alignment

latex = create_latex_alignment("mama gedara")
print(latex)  # LaTeX table code
```

---

## Interactive Interface

### Interactive Transliterator

**File:** `interactive_transliterator.py`

Run interactively:
```bash
python interactive_transliterator.py
```

**Available Commands:**
- `:help` - Show help message
- `:alternatives on/off` - Toggle n-best alternatives
- `:alignment on/off` - Toggle alignment display
- `:oov on/off` - Toggle OOV detection
- `:nbest N` - Set number of alternatives
- `:history` - Show translation history
- `:stats` - Show session statistics
- `:quit` - Exit program

**Non-interactive Mode:**
```bash
python interactive_transliterator.py "mama gedara yanawa"
# Output: මම ගෙදර යනවා
```

---

## Usage Examples

### Example 1: Basic Translation Pipeline

```python
from module1 import transliterate

# Translate a single sentence
singlish = "mama iskole yanawa"
sinhala = transliterate(sinlish)
print(f"{sinlish} → {sinhala}")
```

### Example 2: Handling Ambiguity

```python
from module1 import transliterate_nbest

# Get multiple hypotheses
text = "mama"
alternatives = transliterate_nbest(text, n=5, return_scores=True)

print(f"Input: {text}")
for i, (trans, score) in enumerate(alternatives, 1):
    print(f"  {i}. {trans} (confidence: {score:.3f})")
```

### Example 3: OOV Detection and Handling

```python
from module1 import detect_oov, transliterate

text = "mama xyz yanawa"

# Check for OOV
oov_info = detect_oov(text)

if oov_info['has_oov']:
    print(f"Warning: {len(oov_info['oov_words'])} OOV word(s)")
    for word, suggestions in oov_info['suggestions'].items():
        print(f"  '{word}' - try: {', '.join(suggestions)}")
    
    # Transliterate with OOV handling
    result = transliterate(text, handle_oov=True)
else:
    result = transliterate(text)

print(f"Result: {result}")
```

### Example 4: Detailed Alignment Analysis

```python
from module1 import get_alignment
from alignment_visualizer import visualize_alignment

text = "eyala potha kiyawanawa"

# Get programmatic alignment
alignment = get_alignment(text)
print("Alignment pairs:")
for inp, out in alignment:
    print(f"  '{inp}' → '{out}' (ratio: {len(out)}/{len(inp)})")

# Get formatted visualization
print("\n" + visualize_alignment(text, style='detailed'))
```

### Example 5: Rule Coverage Analysis

```python
from rule_analyzer import (analyze_rule_usage, 
                           find_unused_rules,
                           recommend_rule_improvements)

# Analyze rule usage
analysis = analyze_rule_usage()
print(f"Total rules: {analysis['total_rules']}")
print(f"Used: {analysis['used_rules']} ({analysis['coverage_rate']*100:.1f}%)")

# Find unused rules
unused = find_unused_rules()
print(f"\nUnused rules: {len(unused)}")
print("First 5:", unused[:5])

# Get recommendations
recs = recommend_rule_improvements()
print("\nRecommendations:")
for rec in recs:
    print(f"  {rec}")
```

### Example 6: Batch Processing

```python
from module1 import transliterate

sentences = [
    "mama gedara yanawa",
    "eyala potha kiyawanawa",
    "oya bath kanawa"
]

results = []
for sentence in sentences:
    try:
        result = transliterate(sentence)
        results.append((sentence, result, "success"))
    except Exception as e:
        results.append((sentence, None, str(e)))

# Print results
for inp, out, status in results:
    if out:
        print(f"✓ {inp:30} → {out}")
    else:
        print(f"✗ {inp:30} → Error: {status}")
```

### Example 7: Performance Benchmarking

```python
import time
from module1 import transliterate

test_sentences = ["mama gedara yanawa"] * 1000

start = time.time()
for sentence in test_sentences:
    transliterate(sentence)
end = time.time()

total_time = (end - start) * 1000  # Convert to ms
avg_time = total_time / len(test_sentences)

print(f"Total time: {total_time:.2f}ms")
print(f"Average per sentence: {avg_time:.3f}ms")
print(f"Throughput: {len(test_sentences)/total_time*1000:.0f} sentences/sec")
```

---

## Error Handling

### Common Exceptions

**FileNotFoundError:**
```python
# Raised when FST file not found
# Solution: Run python build_fst.py
```

**Exception (Transliteration Failed):**
```python
# Raised when input contains untransliterable characters
# Solution: Use handle_oov=True or check with detect_oov()
```

### Best Practices

1. **Always check for OOV before batch processing:**
```python
oov_info = detect_oov(text)
if not oov_info['has_oov']:
    result = transliterate(text)
```

2. **Use try-except for robust applications:**
```python
try:
    result = transliterate(text)
except Exception as e:
    result = transliterate(text, handle_oov=True)
    logger.warning(f"OOV detected: {e}")
```

3. **Cache FST loading (already done):**
```python
# FST is loaded once at module import
# No need to reload for each transliteration
```

---

## Performance Characteristics

| Operation | Time Complexity | Space Complexity |
|-----------|----------------|------------------|
| transliterate | O(n × m) | O(n) |
| transliterate_nbest | O(n × m + k log k) | O(k × n) |
| detect_oov | O(w × n × m) | O(w) |
| get_alignment | O(n × m) | O(n) |
| FST loading | O(\|Q\| + \|δ\|) | O(\|Q\| + \|δ\|) |

Where:
- n = input length
- m = max rule length  
- k = number of hypotheses
- w = number of words
- Q = FST states
- δ = FST transitions

---

## Version History

**v1.0 (October 2025)**
- Initial release with core transliteration
- N-best path generation
- OOV detection
- Character alignment
- Interactive CLI
- Comprehensive analysis tools

---

**For detailed theoretical background, see MODULE1_REPORT.md**

