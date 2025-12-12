#!/usr/bin/env python3
"""
Create visualizations for thematic analysis results.
"""

import matplotlib.pyplot as plt
import numpy as np
import re
from collections import Counter

# Define thematic word groups
THEMES = {
    'Identity & Social': [
        'identity', 'race', 'sex', 'sexual', 'gender', 'diversity', 'equality', 'equity',
        'discrimination', 'oppression', 'victim', 'patriarchal', 'class', 'groups', 'group'
    ],
    'Ideas & Thought': [
        'ideas', 'idea', 'think', 'thinking', 'philosophy', 'philosopher', 'ideology',
        'concept', 'concepts', 'truth', 'belief', 'believe', 'believers'
    ],
    'Political & Ideological': [
        'marx', 'marxist', 'radical', 'radicals', 'left', 'progressive', 'ideology', 'politics',
        'political', 'capitalism', 'socialist', 'communist', 'revolution', 'postmodernism', 'post'
    ],
    'Education & Academia': [
        'education', 'university', 'universities', 'college', 'campus', 'professor', 'professors',
        'degree', 'learn', 'student', 'students', 'teaching', 'academic', 'school', 'children'
    ],
    'Cultural & Western': [
        'western', 'west', 'civilization', 'culture', 'cultural', 'society', 'values',
        'tradition', 'traditional', 'shakespeare', 'history', 'heritage'
    ],
    'Power & Conflict': [
        'power', 'struggle', 'conflict', 'war', 'fought', 'violence', 'violent', 'violently',
        'corrupt', 'dangerous', 'destructive', 'undermine', 'oppose', 'attack'
    ],
    'Freedom & Rights': [
        'freedom', 'free', 'rights', 'speech', 'liberty', 'democracy', 'democratic',
        'expression', 'opinion', 'consensus'
    ],
    'Time & History': [
        'history', 'historical', 'century', '19th', '60s', '70s', 'today', 'now',
        'currently', 'recently', 'decades', 'time', 'first', 'second'
    ],
    'People & Society': [
        'people', 'individuals', 'society', 'generations', 'children', 'young', 'families',
        'communities', 'population', 'humanity', 'human'
    ],
    'Action & Change': [
        'made', 'making', 'become', 'became', 'change', 'changing', 'spread', 'produced',
        'created', 'take', 'took', 'done'
    ]
}

