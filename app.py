"""
Gradio Web Interface for Singlish-to-English Translator
========================================================

Interactive web UI that displays all three pipeline stages:
- Module 1: FST Transliteration (Singlish → Sinhala)
- Module 2: RBMT Translation (Sinhala → Raw English)
- Module 3: Post-Processing (Raw English → Fluent English)

Usage:
    python app.py
    
Then open browser at http://127.0.0.1:7860
"""

import gradio as gr
from pipeline import translate_singlish
from evaluation.module3 import post_process


def translate_with_details(singlish_input):
    """
    Wrapper function for Gradio that returns all pipeline stages.
    
    Args:
        singlish_input: Singlish text from user
        
    Returns:
        Tuple of (sinhala_output, raw_english, parse_details, final_english, status_message)
    """
    if not singlish_input or not singlish_input.strip():
        return (
            "",
            "",
            "⚠️ Please enter some Singlish text to translate.",
            "",
            "❌ No input provided"
        )
    
    try:
        # Run the full pipeline
        result = translate_singlish(singlish_input.strip(), verbose=False)
        
        if not result['success']:
            error_msg = result.get('error', 'Unknown error')
            return (
                "",
                "",
                f"❌ Translation failed: {error_msg}",
                "",
                "❌ Error occurred"
            )
        
        # Extract outputs
        sinhala_output = result['sinhala']
        raw_english = result['parse'].get('raw_translation', '')
        
        # Apply Module 3 post-processing
        final_english = post_process(result['parse'])
        
        # Format parse details
        parse_info = result['parse']
        parse_details = "**Parse Structure:**\n\n"
        
        # Subject
        if parse_info.get('subject'):
            subj = parse_info['subject']
            parse_details += f"• **Subject:** {subj.get('en', 'N/A')}"
            if subj.get('pos'):
                parse_details += f" ({subj.get('pos')})"
            if subj.get('person'):
                parse_details += f" - {subj.get('person')} person"
            if subj.get('number'):
                parse_details += f", {subj.get('number')}"
            parse_details += "\n"
        
        # Verb
        if parse_info.get('verb'):
            verb = parse_info['verb']
            parse_details += f"• **Verb:** {verb.get('en', 'N/A')}"
            if verb.get('pos'):
                parse_details += f" ({verb.get('pos')})"
            if verb.get('tense'):
                tense = verb.get('tense', '').replace('_', ' ').title()
                parse_details += f" - {tense}"
            parse_details += "\n"
        
        # Object
        if parse_info.get('object'):
            obj = parse_info['object']
            parse_details += f"• **Object:** {obj.get('en', 'N/A')}"
            if obj.get('pos'):
                parse_details += f" ({obj.get('pos')})"
            parse_details += "\n"
        
        # Negation
        if parse_info.get('negation'):
            parse_details += "• **Negation:** Yes\n"
        
        # Check for spell corrections
        if result.get('spell_corrections'):
            parse_details += "\n**Spell Corrections:**\n"
            for corr in result['spell_corrections']:
                parse_details += f"• '{corr['original']}' → '{corr['corrected']}' "
                parse_details += f"(confidence: {corr['confidence']:.0%})\n"
        
        status_message = "✅ Translation successful!"
        
        return (
            sinhala_output,
            raw_english,
            parse_details,
            final_english,
            status_message
        )
        
    except Exception as e:
        error_details = f"**Error Details:**\n{str(e)}"
        return (
            "",
            "",
            error_details,
            "",
            f"❌ Error: {str(e)}"
        )


# Example sentences for quick testing
EXAMPLES = [
    ["mama gedara yanawa"],
    ["eyala potha kiyawanawa"],
    ["oya bath kanawa"],
    ["mama iskole yanawa"],
    ["eyala watura bonawa"],
    ["mama liyanawa"],
    ["oya television balanawa"],
    ["eyala game gahanawa"],
]


