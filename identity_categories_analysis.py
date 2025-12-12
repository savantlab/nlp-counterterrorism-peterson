#!/usr/bin/env python3
"""
Search for identity politics categories in the 2083 document.
"""

import re
from collections import Counter, defaultdict

# Define search terms for each identity category
IDENTITY_CATEGORIES = {
    'Race/Ethnicity': [
        'race', 'racial', 'racism', 'racist', 'ethnic', 'ethnicity', 'white', 'black',
        'asian', 'latino', 'hispanic', 'indigenous', 'native', 'african', 'european',
        'caucasian', 'minority', 'minorities', 'multicultural', 'multiculturalism'
    ],
    'Gender': [
        'gender', 'male', 'female', 'men', 'women', 'masculine', 'feminine',
        'feminism', 'feminist', 'feminists', 'patriarchy', 'patriarchal', 'matriarchy',
        'sexism', 'sexist', 'misogyny', 'misogynist'
    ],
    'Sexual Orientation': [
        'gay', 'lesbian', 'homosexual', 'heterosexual', 'bisexual', 'transgender',
        'trans', 'lgbt', 'lgbtq', 'queer', 'sexuality', 'sexual orientation'
    ],
    'Religion': [
        'religion', 'religious', 'islam', 'muslim', 'muslims', 'christian', 'christianity',
        'christians', 'jewish', 'judaism', 'hindu', 'hinduism', 'buddhist', 'buddhism',
        'atheist', 'atheism', 'secular', 'secularism'
    ],
    'Disability Status': [
        'disability', 'disabled', 'handicap', 'handicapped', 'impairment', 'differently abled',
        'accessibility', 'accommodation', 'wheelchair', 'blind', 'deaf'
    ],
    'Class': [
        'class', 'working class', 'middle class', 'upper class', 'lower class',
        'bourgeois', 'bourgeoisie', 'proletariat', 'elite', 'elites', 'elitism',
        'privileged', 'privilege', 'wealthy', 'poor', 'poverty', 'economic inequality'
    ],
    'Nationality': [
        'nationality', 'national', 'nation', 'nations', 'citizen', 'citizenship',
        'immigrant', 'immigrants', 'immigration', 'migrant', 'migrants', 'refugee',
        'refugees', 'border', 'borders', 'nationalist', 'nationalism'
    ]
}

def search_document(text, search_terms):
    """Search for terms and return frequency and context."""
    text_lower = text.lower()
    results = {}
    
    for term in search_terms:
        # Use word boundaries to avoid partial matches
        pattern = r'\b' + re.escape(term) + r'\b'
        matches = re.findall(pattern, text_lower)
        count = len(matches)
        
        if count > 0:
            results[term] = count
    
    return results

def get_context_samples(text, term, num_samples=3):
    """Get sample contexts where term appears."""
    text_lower = text.lower()
    pattern = r'.{0,80}\b' + re.escape(term) + r'\b.{0,80}'
    matches = re.findall(pattern, text_lower, re.IGNORECASE)
    
    # Return up to num_samples unique contexts
    unique_matches = []
    for match in matches:
        if len(unique_matches) >= num_samples:
            break
        # Clean up the match
        clean = ' '.join(match.split())
        if clean not in unique_matches:
            unique_matches.append(clean)
    
    return unique_matches

def main():
    print("Loading 2083 document...\n")
    
    with open('2083. EUROPEAN DECLARATION OF INDEPENDENCE.txt', 'r', encoding='utf-8', errors='ignore') as f:
        doc_text = f.read()
    
    print(f"Document size: {len(doc_text):,} characters\n")
    print("="*80)
    print("IDENTITY CATEGORIES ANALYSIS")
    print("="*80)
    
    # Analyze each category
    all_results = {}
    category_totals = {}
    
    for category, terms in IDENTITY_CATEGORIES.items():
        print(f"\n{'='*80}")
        print(f"CATEGORY: {category}")
        print(f"{'='*80}")
        
        results = search_document(doc_text, terms)
        
        if results:
            # Sort by frequency
            sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)
            total = sum(results.values())
            category_totals[category] = total
            all_results[category] = sorted_results
            
            print(f"\nTotal occurrences: {total:,}")
            print(f"Unique terms found: {len(results)}/{len(terms)}")
            print(f"\nTop terms:")
            
            for term, count in sorted_results[:10]:
                print(f"  {term:30} - {count:,} occurrences")
            
            if len(sorted_results) > 10:
                print(f"  ... and {len(sorted_results) - 10} more terms")
            
            # Show sample contexts for top term
            if sorted_results:
                top_term = sorted_results[0][0]
                print(f"\nSample contexts for '{top_term}':")
                samples = get_context_samples(doc_text, top_term, 3)
                for i, sample in enumerate(samples, 1):
                    print(f"\n  {i}. ...{sample}...")
        else:
            print("\nNo terms found in this category.")
            category_totals[category] = 0
    
    # Summary
    print("\n" + "="*80)
    print("SUMMARY: IDENTITY CATEGORIES IN 2083 DOCUMENT")
    print("="*80)
    
    sorted_categories = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)
    
    print(f"\n{'Category':<25} {'Total Occurrences':<20} {'Presence'}")
    print("-"*80)
    
    for category, total in sorted_categories:
        presence = "✓ PRESENT" if total > 0 else "✗ ABSENT"
        print(f"{category:<25} {total:>10,}             {presence}")
    
    # Write detailed results to file
    with open('identity_categories_results.txt', 'w') as f:
        f.write("IDENTITY POLITICS CATEGORIES IN 2083 DOCUMENT\n")
        f.write("="*80 + "\n\n")
        
        for category in sorted(IDENTITY_CATEGORIES.keys()):
            f.write(f"\n{'='*80}\n")
            f.write(f"{category}\n")
            f.write(f"{'='*80}\n")
            
            if category in all_results and all_results[category]:
                f.write(f"\nTotal occurrences: {category_totals[category]:,}\n\n")
                
                for term, count in all_results[category]:
                    f.write(f"  {term:30} - {count:,}\n")
            else:
                f.write("\nNo terms found.\n")
    
    print("\n✓ Detailed results saved to: identity_categories_results.txt")
    
    # Calculate percentages
    total_all = sum(category_totals.values())
    print(f"\nTotal identity-related terms: {total_all:,}")
    print(f"\nPercentage breakdown:")
    for category, total in sorted_categories:
        if total > 0:
            pct = (total / total_all) * 100
            print(f"  {category:<25} {pct:>5.1f}%")

if __name__ == "__main__":
    main()
