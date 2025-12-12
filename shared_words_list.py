#!/usr/bin/env python3
"""
Extract all words shared between documents (excluding stop words).
"""

import re
from collections import Counter

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

def preprocess_text(text):
    """Clean and tokenize text."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    tokens = text.split()
    # Remove stop words and short words
    tokens = [t for t in tokens if t not in STOP_WORDS and len(t) > 2]
    return tokens

def main():
    # Read documents
    print("Loading documents...")
    with open('2083. EUROPEAN DECLARATION OF INDEPENDENCE.txt', 'r', encoding='utf-8', errors='ignore') as f:
        doc_text = f.read()
    
    with open('youtube_transcript_clean.txt', 'r', encoding='utf-8', errors='ignore') as f:
        yt_text = f.read()
    
    print("Preprocessing...")
    doc_tokens = preprocess_text(doc_text)
    yt_tokens = preprocess_text(yt_text)
    
    # Get frequency counts
    doc_freq = Counter(doc_tokens)
    yt_freq = Counter(yt_tokens)
    
    # Find common words
    doc_vocab = set(doc_tokens)
    yt_vocab = set(yt_tokens)
    common_words = doc_vocab & yt_vocab
    
    print(f"\nTotal content words in Document: {len(doc_vocab):,}")
    print(f"Total content words in YouTube: {len(yt_vocab):,}")
    print(f"Shared content words: {len(common_words):,}")
    print(f"Overlap: {len(common_words) / len(yt_vocab) * 100:.1f}% of YT vocabulary")
    
    # Sort by YouTube frequency (most important to the YT video)
    common_sorted_yt = sorted(
        [(word, yt_freq[word], doc_freq[word]) for word in common_words],
        key=lambda x: x[1],
        reverse=True
    )
    
    # Sort by document frequency
    common_sorted_doc = sorted(
        [(word, yt_freq[word], doc_freq[word]) for word in common_words],
        key=lambda x: x[2],
        reverse=True
    )
    
    # Sort alphabetically
    common_sorted_alpha = sorted(common_words)
    
    # Write to files
    print("\nWriting results to files...")
    
    # 1. Sorted by YT frequency
    with open('shared_words_by_yt_frequency.txt', 'w') as f:
        f.write("SHARED WORDS SORTED BY YOUTUBE TRANSCRIPT FREQUENCY\n")
        f.write("="*70 + "\n\n")
        f.write(f"Total: {len(common_words)} words\n\n")
        f.write(f"{'Word':<20} {'YT Freq':>10} {'Doc Freq':>10}\n")
        f.write("-"*70 + "\n")
        for word, yt_f, doc_f in common_sorted_yt:
            f.write(f"{word:<20} {yt_f:>10} {doc_f:>10}\n")
    
    print("✓ Created: shared_words_by_yt_frequency.txt")
    
    # 2. Sorted by document frequency
    with open('shared_words_by_doc_frequency.txt', 'w') as f:
        f.write("SHARED WORDS SORTED BY DOCUMENT FREQUENCY\n")
        f.write("="*70 + "\n\n")
        f.write(f"Total: {len(common_words)} words\n\n")
        f.write(f"{'Word':<20} {'YT Freq':>10} {'Doc Freq':>10}\n")
        f.write("-"*70 + "\n")
        for word, yt_f, doc_f in common_sorted_doc:
            f.write(f"{word:<20} {yt_f:>10} {doc_f:>10}\n")
    
    print("✓ Created: shared_words_by_doc_frequency.txt")
    
    # 3. Alphabetical list
    with open('shared_words_alphabetical.txt', 'w') as f:
        f.write("SHARED WORDS - ALPHABETICAL LIST\n")
        f.write("="*70 + "\n\n")
        f.write(f"Total: {len(common_words)} words\n\n")
        for word in common_sorted_alpha:
            f.write(f"{word}\n")
    
    print("✓ Created: shared_words_alphabetical.txt")
    
    # 4. Summary with statistics
    with open('shared_words_summary.txt', 'w') as f:
        f.write("SHARED VOCABULARY ANALYSIS SUMMARY\n")
        f.write("="*70 + "\n\n")
        
        f.write("STATISTICS:\n")
        f.write(f"  Document unique content words: {len(doc_vocab):,}\n")
        f.write(f"  YouTube unique content words: {len(yt_vocab):,}\n")
        f.write(f"  Shared content words: {len(common_words):,}\n")
        f.write(f"  YouTube vocabulary coverage: {len(common_words) / len(yt_vocab) * 100:.1f}%\n")
        f.write(f"  Document vocabulary coverage: {len(common_words) / len(doc_vocab) * 100:.1f}%\n\n")
        
        f.write("TOP 50 SHARED WORDS (by YouTube importance):\n")
        f.write("-"*70 + "\n")
        f.write(f"{'Word':<20} {'YT Freq':>10} {'Doc Freq':>10}\n")
        f.write("-"*70 + "\n")
        for word, yt_f, doc_f in common_sorted_yt[:50]:
            f.write(f"{word:<20} {yt_f:>10} {doc_f:>10}\n")
        
        f.write("\n\nTOP 50 SHARED WORDS (by Document importance):\n")
        f.write("-"*70 + "\n")
        f.write(f"{'Word':<20} {'YT Freq':>10} {'Doc Freq':>10}\n")
        f.write("-"*70 + "\n")
        for word, yt_f, doc_f in common_sorted_doc[:50]:
            f.write(f"{word:<20} {yt_f:>10} {doc_f:>10}\n")
    
    print("✓ Created: shared_words_summary.txt")
    
    print("\n" + "="*70)
    print("DONE! Created 4 files:")
    print("  1. shared_words_by_yt_frequency.txt - Sorted by YouTube importance")
    print("  2. shared_words_by_doc_frequency.txt - Sorted by Document importance")
    print("  3. shared_words_alphabetical.txt - Simple alphabetical list")
    print("  4. shared_words_summary.txt - Overview with top 50 from each")
    print("="*70)

if __name__ == "__main__":
    main()
