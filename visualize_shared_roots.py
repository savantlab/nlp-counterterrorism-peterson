#!/usr/bin/env python3
"""
Visualize the shared roots and conceptual overlaps between YouTube and 2083.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

def create_shared_roots_diagram():
    """Create a comprehensive visualization of shared intellectual roots."""
    
    fig = plt.figure(figsize=(20, 14))
    
    # Create main axis
    ax = plt.subplot(111)
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 14)
    ax.axis('off')
    
    # Title
    ax.text(10, 13.5, 'Shared Intellectual Roots: YouTube vs 2083 Document', 
            fontsize=20, fontweight='bold', ha='center')
    ax.text(10, 13, 'How Two Texts Critique the Same Ideological Movement', 
            fontsize=14, ha='center', style='italic', color='gray')
    
    # ============================================================================
    # SECTION 1: Shared Root (top)
    # ============================================================================
    
    # Marxist root box
    root_box = FancyBboxPatch((7, 11), 6, 1.8, boxstyle="round,pad=0.1", 
                              edgecolor='darkred', facecolor='#ffcccc', linewidth=3)
    ax.add_patch(root_box)
    ax.text(10, 12.5, 'SHARED ROOT', fontsize=11, fontweight='bold', ha='center')
    ax.text(10, 12.1, 'Marxist Theory → Cultural Analysis', fontsize=10, ha='center')
    ax.text(10, 11.8, '(Germany)', fontsize=9, ha='center', style='italic')
    ax.text(10, 11.5, 'Marx (1818-1883): Economic class struggle', fontsize=8, ha='center')
    ax.text(10, 11.25, 'Frankfurt School (1930s): Cultural criticism', fontsize=8, ha='center')
    
    # ============================================================================
    # SECTION 2: Divergent Terminology (middle branches)
    # ============================================================================
    
    # YouTube branch (left)
    yt_box = FancyBboxPatch((1, 8.5), 7, 1.8, boxstyle="round,pad=0.1",
                            edgecolor='#e67e22', facecolor='#ffe6cc', linewidth=2)
    ax.add_patch(yt_box)
    ax.text(4.5, 10, 'YOUTUBE TERMS', fontsize=11, fontweight='bold', ha='center', color='#d35400')
    ax.text(4.5, 9.6, '• Post-modernism', fontsize=9, ha='center')
    ax.text(4.5, 9.3, '• Neo-Marxism', fontsize=9, ha='center')
    ax.text(4.5, 9, '• Identity politics', fontsize=9, ha='center')
    ax.text(4.5, 8.7, 'GENERAL critique', fontsize=8, ha='center', style='italic')
    
    # 2083 branch (right)
    doc_box = FancyBboxPatch((12, 8.5), 7, 1.8, boxstyle="round,pad=0.1",
                             edgecolor='#3498db', facecolor='#cce5ff', linewidth=2)
    ax.add_patch(doc_box)
    ax.text(15.5, 10, '2083 TERMS', fontsize=11, fontweight='bold', ha='center', color='#2874a6')
    ax.text(15.5, 9.6, '• Political Correctness', fontsize=9, ha='center')
    ax.text(15.5, 9.3, '• Cultural Marxism', fontsize=9, ha='center')
    ax.text(15.5, 9, '• Identity politics + Feminism', fontsize=9, ha='center')
    ax.text(15.5, 8.7, 'SPECIFIC manifestations', fontsize=8, ha='center', style='italic')
    
    # Arrows from root to branches
    arrow1 = FancyArrowPatch((8.5, 11), (5, 10.3), arrowstyle='->', 
                            lw=2, color='darkred', mutation_scale=20)
    ax.add_patch(arrow1)
    arrow2 = FancyArrowPatch((11.5, 11), (15, 10.3), arrowstyle='->', 
                            lw=2, color='darkred', mutation_scale=20)
    ax.add_patch(arrow2)
    
    # ============================================================================
    # SECTION 3: Conceptual Mappings (middle)
    # ============================================================================
    
    mappings_y = 7.5
    ax.text(10, mappings_y, '3 KEY CONCEPTUAL MAPPINGS', fontsize=12, 
            fontweight='bold', ha='center', bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3))
    
    # Mapping 1
    map1_y = 6.5
    ax.add_patch(mpatches.Rectangle((1, map1_y-0.3), 7, 0.8, 
                                    edgecolor='#e67e22', facecolor='#ffe6cc', linewidth=1.5))
    ax.text(4.5, map1_y+0.2, 'Post-modernism', fontsize=9, ha='center', fontweight='bold')
    
    ax.add_patch(mpatches.Rectangle((12, map1_y-0.3), 7, 0.8, 
                                    edgecolor='#3498db', facecolor='#cce5ff', linewidth=1.5))
    ax.text(15.5, map1_y+0.2, 'Political Correctness', fontsize=9, ha='center', fontweight='bold')
    
    ax.annotate('', xy=(11.8, map1_y+0.1), xytext=(8.2, map1_y+0.1),
                arrowprops=dict(arrowstyle='<->', lw=2, color='green'))
    ax.text(10, map1_y+0.5, '=', fontsize=14, ha='center', fontweight='bold', color='green')
    ax.text(10, map1_y-0.6, 'Reject objective truth', fontsize=8, ha='center', style='italic')
    
    # Mapping 2
    map2_y = 5.2
    ax.add_patch(mpatches.Rectangle((1, map2_y-0.3), 7, 0.8, 
                                    edgecolor='#e67e22', facecolor='#ffe6cc', linewidth=1.5))
    ax.text(4.5, map2_y+0.2, 'Neo-Marxism', fontsize=9, ha='center', fontweight='bold')
    
    ax.add_patch(mpatches.Rectangle((12, map2_y-0.3), 7, 0.8, 
                                    edgecolor='#3498db', facecolor='#cce5ff', linewidth=1.5))
    ax.text(15.5, map2_y+0.2, 'Cultural Marxism', fontsize=9, ha='center', fontweight='bold')
    
    ax.annotate('', xy=(11.8, map2_y+0.1), xytext=(8.2, map2_y+0.1),
                arrowprops=dict(arrowstyle='<->', lw=2, color='green'))
    ax.text(10, map2_y+0.5, '=', fontsize=14, ha='center', fontweight='bold', color='green')
    ax.text(10, map2_y-0.6, 'Marxism applied to culture', fontsize=8, ha='center', style='italic')
    
    # Mapping 3
    map3_y = 3.9
    ax.add_patch(mpatches.Rectangle((1, map3_y-0.3), 7, 0.8, 
                                    edgecolor='#e67e22', facecolor='#ffe6cc', linewidth=1.5))
    ax.text(4.5, map3_y+0.2, 'Identity politics', fontsize=9, ha='center', fontweight='bold')
    
    ax.add_patch(mpatches.Rectangle((12, map3_y-0.3), 7, 0.8, 
                                    edgecolor='#3498db', facecolor='#cce5ff', linewidth=1.5))
    ax.text(15.5, map3_y+0.2, 'Identity + Feminism', fontsize=9, ha='center', fontweight='bold')
    
    ax.annotate('', xy=(11.8, map3_y+0.1), xytext=(8.2, map3_y+0.1),
                arrowprops=dict(arrowstyle='<->', lw=2, color='orange'))
    ax.text(10, map3_y+0.5, '≈', fontsize=14, ha='center', fontweight='bold', color='orange')
    ax.text(10, map3_y-0.6, 'Group-based politics (2083 adds specific example)', 
            fontsize=8, ha='center', style='italic')
    
    # ============================================================================
    # SECTION 4: Overlap Statistics (bottom)
    # ============================================================================
    
    stats_y = 2.5
    
    # Overlap circle (left)
    overlap_circle = plt.Circle((4, stats_y-0.5), 0.8, color='#2ecc71', alpha=0.3)
    ax.add_patch(overlap_circle)
    ax.text(4, stats_y-0.5, '75%', fontsize=16, ha='center', fontweight='bold', color='#27ae60')
    ax.text(4, stats_y-1.5, 'Conceptual\nOverlap', fontsize=9, ha='center', fontweight='bold')
    
    # Overlap details
    ax.text(7, stats_y-0.2, 'SHARED (75%):', fontsize=10, fontweight='bold')
    ax.text(7, stats_y-0.5, '• Post-modernism = PC', fontsize=8)
    ax.text(7, stats_y-0.75, '• Neo-Marxism = Cultural Marxism', fontsize=8)
    ax.text(7, stats_y-1, '• Identity politics framework', fontsize=8)
    ax.text(7, stats_y-1.25, '• Universities as source (60s-70s)', fontsize=8)
    ax.text(7, stats_y-1.5, '• West under attack', fontsize=8)
    
    # Unique circle (right)
    unique_circle = plt.Circle((16, stats_y-0.5), 0.8, color='#e74c3c', alpha=0.3)
    ax.add_patch(unique_circle)
    ax.text(16, stats_y-0.5, '25%', fontsize=16, ha='center', fontweight='bold', color='#c0392b')
    ax.text(16, stats_y-1.5, 'Unique to\n2083', fontsize=9, ha='center', fontweight='bold')
    
    # Unique details
    ax.text(13, stats_y-0.2, 'UNIQUE TO 2083 (25%):', fontsize=10, fontweight='bold')
    ax.text(13, stats_y-0.5, '• Islam (51% of identity terms)', fontsize=8)
    ax.text(13, stats_y-0.75, '• Explicit feminism critique (75x)', fontsize=8)
    ax.text(13, stats_y-1, '• European-specific context', fontsize=8)
    ax.text(13, stats_y-1.25, '• Detailed policy proposals', fontsize=8)
    
    # ============================================================================
    # SECTION 5: Bottom summary
    # ============================================================================
    
    summary_box = FancyBboxPatch((2, 0.2), 16, 0.8, boxstyle="round,pad=0.1",
                                 edgecolor='purple', facecolor='#f0e6ff', linewidth=2)
    ax.add_patch(summary_box)
    ax.text(10, 0.75, 'CONCLUSION: Same ideological critique (75% overlap), but 2083 adds specific targets (feminism) and threats (Islam)', 
            fontsize=10, ha='center', fontweight='bold')
    ax.text(10, 0.4, 'This explains 16% TF-IDF similarity: shared concepts but different scope and specificity', 
            fontsize=9, ha='center', style='italic')
    
    plt.tight_layout()
    
    # Save
    output_file = 'shared_roots_visualization.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ Saved: {output_file}")
    
    plt.show()

def create_venn_style_overlap():
    """Create a Venn-style diagram showing overlap."""
    
    fig, ax = plt.subplots(figsize=(12, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(5, 9.5, 'Conceptual Overlap: YouTube vs 2083', 
            fontsize=16, fontweight='bold', ha='center')
    
    # YouTube circle (left)
    yt_circle = plt.Circle((3.5, 5.5), 2.5, color='#e67e22', alpha=0.3, linewidth=3, 
                           edgecolor='#d35400')
    ax.add_patch(yt_circle)
    
    # 2083 circle (right)
    doc_circle = plt.Circle((6.5, 5.5), 2.5, color='#3498db', alpha=0.3, linewidth=3,
                            edgecolor='#2874a6')
    ax.add_patch(doc_circle)
    
    # YouTube label
    ax.text(2.3, 8, 'YOUTUBE', fontsize=12, fontweight='bold', color='#d35400')
    ax.text(2.3, 7.5, 'Post-modernism', fontsize=9)
    ax.text(2.3, 7.2, 'Neo-Marxism', fontsize=9)
    ax.text(2.3, 6.9, 'Identity politics', fontsize=9)
    ax.text(2.3, 6.5, '(726 words)', fontsize=8, style='italic')
    
    # 2083 label  
    ax.text(7.5, 8, '2083 DOC', fontsize=12, fontweight='bold', color='#2874a6')
    ax.text(7.5, 7.5, 'Political Correctness', fontsize=9)
    ax.text(7.5, 7.2, 'Cultural Marxism', fontsize=9)
    ax.text(7.5, 6.9, 'Feminism', fontsize=9)
    ax.text(7.5, 6.6, 'Islam (dominant)', fontsize=9)
    ax.text(7.5, 6.2, '(41,548 words)', fontsize=8, style='italic')
    
    # Overlap section (center)
    ax.text(5, 6.5, 'SHARED', fontsize=11, fontweight='bold', ha='center', color='#27ae60')
    ax.text(5, 6.1, '75%', fontsize=14, fontweight='bold', ha='center', color='#27ae60')
    ax.text(5, 5.7, 'Same ideology', fontsize=8, ha='center')
    ax.text(5, 5.4, 'Different terms', fontsize=8, ha='center')
    ax.text(5, 5, '• Marxist roots', fontsize=7, ha='center')
    ax.text(5, 4.7, '• Identity politics', fontsize=7, ha='center')
    ax.text(5, 4.4, '• Universities', fontsize=7, ha='center')
    ax.text(5, 4.1, '• West threatened', fontsize=7, ha='center')
    
    # Bottom stats
    ax.text(2, 2, 'YouTube focus:', fontsize=10, fontweight='bold')
    ax.text(2, 1.6, 'GENERAL ideology critique', fontsize=9)
    ax.text(2, 1.3, 'No feminism mentions', fontsize=8, color='red')
    ax.text(2, 1, 'No Islam mentions', fontsize=8, color='red')
    
    ax.text(8, 2, '2083 focus:', fontsize=10, fontweight='bold')
    ax.text(8, 1.6, 'SPECIFIC manifestations', fontsize=9)
    ax.text(8, 1.3, 'Feminism: 75 mentions', fontsize=8, color='blue')
    ax.text(8, 1, 'Islam: 390 mentions', fontsize=8, color='blue')
    
    # TF-IDF explanation
    ax.text(5, 0.5, '16% TF-IDF Similarity = Shared framework + Different scope', 
            fontsize=9, ha='center', bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5))
    
    plt.tight_layout()
    
    output_file = 'overlap_venn_diagram.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ Saved: {output_file}")
    
    plt.show()

if __name__ == "__main__":
    print("Creating shared roots visualizations...\n")
    create_shared_roots_diagram()
    create_venn_style_overlap()
    print("\n✓ Both visualizations created successfully!")
