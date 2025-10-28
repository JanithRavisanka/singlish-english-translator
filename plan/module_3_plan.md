# Project Canvas: Module 3 (Post-Processor & Evaluator)

**Module Owner:** Student 3

**Core Technology:** Rule-Based Post-processing, MT Evaluation (BLEU, Adequacy, Fluency)

**Primary Dependency:** `nltk` (for BLEU score), `json`, and (critically) the output dict from Module 2.

---

## 1. Core Objective

This module has two primary objectives:

1. **Post-Processing:** To build a Target Language Generation engine that consumes the structured dictionary from Module 2 and applies English-specific grammar rules to generate a fluent, grammatically correct English sentence.
2. **Evaluation:** To design and execute a comprehensive MT Evaluation plan (both automatic and human) for the entire pipeline, as specified in your course notes.

---

## 2. Core NLP Task

This module is a direct implementation of the final stages of the MT pipeline:

1. **Target Language Generation:** Applying rules for English morphology (e.g., verb conjugation like "go" -> "is going") and syntax (e.g., article insertion like "a", "the").
2. **Error Correction & Post-processing:** Fixing punctuation and capitalization.
3. **Automatic Evaluation:** Implementing the BLEU Score to get a quantitative measure of the system's quality.
4. **Human Evaluation:** Implementing the Adequacy & Fluency metrics to get a qualitative, human-centric measure of performance.

---

## 3. Module Architecture (No Code Plan)

Your module consists of two distinct, independent components.

### Part A: The Post-Processing Engine (module3.py)

This module will provide one main function: `post_process(translation_dict)`.

- It will read the structured dict from Module 2 (e.g., `{'raw_translation': 'I book read', 'verb': {'tense': 'PRESENT_CONTINUOUS'}, 'subject': {'person': '1st'}}`).
- It will contain a set of English grammar rules that are applied in order:
  - **Rule 1: Verb Conjugation.** This is your main rule. It will check the `verb['tense']` and `subject['person']` to correctly modify the verb (e.g., `read -> am reading`).
  - **Rule 2: Article Insertion.** A simpler rule to try and insert "a" or "the" before nouns (e.g., `book -> a book`).
  - **Rule 3: Punctuation & Capitalization.** The final, simple rule to capitalize the first letter and add a period.

### Part B: The Evaluation Harness (run_evaluation.py)

This will be the "main" script for the entire project.

- It will import the functions from `module1.py`, `module2.py`, and `module3.py`.
- It will load the shared `corpus.json` to get the inputs and the human "reference" translations.
- It will loop through every item in the corpus and execute the full end-to-end pipeline:
  - `sinhala = module1.transliterate(item['sinlish'])`
  - `dict = module2.translate(sinhala)`
  - `hypothesis = module3.post_process(dict)`
- It will store all the hypothesis sentences and all the reference sentences.
- Finally, it will use `nltk.translate.bleu_score.corpus_bleu` to calculate the final BLEU score for the project and print it.

---

## 4. Key Deliverables (Your 5 Files)

### 1. module3.py (The API)

**Function:** The post-processing engine containing your `post_process(translation_dict)` function.

### 2. test_module3.py (The Proof)

**Function:** A unit test script for your module only. You will create hand-made, example dictionaries to feed into your `post_process` function and assert that the output string is grammatically perfect.

### 3. run_evaluation.py (The Project "Main" Script)

**Function:** The master script that runs the full pipeline from Sinlish to English and prints the final BLEU score. This is the script your team will run to demo the project.

### 4. human_evaluation_sheet.csv (The Tool)

**Function:** A simple CSV/spreadsheet template for your human raters.

**Columns:** `Sentence_ID`, `Source_Text`, `Machine_Translation`, `Adequacy (1-5)`, `Fluency (1-5)`, `Comments`.

### 5. evaluation_report.md (The Final Report)

**Function:** A short 1-2 page report summarizing your findings. It must include:
- The final BLEU Score.
- The average Adequacy and Fluency scores from your human raters.
- A brief analysis of the types of errors the system makes (e.g., "Fails on past-tense verbs," "Module 1 errors," etc.).

---

## 5. Testing Strategy

1. **Unit Testing (test_module3.py):** You must test your `post_process` function in isolation. Create 5-10 "fake" dictionaries that simulate Module 2's output and assert that your function produces the correct English string.

2. **Integration Testing (run_evaluation.py):** This script is the integration test. Its successful execution proves that all three modules work together.

3. **Quality Testing (human_evaluation_sheet.csv):** This is the final, qualitative test to prove your translation is good, not just functional.

---

## 6. Week-by-Week Action Plan

### Week 1: Foundations & Evaluation Design

**Task 1: Setup.** Install Python, `nltk`, and set up your file structure (`module3.py`, `run_evaluation.py`, `test_module3.py`).

**Task 2: Corpus Creation (Team Task).** Meet with Students 1 & 2. Agree on the first 20-30 sentences for `corpus.json`.

**Task 3: Design Human Evaluation.** Create the `human_evaluation_sheet.csv`. Write clear definitions for your 1-5 scales for Adequacy and Fluency (e.g., "5 = All meaning preserved", "1 = No meaning preserved").

**Task 4: Build Unit Tests.** Write `test_module3.py` and first, create your 5-10 fake "test dictionaries" that you will test against.

### Week 2: Build the Post-Processor

**Task 1: Build the API.** Write the main `post_process` function in `module3.py`.

**Task 2: Implement Rules.** Start with the easy rules (capitalization, punctuation).

**Task 3: Implement Verb Rules.** This is your main challenge. Write the if/else logic to handle tense and `subject['person']` (e.g., `if tense == 'PRESENT' and person == '3rd': add 's' to verb`).

**Task 4: Unit Test.** Run `test_module3.py` against your function. Debug `module3.py` until all your unit tests pass.

### Week 3: Build the Evaluation Harness

**Task 1: Write run_evaluation.py.** Write the main script.

**Task 2: Import & Integrate.** `import` the functions from `module1.py` and `module2.py`.

**Task 3: Write the Main Loop.** Write the loop that loads `corpus.json` and calls the full pipeline (Module 1 -> Module 2 -> Module 3).

**Task 4: Calculate BLEU.** Add the `nltk.translate.bleu_score` logic to the end of the script.

**Task 5: First Integration Run.** Run `python run_evaluation.py`. Expect it to fail. This is the start of the integration phase.

### Week 4: Integration, Execution & Reporting

**Task 1: Integration Debug (Team Task).** Sit with your team. Run `run_evaluation.py` and debug all the errors. The error might be in Module 1, 2, or 3. Your script is the "master" that finds these bugs.

**Task 2: Execute Human Evaluation.** Once the pipeline is stable, generate the final "Machine Translation" for all corpus items. Copy these into `human_evaluation_sheet.csv`. Get 2-3 people to act as raters and fill it out.

**Task 3: Collate & Report.** Calculate the average Adequacy and Fluency scores. Get the final BLEU score from your script.

**Task 4: Write evaluation_report.md.** Write your final 1-page report summarizing all findings. This report is the final deliverable for the entire project.