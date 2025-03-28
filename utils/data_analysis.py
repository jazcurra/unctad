# utils/data_analysis.py
import re
from collections import Counter

def extract_keywords(text, num_keywords=10):
    """Extracts keywords from the contract text."""
    try:
        # Remove punctuation and convert to lowercase
        text = re.sub(r'[^\w\s]', '', text).lower()
        words = text.split()

        # Remove common stop words (you can expand this list)
        stop_words = set(["the", "a", "an", "is", "are", "of", "in", "to", "and", "for", "this", "that", "it", "be"])
        words = [word for word in words if word not in stop_words]

        # Count word frequencies
        word_counts = Counter(words)

        # Get the most common words as keywords
        keywords = [word for word, count in word_counts.most_common(num_keywords)]
        return keywords
    except Exception as e:
        print(f"Error extracting keywords: {e}")
        return []