"""
Network Analysis of Key Terms Co-occurrence
Visualizes how concepts cluster differently in Peterson video vs Breivik manifesto
"""

import re
from collections import defaultdict, Counter
from itertools import combinations
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# File paths
YOUTUBE_FILE = "txt/youtube_transcript_clean.txt"
DOC_2083_FILE = "txt/2083. EUROPEAN DECLARATION OF INDEPENDENCE.txt"

def load_text(filepath):
    """Load and return text content."""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read().lower()

def tokenize(text):
    """Convert text to list of words."""
    return re.findall(r'\b[a-z]+\b', text)

def get_shared_keywords():
    """Return the key shared terms we want to analyze."""
    return [
        # Core ideological terms
        'marx', 'marxism', 'marxist',
        'postmodern', 'postmodernism',
        'feminism', 'feminist',
        'islam', 'muslim',
        
        # Conceptual framework terms
        'identity', 'politics',
        'power', 'oppression', 'oppressive',
        'western', 'civilization', 'culture',
        'radical', 'progressive',
        
        # Institutional terms
        'university', 'universities', 'campus', 'professor',
        'student', 'students', 'education',
        
        # Political correctness cluster
        'political', 'correctness', 'freedom', 'speech',
        
        # Identity categories
        'race', 'gender', 'sex', 'sexual', 'class',
        'diversity', 'equity', 'equality',
        
        # Action/conflict terms
        'war', 'conflict', 'struggle', 'fight',
        'freedom', 'rights', 'truth'
    ]

def build_cooccurrence_network(text, keywords, window_size=10):
    """
    Build a network where edges represent co-occurrence of terms within a window.
    
    Args:
        text: String of text
        keywords: List of terms to track
        window_size: Number of words to consider as "co-occurring"
    
    Returns:
        networkx.Graph with weighted edges
    """
    words = tokenize(text)
    
    # Track co-occurrences
    cooccurrence = defaultdict(int)
    keyword_counts = Counter()
    
    # Slide window through text
    for i in range(len(words)):
        window = words[i:i+window_size]
        
        # Find which keywords appear in this window
        keywords_in_window = [w for w in window if w in keywords]
        keyword_counts.update(keywords_in_window)
        
        # Record all pairs that co-occur
        for pair in combinations(set(keywords_in_window), 2):
            # Sort pair to ensure (a,b) and (b,a) are treated the same
            pair = tuple(sorted(pair))
            cooccurrence[pair] += 1
    
    # Build network
    G = nx.Graph()
    
    # Add nodes with frequency as attribute
    for keyword, count in keyword_counts.items():
        if count > 0:  # Only add keywords that actually appear
            G.add_node(keyword, frequency=count)
    
    # Add edges with co-occurrence count as weight
    for (word1, word2), count in cooccurrence.items():
        if count >= 2:  # Only include pairs that co-occur at least twice
            G.add_edge(word1, word2, weight=count)
    
    return G, keyword_counts, cooccurrence

def visualize_network(G, title, filename, keyword_counts):
    """Create network visualization."""
    plt.figure(figsize=(20, 20))
    
    # Use spring layout for positioning
    pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
    
    # Node sizes based on frequency
    node_sizes = [keyword_counts.get(node, 1) * 100 for node in G.nodes()]
    
    # Edge widths based on co-occurrence weight
    edges = G.edges()
    weights = [G[u][v]['weight'] for u, v in edges]
    max_weight = max(weights) if weights else 1
    edge_widths = [w / max_weight * 5 for w in weights]
    
    # Color nodes by degree centrality (how connected they are)
    if len(G.nodes()) > 0:
        centrality = nx.degree_centrality(G)
        node_colors = [centrality.get(node, 0) for node in G.nodes()]
    else:
        node_colors = []
    
    # Draw network
    nx.draw_networkx_nodes(G, pos, 
                          node_size=node_sizes,
                          node_color=node_colors,
                          cmap=plt.cm.plasma,
                          alpha=0.7)
    
    nx.draw_networkx_edges(G, pos,
                          width=edge_widths,
                          alpha=0.3,
                          edge_color='gray')
    
    nx.draw_networkx_labels(G, pos,
                           font_size=12,
                           font_weight='bold')
    
    plt.title(title, fontsize=20, fontweight='bold', pad=20)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {filename}")
    plt.close()

