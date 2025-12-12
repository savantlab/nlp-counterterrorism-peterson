#!/usr/bin/env python3
"""
Comprehensive analysis of feminism discourse in the 2083 document.
"""

import re
from collections import Counter

def count_term(text, term):
    """Count occurrences of a term."""
    pattern = r'\b' + re.escape(term) + r'\b'
    return len(re.findall(pattern, text, re.IGNORECASE))

def get_all_contexts(text, term, context_size=150):
    """Get ALL contexts where term appears."""
    pattern = r'.{{0,{}}}\b{}\b.{{0,{}}}'.format(context_size, re.escape(term), context_size)
    matches = re.findall(pattern, text, re.IGNORECASE)
    return matches

def get_surrounding_words(text, term, window=7):
    """Get words appearing near the term."""
    text_lower = text.lower()
    words = re.findall(r'\b\w+\b', text_lower)
    
    collocations = []
    for i, word in enumerate(words):
        if word == term.lower():
            start = max(0, i - window)
            end = min(len(words), i + window + 1)
            context_words = words[start:i] + words[i+1:end]
            collocations.extend(context_words)
    
    return collocations

def main():
    print("Loading 2083 document...\n")
    
    with open('2083. EUROPEAN DECLARATION OF INDEPENDENCE.txt', 'r', encoding='utf-8', errors='ignore') as f:
        doc_text = f.read()
    
    print("="*80)
    print("FEMINISM DISCOURSE ANALYSIS IN 2083 DOCUMENT")
    print("="*80)
    
    # Count all feminism-related terms
    feminism_terms = {
        'feminism': count_term(doc_text, 'feminism'),
        'feminist': count_term(doc_text, 'feminist'),
        'feminists': count_term(doc_text, 'feminists'),
        'patriarchy': count_term(doc_text, 'patriarchy'),
        'patriarchal': count_term(doc_text, 'patriarchal'),
        'matriarchy': count_term(doc_text, 'matriarchy'),
        'sexism': count_term(doc_text, 'sexism'),
        'misogyny': count_term(doc_text, 'misogyny')
    }
    
    print(f"\nFeminism-related term frequencies:")
    print("-"*80)
    total = 0
    for term, count in sorted(feminism_terms.items(), key=lambda x: x[1], reverse=True):
        print(f"  {term:20} - {count} occurrences")
        total += count
    
    print(f"\n  {'TOTAL':20} - {total} occurrences")
    
    # Get all feminism contexts
    print("\n" + "="*80)
    print("ALL FEMINISM CONTEXTS")
    print("="*80)
    
    feminism_contexts = get_all_contexts(doc_text, 'feminism', 120)
    print(f"\nTotal contexts extracted: {len(feminism_contexts)}\n")
    
    for i, context in enumerate(feminism_contexts, 1):
        clean = ' '.join(context.split())
        print(f"{i}. ...{clean}...\n")
    
    # Get all feminist contexts
    print("\n" + "="*80)
    print("ALL FEMINIST CONTEXTS")
    print("="*80)
    
    feminist_contexts = get_all_contexts(doc_text, 'feminist', 120)
    print(f"\nTotal contexts extracted: {len(feminist_contexts)}\n")
    
    for i, context in enumerate(feminist_contexts, 1):
        clean = ' '.join(context.split())
        print(f"{i}. ...{context}...\n")
    
    # Get common collocations
    print("\n" + "="*80)
    print("COMMON WORDS APPEARING NEAR 'FEMINISM'")
    print("="*80)
    
    feminism_collocations = get_surrounding_words(doc_text, 'feminism', window=7)
    feminism_common = Counter(feminism_collocations).most_common(30)
    
    for word, count in feminism_common:
        if len(word) > 2:
            print(f"  {word:20} - {count} times")
    
    # Look for specific themes
    print("\n" + "="*80)
    print("THEMATIC PHRASES")
    print("="*80)
    
    themes = [
        ('feminism.*oppression', 'Feminism & Oppression'),
        ('feminism.*women', 'Feminism & Women'),
        ('feminism.*islam', 'Feminism & Islam'),
        ('feminism.*marxism', 'Feminism & Marxism'),
        ('feminism.*boys', 'Feminism & Boys'),
        ('feminist.*war', 'Feminist War'),
        ('cultural marxism.*feminism', 'Cultural Marxism & Feminism'),
        ('political correctness.*feminism', 'Political Correctness & Feminism')
    ]
    
    for pattern, label in themes:
        matches = re.findall(r'.{0,100}' + pattern + r'.{0,100}', doc_text, re.IGNORECASE)
        if matches:
            print(f"\n{label}: {len(matches)} matches")
            sample = ' '.join(matches[0].split())
            print(f"  Sample: ...{sample}...")
    
    # Save comprehensive report
    with open('feminism_analysis_report.txt', 'w') as f:
        f.write("COMPREHENSIVE FEMINISM ANALYSIS - 2083 DOCUMENT\n")
        f.write("="*80 + "\n\n")
        
        f.write("FREQUENCY SUMMARY\n")
        f.write("-"*80 + "\n")
        for term, count in sorted(feminism_terms.items(), key=lambda x: x[1], reverse=True):
            f.write(f"{term:20} - {count}\n")
        f.write(f"\nTOTAL: {total}\n\n")
        
        f.write("="*80 + "\n")
        f.write("ALL FEMINISM CONTEXTS\n")
        f.write("="*80 + "\n\n")
        
        for i, context in enumerate(feminism_contexts, 1):
            clean = ' '.join(context.split())
            f.write(f"{i}. ...{clean}...\n\n")
        
        f.write("\n" + "="*80 + "\n")
        f.write("ALL FEMINIST CONTEXTS\n")
        f.write("="*80 + "\n\n")
        
        for i, context in enumerate(feminist_contexts, 1):
            clean = ' '.join(context.split())
            f.write(f"{i}. ...{clean}...\n\n")
        
        f.write("\n" + "="*80 + "\n")
        f.write("COMMON COLLOCATIONS WITH 'FEMINISM'\n")
        f.write("="*80 + "\n\n")
        
        for word, count in feminism_common:
            if len(word) > 2:
                f.write(f"{word:20} - {count}\n")
        
        f.write("\n" + "="*80 + "\n")
        f.write("THEMATIC PHRASE ANALYSIS\n")
        f.write("="*80 + "\n\n")
        
        for pattern, label in themes:
            matches = re.findall(r'.{0,150}' + pattern + r'.{0,150}', doc_text, re.IGNORECASE)
            f.write(f"\n{label}: {len(matches)} matches\n")
            f.write("-"*80 + "\n")
            if matches:
                for i, match in enumerate(matches[:10], 1):  # First 10 of each
                    clean = ' '.join(match.split())
                    f.write(f"{i}. ...{clean}...\n\n")
    
    print("\n✓ Comprehensive report saved to: feminism_analysis_report.txt")
    
    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"\n• Total feminism-related terms: {total}")
    print(f"• Feminism appears in {len(feminism_contexts)} distinct contexts")
    print(f"• Feminist appears in {len(feminist_contexts)} distinct contexts")
    print(f"\nMost common themes:")
    print(f"  - Feminism: {feminism_terms['feminism']} mentions")
    print(f"  - Feminist: {feminism_terms['feminist']} mentions")
    print(f"  - Feminists: {feminism_terms['feminists']} mentions")
    print(f"  - Patriarchal: {feminism_terms['patriarchal']} mentions")

if __name__ == "__main__":
    main()
