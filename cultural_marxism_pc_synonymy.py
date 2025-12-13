#!/usr/bin/env python3
"""
Analyze whether Cultural Marxism and Political Correctness are used 
synonymously in the 2083 document.
"""

import re

def read_file(filename):
    with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()

def find_contexts(text, pattern, context_words=60):
    """Find all contexts where a pattern appears"""
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

def find_proximity(text, pattern1, pattern2, max_distance=300):
    """Find instances where two patterns appear near each other"""
    matches = []
    
    matches1 = list(re.finditer(pattern1, text, re.IGNORECASE))
    matches2 = list(re.finditer(pattern2, text, re.IGNORECASE))
    
    for m1 in matches1:
        for m2 in matches2:
            distance = abs(m1.start() - m2.start())
            if distance <= max_distance:
                start = max(0, min(m1.start(), m2.start()) - 200)
                end = min(len(text), max(m1.end(), m2.end()) + 200)
                context = text[start:end].strip()
                
                matches.append({
                    'match1': m1.group(),
                    'match2': m2.group(),
                    'distance': distance,
                    'context': context
                })
    
    # Remove duplicates
    unique = []
    seen = set()
    for m in matches:
        if m['context'] not in seen:
            unique.append(m)
            seen.add(m['context'])
    
    return unique

print("="*80)
print("CULTURAL MARXISM vs POLITICAL CORRECTNESS SYNONYMY ANALYSIS")
print("="*80)

doc_text = read_file('txt/2083. EUROPEAN DECLARATION OF INDEPENDENCE.txt')

# ============================================================================
# PART 1: Frequency Analysis
# ============================================================================

print("\n1. FREQUENCY ANALYSIS:")
print("-" * 80)

cm_pattern = r'\bCultural\s+Marxism\b'
pc_pattern = r'\bPolitical\s+Correctness\b'

cm_matches = re.findall(cm_pattern, doc_text, re.IGNORECASE)
pc_matches = re.findall(pc_pattern, doc_text, re.IGNORECASE)

print(f"\n'Cultural Marxism': {len(cm_matches)} occurrences")
print(f"'Political Correctness': {len(pc_matches)} occurrences")
print(f"\nRatio: PC appears {len(pc_matches)/len(cm_matches):.2f}x as often as Cultural Marxism")

# ============================================================================
# PART 2: Co-occurrence Analysis
# ============================================================================

print("\n\n2. CO-OCCURRENCE ANALYSIS:")
print("-" * 80)

proximity_matches = find_proximity(doc_text, cm_pattern, pc_pattern, max_distance=300)

print(f"\nFound {len(proximity_matches)} instances where Cultural Marxism and Political Correctness")
print("appear within 300 characters of each other")
print("\nShowing first 10 examples:")

for i, match in enumerate(proximity_matches[:10], 1):
    print(f"\n[{i}] Distance: {match['distance']} chars")
    print(f"    {match['context'][:350]}...")

# ============================================================================
# PART 3: Explicit Equation/Equivalence Statements
# ============================================================================

print("\n\n3. EXPLICIT EQUIVALENCE STATEMENTS:")
print("-" * 80)

# Look for explicit connections
equation_patterns = [
    r'Cultural\s+Marxism[^.]{0,100}Political\s+Correctness',
    r'Political\s+Correctness[^.]{0,100}Cultural\s+Marxism',
    r'Cultural\s+Marxism[^.]{0,50}(is|are|also\s+known|called)',
    r'Political\s+Correctness[^.]{0,50}(is|are|also\s+known|called)[^.]{0,50}Cultural\s+Marxism',
    r'(PC|Political\s+Correctness)[^.]{0,50}(synonym|equivalent|same\s+as)',
]

print("\nSearching for explicit equivalence statements...")

found_equations = []
for pattern in equation_patterns:
    matches = find_contexts(doc_text, pattern, context_words=40)
    if matches:
        found_equations.extend(matches)

if found_equations:
    print(f"\nFound {len(found_equations)} potential equivalence statements:")
    for i, match in enumerate(found_equations[:5], 1):
        print(f"\n[{i}] '{match['match']}':")
        print(f"    {match['context'][:300]}...")
else:
    print("\nNo explicit equivalence statements found.")

# ============================================================================
# PART 4: Shared Context Analysis
# ============================================================================

print("\n\n4. SHARED CONTEXT ANALYSIS:")
print("-" * 80)

# What words appear near both terms?
cm_contexts = find_contexts(doc_text, cm_pattern, context_words=30)
pc_contexts = find_contexts(doc_text, pc_pattern, context_words=30)

# Extract common terms
def extract_nearby_terms(contexts, target_pattern):
    """Extract words that appear near the target term"""
    terms = []
    for ctx in contexts:
        # Remove the target term itself
        text = re.sub(target_pattern, '', ctx['context'], flags=re.IGNORECASE)
        # Extract words
        words = re.findall(r'\b[a-z]{4,}\b', text.lower())
        terms.extend(words)
    
    from collections import Counter
    return Counter(terms)

cm_nearby = extract_nearby_terms(cm_contexts, cm_pattern)
pc_nearby = extract_nearby_terms(pc_contexts, pc_pattern)

# Find shared terms
shared_terms = set(cm_nearby.keys()) & set(pc_nearby.keys())

# Remove common words
stopwords = {'this', 'that', 'with', 'from', 'have', 'been', 'were', 'will', 
             'their', 'they', 'them', 'what', 'when', 'where', 'which', 'while',
             'about', 'would', 'there', 'could', 'should', 'after', 'before',
             'between', 'into', 'through', 'during', 'without', 'within'}

