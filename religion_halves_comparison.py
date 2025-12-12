#!/usr/bin/env python3
"""
Compare how religion is mentioned in first half vs second half of 2083 document.
"""

import re
from collections import Counter

def count_terms(text, terms):
    """Count occurrences of terms in text."""
    text_lower = text.lower()
    results = {}
    
    for term in terms:
        pattern = r'\b' + re.escape(term) + r'\b'
        count = len(re.findall(pattern, text_lower))
        results[term] = count
    
    return results

def get_sample_contexts(text, term, num_samples=5):
    """Get sample contexts."""
    text_lower = text.lower()
    pattern = r'.{0,100}\b' + re.escape(term) + r'\b.{0,100}'
    matches = re.findall(pattern, text_lower, re.IGNORECASE)
    
    unique = []
    for match in matches:
        clean = ' '.join(match.split())
        if clean not in unique and len(unique) < num_samples:
            unique.append(clean)
    
    return unique

def main():
    print("Loading documents...\n")
    
    # Read the split documents
    with open('2083_first_half.txt', 'r', encoding='utf-8', errors='ignore') as f:
        first_half = f.read()
    
    with open('2083_second_half.txt', 'r', encoding='utf-8', errors='ignore') as f:
        second_half = f.read()
    
    print(f"First half size: {len(first_half):,} characters")
    print(f"Second half size: {len(second_half):,} characters\n")
    
    # Define religious terms
    religious_terms = [
        'islam', 'muslim', 'muslims', 
        'christian', 'christianity', 'christians',
        'jewish', 'judaism',
        'religion', 'religious'
    ]
    
    # Count in each half
    first_counts = count_terms(first_half, religious_terms)
    second_counts = count_terms(second_half, religious_terms)
    
    print("="*80)
    print("RELIGION MENTIONS: FIRST HALF vs SECOND HALF")
    print("="*80)
    
    print(f"\n{'Term':<20} {'First Half':<15} {'Second Half':<15} {'Total':<10} {'% in 1st':<10}")
    print("-"*80)
    
    totals = {}
    for term in religious_terms:
        first = first_counts[term]
        second = second_counts[term]
        total = first + second
        totals[term] = total
        
        if total > 0:
            pct_first = (first / total) * 100
            print(f"{term:<20} {first:<15} {second:<15} {total:<10} {pct_first:>6.1f}%")
    
    # Calculate category totals
    print("\n" + "="*80)
    print("CATEGORY TOTALS")
    print("="*80)
    
    islam_first = first_counts['islam'] + first_counts['muslim'] + first_counts['muslims']
    islam_second = second_counts['islam'] + second_counts['muslim'] + second_counts['muslims']
    islam_total = islam_first + islam_second
    
    christian_first = first_counts['christian'] + first_counts['christianity'] + first_counts['christians']
    christian_second = second_counts['christian'] + second_counts['christianity'] + second_counts['christians']
    christian_total = christian_first + christian_second
    
    print(f"\nIslam-related terms:")
    print(f"  First half:  {islam_first} ({islam_first/islam_total*100:.1f}%)")
    print(f"  Second half: {islam_second} ({islam_second/islam_total*100:.1f}%)")
    print(f"  Total:       {islam_total}")
    
    print(f"\nChristianity-related terms:")
    print(f"  First half:  {christian_first} ({christian_first/christian_total*100:.1f}%)")
    print(f"  Second half: {christian_second} ({christian_second/christian_total*100:.1f}%)")
    print(f"  Total:       {christian_total}")
    
    # Sample contexts from first half
    print("\n" + "="*80)
    print("SAMPLE CONTEXTS FROM FIRST HALF")
    print("="*80)
    
    print("\nIslam contexts in first half:")
    islam_contexts_first = get_sample_contexts(first_half, 'islam', 5)
    for i, context in enumerate(islam_contexts_first, 1):
        print(f"\n{i}. ...{context}...")
    
    print("\n" + "-"*80)
    print("Christianity contexts in first half:")
    christian_contexts_first = get_sample_contexts(first_half, 'christian', 5)
    for i, context in enumerate(christian_contexts_first, 1):
        print(f"\n{i}. ...{context}...")
    
    # Analysis
    print("\n" + "="*80)
    print("ANALYSIS")
    print("="*80)
    
    if islam_first > islam_second:
        print(f"\n✓ Islam is MORE concentrated in FIRST half")
        print(f"  First half has {islam_first - islam_second} more Islam references")
    else:
        print(f"\n✓ Islam is MORE concentrated in SECOND half")
        print(f"  Second half has {islam_second - islam_first} more Islam references")
    
    if christian_first > christian_second:
        print(f"\n✓ Christianity is MORE concentrated in FIRST half")
        print(f"  First half has {christian_first - christian_second} more Christianity references")
    else:
        print(f"\n✓ Christianity is MORE concentrated in SECOND half")
        print(f"  Second half has {christian_second - christian_first} more Christianity references")
    
    # Overall religious focus per half
    total_religious_first = sum(first_counts.values())
    total_religious_second = sum(second_counts.values())
    
    print(f"\n{'='*80}")
    print("OVERALL RELIGIOUS DISCOURSE")
    print("="*80)
    print(f"\nTotal religious terms:")
    print(f"  First half:  {total_religious_first}")
    print(f"  Second half: {total_religious_second}")
    print(f"  Ratio: {total_religious_first/total_religious_second:.2f}x")
    
    if total_religious_first > total_religious_second:
        print(f"\n✓ First half is MORE focused on religion ({total_religious_first - total_religious_second} more mentions)")
    else:
        print(f"\n✓ Second half is MORE focused on religion ({total_religious_second - total_religious_first} more mentions)")
    
    # Save results
    with open('religion_halves_comparison.txt', 'w') as f:
        f.write("RELIGION MENTIONS: FIRST HALF vs SECOND HALF OF 2083\n")
        f.write("="*80 + "\n\n")
        
        f.write(f"{'Term':<20} {'First Half':<15} {'Second Half':<15} {'Total':<10}\n")
        f.write("-"*80 + "\n")
        
        for term in religious_terms:
            first = first_counts[term]
            second = second_counts[term]
            total = first + second
            f.write(f"{term:<20} {first:<15} {second:<15} {total:<10}\n")
        
        f.write(f"\n{'='*80}\n")
        f.write("ISLAM CONTEXTS FROM FIRST HALF\n")
        f.write("="*80 + "\n\n")
        
        for i, context in enumerate(islam_contexts_first, 1):
            f.write(f"{i}. ...{context}...\n\n")
        
        f.write(f"\n{'='*80}\n")
        f.write("CHRISTIANITY CONTEXTS FROM FIRST HALF\n")
        f.write("="*80 + "\n\n")
        
        for i, context in enumerate(christian_contexts_first, 1):
            f.write(f"{i}. ...{context}...\n\n")
    
    print("\n✓ Results saved to: religion_halves_comparison.txt")

if __name__ == "__main__":
    main()
