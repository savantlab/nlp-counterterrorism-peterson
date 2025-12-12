#!/usr/bin/env python3
"""
Find exact phrase matches and extract named entities (people, places, organizations).
"""

import re
from collections import Counter

def clean_text(text):
    """Clean text while preserving case for name recognition."""
    # Remove extra whitespace but keep case
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def extract_names(text):
    """Extract potential person names (capitalized words/phrases)."""
    # Pattern for capitalized words that could be names
    # Look for sequences of 1-3 capitalized words
    name_pattern = r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2})\b'
    matches = re.findall(name_pattern, text)
    
    # Filter out common words that aren't names
    stop_words = {
        'The', 'A', 'An', 'In', 'Of', 'To', 'For', 'And', 'But', 'Or', 'As', 'At',
        'By', 'From', 'On', 'With', 'This', 'That', 'These', 'Those', 'Is', 'Are',
        'Was', 'Were', 'Be', 'Been', 'Being', 'Have', 'Has', 'Had', 'Do', 'Does',
        'Did', 'Will', 'Would', 'Could', 'Should', 'May', 'Might', 'Must', 'Can',
        'He', 'She', 'It', 'They', 'We', 'You', 'I', 'My', 'Your', 'His', 'Her',
        'Their', 'Our', 'Its', 'When', 'Where', 'Why', 'How', 'What', 'Which',
        'Who', 'Whom', 'Whose', 'English', 'European', 'Europeans', 'Christian',
        'Christians', 'Muslim', 'Muslims', 'Islamic', 'Western', 'Eastern',
        'Northern', 'Southern', 'American', 'British', 'French', 'German',
        'National', 'Political', 'Cultural', 'Social', 'Economic', 'Book'
    }
    
    names = [name for name in matches if name not in stop_words]
    return names

def find_exact_phrases(doc_text, yt_text, min_words=4, max_words=10):
    """Find exact phrase matches of varying lengths."""
    doc_lower = doc_text.lower()
    yt_lower = yt_text.lower()
    
    # Split into sentences for context
    yt_sentences = re.split(r'[.!?]+', yt_text)
    
    matches = []
    
    # For each sentence in YT transcript
    for sentence in yt_sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
            
        words = sentence.lower().split()
        
        # Try different phrase lengths
        for phrase_len in range(max_words, min_words - 1, -1):
            for i in range(len(words) - phrase_len + 1):
                phrase = ' '.join(words[i:i + phrase_len])
                
                # Check if this exact phrase appears in document
                if phrase in doc_lower:
                    # Get context from document
                    idx = doc_lower.find(phrase)
                    context_start = max(0, idx - 50)
                    context_end = min(len(doc_text), idx + len(phrase) + 50)
                    doc_context = doc_text[context_start:context_end].strip()
                    
                    matches.append({
                        'phrase': phrase,
                        'length': phrase_len,
                        'yt_sentence': sentence,
                        'doc_context': doc_context
                    })
                    break  # Found match at this position, move to next position
    
    return matches

