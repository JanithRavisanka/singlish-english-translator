# Project Plan: Singlish-to-English NLP Cascade Translator

**Project:** A 3-Module NLP Pipeline to translate "Singlish" (Sinhala in Roman script) into fluent, grammatically correct English.

**Team:** 3 Students (Student 1, Student 2, Student 3)

**Course:** NLP Machine Translation Module

---

## 1. Project Overview & Core Objectives

This project is a cascading translation system. It will take "Singlish" as input and pass it through three distinct, specialized NLP modules to produce an English translation.

### Core Objectives

1. **Transliterate:** To build a robust Singlish-to-Sinhala transliteration engine using a Finite-State Transducer (FST).
2. **Translate:** To build a Rule-Based Machine Translation (RBMT) engine to translate Sinhala script into a structured English representation, handling key grammatical transformations (e.g., SOV to SVO).
3. **Refine:** To build a post-processing module that converts the structured English into a fluent, readable sentence.
4. **Evaluate:** To scientifically evaluate the entire pipeline's performance using both automatic metrics (BLEU) and human evaluation (Adequacy & Fluency), as specified in the course notes.

---

## 2. System Architecture

The system is a linear pipeline. The output of one module becomes the input for the next.

### Full Data Flow

```
Input (str) 
  -> [Module 1: FST Engine] 
  -> Output (str) 
  -> [Module 2: RBMT Engine] 
  -> Output (dict) 
  -> [Module 3: Post-Processor] 
  -> Output (str) 
  -> [Module 3: Evaluator] 
  -> Output (Score)
```

### Example Flow

```
"mama potha kiyawanawa"
    ↓ (Module 1)
"මම පොත කියවනවා"
    ↓ (Module 2)
{ 'raw': 'I book read', 'tense': 'PRESENT', 'subject': 'I' }
    ↓ (Module 3)
"I read the book."
    ↓ (Evaluation)
BLEU Score: 0.85 (compared to reference)
```

---

## 3. Technology Stack & Dependencies

**Primary Language:** Python 3.9+

### Key Dependencies

- **pynini:** (For Student 1) The Google OpenFst library for Python. Used to build, compile, and apply the FST.
- **nltk:** (For Student 3) Used for automatic evaluation (nltk.translate.bleu_score) and potentially tokenization.
- **json:** (For All) The standard library for reading and writing all shared data files (corpus, rules, lexicons).

---

## 4. Shared Assets (The "Single Source of Truth")

These files form the shared knowledge base for the entire project. They must be created and agreed upon in Week 1.

### corpus.json
The primary testbed. All modules test against this.

```json
[
  {
    "id": 1,
    "sinlish": "mama gedara yanawa",
    "sinhala": "මම ගෙදර යනවා",
    "english_reference": "I am going home."
  },
  {
    "id": 2,
    "sinlish": "eyala potha kiyawanawa",
    "sinhala": "එයාලා පොත කියවනවා",
    "english_reference": "They are reading the book."
  }
]
```

### singlish_rules.json
(Input for Module 1) The mapping file for the FST.

**Crucial Rule:** Must be ordered from longest match to shortest match to ensure correctness.

```json
{
  "gedara": "ගෙදර",
  "yanawa": "යනවා",
  "mama": "මම",
  "potha": "පොත",
  "kaa": "කා",
  "ki": "කි",
  "ka": "ක",
  "g": "ග්",
  "m": "ම්",
  "a": "අ"
}
```

### lexicon.json
(Input for Module 2) The bilingual dictionary and grammar rules.

```json
{
  "මම": { "en": "I", "pos": "PRON", "role": "SUBJ" },
  "ගෙදර": { "en": "home", "pos": "NOUN", "role": "OBJ" },
  "යනවා": { "en": "go", "pos": "VERB", "tense": "PRESENT_CONTINUOUS" },
  "පොත": { "en": "book", "pos": "NOUN", "role": "OBJ" },
  "කියවනවා": { "en": "read", "pos": "VERB", "tense": "PRESENT_CONTINUOUS" }
}
```

---

## 5. Module 1: FST Transliteration Engine (Student 1)

**Objective:** Convert an ambiguous Sinlish string into a perfect Sinhala script string.

**Core NLP Task:** Phonological Modeling & Finite-State Transduction.

### Functionalities & Deliverables

This module has two parts: a build-time script and a run-time script.

#### 1. build_fst.py (Build-Time Script)

**Function:** A utility script you run once (or whenever rules change).

**Steps:**
1. Read the `sinlish_rules.json` file.
2. Convert the JSON dictionary into a list of `(sinlish_str, sinhala_str)` tuples.
3. Create the FST: `fst = pynini.string_map(rules_list)`.
4. Optimize the FST: `fst.optimize()`.
5. Save the compiled FST to disk: `fst.write("transliterate.fst")`.

**Deliverable:** `build_fst.py`

#### 2. transliterate.fst (Compiled FST)

**Function:** The binary, optimized FST file created by `build_fst.py`. This is your "model".

**Deliverable:** `transliterate.fst`

#### 3. module1.py (Run-Time Module)

**Function:** The file that the rest of the team will import.

**Contains one function:** `def transliterate(sinlish_text: str) -> str:`

**Internal Steps:**
- On initialization, load the compiled FST: `fst = pynini.Fst.read("transliterate.fst")`. (This is done once).
- When `transliterate` is called, apply the FST to the input text.
- Use `pynini.rewrite.top_rewrite(sinlish_text, fst)` to get the single best transliteration.
- Return the resulting Sinhala string.

