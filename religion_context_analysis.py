#!/usr/bin/env python3
"""
Analyze how religion is mentioned in the 2083 document.
Extract contexts and patterns of religious discourse.
"""

import re
from collections import Counter, defaultdict

def get_contexts(text, term, context_size=150):
    """Get contexts where term appears."""
    text_lower = text.lower()
    pattern = r'.{{0,{}}}\b{}\b.{{0,{}}}'.format(context_size, re.escape(term), context_size)
    matches = re.findall(pattern, text_lower, re.IGNORECASE)
    return matches

def get_surrounding_words(text, term, window=5):
    """Get words appearing near the term."""
    text_lower = text.lower()
    words = re.findall(r'\b\w+\b', text_lower)
    
    collocations = []
    for i, word in enumerate(words):
        if word == term.lower():
            # Get surrounding words
            start = max(0, i - window)
            end = min(len(words), i + window + 1)
            context_words = words[start:i] + words[i+1:end]
            collocations.extend(context_words)
    
    return collocations

def analyze_sentiment_patterns(contexts):
    """Analyze sentiment and framing patterns."""
    
    negative_words = ['war', 'violence', 'terror', 'threat', 'attack', 'enemy', 'danger', 
                      'radical', 'extreme', 'militant', 'invasion', 'destroy', 'kill',
                      'oppression', 'against', 'conflict', 'hate', 'death']
    
    positive_words = ['peace', 'freedom', 'tolerance', 'respect', 'love', 'unity',
                      'harmony', 'cooperation', 'understanding']
    
    neutral_words = ['culture', 'tradition', 'belief', 'practice', 'community', 'people']
    
    negative_count = 0
    positive_count = 0
    neutral_count = 0
    
    for context in contexts:
        context_lower = context.lower()
        if any(word in context_lower for word in negative_words):
            negative_count += 1
        if any(word in context_lower for word in positive_words):
            positive_count += 1
        if any(word in context_lower for word in neutral_words):
            neutral_count += 1
    
    return negative_count, positive_count, neutral_count