# Build Gradio interface
with gr.Blocks(
    theme=gr.themes.Soft(),
    title="Singlish-to-English Translator",
    css="""
    .output-box {
        font-size: 18px;
        padding: 15px;
        border-radius: 8px;
    }
    .module-header {
        font-weight: bold;
        color: #1976d2;
        margin-bottom: 10px;
    }
    """
) as app:
    
    # Header
    gr.Markdown(
        """
        # 🌐 Singlish-to-English Translator
        
        **A 3-Module NLP Pipeline**: FST Transliteration → RBMT Translation → Post-Processing
        
        Translate romanized Sinhala (Singlish) into fluent, grammatically correct English.
        """
    )
    
    with gr.Row():
        with gr.Column():
            # Input section
            gr.Markdown("## 📝 Input")
            
            singlish_input = gr.Textbox(
                label="Enter Singlish Text",
                placeholder="e.g., mama gedara yanawa",
                lines=3,
                max_lines=5
            )
            
            with gr.Row():
                translate_btn = gr.Button("🔄 Translate", variant="primary", size="lg")
                clear_btn = gr.Button("🗑️ Clear", size="lg")
            
            # Examples
            gr.Markdown("### 💡 Try These Examples:")
            gr.Examples(
                examples=EXAMPLES,
                inputs=singlish_input,
                label="Click an example to auto-fill"
            )
    
    # Output section
    gr.Markdown("---")
    gr.Markdown("## 📊 Pipeline Outputs")
    
    with gr.Row():
        with gr.Column():
            # Module 1 Output
            gr.Markdown("### ✅ Module 1: FST Transliteration")
            gr.Markdown("*Converts Singlish to Sinhala script*")
            sinhala_output = gr.Textbox(
                label="Sinhala Script",
                lines=2,
                interactive=False,
                elem_classes="output-box"
            )
        
        with gr.Column():
            # Module 2 Output
            gr.Markdown("### ✅ Module 2: RBMT Translation")
            gr.Markdown("*Translates Sinhala to English (SOV → SVO)*")
            raw_english = gr.Textbox(
                label="Raw English (Word-by-Word)",
                lines=2,
                interactive=False,
                elem_classes="output-box"
            )
    
    # Parse details
    gr.Markdown("### 🔍 Parse Details")
    parse_details = gr.Markdown(
        value="*Translation results will appear here*",
        elem_classes="output-box"
    )
    
    # Module 3 Output
    gr.Markdown("### ✅ Module 3: Post-Processing")
    gr.Markdown("*Applies grammar rules for fluent English*")
    final_english = gr.Textbox(
        label="Final Fluent English",
        lines=2,
        interactive=False,
        elem_classes="output-box",
        show_label=True
    )
    
    # Status message
    status_message = gr.Textbox(
        label="Status",
        interactive=False,
        show_label=False
    )
    
    # Event handlers
    translate_btn.click(
        fn=translate_with_details,
        inputs=[singlish_input],
        outputs=[sinhala_output, raw_english, parse_details, final_english, status_message]
    )
    
    clear_btn.click(
        fn=lambda: ("", "", "*Translation results will appear here*", "", ""),
        inputs=None,
        outputs=[singlish_input, sinhala_output, parse_details, final_english, status_message]
    )
    
    # Footer
    gr.Markdown(
        """
        ---
        **System Information:**
        - Module 1: 266 transliteration rules with spell checking (Levenshtein distance)
        - Module 2: 68-word bilingual lexicon with POS tagging
        - Module 3: Rule-based grammar correction (verb conjugation, article insertion)
        
        **Performance:** 100% success rate on 50-sentence test corpus | Adequacy: 4.7/5 | Fluency: 4.2/5
        """
    )


# Launch the app
if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Launching Singlish-to-English Translator UI")
    print("=" * 60)
    print("\n📌 System Check:")
    
    # Check if required files exist
    import os
    
    required_files = [
        "pipeline.py",
        "transliteration/module1.py",
        "transliteration/transliterate.fst",
        "translation/module2.py",
        "evaluation/module3.py",
        "data/corpus.json",
        "data/lexicon.json",
        "data/singlish_rules.json"
    ]
    
    all_ok = True
    for file in required_files:
        exists = os.path.exists(file)
        status = "✅" if exists else "❌"
        print(f"{status} {file}")
        if not exists:
            all_ok = False
    
    if not all_ok:
        print("\n⚠️ Warning: Some required files are missing!")
        print("Make sure you have built the FST: cd transliteration && python build_fst.py")
    
    print("\n" + "=" * 60)
    print("🌐 Starting Gradio server...")
    print("=" * 60)
    
    # Launch with options
    app.launch(
        server_name="127.0.0.1",  # Local only
        server_port=7860,          # Default Gradio port
        share=False,               # Set to True for public link
        show_error=True,           # Show errors in UI
        inbrowser=True             # Auto-open browser
    )

