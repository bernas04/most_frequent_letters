import os
from collections import defaultdict
import unicodedata


def frequent_count(text, threshold):
    counters = defaultdict(int)
    for char in text:
        if char.isalpha():
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


def csuros_counter(text, n):
    counters = defaultdict(int)
    for letter in text:
        if letter.isalpha():
            letter = remove_accents(letter)
            counters[letter] += 1

    sorted_counters = sorted(counters.items(), key=lambda x: x[1], reverse=True)
    return sorted_counters[:n]


# remove accents from a string
def remove_accents(letter):
    return unicodedata.normalize("NFD", letter).encode("ascii", "ignore").decode()


if __name__ == "__main__":
    all_text_files = os.listdir("collections")

    for file in all_text_files:
        file = open("collections/" + file, "r")
        text = file.read().upper()
        file.close()

        print("%10s - %10s" % ("Frequen Count", file.name.replace("collections/", "")))
        print(frequent_count(text, 5000), end="\n\n")
        print("%10s" % ("Csuros Counter"))
        print(csuros_counter(text, 3), end="\n\n")
