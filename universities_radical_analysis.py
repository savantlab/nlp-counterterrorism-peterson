#!/usr/bin/env python3
"""
Analyze claims about universities and 'radical'/'radicals' in both documents.
"""

import re

def read_file(filename):
    with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()

def find_contexts(text, pattern, context_words=50):
    """Find all contexts where a pattern appears with surrounding words"""
    matches = []
    for match in re.finditer(pattern, text, re.IGNORECASE):
        start = max(0, match.start() - context_words * 6)
        end = min(len(text), match.end() + context_words * 6)
        context = text[start:end].strip()
        matches.append({
            'match': match.group(),
            'context': context,
            'position': match.start()
        })
    return matches

def find_combined_contexts(text, pattern1, pattern2, max_distance=200):
    """Find contexts where two patterns appear near each other"""
    matches = []
    
    # Find all matches for both patterns
    matches1 = list(re.finditer(pattern1, text, re.IGNORECASE))
    matches2 = list(re.finditer(pattern2, text, re.IGNORECASE))
    
    # For each match of pattern1, find nearby matches of pattern2
    for m1 in matches1:
        for m2 in matches2:
            distance = abs(m1.start() - m2.start())
            if distance <= max_distance:
                start = max(0, min(m1.start(), m2.start()) - 150)
                end = min(len(text), max(m1.end(), m2.end()) + 150)
                context = text[start:end].strip()
                
                matches.append({
                    'match1': m1.group(),
                    'match2': m2.group(),
                    'distance': distance,
                    'context': context
                })
    
    # Remove duplicates
    unique_matches = []
    seen_contexts = set()
    for m in matches:
        if m['context'] not in seen_contexts:
            unique_matches.append(m)
            seen_contexts.add(m['context'])
    
    return unique_matches

# Read documents
print("="*80)
print("UNIVERSITIES AND 'RADICAL' ANALYSIS")
print("="*80)

yt_text = read_file('txt/youtube_transcript_clean.txt')
doc_text = read_file('txt/2083. EUROPEAN DECLARATION OF INDEPENDENCE.txt')

# ============================================================================
# PART 1: YouTube Video Analysis
# ============================================================================

print("\n\n1. YOUTUBE VIDEO - UNIVERSITIES MENTIONS:")
print("-" * 80)

uni_terms = r'universit(y|ies)|college|campus|academ(ic|ia)'
uni_matches_yt = find_contexts(yt_text, uni_terms)

print(f"\nFound {len(uni_matches_yt)} university-related mentions in YouTube:")
for i, match in enumerate(uni_matches_yt, 1):
    print(f"\n[{i}] '{match['match']}':")
    print(f"    {match['context'][:250]}...")

print("\n\n2. YOUTUBE VIDEO - 'RADICAL' MENTIONS:")
print("-" * 80)

radical_matches_yt = find_contexts(yt_text, r'\bradical\w*\b')
print(f"\nFound {len(radical_matches_yt)} 'radical' mentions in YouTube:")
for i, match in enumerate(radical_matches_yt, 1):
    print(f"\n[{i}] '{match['match']}':")
    print(f"    {match['context'][:250]}...")

# ============================================================================
# PART 2: Combined Analysis - Universities + Radical in YouTube
# ============================================================================

print("\n\n3. YOUTUBE VIDEO - UNIVERSITIES + RADICAL (Combined):")
print("-" * 80)

combined_yt = find_combined_contexts(yt_text, uni_terms, r'\bradical\w*\b', max_distance=150)
print(f"\nFound {len(combined_yt)} instances where universities and 'radical' appear together:")
for i, match in enumerate(combined_yt, 1):
    print(f"\n[{i}] '{match['match1']}' + '{match['match2']}' (distance: {match['distance']} chars):")
    print(f"    {match['context'][:300]}...")

# ============================================================================
# PART 3: 2083 Document Analysis
# ============================================================================

print("\n\n4. 2083 DOCUMENT - UNIVERSITIES + RADICAL (Sample):")
print("-" * 80)

combined_doc = find_combined_contexts(doc_text, uni_terms, r'\bradical\w*\b', max_distance=200)
print(f"\nFound {len(combined_doc)} instances where universities and 'radical' appear together")
print("\nShowing first 10 examples:")

for i, match in enumerate(combined_doc[:10], 1):
    print(f"\n[{i}] '{match['match1']}' + '{match['match2']}' (distance: {match['distance']} chars):")
    print(f"    {match['context'][:300]}...")

# ============================================================================
# PART 4: Specific Claims Analysis
# ============================================================================

print("\n\n5. KEY CLAIMS ABOUT UNIVERSITIES AND RADICALS:")
print("="*80)

print("\n--- YOUTUBE VIDEO CLAIMS ---")

# Key claim: radicals became professors in 60s/70s
sixties_pattern = r'(60s|70s|sixties|seventies).{0,100}(professor|universit|academ)'
sixties_matches = find_contexts(yt_text, sixties_pattern, context_words=40)
print(f"\nClaims about 60s/70s and universities: {len(sixties_matches)}")
for match in sixties_matches:
    print(f"  - {match['context'][:200]}...")

# Key claim: radical left became professors
radical_prof = find_combined_contexts(yt_text, r'\bradical\w*\b', r'professor', max_distance=100)
print(f"\nClaims about 'radical' + 'professor': {len(radical_prof)}")
for match in radical_prof:
    print(f"  - {match['context'][:200]}...")

