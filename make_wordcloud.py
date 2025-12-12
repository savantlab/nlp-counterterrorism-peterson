#!/usr/bin/env python3
"""
Generate word cloud from the shared words list file.
"""

from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Read the shared words with frequencies from file
word_freq = {}

print("Reading shared words file...")
with open('shared_words_by_yt_frequency.txt', 'r') as f:
    lines = f.readlines()
    
    # Skip header lines
    for line in lines:
        line = line.strip()
        if not line or '=' in line or '-' in line or 'Total:' in line or 'Word' in line:
            continue
        
        # Parse: "word              YT_freq    Doc_freq"
        parts = line.split()
        if len(parts) >= 2:
            word = parts[0]
            try:
                yt_freq = int(parts[1])
                word_freq[word] = yt_freq
            except:
                continue

print(f"Loaded {len(word_freq)} words\n")

# Create word cloud
print("Generating word cloud...")
wordcloud = WordCloud(
    width=1600,
    height=800,
    background_color='white',
    colormap='viridis',
    relative_scaling=0.5,
    min_font_size=12,
    max_words=200
).generate_from_frequencies(word_freq)

# Create figure
fig, ax = plt.subplots(figsize=(20, 10))
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis('off')
ax.set_title(f'Shared Vocabulary Word Cloud ({len(word_freq)} words, sized by YouTube frequency)',
             fontsize=20, fontweight='bold', pad=20)

# Save
plt.tight_layout()
plt.savefig('wordcloud_shared_vocabulary.png', dpi=300, bbox_inches='tight', facecolor='white')
print("✓ Saved: wordcloud_shared_vocabulary.png\n")

# Show top words
print("Top 20 words:")
sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
for word, freq in sorted_words[:20]:
    print(f"  {word}: {freq}")

# Display
plt.show()
