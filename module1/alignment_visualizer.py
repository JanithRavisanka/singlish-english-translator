"""
Character Alignment Visualizer for FST Transliteration
Student 1 - Module 1 Enhancement

This module visualizes the character-level alignment between Sinlish input
and Sinhala output, showing how the FST maps input segments to output segments.

Theoretical Background:
    Alignment in transduction shows the correspondence between input and output
    symbols. In FST terms, this represents the path taken through the automaton,
    where each transition consumes input symbols (Σ) and produces output symbols (Γ).
    
    The alignment problem: Given input w ∈ Σ* and output v ∈ Γ*, find the
    sequence of FST transitions τ1...τn such that input(τ) = w and output(τ) = v.

Usage:
    python alignment_visualizer.py "mama gedara yanawa"
    
    Or programmatically:
        from alignment_visualizer import visualize_alignment, create_alignment_table
"""

import os
import sys
from typing import List, Tuple
from collections import namedtuple

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from module1 import transliterate, get_alignment
except ImportError as e:
    print(f"Error: Could not import module1")
    print(f"Details: {e}")
    sys.exit(1)

# Named tuple for alignment representation
Alignment = namedtuple('Alignment', ['input_segment', 'output_segment', 'rule_type', 'position'])


def create_detailed_alignment(text: str) -> List[Alignment]:
    """
    Create detailed alignment with metadata.
    
    Args:
        text: Input Sinlish text
        
    Returns:
        List of Alignment objects with position and rule type information
    """
    basic_alignment = get_alignment(text)
    detailed = []
    position = 0
    
    for inp, out in basic_alignment:
        # Determine rule type
        if len(inp) == 1:
            rule_type = "char"
        elif len(inp) == 2:
            rule_type = "bigram"
        elif ' ' in inp:
            rule_type = "space"
        else:
            rule_type = "word/syllable"
        
        detailed.append(Alignment(inp, out, rule_type, position))
        position += len(inp)
    
    return detailed


def visualize_alignment(text: str, style: str = 'table') -> str:
    """
    Create visual representation of transliteration alignment.
    
    Args:
        text: Input text to visualize
        style: Visualization style - 'table', 'inline', or 'detailed'
        
    Returns:
        Formatted string showing alignment
    """
    alignment = create_detailed_alignment(text)
    output = transliterate(text)
    
    if style == 'table':
        return _format_table_alignment(text, output, alignment)
    elif style == 'inline':
        return _format_inline_alignment(alignment)
    elif style == 'detailed':
        return _format_detailed_alignment(text, output, alignment)
    else:
        raise ValueError(f"Unknown style: {style}")


def _format_table_alignment(input_text: str, output_text: str, alignment: List[Alignment]) -> str:
    """Format alignment as a table."""
    lines = []
    lines.append("=" * 80)
    lines.append("CHARACTER ALIGNMENT TABLE")
    lines.append("=" * 80)
    lines.append(f"\nInput:  {input_text}")
    lines.append(f"Output: {output_text}")
    lines.append("\n" + "-" * 80)
    lines.append(f"{'Position':<10} {'Input':<15} {'Output':<15} {'Rule Type':<15} {'Length':<10}")
    lines.append("-" * 80)
    
    for align in alignment:
        lines.append(
            f"{align.position:<10} "
            f"{align.input_segment:<15} "
            f"{align.output_segment:<15} "
            f"{align.rule_type:<15} "
            f"{len(align.input_segment):<10}"
        )
    
    lines.append("-" * 80)
    
    return '\n'.join(lines)


def _format_inline_alignment(alignment: List[Alignment]) -> str:
    """Format alignment inline with arrows."""
    lines = []
    lines.append("\nInline Alignment:")
    lines.append("-" * 60)
    
    for align in alignment:
        if align.input_segment == ' ':
            lines.append("  [space] → [space]")
        else:
            lines.append(f"  '{align.input_segment}' → '{align.output_segment}' ({align.rule_type})")
    
    return '\n'.join(lines)


