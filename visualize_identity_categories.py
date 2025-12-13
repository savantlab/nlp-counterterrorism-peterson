#!/usr/bin/env python3
"""
Visualize identity politics categories in the 2083 document.
"""

import matplotlib.pyplot as plt
import numpy as np

# Data from analysis
categories = ['Religion', 'Race/Ethnicity', 'Gender', 'Nationality', 'Class', 'Sexual Orientation', 'Disability Status']
occurrences = [549, 226, 176, 68, 36, 11, 2]
percentages = [51.4, 21.2, 16.5, 6.4, 3.4, 1.0, 0.2]

# Color palette
colors = ['#e74c3c', '#3498db', '#9b59b6', '#f39c12', '#2ecc71', '#e67e22', '#95a5a6']

# Create figure with multiple visualizations
fig = plt.figure(figsize=(16, 10))

# 1. Bar chart - Occurrences
ax1 = plt.subplot(2, 2, 1)
bars = ax1.bar(categories, occurrences, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
ax1.set_ylabel('Number of Occurrences', fontsize=12, fontweight='bold')
ax1.set_title('Identity Category Frequency in 2083 Document', fontsize=14, fontweight='bold', pad=15)
ax1.set_xticklabels(categories, rotation=45, ha='right', fontsize=10)
ax1.grid(axis='y', alpha=0.3, linestyle='--')

# Add value labels
for bar in bars:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(height)}', ha='center', va='bottom', fontsize=10, fontweight='bold')

# 2. Pie chart - Percentages
ax2 = plt.subplot(2, 2, 2)
explode = (0.05, 0.02, 0.02, 0, 0, 0, 0)  # Explode Religion slice
wedges, texts, autotexts = ax2.pie(occurrences, labels=categories, autopct='%1.1f%%',
                                     colors=colors, explode=explode, startangle=90,
                                     textprops={'fontsize': 10})

# Make percentage text bold
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
    autotext.set_fontsize(11)

ax2.set_title('Distribution of Identity Categories', fontsize=14, fontweight='bold', pad=15)

# 3. Horizontal bar chart for better readability
ax3 = plt.subplot(2, 2, 3)
y_pos = np.arange(len(categories))
bars = ax3.barh(y_pos, occurrences, color=colors, alpha=0.85, edgecolor='black', linewidth=1.5)
ax3.set_yticks(y_pos)
ax3.set_yticklabels(categories, fontsize=11)
ax3.invert_yaxis()
ax3.set_xlabel('Number of Occurrences', fontsize=12, fontweight='bold')
ax3.set_title('Identity Categories Ranked by Frequency', fontsize=14, fontweight='bold', pad=15)
ax3.grid(axis='x', alpha=0.3, linestyle='--')

# Add value labels
for i, (bar, val) in enumerate(zip(bars, occurrences)):
    width = bar.get_width()
    ax3.text(width + 10, bar.get_y() + bar.get_height()/2,
            f'{int(val)}', ha='left', va='center', fontsize=11, fontweight='bold')

# 4. Top terms breakdown
ax4 = plt.subplot(2, 2, 4)
ax4.axis('off')

# Top terms for each category
top_terms = {
    'Religion': [('islam', 198), ('muslim', 109), ('muslims', 83)],
    'Race/Ethnicity': [('european', 147), ('multiculturalism', 23), ('racism', 6)],
    'Gender': [('women', 37), ('men', 35), ('feminism', 23)],
    'Nationality': [('national', 22), ('nations', 16), ('nationalist', 10)],
    'Class': [('class', 14), ('bourgeois', 5), ('elites', 5)],
    'Sexual Orientation': [('sexuality', 5), ('trans', 3), ('heterosexual', 2)],
    'Disability Status': [('accommodation', 2)]
}

title_text = "Top Terms per Category\n" + "="*50 + "\n\n"
y_offset = 0.92

for i, cat in enumerate(categories):
    color = colors[i]
    cat_text = f"{cat} ({occurrences[i]} total):\n"
    
    terms_list = []
    for term, count in top_terms[cat]:
        terms_list.append(f"  • {term}: {count}")
    
    terms_text = "\n".join(terms_list)
    full_text = cat_text + terms_text
    
    ax4.text(0.08, y_offset, full_text, fontsize=9, verticalalignment='top',
             fontfamily='monospace', color=color, fontweight='bold')
    
    y_offset -= 0.135

ax4.set_xlim(0, 1)
ax4.set_ylim(0, 1)
ax4.text(0.5, 0.97, 'Top Terms per Category', fontsize=13, fontweight='bold',
         ha='center', va='top')

plt.suptitle('Identity Politics Categories in 2083 Document (1,068 total occurrences)', 
             fontsize=16, fontweight='bold', y=0.995)

plt.tight_layout(rect=[0, 0, 1, 0.99])

# Save figure
output_file = 'identity_categories_visualization.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"✓ Saved: {output_file}")

plt.show()

# Print summary
print("\n" + "="*80)
print("IDENTITY CATEGORIES SUMMARY")
print("="*80)
print(f"\nTotal identity-related terms: 1,068")
print(f"\n{'Category':<25} {'Count':<10} {'Percentage':<12} {'Status'}")
print("-"*80)

for cat, count, pct in zip(categories, occurrences, percentages):
    status = "✓ PRESENT" if count > 0 else "✗ ABSENT"
    print(f"{cat:<25} {count:<10} {pct:>5.1f}%        {status}")

print("\n" + "="*80)
print("KEY FINDING")
print("="*80)
print("\nAll 7 identity categories are present in the 2083 document.")
print("\nReligion dominates (51.4%), followed by Race/Ethnicity (21.2%) and Gender (16.5%).")
print("Sexual Orientation (1.0%) and Disability Status (0.2%) are minimally present.")
