#!/usr/bin/env python3
"""
Deep analysis of Chunk 2 (the best matching chunk) vs YouTube transcript.
Provides detailed breakdown of similarities and differences.
"""

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter
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
            chunk = ' '.join(words[start_idx:])
        else:
            end_idx = (i + 1) * chunk_size
            chunk = ' '.join(words[start_idx:end_idx])
        chunks.append(chunk)
    
    return chunks

def generate_ngrams(tokens, n):
    """Generate n-grams from token list."""
    ngrams = []
    for i in range(len(tokens) - n + 1):
        ngram = ' '.join(tokens[i:i+n])
        ngrams.append(ngram)
    return ngrams

def main():
    # Read documents
    print("Loading documents...")
    with open('2083. EUROPEAN DECLARATION OF INDEPENDENCE.txt', 'r', encoding='utf-8', errors='ignore') as f:
        doc1_text = f.read()
    
    with open('youtube_transcript_clean.txt', 'r', encoding='utf-8', errors='ignore') as f:
        doc2_text = f.read()
    
    print("Preprocessing documents...")
    doc1_clean = preprocess_text(doc1_text)
    doc2_clean = preprocess_text(doc2_text)
    
    # Get chunk 2
    chunks = split_into_chunks(doc1_clean, num_chunks=4)
    chunk2 = chunks[1]  # Index 1 is chunk 2
    
    print("\n" + "="*70)
    print("CHUNK 2 DETAILED ANALYSIS")
    print("="*70)
    
    # Basic stats
    chunk2_words = chunk2.split()
    yt_words = doc2_clean.split()
    
    print(f"\nChunk 2: {len(chunk2_words):,} words")
    print(f"YouTube Transcript: {len(yt_words):,} words")
    
    # Multiple similarity measures
    documents = [chunk2, doc2_clean]
    
    print("\n" + "="*70)
    print("SIMILARITY SCORES")
    print("="*70)
    
    # 1. TF-IDF with stop words
    vectorizer_tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer_tfidf.fit_transform(documents)
    tfidf_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    print(f"\n1. TF-IDF (stop words removed):           {tfidf_sim * 100:.2f}%")
    
    # 2. TF-IDF with bigrams
    vectorizer_bigram = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
    bigram_matrix = vectorizer_bigram.fit_transform(documents)
    bigram_sim = cosine_similarity(bigram_matrix[0:1], bigram_matrix[1:2])[0][0]
    print(f"2. TF-IDF with bigrams:                   {bigram_sim * 100:.2f}%")
    
    # 3. TF-IDF with trigrams
    vectorizer_trigram = TfidfVectorizer(stop_words='english', ngram_range=(1, 3))
    trigram_matrix = vectorizer_trigram.fit_transform(documents)
    trigram_sim = cosine_similarity(trigram_matrix[0:1], trigram_matrix[1:2])[0][0]
    print(f"3. TF-IDF with trigrams:                  {trigram_sim * 100:.2f}%")
    
    # 4. Bag of words (no stop words)
    chunk2_nostop = [w for w in chunk2_words if len(w) > 2]
    yt_nostop = [w for w in yt_words if len(w) > 2]
    
    chunk2_vocab = set(chunk2_nostop)
    yt_vocab = set(yt_nostop)
    
    common = chunk2_vocab & yt_vocab
    jaccard = len(common) / len(chunk2_vocab | yt_vocab)
    vocab_overlap = len(common) / len(yt_vocab)
    
    print(f"4. Jaccard similarity (vocabulary):       {jaccard * 100:.2f}%")
    print(f"5. YouTube vocab coverage by Chunk 2:     {vocab_overlap * 100:.2f}%")
    
    print("\n" + "="*70)
    print("VOCABULARY ANALYSIS")
    print("="*70)
    
    print(f"\nUnique terms in Chunk 2: {len(chunk2_vocab):,}")
    print(f"Unique terms in YT transcript: {len(yt_vocab):,}")
    print(f"Common terms: {len(common):,}")
    
    # Top terms analysis
    feature_names = vectorizer_tfidf.get_feature_names_out()
    chunk_vector = tfidf_matrix[0].toarray()[0]
    yt_vector = tfidf_matrix[1].toarray()[0]
    
    # Terms unique to YT (high TF-IDF in YT, zero in chunk)
    yt_unique = []
    for idx, term in enumerate(feature_names):
        if yt_vector[idx] > 0.05 and chunk_vector[idx] == 0:
            yt_unique.append((term, yt_vector[idx]))
    
    yt_unique.sort(key=lambda x: x[1], reverse=True)
    
    print("\n--- Key terms in YT transcript NOT in Chunk 2: ---")
    for term, score in yt_unique[:15]:
        print(f"  {term}: {score:.4f}")
    
    # High scoring shared terms
    shared_high = []
    for idx, term in enumerate(feature_names):
        if yt_vector[idx] > 0 and chunk_vector[idx] > 0:
            avg_score = (yt_vector[idx] + chunk_vector[idx]) / 2
            shared_high.append((term, chunk_vector[idx], yt_vector[idx], avg_score))
    
    shared_high.sort(key=lambda x: x[3], reverse=True)
    
    print("\n--- Top 20 shared terms (by average TF-IDF): ---")
    for term, chunk_score, yt_score, avg in shared_high[:20]:
        print(f"  {term}: chunk={chunk_score:.4f}, yt={yt_score:.4f}, avg={avg:.4f}")
    
    # N-gram analysis
    print("\n" + "="*70)
    print("N-GRAM ANALYSIS")
    print("="*70)
    
    # Bigrams
    chunk2_bigrams = generate_ngrams(chunk2_words, 2)
    yt_bigrams = generate_ngrams(yt_words, 2)
    
    chunk2_bigram_set = set(chunk2_bigrams)
    yt_bigram_set = set(yt_bigrams)
    common_bigrams = chunk2_bigram_set & yt_bigram_set
    
    print(f"\nBigrams in Chunk 2: {len(chunk2_bigram_set):,}")
    print(f"Bigrams in YT: {len(yt_bigram_set):,}")
    print(f"Common bigrams: {len(common_bigrams):,}")
    print(f"Bigram overlap: {len(common_bigrams) / len(yt_bigram_set) * 100:.1f}%")
    
    # Top common bigrams
    yt_bigram_freq = Counter(yt_bigrams)
    common_bigram_freq = [(bg, yt_bigram_freq[bg]) for bg in common_bigrams]
    common_bigram_freq.sort(key=lambda x: x[1], reverse=True)
    
    print("\nTop 15 common bigrams (by YT frequency):")
    for bigram, freq in common_bigram_freq[:15]:
        print(f"  '{bigram}': {freq}")
    
    # Trigrams
    chunk2_trigrams = generate_ngrams(chunk2_words, 3)
    yt_trigrams = generate_ngrams(yt_words, 3)
    
    chunk2_trigram_set = set(chunk2_trigrams)
    yt_trigram_set = set(yt_trigrams)
    common_trigrams = chunk2_trigram_set & yt_trigram_set
    
    print(f"\nTrigrams in Chunk 2: {len(chunk2_trigram_set):,}")
    print(f"Trigrams in YT: {len(yt_trigram_set):,}")
    print(f"Common trigrams: {len(common_trigrams):,}")
    print(f"Trigram overlap: {len(common_trigrams) / len(yt_trigram_set) * 100:.1f}%")
    
    # Top common trigrams
    yt_trigram_freq = Counter(yt_trigrams)
    common_trigram_freq = [(tg, yt_trigram_freq[tg]) for tg in common_trigrams]
    common_trigram_freq.sort(key=lambda x: x[1], reverse=True)
    
    print("\nTop 15 common trigrams (by YT frequency):")
    for trigram, freq in common_trigram_freq[:15]:
        print(f"  '{trigram}': {freq}")
    
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"""
Chunk 2 shows moderate similarity to the YouTube transcript:
- Lexical similarity (TF-IDF): {tfidf_sim * 100:.1f}%
- Phrase similarity (bigrams): {bigram_sim * 100:.1f}%  
- Phrase similarity (trigrams): {trigram_sim * 100:.1f}%
- Vocabulary coverage: {vocab_overlap * 100:.1f}% of YT terms appear in Chunk 2

Key missing terms suggest the YT transcript uses vocabulary
not heavily present in Chunk 2, indicating topical differences.
""")

if __name__ == "__main__":
    main()