def compare_networks(G_yt, G_doc, keyword_counts_yt, keyword_counts_doc):
    """Create comparison visualizations."""
    
    # 1. Side-by-side comparison
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(24, 12))
    
    # Peterson network
    plt.sca(ax1)
    pos_yt = nx.spring_layout(G_yt, k=2, iterations=50, seed=42)
    node_sizes_yt = [keyword_counts_yt.get(node, 1) * 200 for node in G_yt.nodes()]
    
    if len(G_yt.nodes()) > 0:
        centrality_yt = nx.degree_centrality(G_yt)
        node_colors_yt = [centrality_yt.get(node, 0) for node in G_yt.nodes()]
    else:
        node_colors_yt = []
    
    nx.draw_networkx_nodes(G_yt, pos_yt, node_size=node_sizes_yt,
                          node_color=node_colors_yt, cmap=plt.cm.Blues,
                          alpha=0.7, ax=ax1)
    nx.draw_networkx_edges(G_yt, pos_yt, alpha=0.3, edge_color='gray', ax=ax1)
    nx.draw_networkx_labels(G_yt, pos_yt, font_size=10, font_weight='bold', ax=ax1)
    ax1.set_title('Peterson: "Who Is Teaching Your Kids?"\nConcept Network', 
                  fontsize=16, fontweight='bold')
    ax1.axis('off')
    
    # Breivik network (sample if too large)
    plt.sca(ax2)
    pos_doc = nx.spring_layout(G_doc, k=2, iterations=50, seed=42)
    node_sizes_doc = [min(keyword_counts_doc.get(node, 1) * 10, 3000) for node in G_doc.nodes()]
    
    if len(G_doc.nodes()) > 0:
        centrality_doc = nx.degree_centrality(G_doc)
        node_colors_doc = [centrality_doc.get(node, 0) for node in G_doc.nodes()]
    else:
        node_colors_doc = []
    
    nx.draw_networkx_nodes(G_doc, pos_doc, node_size=node_sizes_doc,
                          node_color=node_colors_doc, cmap=plt.cm.Reds,
                          alpha=0.7, ax=ax2)
    nx.draw_networkx_edges(G_doc, pos_doc, alpha=0.2, edge_color='gray', ax=ax2)
    nx.draw_networkx_labels(G_doc, pos_doc, font_size=10, font_weight='bold', ax=ax2)
    ax2.set_title('Breivik: "2083 Manifesto"\nConcept Network', 
                  fontsize=16, fontweight='bold')
    ax2.axis('off')
    
    plt.tight_layout()
    plt.savefig('network_comparison_sidebyside.png', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: network_comparison_sidebyside.png")
    plt.close()

def analyze_network_metrics(G, name):
    """Calculate and print network metrics."""
    print(f"\n{'='*60}")
    print(f"{name} - Network Metrics")
    print(f"{'='*60}")
    
    if len(G.nodes()) == 0:
        print("No nodes in network")
        return {}
    
    print(f"Nodes (concepts): {G.number_of_nodes()}")
    print(f"Edges (co-occurrences): {G.number_of_edges()}")
    
    if G.number_of_edges() > 0:
        print(f"Network density: {nx.density(G):.4f}")
        
        # Most central nodes (most connected concepts)
        centrality = nx.degree_centrality(G)
        top_central = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:10]
        
        print(f"\nTop 10 Most Connected Concepts:")
        for term, score in top_central:
            print(f"  {term}: {score:.3f}")
        
        # Betweenness centrality (bridge concepts)
        if G.number_of_nodes() > 2:
            betweenness = nx.betweenness_centrality(G)
            top_between = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)[:5]
            
            print(f"\nTop 5 'Bridge' Concepts (connect different clusters):")
            for term, score in top_between:
                if score > 0:
                    print(f"  {term}: {score:.3f}")
        
        # Clustering coefficient (how clustered the network is)
        avg_clustering = nx.average_clustering(G)
        print(f"\nAverage clustering coefficient: {avg_clustering:.4f}")
        print(f"  (Higher = more tightly clustered concept groups)")
    
    return centrality if G.number_of_edges() > 0 else {}

def find_strongest_associations(cooccurrence, n=20):
    """Find the strongest term pairs."""
    return sorted(cooccurrence.items(), key=lambda x: x[1], reverse=True)[:n]