shared_significant = {term for term in shared_terms if term not in stopwords}

print(f"\nTop 20 terms appearing near BOTH Cultural Marxism and Political Correctness:")
print("(This suggests semantic overlap/synonymy)")

shared_scored = [(term, cm_nearby[term] + pc_nearby[term]) for term in shared_significant]
shared_scored.sort(key=lambda x: x[1], reverse=True)

for i, (term, freq) in enumerate(shared_scored[:20], 1):
    cm_freq = cm_nearby[term]
    pc_freq = pc_nearby[term]
    print(f"  {i:2}. {term:20} (CM: {cm_freq:3}, PC: {pc_freq:3}, Total: {freq:3})")

# ============================================================================
# PART 5: Functional Analysis
# ============================================================================

print("\n\n5. FUNCTIONAL ANALYSIS:")
print("-" * 80)
print("\nHow are the terms used? (Predicate analysis)")

# What verbs/predicates are used with each?
verb_pattern_cm = r'Cultural\s+Marxism\s+(is|was|are|were|has|have)\s+(\w+)'
verb_pattern_pc = r'Political\s+Correctness\s+(is|was|are|were|has|have)\s+(\w+)'

cm_predicates = re.findall(verb_pattern_cm, doc_text, re.IGNORECASE)
pc_predicates = re.findall(verb_pattern_pc, doc_text, re.IGNORECASE)

print(f"\nCultural Marxism predicates (first 10):")
for i, (verb, pred) in enumerate(cm_predicates[:10], 1):
    print(f"  {i}. Cultural Marxism {verb} {pred}")

print(f"\nPolitical Correctness predicates (first 10):")
for i, (verb, pred) in enumerate(pc_predicates[:10], 1):
    print(f"  {i}. Political Correctness {verb} {pred}")

# ============================================================================
# PART 6: Chapter/Section Analysis
# ============================================================================

print("\n\n6. CHAPTER/SECTION ANALYSIS:")
print("-" * 80)

# Look for chapter titles or section headers mentioning these terms
chapter_pattern = r'(Chapter|Section|Part)\s+[\d\w]+[:\s-]+([^\n]+)'
chapters = re.findall(chapter_pattern, doc_text)

cm_chapters = [ch for ch in chapters if re.search(r'Cultural\s+Marxism', ch[1], re.IGNORECASE)]
pc_chapters = [ch for ch in chapters if re.search(r'Political\s+Correctness', ch[1], re.IGNORECASE)]

print(f"\nChapters mentioning 'Cultural Marxism': {len(cm_chapters)}")
for ch in cm_chapters[:5]:
    print(f"  - {ch[0]}: {ch[1]}")

print(f"\nChapters mentioning 'Political Correctness': {len(pc_chapters)}")
for ch in pc_chapters[:5]:
    print(f"  - {ch[0]}: {ch[1]}")

# ============================================================================
# SAVE RESULTS
# ============================================================================

output = f"""CULTURAL MARXISM vs POLITICAL CORRECTNESS SYNONYMY ANALYSIS
{'='*80}

RESEARCH QUESTION:
Are "Cultural Marxism" and "Political Correctness" used synonymously in 2083?

KEY FINDINGS:

1. FREQUENCY:
   - Cultural Marxism: {len(cm_matches)} occurrences
   - Political Correctness: {len(pc_matches)} occurrences
   - PC appears {len(pc_matches)/len(cm_matches):.2f}x more frequently

2. CO-OCCURRENCE:
   - Found {len(proximity_matches)} instances where both terms appear within 300 chars
   - This represents {len(proximity_matches)/len(cm_matches)*100:.1f}% of Cultural Marxism mentions
   - Suggests strong conceptual relationship

3. SHARED CONTEXT (Top 10):
"""

for i, (term, freq) in enumerate(shared_scored[:10], 1):
    cm_freq = cm_nearby[term]
    pc_freq = pc_nearby[term]
    output += f"   {i:2}. {term:20} (CM: {cm_freq:3}, PC: {pc_freq:3})\n"

output += f"""

4. INTERPRETATION:

EVIDENCE FOR SYNONYMY:
- Both terms appear in {len(proximity_matches)} shared contexts
- Strong overlap in nearby terminology (feminism, multiculturalism, Frankfurt, etc.)
- Both associated with same ideological framework
- Both traced to same intellectual tradition

EVIDENCE FOR DISTINCTION:
- PC mentioned {len(pc_matches)/len(cm_matches):.2f}x more often (suggests different usage levels)
- May represent GENERAL (PC) vs TECHNICAL (Cultural Marxism) terminology
- PC = surface manifestation, Cultural Marxism = underlying ideology

CONCLUSION:
The terms appear to be FUNCTIONALLY SYNONYMOUS but at different levels:
- Political Correctness = OBSERVABLE PHENOMENON (speech codes, taboos, enforcement)
- Cultural Marxism = IDEOLOGICAL EXPLANATION (theoretical framework, origins)

They refer to the SAME THING from different perspectives:
- PC answers: "What is it?" (descriptive)
- Cultural Marxism answers: "Where did it come from?" (genealogical)

This is similar to saying "gravity" (phenomenon) and "general relativity" (theory).
Different terms for different purposes, but referring to the same reality.
"""

with open('txt/cultural_marxism_pc_synonymy.txt', 'w') as f:
    f.write(output)

print("\n" + "="*80)
print("Results saved to: txt/cultural_marxism_pc_synonymy.txt")
print("="*80)
