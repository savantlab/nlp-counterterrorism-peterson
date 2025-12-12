#!/usr/bin/env python3
"""
Compute cosine similarity between two text documents.
"""

import re
from collections import Counter
from math import sqrt

def preprocess_text(text):
    """Clean and tokenize text."""
    # Convert to lowercase
    text = text.lower()
    # Remove special characters and keep only alphanumeric and spaces
    text = re.sub(r'[^a-z0-9\s]', '', text)
    # Tokenize
    tokens = text.split()
    return tokens

def compute_tf(tokens):
    """Compute term frequency."""
    return Counter(tokens)

def compute_cosine_similarity(vec1, vec2):
    """Compute cosine similarity between two frequency vectors."""
    # Get all unique terms
    all_terms = set(vec1.keys()) | set(vec2.keys())
    
    # Compute dot product
    dot_product = sum(vec1.get(term, 0) * vec2.get(term, 0) for term in all_terms)
    
    # Compute magnitudes
    magnitude1 = sqrt(sum(count ** 2 for count in vec1.values()))
    magnitude2 = sqrt(sum(count ** 2 for count in vec2.values()))
    
    # Avoid division by zero
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    
    return dot_product / (magnitude1 * magnitude2)

def main():
    # Read documents
    with open('2083. EUROPEAN DECLARATION OF INDEPENDENCE.txt', 'r', encoding='utf-8', errors='ignore') as f:
        doc1_text = f.read()
    
    with open('youtube_transcript_clean.txt', 'r', encoding='utf-8', errors='ignore') as f:
        doc2_text = f.read()
    
    # Preprocess
    print("Preprocessing documents...")
    doc1_tokens = preprocess_text(doc1_text)
    doc2_tokens = preprocess_text(doc2_text)
    
    print(f"Document 1: {len(doc1_tokens)} tokens")
    print(f"Document 2: {len(doc2_tokens)} tokens")
    
    # Compute term frequencies
    doc1_tf = compute_tf(doc1_tokens)
    doc2_tf = compute_tf(doc2_tokens)
    
    print(f"Document 1: {len(doc1_tf)} unique terms")
    print(f"Document 2: {len(doc2_tf)} unique terms")
    
    # Compute cosine similarity
    similarity = compute_cosine_similarity(doc1_tf, doc2_tf)
    
    print(f"\nCosine Similarity: {similarity:.6f}")
    print(f"Similarity Percentage: {similarity * 100:.2f}%")
    
    # Find common terms
    common_terms = set(doc1_tf.keys()) & set(doc2_tf.keys())
    print(f"\nCommon terms: {len(common_terms)}")
    
    # Top 20 common terms by frequency in doc2
    common_sorted = sorted(
        [(term, doc2_tf[term], doc1_tf[term]) for term in common_terms],
        key=lambda x: x[1],
        reverse=True
    )[:20]
    
    print("\nTop 20 common terms (YouTube transcript frequency, Document frequency):")
    for term, freq2, freq1 in common_sorted:
        print(f"  {term}: {freq2} (YT), {freq1} (Doc)")

if __name__ == "__main__":
    main()
