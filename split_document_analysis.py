#!/usr/bin/env python3
"""
Split documents and analyze all similarity combinations:
1. First half of 2083 document vs whole YT video
2. First half of YT video vs whole/parts of 2083
3. Second half of YT video vs whole/parts of 2083
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

def preprocess_text(text):
    """Clean text."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return text

def main():
    # Read documents
    print("Loading documents...")
    with open('2083. EUROPEAN DECLARATION OF INDEPENDENCE.txt', 'r', encoding='utf-8', errors='ignore') as f:
        doc_text = f.read()
    
    with open('youtube_transcript_clean.txt', 'r', encoding='utf-8', errors='ignore') as f:
        yt_text = f.read()
    
    print("Splitting documents...")
    
    # Split 2083 document in half
    doc_words = doc_text.split()
    doc_half_point = len(doc_words) // 2
    doc_first_half = ' '.join(doc_words[:doc_half_point])
    doc_second_half = ' '.join(doc_words[doc_half_point:])
    
    print(f"2083 Document - First half: {len(doc_first_half.split()):,} words")
    print(f"2083 Document - Second half: {len(doc_second_half.split()):,} words")
    
    # Split YT video in half
    yt_words = yt_text.split()
    yt_half_point = len(yt_words) // 2
    yt_first_half = ' '.join(yt_words[:yt_half_point])
    yt_second_half = ' '.join(yt_words[yt_half_point:])
    
    print(f"YouTube - First half: {len(yt_first_half.split()):,} words")
    print(f"YouTube - Second half: {len(yt_second_half.split()):,} words")
    
    # Save split documents
    with open('2083_first_half.txt', 'w', encoding='utf-8') as f:
        f.write(doc_first_half)
    
    with open('2083_second_half.txt', 'w', encoding='utf-8') as f:
        f.write(doc_second_half)
    
    with open('youtube_first_half.txt', 'w', encoding='utf-8') as f:
        f.write(yt_first_half)
    
    with open('youtube_second_half.txt', 'w', encoding='utf-8') as f:
        f.write(yt_second_half)
    
    print("\n✓ Created split documents")
    
    # Preprocess all versions
    doc_full_clean = preprocess_text(doc_text)
    doc_first_clean = preprocess_text(doc_first_half)
    doc_second_clean = preprocess_text(doc_second_half)
    
    yt_full_clean = preprocess_text(yt_text)
    yt_first_clean = preprocess_text(yt_first_half)
    yt_second_clean = preprocess_text(yt_second_half)
    
    print("\n" + "="*70)
    print("SIMILARITY ANALYSIS - ALL COMBINATIONS")
    print("="*70)
    
    results = []
    
    def compute_similarity(text1, text2, name1, name2):
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform([text1, text2])
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return similarity
    
    # YouTube Full vs 2083 variations
    print("\n--- YouTube FULL vs 2083 ---")
    
    sim1 = compute_similarity(doc_full_clean, yt_full_clean, "2083 Full", "YT Full")
    print(f"2083 Full vs YT Full:         {sim1*100:.2f}%")
    results.append(("2083 Full", "YT Full", sim1))
    
    sim2 = compute_similarity(doc_first_clean, yt_full_clean, "2083 First Half", "YT Full")
    print(f"2083 First Half vs YT Full:   {sim2*100:.2f}%")
    results.append(("2083 First Half", "YT Full", sim2))
    
    sim3 = compute_similarity(doc_second_clean, yt_full_clean, "2083 Second Half", "YT Full")
    print(f"2083 Second Half vs YT Full:  {sim3*100:.2f}%")
    results.append(("2083 Second Half", "YT Full", sim3))
    
    # YouTube First Half vs 2083 variations
    print("\n--- YouTube FIRST HALF vs 2083 ---")
    
    sim4 = compute_similarity(doc_full_clean, yt_first_clean, "2083 Full", "YT First Half")
    print(f"2083 Full vs YT First Half:         {sim4*100:.2f}%")
    results.append(("2083 Full", "YT First Half", sim4))
    
    sim5 = compute_similarity(doc_first_clean, yt_first_clean, "2083 First Half", "YT First Half")
    print(f"2083 First Half vs YT First Half:   {sim5*100:.2f}%")
    results.append(("2083 First Half", "YT First Half", sim5))
    
    sim6 = compute_similarity(doc_second_clean, yt_first_clean, "2083 Second Half", "YT First Half")
    print(f"2083 Second Half vs YT First Half:  {sim6*100:.2f}%")
    results.append(("2083 Second Half", "YT First Half", sim6))
    
    # YouTube Second Half vs 2083 variations
    print("\n--- YouTube SECOND HALF vs 2083 ---")
    
    sim7 = compute_similarity(doc_full_clean, yt_second_clean, "2083 Full", "YT Second Half")
    print(f"2083 Full vs YT Second Half:         {sim7*100:.2f}%")
    results.append(("2083 Full", "YT Second Half", sim7))
    
    sim8 = compute_similarity(doc_first_clean, yt_second_clean, "2083 First Half", "YT Second Half")
    print(f"2083 First Half vs YT Second Half:   {sim8*100:.2f}%")
    results.append(("2083 First Half", "YT Second Half", sim8))
    
    sim9 = compute_similarity(doc_second_clean, yt_second_clean, "2083 Second Half", "YT Second Half")
    print(f"2083 Second Half vs YT Second Half:  {sim9*100:.2f}%")
    results.append(("2083 Second Half", "YT Second Half", sim9))
    
    # Find highest and lowest similarities
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    
    results_sorted = sorted(results, key=lambda x: x[2], reverse=True)
    
    print("\n--- Top 3 Highest Similarities: ---")
    for i, (doc_part, yt_part, score) in enumerate(results_sorted[:3], 1):
        print(f"{i}. {doc_part:20} vs {yt_part:20} = {score*100:.2f}%")
    
    print("\n--- Top 3 Lowest Similarities: ---")
    for i, (doc_part, yt_part, score) in enumerate(results_sorted[-3:], 1):
        print(f"{i}. {doc_part:20} vs {yt_part:20} = {score*100:.2f}%")
    
    # Analysis insights
    print("\n" + "="*70)
    print("INSIGHTS")
    print("="*70)
    
    print(f"\nFirst half of 2083 vs Full YT:   {sim2*100:.2f}%")
    print(f"Second half of 2083 vs Full YT:  {sim3*100:.2f}%")
    print(f"Difference: {abs(sim2-sim3)*100:.2f} percentage points")
    
    if sim2 > sim3:
        print("→ First half of 2083 document is MORE similar to YT video")
    else:
        print("→ Second half of 2083 document is MORE similar to YT video")
    
    print(f"\nFirst half of YT vs Full 2083:   {sim4*100:.2f}%")
    print(f"Second half of YT vs Full 2083:  {sim7*100:.2f}%")
    print(f"Difference: {abs(sim4-sim7)*100:.2f} percentage points")
    
    if sim4 > sim7:
        print("→ First half of YT video is MORE similar to 2083 document")
    else:
        print("→ Second half of YT video is MORE similar to 2083 document")
    
    # Cross-comparison
    print(f"\nBest cross-match: {results_sorted[0][0]} vs {results_sorted[0][1]} = {results_sorted[0][2]*100:.2f}%")
    
    # Save results
    with open('split_analysis_results.txt', 'w') as f:
        f.write("SPLIT DOCUMENT SIMILARITY ANALYSIS\\n")
        f.write("="*70 + "\\n\\n")
        f.write("All Combinations (sorted by similarity):\\n")
        f.write("-"*70 + "\\n")
        for doc_part, yt_part, score in results_sorted:
            f.write(f"{doc_part:25} vs {yt_part:20} = {score*100:6.2f}%\\n")
    
    print("\n✓ Results saved to split_analysis_results.txt")

if __name__ == "__main__":
    main()
