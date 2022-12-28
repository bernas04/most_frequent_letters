from collections import Counter
from probstructs import CountMinSketch


def most_frequent_letters(text):
    # Create an empty Csuros' counter with Frequent-Count
    letter_counts = Counter()

    # Iterate through each character in the text and add it to the Csuros' counter with Frequent-Count
    for char in text:
        if char.isalpha():
            letter_counts[char.lower()] += 1

    # Find the most frequent letters using the most_common method of the Csuros' counter with Frequent-Count
    # TODO: Change the parameter to 1,3,5 and 10
    most_common_letters = letter_counts.most_common(3)

    # Print the letters with the highest count
    # If there is a tie for the highest count, print all the letters with the highest count
    for letter, count in most_common_letters:
        print(f"{letter}: {count}")


def most_frequent_letters_approx(text, error_rate, confidence_level):
    # Create a Count-Min Sketch with the desired error rate and confidence level
    sketch = CountMinSketch(error_rate, confidence_level)

    # Iterate through each character in the text and add it to the Count-Min Sketch
    for char in text:
        if char.isalpha():
            sketch.add(char.lower())

    # Create an empty dictionary to store the letter counts
    letter_counts = {}

    # Iterate through each letter in the alphabet
    for letter in "abcdefghijklmnopqrstuvwxyz":
        # Get the approximate count of the letter from the Count-Min Sketch
        count = sketch.estimate(letter)
        # Add the count to the dictionary with the letter as the key and the count as the value
        letter_counts[letter] = count

    # Sort the dictionary by the count of each letter in descending order
    sorted_letter_counts = sorted(
        letter_counts.items(), key=lambda x: x[1], reverse=True
    )

    # Print the 3 letters with the highest count
    for letter, count in sorted_letter_counts[:3]:
        print(f"{letter}: {count}")


if __name__ == "__main__":
    with open("anteroQuental.txt", "r") as f:
        text = f.read()

        most_frequent_letters(text)
        most_frequent_letters_approx(text, 0.01, 0.95)
