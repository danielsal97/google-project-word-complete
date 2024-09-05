import re
from rapidfuzz.distance import Levenshtein

def calculate_score(user_input, sentence):
    """
    Calculate the match score based on how similar the user_input is to the sentence,
    with penalties for substitutions, insertions, and deletions, even when the input is a substring.
    """
    # Normalize both input and sentence to lower case and remove only spaces
    user_input_clean = user_input.lower().strip()
    sentence_clean = sentence.lower().strip()

    # Base score: 2 points per matching character
    base_score = 2 * len(user_input_clean)

    # Calculate Levenshtein distance
    distance = Levenshtein.distance(user_input_clean, sentence_clean)

    # If input is an exact match or a substring, reduce the penalty but still apply it based on distance
    if user_input_clean in sentence_clean:
        if len(user_input_clean) == len(sentence_clean):
            return len(user_input_clean) * 2

        # Even if it's a substring, apply a small penalty for extra characters
        extra_characters = len(sentence_clean) - len(user_input_clean)
        penalty = extra_characters * 2  # Example penalty: 2 points per extra character
        return max(base_score - penalty, 0)  # Ensure the score doesn't go below zero

    # Apply penalties based on the Levenshtein distance
    if distance == 1:
        return max(base_score - 1, 0)  # Small penalty for 1 character difference
    elif distance > 1:
        return max(base_score - distance * 2, 0)  # Larger penalty for more than 1 character difference

    return base_score

def process_sentences(user_input, sentences):
    """
    Process the list of sentences and return the scores for each sentence.
    """
    results = []
    for sentence in sentences:
        score = calculate_score(user_input, sentence)
        results.append((sentence, score))
    return results