#!/usr/bin/env python3
"""
Thematic analysis based on shared vocabulary.
Groups shared words into themes and analyzes their distribution.
"""

import re
from collections import Counter, defaultdict

# Define thematic word groups
THEMES = {
    'Education & Academia': [
        'education', 'university', 'universities', 'college', 'campus', 'professor', 'professors',
        'degree', 'learn', 'student', 'students', 'teaching', 'academic', 'school', 'children'
    ],
    'Political & Ideological': [
        'marx', 'marxist', 'radical', 'radicals', 'left', 'progressive', 'ideology', 'politics',
        'political', 'capitalism', 'socialist', 'communist', 'revolution', 'postmodernism', 'post'
    ],
    'Identity & Social': [
        'identity', 'race', 'sex', 'sexual', 'gender', 'diversity', 'equality', 'equity',
        'discrimination', 'oppression', 'victim', 'patriarchal', 'class', 'groups', 'group'
    ],
    'Cultural & Western': [
        'western', 'west', 'civilization', 'culture', 'cultural', 'society', 'values',
        'tradition', 'traditional', 'shakespeare', 'history', 'heritage'
    ],
    'Power & Conflict': [
        'power', 'struggle', 'conflict', 'war', 'fought', 'violence', 'violent', 'violently',
        'corrupt', 'dangerous', 'destructive', 'undermine', 'oppose', 'attack'
    ],
    'Ideas & Thought': [
        'ideas', 'idea', 'think', 'thinking', 'philosophy', 'philosopher', 'ideology',
        'concept', 'concepts', 'truth', 'belief', 'believe', 'believers'
    ],
    'Freedom & Rights': [
        'freedom', 'free', 'rights', 'speech', 'liberty', 'democracy', 'democratic',
        'expression', 'opinion', 'consensus'
    ],
    'People & Society': [
        'people', 'individuals', 'society', 'generations', 'children', 'young', 'families',
        'communities', 'population', 'humanity', 'human'
    ],
    'Action & Change': [
        'made', 'making', 'become', 'became', 'change', 'changing', 'spread', 'produced',
        'created', 'take', 'took', 'done'
    ],
    'Time & History': [
        'history', 'historical', 'century', '19th', '60s', '70s', 'today', 'now',
        'currently', 'recently', 'decades', 'time', 'first', 'second'
    ]
}

def preprocess_text(text):
    """Clean text."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return text

def main():
    # Read documents
    print("Loading documents...\n")
    with open('2083. EUROPEAN DECLARATION OF INDEPENDENCE.txt', 'r', encoding='utf-8', errors='ignore') as f:
        doc_text = f.read()
    
    with open('youtube_transcript_clean.txt', 'r', encoding='utf-8', errors='ignore') as f:
        yt_text = f.read()
    
    # Read shared words
    shared_words = set()
    with open('shared_words_alphabetical.txt', 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('SHARED') and not line.startswith('=') and not line.startswith('Total'):
                shared_words.add(line)
    
    print(f"Analyzing {len(shared_words)} shared words across {len(THEMES)} themes...\n")
    
    # Preprocess texts
    doc_clean = preprocess_text(doc_text)
    yt_clean = preprocess_text(yt_text)
    
    doc_words = doc_clean.split()
    yt_words = yt_clean.split()
    
    doc_freq = Counter(doc_words)
    yt_freq = Counter(yt_words)
    
    # Analyze each theme
    theme_results = []
    
    print("="*80)
    print("THEMATIC ANALYSIS")
    print("="*80)
    
    for theme_name, theme_words in THEMES.items():
        # Find which theme words are in our shared vocabulary
        theme_shared = [w for w in theme_words if w in shared_words]
        
        if not theme_shared:
            continue
        
        # Count frequencies
        doc_theme_freq = sum(doc_freq[w] for w in theme_shared)
        yt_theme_freq = sum(yt_freq[w] for w in theme_shared)
        
        # Calculate percentages of total words
        doc_pct = (doc_theme_freq / len(doc_words)) * 100
        yt_pct = (yt_theme_freq / len(yt_words)) * 100
        
        theme_results.append({
            'theme': theme_name,
            'shared_words': len(theme_shared),
            'yt_freq': yt_theme_freq,
            'doc_freq': doc_theme_freq,
            'yt_pct': yt_pct,
            'doc_pct': doc_pct,
            'words': theme_shared
        })
    
    # Sort by YouTube frequency
    theme_results.sort(key=lambda x: x['yt_freq'], reverse=True)
    
    # Display results
    for result in theme_results:
        print(f"\n--- {result['theme']} ---")
        print(f"Shared words in theme: {result['shared_words']}")
        print(f"YouTube frequency: {result['yt_freq']} ({result['yt_pct']:.2f}% of transcript)")
        print(f"Document frequency: {result['doc_freq']} ({result['doc_pct']:.2f}% of document)")
        print(f"YT/Doc ratio: {result['yt_freq']/result['doc_freq']:.4f}")
        print(f"Words: {', '.join(sorted(result['words'])[:15])}")
        if len(result['words']) > 15:
            print(f"       ... and {len(result['words']) - 15} more")
    
    # Summary
    print("\n" + "="*80)
    print("THEMATIC EMPHASIS COMPARISON")
    print("="*80)
    
    print("\nTop 5 themes in YouTube (by frequency):")
    for i, result in enumerate(theme_results[:5], 1):
        print(f"{i}. {result['theme']:30} - {result['yt_freq']} occurrences")
    
    print("\nThemes with highest YT/Doc ratio (over-represented in YT):")
    high_ratio = sorted(theme_results, key=lambda x: x['yt_freq']/x['doc_freq'], reverse=True)[:5]
    for result in high_ratio:
        ratio = result['yt_freq']/result['doc_freq']
        print(f"  {result['theme']:30} - {ratio:.4f}x")
    
    # Save results
    with open('thematic_analysis_results.txt', 'w') as f:
        f.write("THEMATIC ANALYSIS OF SHARED VOCABULARY\n")
        f.write("="*80 + "\n\n")
        
        for result in theme_results:
            f.write(f"Theme: {result['theme']}\n")
            f.write(f"  Shared words: {result['shared_words']}\n")
            f.write(f"  YouTube freq: {result['yt_freq']} ({result['yt_pct']:.2f}%)\n")
            f.write(f"  Document freq: {result['doc_freq']} ({result['doc_pct']:.2f}%)\n")
            f.write(f"  YT/Doc ratio: {result['yt_freq']/result['doc_freq']:.4f}\n")
            f.write(f"  Words: {', '.join(sorted(result['words']))}\n")
            f.write("\n")
    
    print("\n✓ Saved: thematic_analysis_results.txt")

if __name__ == "__main__":
    main()
