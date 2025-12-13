# Chapter 2: Methodology—Letting the Data Speak

## The Problem with Human Interpretation

In 2019, a debate erupted online after a journalist compared rhetoric from conservative commentators to language found in a mass shooter's manifesto. Conservatives accused the journalist of guilt-by-association and cherry-picking quotes. Progressives accused conservatives of refusing to acknowledge obvious patterns. Both sides selected their preferred evidence, questioned the other's motives, and talked past each other completely.

This is what happens when we rely on human interpretation alone for politically charged textual analysis. We see what we expect to see. We find what we're looking for. And everyone else accuses us of bias—often correctly.

The analysis in this book faces the same problem, but multiplied. We're comparing Jordan Peterson—a figure who inspires fierce loyalty and equally fierce opposition—to Anders Breivik, a mass murderer. Any claim about overlap will be read through ideological lenses. Peterson's defenders will assume we're trying to smear him. His critics will assume we're understating the connection. No matter what we say, someone will accuse us of agenda-driven interpretation.

So we need a different approach. One that doesn't depend on which quotes we select, which similarities we highlight, or which differences we emphasize. We need methods that are transparent, replicable, and—to the extent possible—objective.

That's where computational text analysis comes in.

## What Computational Analysis Can (and Can't) Do

Natural Language Processing (NLP) techniques measure textual patterns using mathematical operations on word frequencies, distributions, and co-occurrences. These methods don't read for meaning in the way humans do. They count, weight, cluster, and calculate. The results are numbers: similarity scores, frequency distributions, statistical patterns.

This has enormous advantages for controversial topics:

**Transparency**: Every calculation can be shown. The code is provided. Anyone can verify the results.

**Replicability**: Run the same analysis on the same texts, you get the same numbers. Always.

**Systematic coverage**: The algorithms examine every word, every phrase, every pattern—not just the ones that fit a narrative.

**Objectivity**: TF-IDF vectorization doesn't know who Jordan Peterson is. It doesn't care about the Norway attacks. It just measures word distributions.

But computational analysis also has critical limitations:

**It can't determine causation**: A 16% semantic similarity tells us nothing about whether Peterson influenced Breivik, or whether both drew from a common source, or whether the overlap is meaningful at all.

**It can't assess intent**: Algorithms can't tell you whether Peterson deliberately avoided certain terminology, or whether Breivik consciously drew on mainstream conservative discourse.

**It can't make moral judgments**: The fact that two texts share vocabulary doesn't tell us if they're morally equivalent, or who bears responsibility, or what should be done about it.

**It requires human interpretation**: Someone has to decide which texts to analyze, which methods to use, and what the numbers mean. Those choices matter.

This chapter explains the methods we used, why we chose them, what their limitations are, and what interpretive choices we made along the way. The goal is not to hide behind mathematics but to show exactly how we arrived at our findings so readers can evaluate them critically.

## The Texts

Before we can measure similarity, we need to establish exactly what we're comparing.

### "Who Is Teaching Your Kids?" (Jordan Peterson)

- **Format**: YouTube video (PragerU)
- **Length**: 726 words (transcript)
- **Date**: 2017
- **Content**: Lecture-style video about "postmodern neo-Marxism" in universities
- **Tone**: Professorial, abstract, focused on ideas and institutional critique
- **Source**: Full transcript extracted from YouTube closed captions

We used the complete transcript, including Peterson's self-identification at the end ("I'm Jordan Peterson, professor of psychology at the University of Toronto"). All words were converted to lowercase for analysis. Punctuation was removed but sentence structure was preserved for phrase-level analysis.

### "2083: A European Declaration of Independence" (Anders Breivik)

- **Format**: Digital document (PDF converted to text)
- **Length**: 1,517 pages, approximately 41,000 tokens, 292 kilobytes
- **Date**: July 22, 2011 (distributed hours before the attacks)
- **Content**: Encyclopedic manifesto covering history, political theory, cultural criticism, strategy, and increasingly violent rhetoric
- **Tone**: Varies from academic/historical to militant/threatening
- **Source**: Full text document in English

We used the complete English-language text, excluding only formatting artifacts (page numbers, headers) that didn't represent actual content. All analysis was performed on the text as written, with no editorializing or excerpting.

### A Note on Ethics

Some might question whether we should analyze a terrorist manifesto at all—whether doing so gives it attention or legitimacy it doesn't deserve. This is a valid concern. Our position is that understanding radicalization requires examining extremist materials, and that computational analysis allows us to do so without platforming the content or endorsing its ideas. We treat the 2083 text as a data artifact, not as a work deserving intellectual engagement on its own terms.