def main():
    print("Network Analysis of Key Terms Co-occurrence")
    print("=" * 60)
    
    # Load texts
    print("\nLoading texts...")
    yt_text = load_text(YOUTUBE_FILE)
    doc_text = load_text(DOC_2083_FILE)
    print(f"✓ Peterson video: {len(yt_text)} characters")
    print(f"✓ 2083 manifesto: {len(doc_text)} characters")
    
    # Get keywords
    keywords = get_shared_keywords()
    print(f"✓ Tracking {len(keywords)} key terms")
    
    # Build networks (using window size of 10 words)
    print("\nBuilding co-occurrence networks...")
    G_yt, counts_yt, cooc_yt = build_cooccurrence_network(yt_text, keywords, window_size=10)
    G_doc, counts_doc, cooc_doc = build_cooccurrence_network(doc_text, keywords, window_size=10)
    
    print(f"✓ Peterson network: {G_yt.number_of_nodes()} nodes, {G_yt.number_of_edges()} edges")
    print(f"✓ Breivik network: {G_doc.number_of_nodes()} nodes, {G_doc.number_of_edges()} edges")
    
    # Analyze network metrics
    centrality_yt = analyze_network_metrics(G_yt, "Peterson Video")
    centrality_doc = analyze_network_metrics(G_doc, "2083 Manifesto")
    
    # Strongest associations
    print(f"\n{'='*60}")
    print("Strongest Term Associations (Top 20)")
    print(f"{'='*60}")
    
    print("\nPeterson Video:")
    for (term1, term2), count in find_strongest_associations(cooc_yt, 20):
        print(f"  {term1} ↔ {term2}: {count} co-occurrences")
    
    print("\n2083 Manifesto (Top 20):")
    for (term1, term2), count in find_strongest_associations(cooc_doc, 20):
        print(f"  {term1} ↔ {term2}: {count} co-occurrences")
    
    # Create visualizations
    print(f"\n{'='*60}")
    print("Creating visualizations...")
    print(f"{'='*60}")
    
    visualize_network(G_yt, 
                     'Peterson: "Who Is Teaching Your Kids?"\nConcept Co-occurrence Network',
                     'network_peterson.png',
                     counts_yt)
    
    visualize_network(G_doc,
                     'Breivik: "2083 Manifesto"\nConcept Co-occurrence Network',
                     'network_breivik.png',
                     counts_doc)
    
    compare_networks(G_yt, G_doc, counts_yt, counts_doc)
    
    # Identify unique and shared connections
    print(f"\n{'='*60}")
    print("Comparative Analysis")
    print(f"{'='*60}")
    
    # Edges present in both networks
    yt_edges = set(G_yt.edges())
    doc_edges = set(G_doc.edges())
    
    # Normalize edges (since order doesn't matter)
    yt_edges_normalized = {tuple(sorted(e)) for e in yt_edges}
    doc_edges_normalized = {tuple(sorted(e)) for e in doc_edges}
    
    shared_edges = yt_edges_normalized & doc_edges_normalized
    yt_unique = yt_edges_normalized - doc_edges_normalized
    doc_unique = doc_edges_normalized - yt_edges_normalized
    
    print(f"\nShared concept associations: {len(shared_edges)}")
    if shared_edges:
        print("Examples:")
        for term1, term2 in list(shared_edges)[:10]:
            print(f"  {term1} ↔ {term2}")
    
    print(f"\nUnique to Peterson: {len(yt_unique)}")
    if yt_unique:
        print("Examples:")
        for term1, term2 in list(yt_unique)[:10]:
            print(f"  {term1} ↔ {term2}")
    
    print(f"\nUnique to Breivik: {len(doc_unique)}")
    if doc_unique:
        print("Examples:")
        for term1, term2 in list(doc_unique)[:10]:
            print(f"  {term1} ↔ {term2}")
    
    # Save detailed results
    with open('network_analysis_results.txt', 'w') as f:
        f.write("NETWORK ANALYSIS: CO-OCCURRENCE OF KEY TERMS\n")
        f.write("=" * 70 + "\n\n")
        
        f.write("PETERSON VIDEO NETWORK\n")
        f.write("-" * 70 + "\n")
        f.write(f"Nodes: {G_yt.number_of_nodes()}\n")
        f.write(f"Edges: {G_yt.number_of_edges()}\n")
        if G_yt.number_of_edges() > 0:
            f.write(f"Density: {nx.density(G_yt):.4f}\n\n")
            
            f.write("Top Connections:\n")
            for (t1, t2), count in find_strongest_associations(cooc_yt, 30):
                f.write(f"  {t1} ↔ {t2}: {count}\n")
        
        f.write("\n\n2083 MANIFESTO NETWORK\n")
        f.write("-" * 70 + "\n")
        f.write(f"Nodes: {G_doc.number_of_nodes()}\n")
        f.write(f"Edges: {G_doc.number_of_edges()}\n")
        if G_doc.number_of_edges() > 0:
            f.write(f"Density: {nx.density(G_doc):.4f}\n\n")
            
            f.write("Top Connections:\n")
            for (t1, t2), count in find_strongest_associations(cooc_doc, 30):
                f.write(f"  {t1} ↔ {t2}: {count}\n")
        
        f.write("\n\nCOMPARATIVE ANALYSIS\n")
        f.write("-" * 70 + "\n")
        f.write(f"Shared associations: {len(shared_edges)}\n")
        f.write(f"Unique to Peterson: {len(yt_unique)}\n")
        f.write(f"Unique to Breivik: {len(doc_unique)}\n")
        
        if shared_edges:
            f.write("\nShared concept associations:\n")
            for t1, t2 in sorted(shared_edges):
                f.write(f"  {t1} ↔ {t2}\n")
    
    print("\n✓ Saved detailed results: network_analysis_results.txt")
    print("\n" + "=" * 60)
    print("Analysis complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()
