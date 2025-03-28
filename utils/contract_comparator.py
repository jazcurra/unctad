# utils/contract_comparator.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def compare_contracts(contract1_text, contract2_text):
    """Compares two contracts and returns a similarity score."""
    try:
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform([contract1_text, contract2_text])
        similarity_score = cosine_similarity(vectors)[0, 1]
        return similarity_score
    except Exception as e:
        print(f"Error comparing contracts: {e}")
        return 0.0

#Example Usage
if __name__ == "__main__":
    contract1 = "This is the first contract. It has some common clauses."
    contract2 = "This is the second contract. It also has similar clauses."
    similarity = compare_contracts(contract1, contract2)
    print(f"Similarity Score: {similarity}")