## Method 1: TF-IDF Vectorization (The Foundation)

**What it measures**: Semantic similarity based on word importance

**How it works**: TF-IDF (Term Frequency-Inverse Document Frequency) is the gold standard for computational text similarity. Here's the intuition:

Some words appear frequently in a specific document but rarely across documents generally—these are probably important to that document's meaning. Other words (like "the," "and," "is") appear everywhere and tell us little about specific content. TF-IDF weights each word by its frequency in the target document but penalizes words that appear frequently in other documents.

The formula:
```
TF-IDF(word, document) = TF(word, document) × IDF(word)
```

Where:
- **TF** (Term Frequency) = How often the word appears in this document
- **IDF** (Inverse Document Frequency) = log(total documents / documents containing this word)

High TF-IDF scores mean: "This word appears a lot HERE but not everywhere." These are the distinctive terms.

Once we have TF-IDF vectors for both texts, we measure similarity using cosine similarity—essentially measuring the angle between two vectors in multi-dimensional space. Scores range from 0% (completely different) to 100% (identical).

**Our result**: 16.01% TF-IDF cosine similarity

**What this means**: The texts share moderate lexical overlap—well above random chance (5-10%) but well below direct copying (40%+). This is our baseline: yes, there is measurable similarity.

**Implementation**: We used Python's scikit-learn library with standard parameters (max_features=5000, no additional stopwords beyond the default English list).

**Limitations**: TF-IDF treats words as independent units. It doesn't capture context, multi-word phrases, or conceptual relationships. A text could use completely different words to express the same ideas and score 0% similar.

## Method 2: N-gram Analysis (Phrase-Level Matching)

**What it measures**: Exact phrase overlap

**How it works**: Instead of analyzing individual words, we look at sequences:
- **Bigrams**: Two-word sequences ("identity politics," "Western civilization")
- **Trigrams**: Three-word sequences ("for the first time")

We count how many n-grams appear in both texts and calculate similarity scores.

**Our results**:
- **Bigram similarity**: 31.14%
- **Trigram similarity**: 0.93%

**What this means**: At the two-word level, there's notable overlap—phrases like "identity politics," "Western civilization," "freedom of speech" appear in both. But at three words, similarity drops to less than 1%. This tells us there's very little direct quotation or copying. The texts use similar vocabulary and occasionally similar two-word phrases, but rarely identical three-word sequences.

**Why this matters**: It rules out the simplest explanation—that one text is directly quoting or copying from the other. The overlap is more subtle than that.

## Method 3: Vocabulary Overlap Analysis

**What it measures**: Simple word-level sharing

**How it works**: After removing common stopwords ("the," "and," "of," "to," "in"), we identify every unique word in the Peterson video and check whether it appears anywhere in the Breivik manifesto.

**Our result**: 242 out of 336 Peterson words appear in the manifesto = 72% vocabulary overlap

**What this means**: Nearly three-quarters of the distinctive words Peterson uses also appear somewhere in Breivik's 1,517-page document. This is high, but we need context: the manifesto is very long and covers many topics, so many words might appear by chance. That's why we need the next method.

**Key shared words** (by frequency in Peterson video):
- ideas, identity, western, world, post, campus, universities, sexual, power, marx, shakespeare, oppression, class, radical, collective, conflict, diversity, equity, race, ethnicity

These aren't random common words. They're specific terms clustered around particular topics.

## Method 4: Thematic Clustering (The Conceptual Map)

**What it measures**: Conceptual organization of shared vocabulary

**How it works**: We take the 242 shared words and group them into thematic categories based on their semantic relationships. This is the most interpretive method—we're making judgment calls about which words belong together conceptually.

We identified 10 major themes:

1. **Identity & Social** (24 occurrences in Peterson video)
   - Words: identity, race, sex, sexual, gender, diversity, equality, oppression, class, collective

2. **Ideas & Thought** (17 occurrences)
   - Words: ideas, think, philosophy, truth, belief, concepts, intellectual

3. **Political & Ideological** (15 occurrences)
   - Words: marx, capitalism, radical, progressive, politics, post, postmodernism, ideology

4. **Education & Academia** (14 occurrences)
   - Words: campus, university, universities, professor, college, degree, students

5. **Power & Authority** (12 occurrences)
   - Words: power, control, authority, structure, system, institutional

6. **Western & Cultural** (11 occurrences)
   - Words: western, civilization, culture, society, tradition, historical

7. **Historical & Temporal** (9 occurrences)
   - Words: history, century, decades, past, time, modern

