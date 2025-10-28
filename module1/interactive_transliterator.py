"""
Interactive Transliterator - Real-time FST Transliteration CLI
Student 1 - Module 1 Enhancement

Interactive command-line interface for FST transliteration with advanced features:
- Real-time transliteration
- N-best alternatives
- OOV detection and handling
- Rule visualization
- Batch processing

Usage:
    python interactive_transliterator.py
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from module1 import (transliterate, transliterate_nbest, 
                         detect_oov, get_alignment)
except ImportError as e:
    print(f"Error: Could not import module1")
    print(f"Make sure FST is compiled: python build_fst.py")
    sys.exit(1)


class InteractiveTransliterator:
    """Interactive transliteration session manager."""
    
    def __init__(self):
        self.history = []
        self.show_alternatives = False
        self.show_alignment = False
        self.detect_oov_flag = True
        self.n_best = 3
    
    def print_banner(self):
        """Print welcome banner."""
        print("=" * 70)
        print(" INTERACTIVE FST TRANSLITERATOR".center(70))
        print(" Module 1 Enhancement - Student 1".center(70))
        print("=" * 70)
        print()
        print("Features:")
        print("  • Real-time Singlish → Sinhala transliteration")
        print("  • N-best alternative hypotheses")
        print("  • OOV detection and suggestions")
        print("  • Character alignment visualization")
        print()
        print("Commands:")
        print("  :help              Show this help message")
        print("  :alternatives on   Show n-best alternatives")
        print("  :alternatives off  Hide alternatives")
        print("  :alignment on      Show character alignment")
        print("  :alignment off     Hide alignment")
        print("  :oov on/off        Toggle OOV detection")
        print("  :nbest N           Set number of alternatives (default: 3)")
        print("  :history           Show translation history")
        print("  :stats             Show session statistics")
        print("  :quit or :exit     Exit the program")
        print()
        print("Just type Singlish text to transliterate!")
        print("=" * 70)
        print()
    
    def process_command(self, cmd: str) -> bool:
        """
        Process special commands.
        
        Returns:
            True if should continue, False to exit
        """
        cmd = cmd.lower().strip()
        
        if cmd in [':quit', ':exit', ':q']:
            print("\nGoodbye! Transliterations: {}".format(len(self.history)))
            return False
        
        elif cmd == ':help' or cmd == ':h':
            self.print_banner()
        
        elif cmd == ':alternatives on':
            self.show_alternatives = True
            print(f"✓ Alternatives enabled (showing top {self.n_best})")
        
        elif cmd == ':alternatives off':
            self.show_alternatives = False
            print("✓ Alternatives disabled")
        
        elif cmd == ':alignment on':
            self.show_alignment = True
            print("✓ Alignment visualization enabled")
        
        elif cmd == ':alignment off':
            self.show_alignment = False
            print("✓ Alignment visualization disabled")
        
        elif cmd == ':oov on':
            self.detect_oov_flag = True
            print("✓ OOV detection enabled")
        
        elif cmd == ':oov off':
            self.detect_oov_flag = False
            print("✓ OOV detection disabled")
        
        elif cmd.startswith(':nbest'):
            try:
                parts = cmd.split()
                if len(parts) == 2:
                    self.n_best = int(parts[1])
                    print(f"✓ N-best set to {self.n_best}")
                else:
                    print(f"Current n-best: {self.n_best}")
            except ValueError:
                print("Error: Invalid number format. Usage: :nbest N")
        
        elif cmd == ':history':
            self.show_history()
        
        elif cmd == ':stats':
            self.show_stats()
        
        else:
            print(f"Unknown command: {cmd}")
            print("Type :help for available commands")
        
        return True
    
    def show_history(self):
        """Display translation history."""
        print("\n" + "=" * 70)
        print("TRANSLATION HISTORY")
        print("=" * 70)
        
        if not self.history:
            print("No translations yet.")
        else:
            for i, (inp, out) in enumerate(self.history[-10:], 1):
                print(f"{i:2}. {inp:30} → {out}")
        
        print("=" * 70 + "\n")
    
    def show_stats(self):
        """Display session statistics."""
        print("\n" + "=" * 70)
        print("SESSION STATISTICS")
        print("=" * 70)
        
        print(f"Total transliterations: {len(self.history)}")
        
        if self.history:
            avg_input_len = sum(len(inp) for inp, _ in self.history) / len(self.history)
            avg_output_len = sum(len(out) for _, out in self.history) / len(self.history)
            
            print(f"Average input length:  {avg_input_len:.1f} characters")
            print(f"Average output length: {avg_output_len:.1f} characters")
        
        print(f"\nCurrent settings:")
        print(f"  Alternatives: {'ON' if self.show_alternatives else 'OFF'}")
        print(f"  Alignment: {'ON' if self.show_alignment else 'OFF'}")
        print(f"  OOV Detection: {'ON' if self.detect_oov_flag else 'OFF'}")
        print(f"  N-best: {self.n_best}")
        
        print("=" * 70 + "\n")
    
    def transliterate_interactive(self, text: str):
        """
        Perform interactive transliteration with all features.
        
        Args:
            text: Input Singlish text
        """
        print()
        print("-" * 70)
        print(f"Input:  {text}")
        
        try:
            # Main transliteration
            result = transliterate(text)
            print(f"Output: {result}")
            
            # Store in history
            self.history.append((text, result))
            
            # OOV detection
            if self.detect_oov_flag:
                oov_info = detect_oov(text)
                if oov_info['has_oov']:
                    print(f"\n⚠️  OOV Warning:")
                    print(f"   Coverage: {oov_info['coverage']*100:.1f}%")
                    print(f"   OOV words: {', '.join(oov_info['oov_words'])}")
                    if oov_info['suggestions']:
                        print(f"   Suggestions:")
                        for word, suggestions in oov_info['suggestions'].items():
                            print(f"     '{word}' → try: {', '.join(suggestions)}")
            
            # N-best alternatives
            if self.show_alternatives:
                alternatives = transliterate_nbest(text, n=self.n_best, return_scores=True)
                if len(alternatives) > 1:
                    print(f"\nAlternative hypotheses:")
                    for i, (alt, score) in enumerate(alternatives, 1):
                        print(f"  {i}. {alt:30} (confidence: {score:.3f})")
            
            # Alignment
            if self.show_alignment:
                alignment = get_alignment(text)
                print(f"\nCharacter alignment:")
                for inp_seg, out_seg in alignment:
                    if inp_seg != ' ':
                        print(f"  '{inp_seg}' → '{out_seg}'")
            
        except Exception as e:
            print(f"Error: {e}")
        
        print("-" * 70)
        print()
    
    def run(self):
        """Main interactive loop."""
        self.print_banner()
        
        try:
            while True:
                try:
                    # Get input
                    text = input("Singlish> ").strip()
                    
                    if not text:
                        continue
                    
                    # Check if command
                    if text.startswith(':'):
                        if not self.process_command(text):
                            break
                    else:
                        # Transliterate
                        self.transliterate_interactive(text)
                
                except KeyboardInterrupt:
                    print("\n\nInterrupted. Type :quit to exit.")
                    continue
                except EOFError:
                    print("\n\nGoodbye!")
                    break
        
        except Exception as e:
            print(f"\nUnexpected error: {e}")
            import traceback
            traceback.print_exc()


def main():
    """Entry point."""
    # Check for command-line arguments
    if len(sys.argv) > 1:
        # Non-interactive mode: transliterate arguments
        text = ' '.join(sys.argv[1:])
        try:
            result = transliterate(text)
            print(result)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Interactive mode
        app = InteractiveTransliterator()
        app.run()


if __name__ == "__main__":
    main()