def _format_detailed_alignment(input_text: str, output_text: str, alignment: List[Alignment]) -> str:
    """Format detailed alignment with statistics."""
    lines = []
    lines.append("=" * 80)
    lines.append("DETAILED ALIGNMENT ANALYSIS")
    lines.append("=" * 80)
    
    lines.append(f"\nInput Text:  {input_text}")
    lines.append(f"Output Text: {output_text}")
    lines.append(f"\nInput Length:  {len(input_text)} characters")
    lines.append(f"Output Length: {len(output_text)} characters")
    lines.append(f"Segments:      {len(alignment)} rules applied")
    
    # Calculate statistics
    rule_types = {}
    for align in alignment:
        rule_types[align.rule_type] = rule_types.get(align.rule_type, 0) + 1
    
    lines.append("\nRule Type Distribution:")
    for rule_type, count in sorted(rule_types.items()):
        percentage = (count / len(alignment)) * 100
        lines.append(f"  {rule_type:15} {count:3} ({percentage:5.1f}%)")
    
    lines.append("\nSegment-by-Segment Breakdown:")
    lines.append("-" * 80)
    
    for i, align in enumerate(alignment, 1):
        lines.append(f"\n{i}. Position {align.position}")
        lines.append(f"   Input:  '{align.input_segment}' (length {len(align.input_segment)})")
        lines.append(f"   Output: '{align.output_segment}' (length {len(align.output_segment)})")
        lines.append(f"   Type:   {align.rule_type}")
        lines.append(f"   Ratio:  {len(align.output_segment)}/{len(align.input_segment)} = " +
                    f"{len(align.output_segment)/len(align.input_segment) if len(align.input_segment) > 0 else 0:.2f}")
    
    lines.append("\n" + "=" * 80)
    
    return '\n'.join(lines)


def visualize_comparison(texts: List[str]) -> str:
    """
    Create side-by-side comparison of multiple text alignments.
    
    Args:
        texts: List of input texts to compare
        
    Returns:
        Formatted comparison table
    """
    lines = []
    lines.append("=" * 100)
    lines.append("ALIGNMENT COMPARISON")
    lines.append("=" * 100)
    
    for i, text in enumerate(texts, 1):
        output = transliterate(text)
        alignment = get_alignment(text)
        
        lines.append(f"\n{i}. Input: {text}")
        lines.append(f"   Output: {output}")
        lines.append(f"   Segments: {len(alignment)}")
        lines.append("   Alignment: " + " + ".join([f"[{inp}→{out}]" for inp, out in alignment]))
    
    lines.append("\n" + "=" * 100)
    
    return '\n'.join(lines)


def create_latex_alignment(text: str) -> str:
    """
    Generate LaTeX code for alignment (for academic papers/reports).
    
    Args:
        text: Input text
        
    Returns:
        LaTeX code string
    """
    alignment = get_alignment(text)
    output = transliterate(text)
    
    latex = []
    latex.append("% FST Transliteration Alignment")
    latex.append("\\begin{table}[h]")
    latex.append("\\centering")
    latex.append("\\begin{tabular}{|l|l|l|}")
    latex.append("\\hline")
    latex.append("\\textbf{Input} & \\textbf{Output} & \\textbf{Type} \\\\")
    latex.append("\\hline")
    
    for inp, out in alignment:
        rule_type = "char" if len(inp) == 1 else ("space" if inp == ' ' else "multi")
        inp_escaped = inp.replace('_', '\\_').replace(' ', '[space]')
        latex.append(f"{inp_escaped} & {out} & {rule_type} \\\\")
    
    latex.append("\\hline")
    latex.append("\\end{tabular}")
    latex.append(f"\\caption{{Transliteration alignment for ``{text}''}}")
    latex.append("\\label{tab:alignment}")
    latex.append("\\end{table}")
    
    return '\n'.join(latex)


def main():
    """Main function for standalone execution."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Visualize FST transliteration alignment',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python alignment_visualizer.py "mama gedara yanawa"
  python alignment_visualizer.py "mama" --style inline
  python alignment_visualizer.py "oya bath kanawa" --style detailed
  python alignment_visualizer.py --compare "mama" "oya" "eyala"
        """
    )
    
    parser.add_argument('text', nargs='*', help='Text to visualize alignment for')
    parser.add_argument('--style', choices=['table', 'inline', 'detailed'], 
                       default='detailed', help='Visualization style (default: detailed)')
    parser.add_argument('--compare', action='store_true',
                       help='Compare multiple texts side-by-side')
    parser.add_argument('--latex', action='store_true',
                       help='Generate LaTeX output')
    
    args = parser.parse_args()
    
    # If no arguments, show demo
    if not args.text:
        print("No input provided. Running demo...\n")
        demo_texts = [
            "mama gedara yanawa",
            "eyala potha kiyawanawa",
            "oya bath kanawa"
        ]
        
        for text in demo_texts:
            print(visualize_alignment(text, style='detailed'))
            print()
        
        return
    
    # Process input
    if args.compare:
        print(visualize_comparison(args.text))
    elif args.latex:
        for text in args.text:
            print(create_latex_alignment(text))
            print()
    else:
        for text in args.text:
            print(visualize_alignment(text, style=args.style))
            print()


if __name__ == "__main__":
    main()