def main():
    # Read documents
    print("Loading documents...")
    with open('2083. EUROPEAN DECLARATION OF INDEPENDENCE.txt', 'r', encoding='utf-8', errors='ignore') as f:
        doc_text = f.read()
    
    with open('youtube_transcript_clean.txt', 'r', encoding='utf-8', errors='ignore') as f:
        yt_text = f.read()
    
    print("\n" + "="*70)
    print("NAMED ENTITY EXTRACTION")
    print("="*70)
    
    # Extract names from both documents
    doc_names = extract_names(doc_text)
    yt_names = extract_names(yt_text)
    
    doc_name_counts = Counter(doc_names)
    yt_name_counts = Counter(yt_names)
    
    print(f"\nPotential names in document: {len(set(doc_names)):,} unique")
    print(f"Potential names in YT transcript: {len(set(yt_names)):,} unique")
    
    # Names in YT transcript
    print("\n--- Names mentioned in YouTube transcript (frequency > 1): ---")
    for name, count in yt_name_counts.most_common(30):
        if count > 1:
            in_doc = "✓" if name in doc_name_counts else "✗"
            doc_count = doc_name_counts.get(name, 0)
            print(f"  {name}: YT={count}, Doc={doc_count} [{in_doc}]")
    
    # Common names
    common_names = set(yt_name_counts.keys()) & set(doc_name_counts.keys())
    print(f"\n--- Names appearing in BOTH documents ({len(common_names)}): ---")
    common_sorted = sorted([(name, yt_name_counts[name], doc_name_counts[name]) 
                           for name in common_names], 
                          key=lambda x: x[1], reverse=True)
    
    for name, yt_count, doc_count in common_sorted[:20]:
        print(f"  {name}: YT={yt_count}, Doc={doc_count}")
    
    # Key people mentioned
    print("\n--- Key figures (mentioned 10+ times in document): ---")
    key_people = [name for name, count in doc_name_counts.most_common(30) if count >= 10]
    for name in key_people[:15]:
        yt_count = yt_name_counts.get(name, 0)
        in_yt = "✓" if yt_count > 0 else "✗"
        print(f"  {name}: Doc={doc_name_counts[name]}, YT={yt_count} [{in_yt}]")
    
    print("\n" + "="*70)
    print("EXACT PHRASE MATCHING")
    print("="*70)
    
    print("\nSearching for exact phrase matches (4+ words)...")
    matches = find_exact_phrases(doc_text, yt_text, min_words=4, max_words=15)
    
    # Remove duplicates and sort by length
    unique_matches = {}
    for match in matches:
        phrase = match['phrase']
        if phrase not in unique_matches or match['length'] > unique_matches[phrase]['length']:
            unique_matches[phrase] = match
    
    sorted_matches = sorted(unique_matches.values(), key=lambda x: x['length'], reverse=True)
    
    print(f"\nFound {len(sorted_matches)} unique exact phrase matches")
    
    if sorted_matches:
        print("\n--- Longest exact phrase matches: ---")
        for i, match in enumerate(sorted_matches[:20], 1):
            print(f"\n{i}. [{match['length']} words] \"{match['phrase']}\"")
            print(f"   YT context: ...{match['yt_sentence'][:100]}...")
            print(f"   Doc context: ...{match['doc_context'][:100]}...")
    else:
        print("\nNo exact phrase matches found (4+ words)")
    
    # Look for shorter exact matches (3 words)
    print("\n--- Common 3-word exact phrases: ---")
    matches_3word = find_exact_phrases(doc_text, yt_text, min_words=3, max_words=3)
    
    phrase_counts = Counter([m['phrase'] for m in matches_3word])
    for phrase, count in phrase_counts.most_common(20):
        print(f"  \"{phrase}\"")
    
    # Specific searches for key concepts from YT transcript
    print("\n" + "="*70)
    print("CONCEPT SEARCH")
    print("="*70)
    
    key_phrases = [
        "political correctness",
        "cultural marxism",
        "post modernist",
        "postmodernist",
        "diversity equity and inclusion",
        "frankfurt school",
        "western civilization",
        "freedom of speech",
        "jordan peterson"
    ]
    
    doc_lower = doc_text.lower()
    yt_lower = yt_text.lower()
    
    print("\nSearching for key concepts:")
    for phrase in key_phrases:
        in_doc = phrase in doc_lower
        in_yt = phrase in yt_lower
        
        if in_doc:
            doc_count = doc_lower.count(phrase)
        else:
            doc_count = 0
            
        if in_yt:
            yt_count = yt_lower.count(phrase)
        else:
            yt_count = 0
        
        status = ""
        if in_doc and in_yt:
            status = "✓✓ BOTH"
        elif in_doc:
            status = "✓  DOC ONLY"
        elif in_yt:
            status = "  ✓ YT ONLY"
        else:
            status = "✗  NEITHER"
            
        print(f"  {phrase:40} {status:12} (Doc: {doc_count:3}, YT: {yt_count:2})")

if __name__ == "__main__":
    main()
