#!/usr/bin/env python3
"""
Compute N-gram based similarity between two text documents.
Uses bigrams (2-word sequences) and trigrams (3-word sequences).
"""

import re
from collections import Counter
from math import sqrt

def preprocess_text(text):
    """Clean and tokenize text."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    tokens = text.split()
    return tokens

def generate_ngrams(tokens, n):
    """Generate n-grams from token list."""
    ngrams = []
    for i in range(len(tokens) - n + 1):
        ngram = tuple(tokens[i:i+n])
        ngrams.append(ngram)
    return ngrams

def compute_cosine_similarity(vec1, vec2):
    """Compute cosine similarity between two frequency vectors."""
    all_items = set(vec1.keys()) | set(vec2.keys())
    
    dot_product = sum(vec1.get(item, 0) * vec2.get(item, 0) for item in all_items)
    
    magnitude1 = sqrt(sum(count ** 2 for count in vec1.values()))
    magnitude2 = sqrt(sum(count ** 2 for count in vec2.values()))
    
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    
    return dot_product / (magnitude1 * magnitude2)

def compute_jaccard_similarity(set1, set2):
    """Compute Jaccard similarity (intersection over union)."""
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    
    if union == 0:
        return 0.0
    
    return intersection / union

def main():
    # Read documents
    with open('2083. EUROPEAN DECLARATION OF INDEPENDENCE.txt', 'r', encoding='utf-8', errors='ignore') as f:
        doc1_text = f.read()
    
    with open('youtube_transcript_clean.txt', 'r', encoding='utf-8', errors='ignore') as f:
        doc2_text = f.read()
    
    print("Preprocessing documents...")
    doc1_tokens = preprocess_text(doc1_text)
    doc2_tokens = preprocess_text(doc2_text)
    
    print(f"Document 1: {len(doc1_tokens)} tokens")
    print(f"Document 2: {len(doc2_tokens)} tokens")
    
    # Generate bigrams (2-grams)
    print("\n=== Bigram Analysis ===")
    doc1_bigrams = generate_ngrams(doc1_tokens, 2)
    doc2_bigrams = generate_ngrams(doc2_tokens, 2)
    
    doc1_bigram_freq = Counter(doc1_bigrams)
    doc2_bigram_freq = Counter(doc2_bigrams)
    
    print(f"Document 1: {len(doc1_bigrams)} bigrams ({len(doc1_bigram_freq)} unique)")
    print(f"Document 2: {len(doc2_bigrams)} bigrams ({len(doc2_bigram_freq)} unique)")
    
    # Cosine similarity for bigrams
    bigram_cosine = compute_cosine_similarity(doc1_bigram_freq, doc2_bigram_freq)
    print(f"\nBigram Cosine Similarity: {bigram_cosine:.6f} ({bigram_cosine * 100:.2f}%)")
    
    # Jaccard similarity for bigrams
    doc1_bigram_set = set(doc1_bigrams)
    doc2_bigram_set = set(doc2_bigrams)
    bigram_jaccard = compute_jaccard_similarity(doc1_bigram_set, doc2_bigram_set)
    print(f"Bigram Jaccard Similarity: {bigram_jaccard:.6f} ({bigram_jaccard * 100:.2f}%)")
    
    # Common bigrams
    common_bigrams = doc1_bigram_set & doc2_bigram_set
    print(f"Common bigrams: {len(common_bigrams)} out of {len(doc2_bigram_set)}")
    
    # Generate trigrams (3-grams)
    print("\n=== Trigram Analysis ===")
    doc1_trigrams = generate_ngrams(doc1_tokens, 3)
    doc2_trigrams = generate_ngrams(doc2_tokens, 3)
    
    doc1_trigram_freq = Counter(doc1_trigrams)
    doc2_trigram_freq = Counter(doc2_trigrams)
    
    print(f"Document 1: {len(doc1_trigrams)} trigrams ({len(doc1_trigram_freq)} unique)")
    print(f"Document 2: {len(doc2_trigrams)} trigrams ({len(doc2_trigram_freq)} unique)")
    
    # Cosine similarity for trigrams
    trigram_cosine = compute_cosine_similarity(doc1_trigram_freq, doc2_trigram_freq)
    print(f"\nTrigram Cosine Similarity: {trigram_cosine:.6f} ({trigram_cosine * 100:.2f}%)")
    
    # Jaccard similarity for trigrams
    doc1_trigram_set = set(doc1_trigrams)
    doc2_trigram_set = set(doc2_trigrams)
    trigram_jaccard = compute_jaccard_similarity(doc1_trigram_set, doc2_trigram_set)
    print(f"Trigram Jaccard Similarity: {trigram_jaccard:.6f} ({trigram_jaccard * 100:.2f}%)")
    
    # Common trigrams
    common_trigrams = doc1_trigram_set & doc2_trigram_set
    print(f"Common trigrams: {len(common_trigrams)} out of {len(doc2_trigram_set)}")
    
    # Show top common bigrams by frequency in YouTube transcript
    if common_bigrams:
        print("\n=== Top 15 Common Bigrams (YouTube transcript frequency) ===")
        common_bigram_freqs = [(bg, doc2_bigram_freq[bg], doc1_bigram_freq[bg]) 
                               for bg in common_bigrams]
        common_bigram_freqs.sort(key=lambda x: x[1], reverse=True)
        
        for bigram, yt_freq, doc_freq in common_bigram_freqs[:15]:
            print(f"  '{' '.join(bigram)}': YT={yt_freq}, Doc={doc_freq}")
    
    # Show top common trigrams by frequency in YouTube transcript
    if common_trigrams:
        print("\n=== Top 15 Common Trigrams (YouTube transcript frequency) ===")
        common_trigram_freqs = [(tg, doc2_trigram_freq[tg], doc1_trigram_freq[tg]) 
                                for tg in common_trigrams]
        common_trigram_freqs.sort(key=lambda x: x[1], reverse=True)
        
        for trigram, yt_freq, doc_freq in common_trigram_freqs[:15]:
            print(f"  '{' '.join(trigram)}': YT={yt_freq}, Doc={doc_freq}")

if __name__ == "__main__":
    main()