def preprocess_text(text):
    """Clean text."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return text

def main():
    print("Loading documents...\n")
    
    # Read documents
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
    
    # Preprocess texts
    doc_clean = preprocess_text(doc_text)
    yt_clean = preprocess_text(yt_text)
    
    doc_words = doc_clean.split()
    yt_words = yt_clean.split()
    
    doc_freq = Counter(doc_words)
    yt_freq = Counter(yt_words)
    
    # Analyze each theme
    theme_results = []
    
    for theme_name, theme_words in THEMES.items():
        theme_shared = [w for w in theme_words if w in shared_words]
        
        if not theme_shared:
            continue
        
        doc_theme_freq = sum(doc_freq[w] for w in theme_shared)
        yt_theme_freq = sum(yt_freq[w] for w in theme_shared)
        
        doc_pct = (doc_theme_freq / len(doc_words)) * 100
        yt_pct = (yt_theme_freq / len(yt_words)) * 100
        
        theme_results.append({
            'theme': theme_name,
            'shared_words': len(theme_shared),
            'yt_freq': yt_theme_freq,
            'doc_freq': doc_theme_freq,
            'yt_pct': yt_pct,
            'doc_pct': doc_pct,
            'ratio': yt_theme_freq/doc_theme_freq
        })
    
    # Sort by YouTube frequency
    theme_results.sort(key=lambda x: x['yt_freq'], reverse=True)
    
    # Create comprehensive visualization
    fig = plt.figure(figsize=(18, 12))
    
    # 1. Frequency comparison (top left)
    ax1 = plt.subplot(2, 2, 1)
    themes = [r['theme'] for r in theme_results]
    yt_freqs = [r['yt_freq'] for r in theme_results]
    doc_freqs = [r['doc_freq']/10 for r in theme_results]  # Scale down for visibility
    
    x = np.arange(len(themes))
    width = 0.35
    
    bars1 = ax1.bar(x - width/2, yt_freqs, width, label='YouTube', color='coral', alpha=0.8)
    bars2 = ax1.bar(x + width/2, doc_freqs, width, label='Document (÷10)', color='steelblue', alpha=0.8)
    
    ax1.set_xlabel('Theme', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Frequency (count)', fontsize=11, fontweight='bold')
    ax1.set_title('Theme Frequency Comparison', fontsize=13, fontweight='bold', pad=15)
    ax1.set_xticks(x)
    ax1.set_xticklabels(themes, rotation=45, ha='right', fontsize=9)
    ax1.legend(loc='upper right')
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Add value labels on bars
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}', ha='center', va='bottom', fontsize=8)
    
    # 2. YT/Doc ratio (top right)
    ax2 = plt.subplot(2, 2, 2)
    ratios = [r['ratio'] for r in theme_results]
    colors_gradient = plt.cm.viridis(np.linspace(0.3, 0.9, len(themes)))
    
    bars = ax2.barh(themes, ratios, color=colors_gradient, alpha=0.85)
    ax2.set_xlabel('YT/Doc Ratio', fontsize=11, fontweight='bold')
    ax2.set_title('Relative Emphasis in YouTube\n(higher = more over-represented)', 
                  fontsize=13, fontweight='bold', pad=15)
    ax2.grid(axis='x', alpha=0.3, linestyle='--')
    ax2.invert_yaxis()
    
    # Add value labels
    for i, (bar, ratio) in enumerate(zip(bars, ratios)):
        width = bar.get_width()
        ax2.text(width + 0.003, bar.get_y() + bar.get_height()/2, 
                f'{ratio:.4f}', ha='left', va='center', fontsize=9, fontweight='bold')
    
    # 3. Percentage of document composition (bottom left)
    ax3 = plt.subplot(2, 2, 3)
    yt_pcts = [r['yt_pct'] for r in theme_results]
    doc_pcts = [r['doc_pct'] for r in theme_results]
    
    bars1 = ax3.bar(x - width/2, yt_pcts, width, label='YouTube', color='coral', alpha=0.8)
    bars2 = ax3.bar(x + width/2, doc_pcts, width, label='Document', color='steelblue', alpha=0.8)
    
    ax3.set_xlabel('Theme', fontsize=11, fontweight='bold')
    ax3.set_ylabel('Percentage of Total Words (%)', fontsize=11, fontweight='bold')
    ax3.set_title('Theme Density in Each Document', fontsize=13, fontweight='bold', pad=15)
    ax3.set_xticks(x)
    ax3.set_xticklabels(themes, rotation=45, ha='right', fontsize=9)
    ax3.legend(loc='upper right')
    ax3.grid(axis='y', alpha=0.3, linestyle='--')
    
    # 4. Word count per theme (bottom right)
    ax4 = plt.subplot(2, 2, 4)
    word_counts = [r['shared_words'] for r in theme_results]
    
    bars = ax4.bar(themes, word_counts, color='teal', alpha=0.75, edgecolor='darkslategray', linewidth=1.5)
    ax4.set_xlabel('Theme', fontsize=11, fontweight='bold')
    ax4.set_ylabel('Number of Shared Words', fontsize=11, fontweight='bold')
    ax4.set_title('Shared Vocabulary per Theme', fontsize=13, fontweight='bold', pad=15)
    ax4.set_xticklabels(themes, rotation=45, ha='right', fontsize=9)
    ax4.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}', ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    plt.suptitle('Thematic Pattern Analysis: YouTube Transcript vs 2083 Document', 
                 fontsize=16, fontweight='bold', y=0.995)
    
    plt.tight_layout(rect=[0, 0, 1, 0.99])
    
    # Save figure
    output_file = 'thematic_analysis_visualization.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_file}")
    
    plt.show()
    
    # Print summary statistics
    print("\n" + "="*80)
    print("THEMATIC ANALYSIS SUMMARY")
    print("="*80)
    
    print(f"\n{'Theme':<30} {'Words':<8} {'YT Freq':<10} {'Doc Freq':<10} {'Ratio':<10}")
    print("-"*80)
    for r in theme_results:
        print(f"{r['theme']:<30} {r['shared_words']:<8} {r['yt_freq']:<10} "
              f"{r['doc_freq']:<10} {r['ratio']:.4f}")
    
    print("\n" + "="*80)
    print("KEY INSIGHTS")
    print("="*80)
    print(f"\nMost prominent theme in YouTube: {theme_results[0]['theme']}")
    print(f"  - {theme_results[0]['yt_freq']} occurrences ({theme_results[0]['yt_pct']:.2f}% of transcript)")
    
    highest_ratio = max(theme_results, key=lambda x: x['ratio'])
    print(f"\nMost over-represented in YouTube: {highest_ratio['theme']}")
    print(f"  - Ratio: {highest_ratio['ratio']:.4f}x (appears {highest_ratio['ratio']:.2%} as often)")
    
    print(f"\nTotal shared words analyzed: {len(shared_words)}")
    print(f"Themes identified: {len(theme_results)}")

if __name__ == "__main__":
    main()
