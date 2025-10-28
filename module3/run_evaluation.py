"""
Module 3: Full Pipeline Evaluation Script
Student 3

This is the main script for the entire project. It runs the full end-to-end
pipeline (Module 1 -> Module 2 -> Module 3) and calculates the BLEU score.

Usage:
    python run_evaluation.py

Expected Output:
    - Per-sentence results showing the full pipeline
    - Final BLEU score for the entire corpus
"""

# TODO: Implement full pipeline evaluation
# Steps:
# 1. Import functions from all modules:
#    - from module1.module1 import transliterate
#    - from module2.module2 import translate
#    - from module3 import post_process
# 2. Load corpus.json from parent directory
# 3. Initialize lists: hypotheses = [], references = []
# 4. For each item in corpus:
#    - sinlish_input = item['sinlish']
#    - reference_english = item['english_reference']
#    - Run full pipeline:
#      * sinhala = transliterate(sinlish_input)
#      * tx_dict = translate(sinhala)
#      * hypothesis_english = post_process(tx_dict)
#    - Print results for this sentence
#    - Append to hypotheses and references lists
# 5. Calculate BLEU score:
#    - from nltk.translate.bleu_score import corpus_bleu
#    - score = corpus_bleu([[ref] for ref in references], hypotheses)
# 6. Print final report with overall BLEU score