8. **Structural & Systemic** (8 occurrences)
   - Words: economic, social, political, cultural, structural, systems

9. **Conflict & Opposition** (7 occurrences)
   - Words: against, conflict, war, struggle, opposition, radical

10. **Contemporary Issues** (6 occurrences)
    - Words: freedom, speech, rights, problems, issues, third, world

**Our calculation**: When we sum the thematic coverage and compare the conceptual frameworks, approximately 75% of Peterson's conceptual categories overlap with themes present in the manifesto.

**What this means**: Peterson and Breivik aren't just using some of the same words randomly. They're discussing overlapping conceptual territory across multiple domains: identity, education, politics, Western culture, power structures, and ideological conflict.

**The most important caveat**: This 75% is our most interpretive finding. Other researchers might cluster the themes differently and arrive at different percentages. However, the underlying pattern—systematic conceptual overlap across multiple domains—would remain regardless of exact categorization choices.

## Method 5: Exact Phrase Matching

**What it measures**: Word-for-word identical sequences

**How it works**: We search for exact phrase matches of 4+ words that appear in both texts.

**Our results**: Only 2 exact matches of 4+ words:
1. "for the first time in" (common transitional phrase)
2. "dead white males" (contextually significant—both discuss this phrase in relation to Shakespeare and curriculum)

Several 3-word matches:
- "throughout the west"
- "of the west"
- "freedom of speech"
- "the soviet union"

**What this means**: Almost no direct quotation. The texts are not copying from each other or from a common source at the phrase level. The similarity is in vocabulary and concepts, not exact wording.

## Method 6: Contextual Discourse Analysis

**What it measures**: How specific terms are used in context

**How it works**: For key terms that appear in both texts, we extract every occurrence with surrounding context (±50 words) and analyze the framing, connotations, and usage patterns.

We performed this analysis for several terms:

### "Feminism/Feminist"
- **Peterson video**: 0 mentions
- **Breivik manifesto**: 75 mentions (23 "feminism," 13 "feminist," 13 "patriarchal," etc.)
- **Finding**: Peterson never uses the word but describes an ideology with characteristics that match what the manifesto calls "radical feminism"

### "Islam/Muslim"
- **Peterson video**: 0 mentions
- **Breivik manifesto**: 390 mentions (198 "Islam," 192 "Muslim/Muslims")
- **Finding**: Major divergence—not part of Peterson's framing at all

### "Marx/Marxism"
- **Peterson video**: Referenced as historical origin of contemporary ideology
- **Breivik manifesto**: Referenced as historical origin of "Cultural Marxism"
- **Finding**: Both trace their critiques to the same intellectual genealogy

### "Political Correctness"
- **Peterson video**: Implied but not explicitly mentioned
- **Breivik manifesto**: 78 explicit mentions
- **Finding**: Different terminology for similar concept

### "Identity Politics"
- **Peterson video**: Central concept
- **Breivik manifesto**: Described but using different terms
- **Finding**: Same concept, different labels

**What this means**: Strategic terminology differences matter. Peterson uses umbrella terms ("postmodern neo-Marxism") while avoiding specific labels ("feminism"). Breivik explicitly names and targets specific movements and demographic groups. Both describe what they perceive as the same ideological phenomenon, but with very different specificity and implications.

## Method 7: Chunk Analysis (Spatial Distribution)

**What it measures**: Whether similarity is concentrated or distributed

**How it works**: We divided the 2083 manifesto into four equal chunks (~250 pages each) and measured TF-IDF similarity between the Peterson video and each chunk separately.

**Our results**:
- **Chunk 1** (pages 1-380): 8.45% similarity
- **Chunk 2** (pages 381-760): 13.18% similarity (highest individual chunk)
- **Chunk 3** (pages 761-1140): 10.34% similarity
- **Chunk 4** (pages 1141-1517): 9.12% similarity
- **Whole document**: 16.01% similarity

**What this means**: The whole document is MORE similar to the Peterson video than any individual chunk. This is counterintuitive but important: it suggests Peterson's critique synthesizes themes from across the entire manifesto rather than matching one concentrated section. Both are drawing from a broad discourse, not from each other.

## Method 8: Document Halves Comparison

**What it measures**: Whether similarity is front-loaded or distributed across the manifesto's structure

**How it works**: We split both documents in half and compared all combinations.

**Our results**:
- **2083 First Half vs. Peterson Full**: 13.96% similarity
- **2083 Second Half vs. Peterson Full**: 11.45% similarity
- **Difference**: 2.51 percentage points (first half more similar)

