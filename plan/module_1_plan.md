# Project Canvas: Module 1 (Singlish-to-Sinhala Engine)

**Module Owner:** Student 1

**Core Technology:** Finite-State Transducer (FST)

**Primary Dependency:** `pynini` (Google OpenFst Python Library)

---

## 1. Core Objective

To design, build, and compile a Finite-State Transducer (FST) that accurately and efficiently transliterates ambiguous Sinlish (Roman script) text into its correct, unambiguous Sinhala script equivalent.

---

## 2. Core NLP Task

This module directly addresses two key NLP challenges:

1. **Phonological Modeling:** Mapping the sound rules of Sinlish (e.g., `th`, `ng`, `dh`) to the correct Sinhala graphemes.
2. **Ambiguity & Longest-Match:** Solving the core transliteration problem. The FST must be smart enough to choose the rule for "gedara" (ගෙදර) over the rules for "ge" (ගෙ) or "g" (ග්).

---

## 3. Module Architecture (No Code Plan)

Your module will consist of two distinct parts: a "Build-Time" process and a "Run-Time" engine.

### Part A: Build-Time (The "Compiler")

- You will create a human-readable rules file (`sinlish_rules.json`). This file defines all your Sinlish-to-Sinhala mappings (e.g., `"ka" -> "ක"`).
- You will write a build script (`build_fst.py`).
- This script's only job is to read `sinlish_rules.json` and use the `pynini` library to compile all those rules into a single, highly optimized, binary file: `transliterate.fst`.
- This process is done once before the main program runs (or anytime you update your rules).

### Part B: Run-Time (The "Engine")

- You will create the main API file (`module1.py`) that your teammates will import.
- When this file is first imported, it will load the pre-compiled `transliterate.fst` file into memory one time.
- It will provide a single, simple function: `transliterate(text)`.
- When this function is called, it will use pynini's fast "rewrite" methods to apply the compiled FST to the input string and return the result.
- This will be extremely fast because all the complex logic is already compiled into the FST.

---

## 4. Key Deliverables (Your 5 Files)

These are the five files you are responsible for creating:

### 1. sinlish_rules.json (The Data)

**Function:** The "brain" of your module. A JSON file mapping all Sinlish patterns to their Sinhala counterparts.

**Crucial Constraint:** You must order this file from longest-match to shortest-match (e.g., "gedara" must appear before "ge" or "g") for the FST to compile correctly.

### 2. build_fst.py (The Compiler)

**Function:** A Python script that reads `sinlish_rules.json` and uses `pynini` to create the final `transliterate.fst` file.

### 3. transliterate.fst (The Model)

**Function:** The final, binary, compiled FST file. This is your "model." This file (along with `module1.py`) is one of your main hand-offs to the team.

### 4. module1.py (The API)

**Function:** The final, clean Python file for your team to use. It will contain the `transliterate(sinlish_text)` function. This function will load `transliterate.fst` and perform the translation.

### 5. test_module1.py (The Proof)

**Function:** A test script that you use to prove your module works. It will read the shared `corpus.json`, run your `transliterate` function on the "sinlish" text, and check if it matches the "sinhala" text.

---

## 5. Testing Strategy

Your testing will be "golden-data" driven, using the shared `corpus.json`.

The `test_module1.py` script will be your main development tool.

### Process:

1. The script will read `corpus.json`.
2. For each item, it will run `actual = transliterate(item['sinlish'])`.
3. It will compare `actual` to `expected = item['sinhala']`.
4. It will print a PASS or FAIL for each item.

**Your Definition of "Done":** Your module is complete when `test_module1.py` runs and reports "All tests passed!"

---

## 6. Week-by-Week Action Plan

### Week 1: Foundations & Data Collection

**Task 1: Setup.** Install Python, `pynini`, and your code editor. (Note: `pynini` can sometimes be complex to install, so do this first).

**Task 2: Corpus Creation (Team Task).** Meet with Students 2 & 3. Agree on the first 20-30 sentences for the shared `corpus.json` file. This is your "golden" test data.

**Task 3: Rule Creation.** Manually analyze the words in `corpus.json`. Create the first draft of `sinlish_rules.json`. Ensure you add rules for whole words, syllables, and single letters, and order them correctly (longest-first).

### Week 2: Build, Compile, and Test

**Task 1: Build the Compiler.** Write the `build_fst.py` script.

**Task 2: Build the API.** Write the `module1.py` file with its `transliterate` function.

**Task 3: Build the Test Harness.** Write the `test_module1.py` script.

**Task 4: First Run.**
- Run `python build_fst.py` to create your first `transliterate.fst`.
- Run `python test_module1.py`.
- **Expectation:** Most tests will fail. This is normal. Now you have a baseline.

### Week 3: The "Debug Loop" (Your Core Work)

This entire week is an iterative cycle. Your goal is to get `test_module1.py` to pass 100%.

**The Loop:**
1. Run `python test_module1.py`.
2. Observe a FAIL (e.g., `potha` incorrectly becomes `පොtha`).
3. Open `sinlish_rules.json` and fix the rule (e.g., add the `"potha": "පොත"` rule before the `"po"` rule).
4. Run `python build_fst.py` to re-compile your FST with the new rules.
5. Go back to Step 1 and repeat.

**Goal:** By the end of this week, `test_module1.py` reports "All tests passed!"

### Week 4: Integration & Support

**Task 1: Finalize & Deliver.** "Freeze" your working `module1.py` and `transliterate.fst` files.

**Task 2: Hand-off.** Give these two files to Student 2 and Student 3.

**Task 3: Support.** Help your teammates integrate your module. You will be the expert on file paths, `pynini` import errors, and any issues related to your module's output.

**Task 4 (Bonus):** If your team adds more items to `corpus.json`, repeat your "Debug Loop" to ensure your module supports the new words.