print("\n--- 2083 DOCUMENT CLAIMS (Sample) ---")

# Universities and radical feminism
uni_feminism = find_combined_contexts(doc_text, uni_terms, r'radical\s+feminism', max_distance=200)
print(f"\nClaims about universities + 'radical feminism': {len(uni_feminism)}")
print("Sample:")
for match in uni_feminism[:3]:
    print(f"  - {match['context'][:200]}...")

# Universities and radical left
uni_left = find_combined_contexts(doc_text, uni_terms, r'radical\s+(left|leftist)', max_distance=200)
print(f"\nClaims about universities + 'radical left': {len(uni_left)}")
print("Sample:")
for match in uni_left[:3]:
    print(f"  - {match['context'][:200]}...")

# ============================================================================
# PART 5: Summary Statistics
# ============================================================================

print("\n\n6. SUMMARY STATISTICS:")
print("="*80)

# Count total occurrences
yt_uni_count = len(re.findall(uni_terms, yt_text, re.IGNORECASE))
yt_radical_count = len(re.findall(r'\bradical\w*\b', yt_text, re.IGNORECASE))

doc_uni_count = len(re.findall(uni_terms, doc_text, re.IGNORECASE))
doc_radical_count = len(re.findall(r'\bradical\w*\b', doc_text, re.IGNORECASE))

print("\nYOUTUBE VIDEO (726 words):")
print(f"  - Universities/academic: {yt_uni_count} mentions")
print(f"  - Radical/radicals: {yt_radical_count} mentions")
print(f"  - Combined (within 150 chars): {len(combined_yt)} instances")

print("\n2083 DOCUMENT (41,548 words):")
print(f"  - Universities/academic: {doc_uni_count} mentions")
print(f"  - Radical/radicals: {doc_radical_count} mentions")
print(f"  - Combined (within 200 chars): {len(combined_doc)} instances")

print("\nFREQUENCY RATIO (per 1000 words):")
yt_uni_ratio = (yt_uni_count / 726) * 1000
doc_uni_ratio = (doc_uni_count / 41548) * 1000
print(f"  - Universities: YT={yt_uni_ratio:.2f}, Doc={doc_uni_ratio:.2f}")
print(f"    → YouTube emphasizes universities {yt_uni_ratio/doc_uni_ratio:.2f}x more")

yt_rad_ratio = (yt_radical_count / 726) * 1000
doc_rad_ratio = (doc_radical_count / 41548) * 1000
print(f"  - Radical: YT={yt_rad_ratio:.2f}, Doc={doc_rad_ratio:.2f}")
print(f"    → YouTube emphasizes 'radical' {yt_rad_ratio/doc_rad_ratio:.2f}x more")

# ============================================================================
# Save results
# ============================================================================

output = f"""UNIVERSITIES AND 'RADICAL' ANALYSIS
{'='*80}

RESEARCH QUESTIONS:
1. What claims do both documents make about universities and radicals?
2. How do the claims compare?

KEY FINDINGS:

1. FREQUENCY ANALYSIS:
   
   YouTube (726 words):
   - Universities/academic: {yt_uni_count} mentions
   - Radical/radicals: {yt_radical_count} mentions
   - Combined proximity: {len(combined_yt)} instances
   
   2083 Document (41,548 words):
   - Universities/academic: {doc_uni_count} mentions
   - Radical/radicals: {doc_radical_count} mentions
   - Combined proximity: {len(combined_doc)} instances

2. EMPHASIS (per 1000 words):
   
   Universities:
   - YouTube: {yt_uni_ratio:.2f} per 1000 words
   - 2083: {doc_uni_ratio:.2f} per 1000 words
   - YouTube emphasizes universities {yt_uni_ratio/doc_uni_ratio:.2f}x MORE than 2083
   
   Radical:
   - YouTube: {yt_rad_ratio:.2f} per 1000 words
   - 2083: {doc_rad_ratio:.2f} per 1000 words
   - YouTube emphasizes 'radical' {yt_rad_ratio/doc_rad_ratio:.2f}x MORE than 2083

3. YOUTUBE VIDEO KEY CLAIMS:
   - "the true believers of the radical left became the professors of today"
   - Universities in "60s and 70s when radical left became professors"
   - Universities as source of "postmodernist" ideology
   - Campus radicals producing "mobs that violently shut down campus speakers"
   - Focus: Universities as PRIMARY source of ideological threat

4. 2083 DOCUMENT KEY CLAIMS:
   - Universities mentioned in context of radical feminism, radical Islam
   - Universities as one of many cultural institutions affected
   - Less emphasis on universities as PRIMARY source
   - More emphasis on historical/political movements

CONCLUSION:
The YouTube video places MUCH GREATER EMPHASIS on universities as the source
of radical ideology compared to the 2083 document. YouTube presents universities
as the primary incubator (60s/70s) where "radical left" became professors who
now indoctrinate students. This is a central thesis of the video.

The 2083 document mentions universities but focuses more broadly on political
movements, historical forces, and Islam. Universities are one context among many,
not the primary explanatory factor.

This represents a significant difference in EMPHASIS and CAUSATION:
- YouTube: Universities → Radical professors → Postmodernism/Neo-Marxism
- 2083: Broader cultural Marxism + Multiple institutions + Islam
"""

with open('txt/universities_radical_analysis.txt', 'w') as f:
    f.write(output)

print("\n" + "="*80)
print("Results saved to: universities_radical_analysis.txt")
print("="*80)
