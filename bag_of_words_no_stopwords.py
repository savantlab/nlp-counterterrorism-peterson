#!/usr/bin/env python3
"""
Compute cosine similarity between two text documents using bag-of-words
with stop words removed.
"""

import re
from collections import Counter
from math import sqrt

# Common English stop words
STOP_WORDS = {
    'a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', 
    'arent', 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 
    'but', 'by', 'cant', 'cannot', 'could', 'couldnt', 'did', 'didnt', 'do', 'does', 'doesnt', 
    'doing', 'dont', 'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', 'hadnt', 
    'has', 'hasnt', 'have', 'havent', 'having', 'he', 'hed', 'hell', 'hes', 'her', 'here', 
    'heres', 'hers', 'herself', 'him', 'himself', 'his', 'how', 'hows', 'i', 'id', 'ill', 'im', 
    'ive', 'if', 'in', 'into', 'is', 'isnt', 'it', 'its', 'its', 'itself', 'lets', 'me', 'more', 
    'most', 'mustnt', 'my', 'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 
    'or', 'other', 'ought', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 'same', 'shant', 
    'she', 'shed', 'shell', 'shes', 'should', 'shouldnt', 'so', 'some', 'such', 'than', 'that', 
    'thats', 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', 'theres', 'these', 
    'they', 'theyd', 'theyll', 'theyre', 'theyve', 'this', 'those', 'through', 'to', 'too', 
    'under', 'until', 'up', 'very', 'was', 'wasnt', 'we', 'wed', 'well', 'were', 'weve', 'werent', 
    'what', 'whats', 'when', 'whens', 'where', 'wheres', 'which', 'while', 'who', 'whos', 'whom', 
    'why', 'whys', 'with', 'wont', 'would', 'wouldnt', 'you', 'youd', 'youll', 'youre', 'youve', 
    'your', 'yours', 'yourself', 'yourselves'
}

def preprocess_text(text, remove_stopwords=True):
    """Clean and tokenize text."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    tokens = text.split()
    
    if remove_stopwords:
        tokens = [t for t in tokens if t not in STOP_WORDS]
    
    return tokens

def compute_tf(tokens):
    """Compute term frequency."""
    return Counter(tokens)

def compute_cosine_similarity(vec1, vec2):
    """Compute cosine similarity between two frequency vectors."""
    all_terms = set(vec1.keys()) | set(vec2.keys())
    
    dot_product = sum(vec1.get(term, 0) * vec2.get(term, 0) for term in all_terms)
    
    magnitude1 = sqrt(sum(count ** 2 for count in vec1.values()))
    magnitude2 = sqrt(sum(count ** 2 for count in vec2.values()))
    
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    
    return dot_product / (magnitude1 * magnitude2)

def main():
    # Read documents
    with open('2083. EUROPEAN DECLARATION OF INDEPENDENCE.txt', 'r', encoding='utf-8', errors='ignore') as f:
        doc1_text = f.read()
    
    with open('youtube_transcript_clean.txt', 'r', encoding='utf-8', errors='ignore') as f:
        doc2_text = f.read()
    
    print("Preprocessing documents (removing stop words)...")
    doc1_tokens = preprocess_text(doc1_text, remove_stopwords=True)
    doc2_tokens = preprocess_text(doc2_text, remove_stopwords=True)
    
    print(f"Document 1: {len(doc1_tokens)} tokens (after stop word removal)")
    print(f"Document 2: {len(doc2_tokens)} tokens (after stop word removal)")
    
    # Compute term frequencies
    doc1_tf = compute_tf(doc1_tokens)
    doc2_tf = compute_tf(doc2_tokens)
    
    print(f"Document 1: {len(doc1_tf)} unique terms")
    print(f"Document 2: {len(doc2_tf)} unique terms")
    
    # Compute cosine similarity
    similarity = compute_cosine_similarity(doc1_tf, doc2_tf)
    
    print(f"\n=== Bag-of-Words (No Stop Words) Cosine Similarity ===")
    print(f"Cosine Similarity: {similarity:.6f}")
    print(f"Similarity Percentage: {similarity * 100:.2f}%")
    
    # Find common terms
    common_terms = set(doc1_tf.keys()) & set(doc2_tf.keys())
    print(f"\nCommon terms: {len(common_terms)}")
    print(f"Vocabulary overlap: {len(common_terms) / len(doc2_tf) * 100:.1f}%")
    
    # Top 20 common terms by frequency in doc2
    common_sorted = sorted(
        [(term, doc2_tf[term], doc1_tf[term]) for term in common_terms],
        key=lambda x: x[1],
        reverse=True
    )[:20]
    
    print("\nTop 20 common content words (YouTube transcript frequency, Document frequency):")
    for term, freq2, freq1 in common_sorted:
        print(f"  {term}: {freq2} (YT), {freq1} (Doc)")
    
    # Compare with original (with stop words)
    print("\n=== Comparison with Stop Words Included ===")
    doc1_tokens_with_stops = preprocess_text(doc1_text, remove_stopwords=False)
    doc2_tokens_with_stops = preprocess_text(doc2_text, remove_stopwords=False)
    
    doc1_tf_with_stops = compute_tf(doc1_tokens_with_stops)
    doc2_tf_with_stops = compute_tf(doc2_tokens_with_stops)
    
    similarity_with_stops = compute_cosine_similarity(doc1_tf_with_stops, doc2_tf_with_stops)
    
    print(f"With stop words: {similarity_with_stops * 100:.2f}%")
    print(f"Without stop words: {similarity * 100:.2f}%")
    print(f"Difference: {(similarity_with_stops - similarity) * 100:.2f} percentage points")

if __name__ == "__main__":
    main()
