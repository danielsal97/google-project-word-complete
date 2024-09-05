import pickle
import re


def read_file_and_build_structures(file_path, word_trie):
    """
    Reads a file and builds the Trie structure for words and sentences.
    """
    with open(file_path, 'r') as file:
        file_name = file_path.split('/')[-1]
        line_offset = 0
        for line in file:
            sentence = line.strip()

            doc_info = (file_name, line_offset, sentence)  # Include sentence, file name, and line number
            word_trie.insert(sentence.lower(), doc_info)  # Insert the full sentence

            words = re.findall(r'\b\w+\b', sentence.lower())  # Extract words from the sentence
            for word in words:
                word_trie.insert(word, doc_info)  # Insert each word into the Trie

            line_offset += 1


def save_data(word_trie, output_file='word_trie_data.pkl'):
    """
    Saves the Trie structure to a pickle file.
    """
    try:
        with open(output_file, 'wb') as f:
            pickle.dump(word_trie, f)
        print(f"Data successfully saved to {output_file}")
    except Exception as e:
        print(f"An error occurred while saving data: {e}")


def load_data(file_path='word_trie_data.pkl'):
    """
    Loads the Trie structure from a pickle file.
    """
    try:
        with open(file_path, 'rb') as f:
            return pickle.load(f)
    except Exception as e:
        print(f"An error occurred while loading data: {e}")
        return None
