#!/usr/bin/env python3
"""
Create visualization showing how YouTube video implicitly references 
radical feminism through 'postmodern neo-marxist' terminology.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

# Create figure with white background
fig, ax = plt.subplots(figsize=(18, 12))
fig.patch.set_facecolor('white')
ax.set_xlim(0, 10)
ax.set_ylim(0, 11)
ax.axis('off')

# Title
ax.text(5, 10.5, 'Strategic Terminology: "Postmodern Neo-Marxists" as Implicit Reference', 
        ha='center', fontsize=18, fontweight='bold')
ax.text(5, 10.0, 'YouTube Video Avoids "Feminism" While Describing Radical Feminist Ideology', 
        ha='center', fontsize=12, style='italic', color='#555')

# LEFT SIDE: YouTube Video
# Box for YouTube
youtube_box = FancyBboxPatch((0.3, 7.2), 4, 2.2, 
                             boxstyle="round,pad=0.1", 
                             edgecolor='#FF0000', facecolor='#FFE6E6', 
                             linewidth=3)
ax.add_patch(youtube_box)

ax.text(2.3, 9.1, 'YOUTUBE VIDEO', ha='center', fontsize=14, fontweight='bold', color='#CC0000')
ax.text(2.3, 8.75, 'Jordan Peterson - Postmodernism', ha='center', fontsize=10, style='italic')
ax.text(2.3, 8.35, 'Uses term:', ha='center', fontsize=11, fontweight='bold')
ax.text(2.3, 7.95, '"Postmodern Neo-Marxists"', ha='center', fontsize=12, 
        bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3))
ax.text(2.3, 7.5, 'Mentions "feminism": 0 times', ha='center', fontsize=9, 
        color='#CC0000', fontweight='bold')

# Characteristics of "postmodern neo-marxists" in YouTube
char_y = 6.6
ax.text(2.3, char_y, 'Characteristics Described:', ha='center', fontsize=11, 
        fontweight='bold', color='#333')
characteristics_yt = [
    '✓ Western civilization is "patriarchal"',
    '✓ "All sex differences are socially constructed"',
    '✓ "Politics of identity" framework',
    '✓ Push "progressive activism" on campus',
    '✓ Enforce "fabricated gender pronouns"',
    '✓ Root out discrimination'
]

y_pos = char_y - 0.5
for char in characteristics_yt:
    ax.text(2.3, y_pos, char, ha='center', fontsize=8.5, color='#000')
    y_pos -= 0.4

# RIGHT SIDE: 2083 Document
# Box for 2083
doc_box = FancyBboxPatch((5.7, 7.2), 4, 2.2, 
                         boxstyle="round,pad=0.1", 
                         edgecolor='#0066CC', facecolor='#E6F2FF', 
                         linewidth=3)
ax.add_patch(doc_box)

ax.text(7.7, 9.1, '2083 DOCUMENT', ha='center', fontsize=14, fontweight='bold', color='#0066CC')
ax.text(7.7, 8.75, 'European Declaration', ha='center', fontsize=10, style='italic')
ax.text(7.7, 8.35, 'Uses term:', ha='center', fontsize=11, fontweight='bold')
ax.text(7.7, 7.95, '"Radical Feminism"', ha='center', fontsize=12, 
        bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.3))
ax.text(7.7, 7.5, 'Mentions "feminism": 75 times', ha='center', fontsize=9, 
        color='#0066CC', fontweight='bold')

# Characteristics of "radical feminism" in 2083
ax.text(7.7, 6.6, 'Characteristics Described:', ha='center', fontsize=11, 
        fontweight='bold', color='#333')
characteristics_doc = [
    '✓ Part of "Cultural Marxism" ideology',
    '✓ Views Western civilization as "patriarchal"',
    '✓ Denies biological sex differences',
    '✓ Uses identity politics framework',
    '✓ Campus activism & political correctness',
    '✓ Progressive/leftist movement'
]

y_pos = 6.1
for char in characteristics_doc:
    ax.text(7.7, y_pos, char, ha='center', fontsize=8.5, color='#000')
    y_pos -= 0.4

# CENTER: Overlap analysis
overlap_box = FancyBboxPatch((2, 2.8), 6, 1.8, 
                             boxstyle="round,pad=0.1", 
                             edgecolor='#00AA00', facecolor='#E6FFE6', 
                             linewidth=3)
ax.add_patch(overlap_box)

ax.text(5, 4.3, 'CONCEPTUAL OVERLAP: 6 Shared Characteristics', 
        ha='center', fontsize=12, fontweight='bold', color='#00AA00')

shared = [
    '1. Patriarchal critique',
    '2. Social construction of sex/gender',
    '3. Identity politics',
    '4. Marxist ideological roots',
    '5. Campus/academic activism',
    '6. Political correctness'
]

# Display shared characteristics in 2 columns
col1_x = 3.5
col2_x = 6.5
y_start = 3.8

for i, item in enumerate(shared):
    if i < 3:
        ax.text(col1_x, y_start - (i * 0.35), item, ha='center', fontsize=9, color='#000')
    else:
        ax.text(col2_x, y_start - ((i-3) * 0.35), item, ha='center', fontsize=9, color='#000')

# Arrows showing connection
arrow1 = FancyArrowPatch((2.3, 4.6), (5, 4.6),
                        arrowstyle='->', mutation_scale=20, 
                        color='#FF6B6B', linewidth=2)
ax.add_patch(arrow1)

arrow2 = FancyArrowPatch((7.7, 4.6), (5, 4.6),
                        arrowstyle='->', mutation_scale=20, 
                        color='#4DA6FF', linewidth=2)
ax.add_patch(arrow2)

# BOTTOM: Conclusion box
conclusion_box = FancyBboxPatch((0.8, 0.4), 8.4, 1.9, 
                                boxstyle="round,pad=0.1", 
                                edgecolor='#FF6600', facecolor='#FFF4E6', 
                                linewidth=3)
ax.add_patch(conclusion_box)

ax.text(5, 2.05, 'STRATEGIC FRAMING ANALYSIS', ha='center', fontsize=13, 
        fontweight='bold', color='#FF6600')

conclusion_text = [
    'The YouTube video uses "postmodern neo-marxists" as an UMBRELLA TERM that implicitly includes radical feminism.',
    'Both texts describe the SAME ideological movement with DIFFERENT terminology and levels of specificity.',
    'YouTube: GENERAL critique without naming feminism explicitly | 2083: SPECIFIC focus on radical feminism'
]

y_pos = 1.65
for line in conclusion_text:
    ax.text(5, y_pos, line, ha='center', fontsize=9, color='#000')
    y_pos -= 0.35

# Add data note
ax.text(5, 0.6, 'Data: YouTube transcript (726 words, 0 feminism mentions) vs 2083 document (41,000 words, 75 feminism mentions)', 
        ha='center', fontsize=8, style='italic', color='#666')

plt.tight_layout()
plt.savefig('implicit_feminism_reference_visualization.png', dpi=300, bbox_inches='tight', 
            facecolor='white', edgecolor='none')
print("Visualization saved: implicit_feminism_reference_visualization.png")
