# Project Canvas: Module 2 (Sinhala-to-English Engine)

**Module Owner:** Student 2

**Core Technology:** Rule-Based Machine Translation (RBMT)

**Primary Dependency:** `json` (for reading the shared lexicon)

---

## 1. Core Objective

To design and build a Rule-Based Machine Translation (RBMT) engine that parses clean Sinhala script (from Module 1) and translates it into a structured Python dictionary. This dictionary will contain the raw English translation and the rich grammatical metadata (tense, part-of-speech, roles) required by Module 3 for fluent sentence generation.

---

## 2. Core NLP Task

This module directly addresses several key challenges from your course notes:

1. **Source Language Analysis:** Performing morphological and simple syntactic analysis on the Sinhala input to understand "who did what to whom."
2. **Lexical Selection:** Choosing the correct English equivalent for each Sinhala word using a bilingual lexicon.
3. **Syntactic Transfer:** Applying linguistic rules to transform the Sinhala Subject-Object-Verb (SOV) grammatical structure into an English-compatible Subject-Verb-Object (SVO) structure.

---

## 3. Module Architecture (No Code Plan)

Your module's core logic will be a 4-stage internal pipeline, all contained within your main `translate` function.

### Stage 1: Tokenization

The input (e.g., "මම පොත කියවනවා") will be split into a list of word tokens: `['මම', 'පොත', 'කියවනවා']`.

### Stage 2: Lexical Analysis (Tagging)

- You will loop through each token.
- For each token, you will look it up in the shared `lexicon.json`.
- You will build a new internal list of "tagged" tokens, containing all the information from the lexicon (e.g., `[{'word': 'මම', 'en': 'I', 'role': 'SUBJ'}, {'word': 'පොත', ...}]`).

### Stage 3: Syntactic Parsing & Transfer (The "Rule")

- You will parse your tagged token list to identify the key components: the Subject, the Object, and the Verb (based on the `'role'` property you defined in the lexicon).
- You will then apply your primary transfer rule: re-order these components from SOV to SVO.

### Stage 4: Structured Output Generation

- You will construct the final output dictionary.
- The `raw_translation` key will be the re-ordered English words (e.g., `S['en'] + " " + V['en'] + " " + O['en']`).
- You will then add all the other grammatical metadata (like the verb's tense, the subject's properties, etc.) to the dictionary for Module 3 to use.

---

## 4. Key Deliverables (Your 3 Files)

These are the files you are responsible for creating and managing:

### 1. module2.py (The API)

**Function:** The final, clean Python file for your team to use. It will contain your primary function: `translate(sinhala_text: str) -> dict:`.

This file will contain all the 4-stage pipeline logic described above.

### 2. test_module2.py (The Proof)

**Function:** A test script that you use to prove your module works. It will read the shared `corpus.json`, run your `translate` function on the "sinhala" text, and check if the output dictionary's key values are correct.

### 3. lexicon.json (Shared Data - You are the Owner)

**Function:** The "brain" of your module. While this is a shared team file, you are the primary owner and manager.

**Your Responsibility:** You must ensure every Sinhala word in the `corpus.json` has a complete and accurate entry in this file.

**Example Entry:**

```json
"කියවනවා": {
  "en": "read",
  "pos": "VERB",
  "role": "VERB",
  "tense": "PRESENT_CONTINUOUS"
}
```

---

## 5. Testing Strategy

Your testing will be "golden-data" driven, using the shared `corpus.json`.

The `test_module2.py` script will be your main development tool.

### Process:

1. The script will read `corpus.json`.
2. For each item, it will run `actual_dict = translate(item['sinhala'])`.
3. You will need to create an "expected output" for each test.
4. It will assert that key values are correct (e.g., `assert actual_dict['raw_translation'] == "I read book"`).
5. It will print a PASS or FAIL for each item.

**Your Definition of "Done":** Your module is complete when `test_module2.py` runs and all tests pass.

---

## 6. Week-by-Week Action Plan

### Week 1: Foundations & Lexicon Creation

**Task 1: Setup.** Install Python and set up your file structure (`module2.py`, `test_module2.py`).

**Task 2: Corpus Creation (Team Task).** Meet with Students 1 & 3. Agree on the first 20-30 sentences for the shared `corpus.json` file.

**Task 3: Lexicon Creation.** This is your main task this week. Manually analyze every Sinhala word in the `corpus.json`. Create the first draft of `lexicon.json`. Define your data structure (e.g., `en`, `pos`, `role`, `tense`) and fill it out completely.

### Week 2: Build, Tokenize, and Parse

**Task 1: Build the API.** Write the main `translate` function in `module2.py`.

**Task 2: Implement Pipeline Stages 1 & 2.** Write the logic for the Tokenizer and the Lexical Analyzer (the part that looks up tokens in your `lexicon.json`).

**Task 3: Implement Stage 3 (The Rule).** Write the logic to identify the S, O, and V from your tagged tokens and re-order them.

**Task 4: Build the Test Harness.** Write the `test_module2.py` script. Define your "expected" dictionaries for your tests.

### Week 3: The "Debug Loop" (Your Core Work)

This entire week is an iterative cycle. Your goal is to get `test_module2.py` to pass 100%.

**The Loop:**
1. Run `python test_module2.py`.
2. Observe a FAIL (e.g., `KeyError: 'කියවනවා'` or `AssertionError: 'raw_translation' is wrong`).
3. **Debug:**
   - If it's a `KeyError`, you missed a word. Fix `lexicon.json`.
   - If it's an `AssertionError`, your logic is wrong. Fix `module2.py`.
4. Go back to Step 1 and repeat.

**Goal:** By the end of this week, `test_module2.py` reports "All tests passed!"

### Week 4: Integration & Support

**Task 1: Finalize & Deliver.** "Freeze" your working `module2.py`. Make sure `lexicon.json` is complete.

**Task 2: Integration Test 1 (with Module 1).** Work with Student 1. Run your function using their output: `translate(module1.transliterate("mama potha kiyawanawa"))`. Debug any issues.

**Task 3: Hand-off & Support (for Module 3).** Give Student 3 your final `module2.py` and `lexicon.json`. You must be the expert on the exact structure of the dictionary your function returns, as Student 3 depends on it 100%.