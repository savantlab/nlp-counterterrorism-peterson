# NLP Analysis: Document Similarity Study

This project analyzes textual similarity between two documents using NLP techniques.

## Files

- `2083. EUROPEAN DECLARATION OF INDEPENDENCE.txt` - Source document (292KB, ~41K tokens)
- `youtube_transcript_clean.txt` - YouTube video transcript (4.4KB, 726 tokens)
- `bag_of_words_score.py` - Simple bag-of-words cosine similarity
- `tfidf_score.py` - TF-IDF based cosine similarity

## Results

### Bag of Words Similarity
- **Score: 91.05%**
- Common terms: 306 out of 401 (76.3% vocabulary overlap)
- This method weights all words equally, leading to high similarity due to common stop words

### TF-IDF Similarity  
- **Score: 0.00%**
- With only 2 documents, IDF calculation assigns 0 weight to shared terms
- Top unique terms in YouTube transcript: modernists, equity, oppressive, inclusion, poor, prager

## Analysis

The high bag-of-words score indicates significant vocabulary overlap, but the TF-IDF approach reveals that most overlap comes from common words. The unique, topic-specific terms in the YouTube transcript are not present in the larger document.

## Usage

```bash
python3 bag_of_words_score.py
python3 tfidf_score.py
```

## Requirements

- Python 3
- Standard library only (re, collections, math)
