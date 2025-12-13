#!/usr/bin/env python3
"""
Analyze chunks of the large document against the YouTube transcript.
Splits the document into approximately equal chunks and compares each.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

def preprocess_text(text):
    """Clean text."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return text

def split_into_chunks(text, num_chunks=4):
    """Split text into approximately equal chunks."""
    words = text.split()
    chunk_size = len(words) // num_chunks
    
    chunks = []
    for i in range(num_chunks):
        start_idx = i * chunk_size
        if i == num_chunks - 1:
            # Last chunk gets remaining words
            chunk = ' '.join(words[start_idx:])
        else:
            end_idx = (i + 1) * chunk_size
            chunk = ' '.join(words[start_idx:end_idx])
        chunks.append(chunk)
    
    return chunks

def main():
    # Read documents
    print("Loading documents...")
    with open('txt/2083. EUROPEAN DECLARATION OF INDEPENDENCE.txt', 'r', encoding='utf-8', errors='ignore') as f:
        doc1_text = f.read()
    
    with open('txt/youtube_transcript_clean.txt', 'r', encoding='utf-8', errors='ignore') as f:
        doc2_text = f.read()
    
    print("Preprocessing documents...")
    doc1_clean = preprocess_text(doc1_text)
    doc2_clean = preprocess_text(doc2_text)
    
    # Split large document into 4 chunks (roughly 250 pages each)
    print("\nSplitting document into 4 chunks...")
    chunks = split_into_chunks(doc1_clean, num_chunks=4)
    
    for i, chunk in enumerate(chunks):
        word_count = len(chunk.split())
        print(f"Chunk {i+1}: {word_count:,} words")
    
    # Analyze each chunk
    print("\n" + "="*70)
    print("ANALYZING CHUNKS WITH TF-IDF (stop words removed)")
    print("="*70)
    
    results = []
    
    for i, chunk in enumerate(chunks):
        print(f"\n--- Chunk {i+1} vs YouTube Transcript ---")
        
        documents = [chunk, doc2_clean]
        
        # TF-IDF with stop words removed
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(documents)
        
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        
        print(f"Cosine Similarity: {similarity:.6f} ({similarity * 100:.2f}%)")
        
        results.append((i+1, similarity))
        
        # Get top shared terms
        feature_names = vectorizer.get_feature_names_out()
        chunk_vector = tfidf_matrix[0].toarray()[0]
        yt_vector = tfidf_matrix[1].toarray()[0]
        
        # Find terms that appear in both with non-zero scores
        shared_terms = []
        for idx, term in enumerate(feature_names):
            if chunk_vector[idx] > 0 and yt_vector[idx] > 0:
                shared_terms.append((term, chunk_vector[idx], yt_vector[idx]))
        
        # Sort by YouTube transcript score
        shared_terms.sort(key=lambda x: x[2], reverse=True)
        
        print(f"\nTop 10 shared terms (sorted by YT importance):")
        for term, chunk_score, yt_score in shared_terms[:10]:
            print(f"  {term}: chunk={chunk_score:.4f}, yt={yt_score:.4f}")
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    
    results.sort(key=lambda x: x[1], reverse=True)
    
    print("\nChunks ranked by similarity to YouTube transcript:")
    for chunk_num, similarity in results:
        print(f"Chunk {chunk_num}: {similarity * 100:.2f}%")
    
    # Also run analysis with N-grams
    print("\n" + "="*70)
    print("ANALYZING CHUNKS WITH TF-IDF + N-GRAMS (1-3)")
    print("="*70)
    
    ngram_results = []
    
    for i, chunk in enumerate(chunks):
        documents = [chunk, doc2_clean]
        
        vectorizer_ngram = TfidfVectorizer(stop_words='english', ngram_range=(1, 3), max_features=10000)
        tfidf_matrix_ngram = vectorizer_ngram.fit_transform(documents)
        
        similarity_ngram = cosine_similarity(tfidf_matrix_ngram[0:1], tfidf_matrix_ngram[1:2])[0][0]
        
        ngram_results.append((i+1, similarity_ngram))
        print(f"Chunk {i+1}: {similarity_ngram * 100:.2f}%")
    
    print("\n" + "="*70)
    print("COMPARISON: WHOLE DOCUMENT vs BEST CHUNK")
    print("="*70)
    
    # Calculate whole document similarity for comparison
    documents_whole = [doc1_clean, doc2_clean]
    vectorizer_whole = TfidfVectorizer(stop_words='english')
    tfidf_matrix_whole = vectorizer_whole.fit_transform(documents_whole)
    similarity_whole = cosine_similarity(tfidf_matrix_whole[0:1], tfidf_matrix_whole[1:2])[0][0]
    
    best_chunk_num, best_similarity = max(results, key=lambda x: x[1])
    
    print(f"\nWhole document similarity: {similarity_whole * 100:.2f}%")
    print(f"Best chunk (Chunk {best_chunk_num}): {best_similarity * 100:.2f}%")
    print(f"Improvement over whole: {(best_similarity - similarity_whole) * 100:.2f} percentage points")

if __name__ == "__main__":
    main()
