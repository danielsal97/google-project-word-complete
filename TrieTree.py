import re
from rapidfuzz.distance.metrics_cpp import levenshtein_distance

from score_calculation import calculate_score


class WordTrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.inverted_index = set()  # Store sentences or document info


def _find_corrections(word):
    """
    Find possible corrections for the given word using Damerau-Levenshtein-like operations.
    Includes substitution, insertion, deletion, and transposition.
    Only returns corrections with a Levenshtein distance of 1.
    """
    letters = 'abcdefghijklmnopqrstuvwxyz'
    corrections = set()

    # Substitution: Replace each character with every letter in the alphabet
    for i in range(len(word)):
        for letter in letters:
            if letter != word[i]:  # Avoid replacing the same letter
                corrected_word = word[:i] + letter + word[i + 1:]
                corrections.add(corrected_word)

    # Insertion: Insert a letter at each position
    for i in range(len(word) + 1):
        for letter in letters:
            corrected_word = word[:i] + letter + word[i:]
            corrections.add(corrected_word)

    # Deletion: Remove each character
    for i in range(len(word)):
        corrected_word = word[:i] + word[i + 1:]
        corrections.add(corrected_word)

    # Transposition: Swap adjacent characters
    for i in range(len(word) - 1):
        if word[i] != word[i + 1]:  # Avoid unnecessary swaps of the same character
            corrected_word = word[:i] + word[i + 1] + word[i] + word[i + 2:]
            corrections.add(corrected_word)

    # Filter the corrections to only allow those with a Levenshtein distance of 1
    valid_corrections = {correction for correction in corrections if levenshtein_distance(word, correction) == 1}

    return valid_corrections


def _collect_results(node, prefix):
    results = []
    nodes_to_visit = [(node, prefix)]
    while nodes_to_visit:
        current_node, current_prefix = nodes_to_visit.pop()
        if current_node.is_end_of_word:
            for doc_info in current_node.inverted_index:
                original_sentence = doc_info[2]  # Full original sentence
                score = calculate_score(prefix, original_sentence)  # Calculate score
                results.append((doc_info, score))
        for char, child_node in current_node.children.items():
            nodes_to_visit.append((child_node, current_prefix + char))
    return sorted(results, key=lambda x: x[1], reverse=True)[:5]  # Top 5 results


class WordTrie:
    def __init__(self):
        self.root = WordTrieNode()

    def insert(self, text, doc_info):
        text = text.lower()  # Insert the word in lowercase for case-insensitive search
        node = self.root
        for char in text:
            if char not in node.children:
                node.children[char] = WordTrieNode()
            node = node.children[char]
        node.is_end_of_word = True
        node.inverted_index.add(doc_info)  # Store sentence, file info, and line number

    def search_substring(self, substring):
        substring = substring.lower()  # Case-insensitive search
        results = self._search_exact(substring)

        if not results:
            corrections = _find_corrections(substring)
            for corrected_word in corrections:
                results = self._search_exact(corrected_word)
                if results:
                    break

        return results or "No results found."

    def _search_exact(self, substring):
        node = self.root
        for char in substring:
            if char in node.children:
                node = node.children[char]
            else:
                return None
        return _collect_results(node, substring)

