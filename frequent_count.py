import os
from collections import defaultdict
import unicodedata
import random
import string


def letter_count(text):
    counters = defaultdict(int)
    for char in text:
        if char.isalpha() and char != "":
            char = remove_accents(char)
            counters[char] += 1
    return counters


def frequent_count(text, threshold):
    """function used to implement the frequent count algorithm"""
    counters = defaultdict(int)
    for char in text:
        if char.isalpha() and char != "":
            char = remove_accents(char)
            counters[char] += 1

    sortedDict = sorted(counters.items(), key=lambda x: x[1], reverse=True)
    for letter, count in sortedDict:
        print("%5s : %3d" % (letter, count))

    frequent_items = []
    for item, count in counters.items():
        if count > threshold:
            frequent_items.append(item)
    return frequent_items


def incrementLetter(x, m):
    t = x // m
    while t > 0:
        if random.getrandbits(1) == 1:
            return x
        t -= 1
    return x + 1


def estimate_frequent_letters(text, threshold):
    """function used to implement the Csuros counter algorithm"""
    letter_count = {letter: 0 for letter in string.ascii_uppercase}

    for char in text:
        if char.isalpha():
            char = remove_accents(char)
            if char != "":
                letter_count[char] = incrementLetter(letter_count[char], threshold)

    sorted_letters = sorted(letter_count, key=lambda x: letter_count[x], reverse=True)

    return sorted_letters, letter_count


# remove accents from a string
def remove_accents(letter):
    return unicodedata.normalize("NFD", letter).encode("ascii", "ignore").decode()


if __name__ == "__main__":
    all_text_files = os.listdir("collections")

    for file in all_text_files:
        file = open("collections/" + file, "r")
        text = file.read().upper()
        file.close()

        print(file.name.replace("collections/", "").upper().center(24, "-"))
        print("{:s}".format("Basic Counter"))
        counter = letter_count(text)
        for letter, freq in counter.items():
            print("%5s : %3d" % (letter, freq))

        print("{:s}".format("Csuros Counter"))
        sorted_letters = estimate_frequent_letters(text, 5000)
        letters, dict_freq = sorted_letters
        for letter, freq in dict_freq.items():
            print("%5s : %3d" % (letter, freq))
        print(letters)

        print("{:s}".format("Frequent Counter"))
        print(frequent_count(text, 5000), end="\n\n")