def main():
    print("Loading 2083 document...\n")
    
    with open('txt/2083. EUROPEAN DECLARATION OF INDEPENDENCE.txt', 'r', encoding='utf-8', errors='ignore') as f:
        doc_text = f.read()
    
    print("="*80)
    print("RELIGION DISCOURSE ANALYSIS IN 2083 DOCUMENT")
    print("="*80)
    
    # Key religious terms
    religious_terms = {
        'islam': 198,
        'muslim': 109,
        'muslims': 83,
        'christian': 34,
        'christianity': 20,
        'christians': 18,
        'religion': 35,
        'religious': 18,
        'jewish': 14
    }
    
    results = {}
    
    # Analyze Islam specifically (highest frequency)
    print("\n" + "="*80)
    print("ISLAM DISCOURSE ANALYSIS (198 occurrences)")
    print("="*80)
    
    islam_contexts = get_contexts(doc_text, 'islam', 120)
    print(f"\nTotal contexts extracted: {len(islam_contexts)}")
    
    # Sample contexts
    print("\nSample contexts for 'islam':")
    for i, context in enumerate(islam_contexts[:10], 1):
        clean = ' '.join(context.split())
        print(f"\n{i}. ...{clean}...")
    
    # Get common collocations
    islam_collocations = get_surrounding_words(doc_text, 'islam', window=5)
    islam_common = Counter(islam_collocations).most_common(20)
    
    print("\n" + "-"*80)
    print("Most common words appearing near 'islam':")
    print("-"*80)
    for word, count in islam_common:
        if len(word) > 2:  # Filter short words
            print(f"  {word:20} - {count} times")
    
    # Sentiment analysis
    neg, pos, neu = analyze_sentiment_patterns(islam_contexts)
    print("\n" + "-"*80)
    print("Context sentiment patterns for 'islam':")
    print("-"*80)
    print(f"  Contexts with conflict/negative framing: {neg}")
    print(f"  Contexts with positive framing: {pos}")
    print(f"  Contexts with neutral/descriptive framing: {neu}")
    
    # Christianity analysis
    print("\n" + "="*80)
    print("CHRISTIANITY DISCOURSE ANALYSIS (72 occurrences total)")
    print("="*80)
    
    christianity_contexts = get_contexts(doc_text, 'christian', 120)
    print(f"\nTotal contexts extracted: {len(christianity_contexts)}")
    
    print("\nSample contexts for 'christian':")
    for i, context in enumerate(christianity_contexts[:5], 1):
        clean = ' '.join(context.split())
        print(f"\n{i}. ...{clean}...")
    
    # Compare Islam vs Christianity framing
    print("\n" + "="*80)
    print("COMPARATIVE ANALYSIS: ISLAM vs CHRISTIANITY")
    print("="*80)
    
    print(f"\nFrequency comparison:")
    print(f"  Islam-related terms: {198 + 109 + 83} = 390 occurrences")
    print(f"  Christianity-related terms: {34 + 20 + 18} = 72 occurrences")
    print(f"  Ratio: Islam mentioned {390/72:.1f}x more than Christianity")
    
    # Look for specific phrases
    print("\n" + "-"*80)
    print("Key phrases and framings:")
    print("-"*80)
    
    key_phrases = [
        'islam.*war',
        'islam.*peace',
        'islam.*terror',
        'islam.*europe',
        'islam.*threat',
        'islam.*invasion',
        'christian.*europe',
        'religion.*peace',
        'religion.*violence'
    ]
    
    for phrase_pattern in key_phrases:
        matches = re.findall(r'.{0,80}' + phrase_pattern + r'.{0,80}', doc_text, re.IGNORECASE)
        if matches:
            print(f"\n'{phrase_pattern}' - {len(matches)} matches")
            if matches:
                sample = ' '.join(matches[0].split())
                print(f"  Sample: ...{sample}...")
    
    # Save detailed report
    with open('txt/religion_discourse_analysis.txt', 'w') as f:
        f.write("RELIGION DISCOURSE ANALYSIS - 2083 DOCUMENT\n")
        f.write("="*80 + "\n\n")
        
        f.write("FREQUENCY SUMMARY\n")
        f.write("-"*80 + "\n")
        f.write(f"Islam: 198 occurrences\n")
        f.write(f"Muslim: 109 occurrences\n")
        f.write(f"Muslims: 83 occurrences\n")
        f.write(f"Christian: 34 occurrences\n")
        f.write(f"Christianity: 20 occurrences\n")
        f.write(f"Religion: 35 occurrences\n\n")
        
        f.write("ISLAM CONTEXTS (first 50)\n")
        f.write("="*80 + "\n\n")
        for i, context in enumerate(islam_contexts[:50], 1):
            clean = ' '.join(context.split())
            f.write(f"{i}. ...{clean}...\n\n")
        
        f.write("\n" + "="*80 + "\n")
        f.write("CHRISTIANITY CONTEXTS (all)\n")
        f.write("="*80 + "\n\n")
        for i, context in enumerate(christianity_contexts, 1):
            clean = ' '.join(context.split())
            f.write(f"{i}. ...{clean}...\n\n")
        
        f.write("\n" + "="*80 + "\n")
        f.write("COMMON COLLOCATIONS WITH 'ISLAM'\n")
        f.write("="*80 + "\n\n")
        for word, count in islam_common:
            if len(word) > 2:
                f.write(f"{word:20} - {count}\n")
    
    print("\n✓ Detailed report saved to: religion_discourse_analysis.txt")
    
    # Final summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print("\nReligion in 2083 document:")
    print("  • Islam is the dominant religious focus (71% of religious terms)")
    print("  • Islam mentioned 5.4x more frequently than Christianity")
    print(f"  • {neg} Islam contexts contain conflict/threat framing")
    print("  • Document appears focused on Islam as primary religious topic")

if __name__ == "__main__":
    main()
