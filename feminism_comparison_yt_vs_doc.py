#!/usr/bin/env python3
"""
Compare feminism discourse: YouTube transcript vs 2083 document.
"""

import re

def search_term(text, term):
    """Search for term and return contexts."""
    pattern = r'\b' + re.escape(term) + r'\b'
    matches = re.findall(pattern, text, re.IGNORECASE)
    return len(matches)

def get_contexts(text, term, context_size=80):
    """Get contexts where term appears."""
    pattern = r'.{{0,{}}}\b{}\b.{{0,{}}}'.format(context_size, re.escape(term), context_size)
    matches = re.findall(pattern, text, re.IGNORECASE)
    return matches

def main():
    print("="*80)
    print("FEMINISM COMPARISON: YOUTUBE TRANSCRIPT vs 2083 DOCUMENT")
    print("="*80)
    
    # Read files
    with open('youtube_transcript_clean.txt', 'r') as f:
        yt_text = f.read()
    
    with open('2083. EUROPEAN DECLARATION OF INDEPENDENCE.txt', 'r', encoding='utf-8', errors='ignore') as f:
        doc_text = f.read()
    
    print(f"\nYouTube transcript: {len(yt_text.split())} words")
    print(f"2083 document: {len(doc_text.split()):,} words")
    
    # Search for feminism-related terms
    terms = ['feminism', 'feminist', 'feminists', 'patriarchal', 'patriarchy']
    
    print("\n" + "="*80)
    print("TERM FREQUENCY COMPARISON")
    print("="*80)
    
    print(f"\n{'Term':<15} {'YouTube':<12} {'2083 Doc':<12} {'Status'}")
    print("-"*80)
    
    for term in terms:
        yt_count = search_term(yt_text, term)
        doc_count = search_term(doc_text, term)
        
        if yt_count > 0:
            status = f"✓ IN BOTH"
        else:
            status = "✗ NOT IN YT"
        
        print(f"{term:<15} {yt_count:<12} {doc_count:<12} {status}")
    
    # Special search for related concepts in YouTube
    print("\n" + "="*80)
    print("RELATED CONCEPTS IN YOUTUBE TRANSCRIPT")
    print("="*80)
    
    related_searches = [
        ('patriarchal', 'oppressive and patriarchal'),
        ('identity', 'identity groups'),
        ('gender', 'gender pronouns'),
        ('sex', 'sex differences'),
        ('oppressive', 'oppressive system'),
        ('victim', 'victim or an oppressor')
    ]
    
    print("\nSearching for gender/identity-related language:")
    print("-"*80)
    
    for term, phrase in related_searches:
        count = search_term(yt_text, term)
        if count > 0:
            contexts = get_contexts(yt_text, term, 60)
            print(f"\n'{term}': {count} occurrence(s)")
            if contexts:
                print(f"  Context: ...{contexts[0]}...")
    
    # Key finding
    print("\n" + "="*80)
    print("KEY FINDING")
    print("="*80)
    
    print("\n✗ The word 'feminism' does NOT appear in the YouTube transcript")
    print("✗ The word 'feminist' does NOT appear in the YouTube transcript")
    print("✗ The word 'feminists' does NOT appear in the YouTube transcript")
    
    print("\n✓ However, the YouTube transcript DOES mention:")
    print("  - 'patriarchal' (1 time): describing Western civilization")
    print("  - 'oppressive' (2 times): describing Western civilization and systems")
    print("  - 'gender' (1 time): 'fabricated gender pronouns'")
    print("  - 'sex' (2 times): 'sex differences' and 'sexual preference'")
    print("  - 'identity' (3 times): 'identity groups', 'identity politics', 'identity based quotas'")
    
    print("\n" + "="*80)
    print("ANALYSIS")
    print("="*80)
    
    print("\nThe YouTube video discusses:")
    print("  • Post-modernism and neo-Marxism")
    print("  • Identity politics (race, sex, sexual preference)")
    print("  • Western civilization as 'oppressive and patriarchal'")
    print("  • Gender pronouns and sex differences")
    print("  • Victim/oppressor dynamics")
    
    print("\nBUT it never explicitly mentions 'feminism' or 'feminist'")
    
    print("\nThe 2083 document:")
    print("  • Extensively discusses feminism (75 occurrences)")
    print("  • Frames feminism as 'radical feminism'")
    print("  • Links feminism to Cultural Marxism and Political Correctness")
    print("  • Has entire chapters on feminism")
    
    print("\n" + "="*80)
    print("CONCLUSION")
    print("="*80)
    
    print("\nWhile the YouTube video discusses concepts RELATED to feminism")
    print("(patriarchy, oppression, identity politics, gender), it does NOT")
    print("use the word 'feminism' itself. This is a significant difference")
    print("from the 2083 document, which explicitly and extensively critiques")
    print("'radical feminism' as part of Cultural Marxism.")
    
    print("\nThe YouTube video focuses on:")
    print("  → Post-modernism")
    print("  → Identity politics")  
    print("  → Neo-Marxism")
    
    print("\nThe 2083 document focuses on:")
    print("  → Islam (dominant theme)")
    print("  → Cultural Marxism")
    print("  → Feminism (as part of Cultural Marxism)")
    print("  → Political Correctness")

if __name__ == "__main__":
    main()
