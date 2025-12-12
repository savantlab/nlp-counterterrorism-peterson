#!/usr/bin/env python3
"""
Quick similarity analysis for truncated YouTube transcript (before Hobbes).
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from collections import Counter

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
    
    with open('youtube_transcript_before_hobbes.txt', 'r', encoding='utf-8', errors='ignore') as f:
        yt_truncated = f.read()
    
    with open('youtube_transcript_clean.txt', 'r', encoding='utf-8', errors='ignore') as f:
        yt_full = f.read()
    
    print("\n" + "="*70)
    print("COMPARISON: FULL vs TRUNCATED YOUTUBE TRANSCRIPT")
    print("="*70)
    
    # Basic stats
    yt_full_words = len(yt_full.split())
    yt_truncated_words = len(yt_truncated.split())
    
    print(f"\nFull transcript: {yt_full_words} words")
    print(f"Truncated (before Hobbes): {yt_truncated_words} words")
    print(f"Reduction: {yt_full_words - yt_truncated_words} words ({(1 - yt_truncated_words/yt_full_words)*100:.1f}%)")
    
    # Preprocess
    doc_clean = preprocess_text(doc_text)
    yt_truncated_clean = preprocess_text(yt_truncated)
    yt_full_clean = preprocess_text(yt_full)
    
    print("\n" + "="*70)
    print("TF-IDF SIMILARITY SCORES")
    print("="*70)
    
    # Full transcript similarity
    print("\n--- Full YouTube Transcript ---")
    vectorizer_full = TfidfVectorizer(stop_words='english')
    tfidf_full = vectorizer_full.fit_transform([doc_clean, yt_full_clean])
    similarity_full = cosine_similarity(tfidf_full[0:1], tfidf_full[1:2])[0][0]
    print(f"TF-IDF Similarity: {similarity_full:.6f} ({similarity_full * 100:.2f}%)")
    
    # Truncated transcript similarity
    print("\n--- Truncated YouTube Transcript (before Hobbes) ---")
    vectorizer_trunc = TfidfVectorizer(stop_words='english')
    tfidf_trunc = vectorizer_trunc.fit_transform([doc_clean, yt_truncated_clean])
    similarity_trunc = cosine_similarity(tfidf_trunc[0:1], tfidf_trunc[1:2])[0][0]
    print(f"TF-IDF Similarity: {similarity_trunc:.6f} ({similarity_trunc * 100:.2f}%)")
    
    print(f"\nDifference: {(similarity_full - similarity_trunc) * 100:.2f} percentage points")
    
    # Vocabulary analysis
    print("\n" + "="*70)
    print("VOCABULARY ANALYSIS")
    print("="*70)
    
    doc_tokens = [w for w in doc_clean.split() if len(w) > 2]
    yt_full_tokens = [w for w in yt_full_clean.split() if len(w) > 2]
    yt_trunc_tokens = [w for w in yt_truncated_clean.split() if len(w) > 2]
    
    doc_vocab = set(doc_tokens)
    yt_full_vocab = set(yt_full_tokens)
    yt_trunc_vocab = set(yt_trunc_tokens)
    
    common_full = doc_vocab & yt_full_vocab
    common_trunc = doc_vocab & yt_trunc_vocab
    
    print(f"\nFull transcript unique terms: {len(yt_full_vocab)}")
    print(f"Truncated unique terms: {len(yt_trunc_vocab)}")
    print(f"\nCommon with document (full): {len(common_full)} ({len(common_full)/len(yt_full_vocab)*100:.1f}%)")
    print(f"Common with document (truncated): {len(common_trunc)} ({len(common_trunc)/len(yt_trunc_vocab)*100:.1f}%)")
    
    # Terms unique to the second half (after Hobbes)
    second_half_vocab = yt_full_vocab - yt_trunc_vocab
    print(f"\nTerms unique to second half (after Hobbes): {len(second_half_vocab)}")
    print("Sample of second half terms:")
    print(list(second_half_vocab)[:30])
    
    # Top terms in truncated version
    feature_names = vectorizer_trunc.get_feature_names_out()
    trunc_vector = tfidf_trunc[1].toarray()[0]
    doc_vector = tfidf_trunc[0].toarray()[0]
    
    trunc_scores = [(feature_names[i], trunc_vector[i], doc_vector[i]) 
                    for i in range(len(feature_names)) if trunc_vector[i] > 0]
    trunc_scores.sort(key=lambda x: x[1], reverse=True)
    
    print("\n" + "="*70)
    print("TOP 20 TERMS IN TRUNCATED TRANSCRIPT (by TF-IDF)")
    print("="*70)
    print(f"{'Term':<20} {'Truncated':>12} {'Document':>12} {'In Doc?':>10}")
    print("-"*70)
    for term, trunc_score, doc_score in trunc_scores[:20]:
        in_doc = "✓" if doc_score > 0 else "✗"
        print(f"{term:<20} {trunc_score:>12.6f} {doc_score:>12.6f} {in_doc:>10}")
    
    # N-gram analysis
    print("\n" + "="*70)
    print("N-GRAM ANALYSIS")
    print("="*70)
    
    # Truncated with n-grams
    vectorizer_ngram = TfidfVectorizer(stop_words='english', ngram_range=(1, 3), max_features=10000)
    tfidf_ngram = vectorizer_ngram.fit_transform([doc_clean, yt_truncated_clean])
    similarity_ngram = cosine_similarity(tfidf_ngram[0:1], tfidf_ngram[1:2])[0][0]
    
    print(f"\nTruncated with N-grams (1-3): {similarity_ngram * 100:.2f}%")
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"""
Truncated transcript (before "Hobbes"):
- Words: {yt_truncated_words} (vs {yt_full_words} full)
- Unique terms: {len(yt_trunc_vocab)} (vs {len(yt_full_vocab)} full)
- TF-IDF similarity: {similarity_trunc * 100:.2f}% (vs {similarity_full * 100:.2f}% full)
- Vocabulary overlap: {len(common_trunc)/len(yt_trunc_vocab)*100:.1f}%

The truncated version {"increases" if similarity_trunc > similarity_full else "decreases"} similarity by {abs(similarity_full - similarity_trunc) * 100:.2f} percentage points.
This suggests the content {"before" if similarity_trunc > similarity_full else "after"} Hobbes is {"more" if similarity_trunc > similarity_full else "less"} aligned with the document.
""")

if __name__ == "__main__":
    main()