**Deliverable:** `module1.py`

---

## 6. Module 2: RBMT Translation Engine (Student 2)

**Objective:** Translate clean Sinhala script (from Module 1) into a structured English representation (a Python dictionary).

**Core NLP Task:** Syntactic Parsing & Rule-Based Transfer (SOV -> SVO).

### Functionalities & Deliverables

#### 1. module2.py (Run-Time Module)

**Function:** Contains the core translation logic in a single function.

**Function:** `def translate(sinhala_text: str) -> dict:`

**Internal Pipeline:**
1. **Tokenize:** Split `sinhala_text` into a list of tokens (words). e.g., `['මම', 'පොත', 'කියවනවා']`.
2. **Lexical Analysis:** Loop through tokens. Look up each token in the shared `lexicon.json` to get its `en` translation, `pos`, `role`, and `tense`.
3. **Syntactic Parse:** Identify the main components: Subject, Object, Verb (based on the "role" from the lexicon).
4. **Transfer Rule:** Apply the primary SOV -> SVO grammar rule by re-ordering the parsed components.
5. **Generate Output Dictionary:** Construct and return a Python dictionary with all the structured information Module 3 will need. This is your critical output.

**Example Output:**

```json
{
  "raw_translation": "I book read",
  "subject": { "en": "I", "pos": "PRON" },
  "object": { "en": "book", "pos": "NOUN" },
  "verb": { "en": "read", "tense": "PRESENT_CONTINUOUS" },
  "negation": false
}
```

**Deliverable:** `module2.py`

**Shared Duty:** Student 2 is the primary owner/manager of the `lexicon.json` file.

---

## 7. Module 3: Post-Processor & Evaluator (Student 3)

**Objective:** Convert the raw dictionary from Module 2 into a fluent English sentence AND scientifically evaluate the entire pipeline.

**Core NLP Task:** Target Language Generation & MT Evaluation.

### Functionalities & Deliverables

#### 1. module3.py (Run-Time Module)

**Function:** Contains the post-processing logic.

**Function:** `def post_process(translation_dict: dict) -> str:`

**Internal Rules:**
- **Verb Conjugation:** Use `translation_dict['subject']` and `translation_dict['verb']` to generate the correct verb form. (e.g., if subject is `he` and verb is `go`, output `goes`).
- **Article Insertion:** (A simple rule) If object is a singular NOUN, add "a" or "the" before it.
- **Tense Handling:** Use `verb['tense']` to construct the correct form (e.g., PRESENT_CONTINUOUS -> is reading).
- **Formatting:** Join the final words, capitalize the first letter, and add a period.
- Return the final, fluent English string.

**Deliverable:** `module3.py`

#### 2. run_evaluation.py (The "Main" Project Script)

**Function:** This script ties everything together and runs the final evaluation.

**Internal Steps:**
1. `import` functions from `module1.py`, `module2.py`, and `module3.py`.
2. Load the shared `corpus.json`.
3. Initialize lists: `hypotheses = []`, `references = []`.
4. Loop through every item in the corpus:
   - `sinlish_input = item['sinlish']`
   - `reference_english = item['english_reference']`
   - **Run the Full Pipeline:**
     - `sinhala = module1.transliterate(sinlish_input)`
     - `tx_dict = module2.translate(sinhala)`
     - `hypothesis_english = module3.post_process(tx_dict)`
   - Print the result for this sentence.
   - Add `hypothesis_english` and `reference_english` to your lists.
5. After the loop, calculate metrics:
   - **BLEU Score:** `score = nltk.translate.bleu_score.corpus_bleu(references, hypotheses)`
   - Print a final report with the overall BLEU score.

**Deliverable:** `run_evaluation.py`

#### 3. Evaluation_Report.md (The Final Report)

**Function:** A written analysis of the project's success.

**Contents:**
- The final BLEU Score from `run_evaluation.py`.
- **Human Evaluation Scores:** A table showing the Adequacy and Fluency scores (1-5) for your translations (as rated by your teammates).
- **Error Analysis:** A brief discussion of why the system failed. (e.g., "Our FST failed on this word," or "Our RBMT rules didn't cover this sentence structure.").

**Deliverable:** `Evaluation_Report.md`

---

## 8. Project Timeline & Milestones

### Week 1: Setup & Data (All Students)

**Goal:** Set up the project, install dependencies (`pynini`, `nltk`).

**CRITICAL TASK:** All three students must meet and agree on the first 20-30 entries for `corpus.json`, `sinlish_rules.json`, and `lexicon.json`. Do not start coding until this is done.

### Week 2: Independent Module Development

- **Student 1:** Build `build_fst.py` and the first version of `module1.py`. Test it against `corpus.json`.
- **Student 2:** Build the first version of `module2.py`. Test it against the `sinhala` field in `corpus.json`.
- **Student 3:** Build `module3.py`. Mock the input dictionary (e.g., `test_dict = {'raw': ...}`) to test your `post_process` function.

### Week 3: Integration & Evaluation Script

- **Student 3:** Build `run_evaluation.py` and attempt the first integration run.
- **All Students:** Meet to debug the pipeline. Fix errors in the data files (`.json`) and module logic based on the integration test.

### Week 4: Refinement & Final Evaluation

- **All Students:** Continue to fix bugs and add more rules/words to the shared JSON files to handle more sentences from the corpus.
- **Student 3:** Run the human evaluation (Adequacy & Fluency) with the other two students as raters.
- **All Students:** Finalize the code. Student 3 generates the final `Evaluation_Report.md`.