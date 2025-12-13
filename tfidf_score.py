#!/usr/bin/env python3
"""
Compute cosine similarity between two text documents using TF-IDF.
This is a more accurate measure than raw term frequency.
"""

import re
from collections import Counter
from math import sqrt, log

def preprocess_text(text):
    """Clean and tokenize text."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    tokens = text.split()
    return tokens

def compute_tf(tokens):
    """Compute term frequency (normalized)."""
    counter = Counter(tokens)
    total = len(tokens)
    return {term: count / total for term, count in counter.items()}

def compute_idf(doc1_tokens, doc2_tokens):
    """Compute inverse document frequency."""
    # Total number of documents
    num_docs = 2
    
    # Count document frequency for each term
    all_terms = set(doc1_tokens) | set(doc2_tokens)
    doc_freq = {}
    
    for term in all_terms:
        count = 0
        if term in doc1_tokens:
            count += 1
        if term in doc2_tokens:
            count += 1
        doc_freq[term] = count
    
    # Compute IDF
    idf = {}
    for term, freq in doc_freq.items():
        idf[term] = log(num_docs / freq)
    
    return idf

def compute_tfidf(tf, idf):
    """Compute TF-IDF vectors."""
    return {term: tf_val * idf.get(term, 0) for term, tf_val in tf.items()}

def compute_cosine_similarity(vec1, vec2):
    """Compute cosine similarity between two TF-IDF vectors."""
    # Get all unique terms
    all_terms = set(vec1.keys()) | set(vec2.keys())
    
    # Compute dot product
    dot_product = sum(vec1.get(term, 0) * vec2.get(term, 0) for term in all_terms)
    
    # Compute magnitudes
    magnitude1 = sqrt(sum(val ** 2 for val in vec1.values()))
    magnitude2 = sqrt(sum(val ** 2 for val in vec2.values()))
    
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    
    return dot_product / (magnitude1 * magnitude2)

def main():
    # Read documents
    with open('txt/2083. EUROPEAN DECLARATION OF INDEPENDENCE.txt', 'r', encoding='utf-8', errors='ignore') as f:
        doc1_text = f.read()
    
    with open('txt/youtube_transcript_clean.txt', 'r', encoding='utf-8', errors='ignore') as f:
        doc2_text = f.read()
    
    print("Preprocessing documents...")
    doc1_tokens = preprocess_text(doc1_text)
    doc2_tokens = preprocess_text(doc2_text)
    
    print(f"Document 1: {len(doc1_tokens)} tokens")
    print(f"Document 2: {len(doc2_tokens)} tokens")
    
    # Get unique tokens for IDF calculation
    doc1_unique = set(doc1_tokens)
    doc2_unique = set(doc2_tokens)
    
    print(f"Document 1: {len(doc1_unique)} unique terms")
    print(f"Document 2: {len(doc2_unique)} unique terms")
    
    # Compute term frequencies
    doc1_tf = compute_tf(doc1_tokens)
    doc2_tf = compute_tf(doc2_tokens)
    
    # Compute IDF
    idf = compute_idf(doc1_unique, doc2_unique)
    
    # Compute TF-IDF vectors
    doc1_tfidf = compute_tfidf(doc1_tf, idf)
    doc2_tfidf = compute_tfidf(doc2_tf, idf)
    
    # Compute cosine similarity
    similarity = compute_cosine_similarity(doc1_tfidf, doc2_tfidf)
    
    print(f"\n=== TF-IDF Cosine Similarity ===")
    print(f"Cosine Similarity: {similarity:.6f}")
    print(f"Similarity Percentage: {similarity * 100:.2f}%")
    
    # Find common terms
    common_terms = doc1_unique & doc2_unique
    print(f"\n=== Analysis ===")
    print(f"Common terms: {len(common_terms)} out of {len(doc2_unique)} in YouTube transcript")
    print(f"Vocabulary overlap: {len(common_terms) / len(doc2_unique) * 100:.1f}%")
    
    # Top terms by TF-IDF score in YouTube transcript
    yt_scores = sorted(doc2_tfidf.items(), key=lambda x: x[1], reverse=True)[:20]
    print("\nTop 20 terms in YouTube transcript by TF-IDF score:")
    for term, score in yt_scores:
        in_doc1 = "✓" if term in doc1_unique else "✗"
        print(f"  {term}: {score:.6f} [in Doc1: {in_doc1}]")

if __name__ == "__main__":
    main()
