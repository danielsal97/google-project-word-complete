import os
import sys
from FileHandler import load_data, save_data, read_file_and_build_structures
from TrieTree import WordTrie
from score_calculation import calculate_score


def search_with_score(trie, user_input):
    """
    Search for the closest matching words or sentences in the trie
    and calculate the score between the user's input and the matches.
    """
    occurrences = trie.search_substring(user_input)  # Retrieve matches from the trie

    results = []
    if occurrences != "No results found.":
        for doc_info in occurrences:
            file_info, _ = doc_info
            if isinstance(file_info, tuple) and len(file_info) >= 3:
                sentence = file_info[2]
                calculated_score = calculate_score(user_input, sentence)
                results.append((file_info, calculated_score))
    return results


# Display search results with their calculated scores
def display_results(results, user_input):
    """
    Display the search results with their calculated scores.
    """
    if results:
        print(f"\nOccurrences of '{user_input}':")
        for file_info, score in results:
            file_name, line_number, sentence = file_info
            print(f"- File: {file_name} , Line: {line_number + 1} , Sentence: {sentence} , Score: {score}")
    else:
        print(f"No results found for '{user_input}'.")


# Main program logic
if __name__ == '__main__':
    sys.setrecursionlimit(10000)  # Increase recursion limit for deep tries
    print("Welcome to the auto word completion program!")

    # Step 1: Ask if the user wants to upload new data or load previously saved data
    upload_data = input("Do you want to upload new data from a directory?\nEnter 'yes' for upload or any other key to load existing data: ")

    if upload_data.lower() == "yes":
        directory = input("Enter the path of the data directory: ")
        if not os.path.isdir(directory):
            print("Invalid directory. Please try again.")
            exit(1)

        word_trie = WordTrie()
        print("Creating new dataset...")

        # Walk through the directory and process text files
        for root, dirs, files in os.walk(directory):
            for file_name in files:
                if file_name.endswith('.txt'):  # Only process text files
                    file_path = os.path.join(root, file_name)
                    read_file_and_build_structures(file_path, word_trie)

        # Save the Trie structure for future use
        save_data(word_trie, 'word_trie_data.pkl')
        print("Data from the directory uploaded and saved successfully!")

    else:
        # Load the previously saved trie from the pickle file
        print("Loading existing trie data...")
        word_trie = load_data('word_trie_data.pkl')

        if word_trie:
            print("Trie loaded successfully!")
        else:
            print("Error: Could not load the trie data.")
            exit(1)

    # Step 2: User interaction loop for searching words or substrings
    user_input = input("Enter your word or substring (type 'exit' to quit): ").strip()

    while user_input != "exit":
        results = search_with_score(word_trie, user_input)
        display_results(results, user_input)

        # Ask for the next word or substring to search for
        user_input = input("Enter your word or substring: ").strip()

    print("Exiting the program.")