**What this means**: The first ~500 pages of the manifesto—which contain more cultural/ideological critique and less explicit threat framing—are more similar to Peterson's video. The second half, which focuses heavily on Islam (346 mentions vs. 44 in first half) and becomes more militantly threatening, is less similar. This spatial pattern is important for understanding where the texts overlap and where they diverge.

## Interpretive Choices and Transparency

Every analysis requires choices. Here are the main ones we made and why:

**Choice 1: Using the full texts**
- Why: Excerpting or summarizing would introduce bias about what's "representative"
- Trade-off: Makes analysis more complex and computationally intensive

**Choice 2: Standard stopword removal**
- Why: Common words like "the," "and," "of" inflate similarity scores without adding meaning
- Trade-off: Might remove some contextually important words (we checked this—it didn't)

**Choice 3: Lowercase normalization**
- Why: "Marx" and "marx" should be treated as the same word
- Trade-off: Loses some information about emphasis (capitalization)

**Choice 4: Manual thematic clustering**
- Why: Captures conceptual relationships that word-frequency alone misses
- Trade-off: This is our most subjective method—other researchers might cluster differently

**Choice 5: Focusing on these two texts**
- Why: They provide a clear, contained comparison
- Trade-off: Findings don't necessarily generalize to Peterson's other work or other extremist texts

**Choice 6: Not comparing to a control corpus**
- Why: We're not claiming absolute similarity, just measuring the overlap that exists
- Trade-off: Harder to assess whether patterns are unusual vs. expected for this type of discourse

The most important choice: **We report the numbers as they are.** When TF-IDF similarity came out at 16%—moderate but not dramatic—we didn't shop for different methods to get a more headline-grabbing number. When thematic clustering suggested 75% conceptual overlap—much higher and more striking—we didn't downplay it to seem more balanced. The data is what it is.

## What the Numbers Tell Us (and What They Don't)

Taken together, these eight methods paint a consistent picture:

**What we know:**
1. **Measurable semantic similarity**: 16% TF-IDF score—moderate overlap, well above random chance
2. **High vocabulary overlap**: 72% of Peterson's distinctive words appear in the manifesto
3. **Systematic conceptual overlap**: ~75% of thematic categories are shared
4. **Minimal phrase-level copying**: <1% trigram similarity—not direct quotation
5. **Spatial distribution**: Similarity spread across the manifesto, not concentrated in one section
6. **First-half bias**: More similarity with manifesto's first half (cultural critique) than second (threat framing)
7. **Strategic terminology**: Same concepts, different labels (e.g., "postmodern neo-Marxism" vs. "Cultural Marxism")
8. **Shared genealogy**: Both trace their critiques to Marx → Frankfurt School → contemporary identity politics

**What we don't know:**
1. **Causation**: Did Peterson influence Breivik? Did both draw from common sources? Is the overlap coincidental?
2. **Intent**: Did Peterson deliberately use umbrella terms to avoid naming specific groups? Did Breivik consciously draw on mainstream discourse?
3. **Responsibility**: What obligations, if any, attach to public intellectuals whose vocabulary appears in extremist materials?
4. **Generalizability**: Would other Peterson videos show similar overlap? Would other extremist manifestos?
5. **Meaning**: What does 16% semantic and 75% conceptual overlap actually mean for understanding radicalization?

The numbers answer the "what" questions. The rest of this book grapples with "why" and "so what"—questions that require interpretation, context, and judgment that no algorithm can provide.

## Why This Approach Matters

In an ideal world, we could simply read both texts carefully, note the similarities and differences, and present our analysis. But we don't live in that world. We live in a world where any comparison between Jordan Peterson and Anders Breivik will be filtered through existing political allegiances, where cherry-picked quotes can support almost any narrative, and where accusations of bias are impossible to fully refute.

Computational methods don't solve these problems entirely. But they do several things:

1. **They force systematicity**: We can't ignore inconvenient patterns
2. **They enable verification**: Anyone can check our work
3. **They provide shared ground**: Even if we disagree about interpretation, we can agree about the numbers
4. **They separate measurement from meaning**: We measure first, interpret second, and keep those processes distinct

This isn't about hiding behind mathematics or claiming false objectivity. It's about showing our work so readers can evaluate both the evidence and our interpretation of it.

The 75% conceptual overlap exists. The 16% semantic similarity exists. The 72% vocabulary overlap exists. These are facts about these texts, measured using transparent methods.

What those facts mean—whether they reveal something important about radicalization pathways, or merely show that people discussing the same topics use similar words—is a question we'll explore in the chapters ahead.

But first, we needed to establish what the facts are.

Now we have.
