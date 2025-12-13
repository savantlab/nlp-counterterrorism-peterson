#!/usr/bin/env python3
"""
Compute vector-based similarity using TF-IDF vectorization.
Uses scikit-learn's TfidfVectorizer for professional implementation.
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
    with open('txt/2083. EUROPEAN DECLARATION OF INDEPENDENCE.txt', 'r', encoding='utf-8', errors='ignore') as f:
        doc1_text = f.read()
    
    with open('txt/youtube_transcript_clean.txt', 'r', encoding='utf-8', errors='ignore') as f:
        doc2_text = f.read()
    
    print("Preprocessing documents...")
    doc1_clean = preprocess_text(doc1_text)
    doc2_clean = preprocess_text(doc2_text)
    
    documents = [doc1_clean, doc2_clean]
    
    # Create TF-IDF vectors
    print("\n=== TF-IDF Vectorization (with stop words) ===")
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(documents)
    
    # Compute cosine similarity
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    
    print(f"Cosine Similarity: {similarity:.6f}")
    print(f"Similarity Percentage: {similarity * 100:.2f}%")
    
    # Show feature info
    feature_names = vectorizer.get_feature_names_out()
    print(f"\nTotal features (unique terms): {len(feature_names)}")
    
    # Get top features for each document
    doc1_vector = tfidf_matrix[0].toarray()[0]
    doc2_vector = tfidf_matrix[1].toarray()[0]
    
    # Top terms in YouTube transcript
    doc2_scores = [(feature_names[i], doc2_vector[i]) for i in range(len(feature_names)) if doc2_vector[i] > 0]
    doc2_scores.sort(key=lambda x: x[1], reverse=True)
    
    print("\nTop 20 terms in YouTube transcript by TF-IDF score:")
    for term, score in doc2_scores[:20]:
        doc1_score = doc1_vector[list(feature_names).index(term)]
        in_doc1 = "✓" if doc1_score > 0 else "✗"
        print(f"  {term}: {score:.6f} [in Doc1: {in_doc1}]")
    
    # Now without stop words removal for comparison
    print("\n=== TF-IDF Vectorization (no stop word removal) ===")
    vectorizer_no_stop = TfidfVectorizer(stop_words=None)
    tfidf_matrix_no_stop = vectorizer_no_stop.fit_transform(documents)
    
    similarity_no_stop = cosine_similarity(tfidf_matrix_no_stop[0:1], tfidf_matrix_no_stop[1:2])[0][0]
    
    print(f"Cosine Similarity: {similarity_no_stop:.6f}")
    print(f"Similarity Percentage: {similarity_no_stop * 100:.2f}%")
    
    # Using bigrams and trigrams (n-grams)
    print("\n=== TF-IDF with N-grams (1-3) ===")
    vectorizer_ngram = TfidfVectorizer(stop_words='english', ngram_range=(1, 3), max_features=10000)
    tfidf_matrix_ngram = vectorizer_ngram.fit_transform(documents)
    
    similarity_ngram = cosine_similarity(tfidf_matrix_ngram[0:1], tfidf_matrix_ngram[1:2])[0][0]
    
    print(f"Cosine Similarity: {similarity_ngram:.6f}")
    print(f"Similarity Percentage: {similarity_ngram * 100:.2f}%")
    
    # Summary
    print("\n=== Summary ===")
    print(f"TF-IDF (with stop word removal):    {similarity * 100:.2f}%")
    print(f"TF-IDF (no stop word removal):      {similarity_no_stop * 100:.2f}%")
    print(f"TF-IDF with N-grams (1-3):          {similarity_ngram * 100:.2f}%")

if __name__ == "__main__":
    main()
