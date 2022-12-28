from collections import Counter
import random


def count_frequent_letters(text):
  """Count exactly the number of times each letter appears in the text."""
  # create a dictionary to store the letter counts
  letter_counts = {}

  # open the file and read its contents

  # iterate over each character in the file contents
  for c in text:
    # only count letters (ignore spaces, punctuation, etc.)
    if c.isalpha():
      # convert the letter to lowercase
      c = c.lower()
      # if the letter is already in the dictionary, increment its count
      if c in letter_counts:
        letter_counts[c] += 1
      # if the letter is not yet in the dictionary, add it with a count of 1
      else:
        letter_counts[c] = 1
  
  sorted_counts = sorted(letter_counts.items(), key=lambda x: x[1], reverse=True)

  # return the sorted dictionary
  return sorted_counts

def most_frequent_letters(data_stream, window_size):
  # create a Counter to store the counts of letters in the window
  counts = Counter()

  # initialize a list to store the most frequent letters and their counts
  most_frequent = []

  # iterate over the data stream
  for letter in data_stream:
    # only count letters (ignore spaces, punctuation, etc.)
    if letter.isalpha():
      letter = letter.lower()
      # add the new letter to the Counter
      counts[letter] += 1

      # if the Counter is full (i.e., has reached the window size), remove the oldest letter
      if len(counts) > window_size:
        del counts[letter[0]]

      # if the letter has a count greater than or equal to the maximum count in the Counter, add it to the list of most frequent letters
      if counts[letter] == counts.most_common(1)[0][1]:
        most_frequent.append((letter, counts[letter]))

  # return the list of most frequent letters and their counts
  return most_frequent

def approximateAlgorithm(text):
  # create a Counter to store the letter counts
  letter_counts = Counter()



  # iterate over each character in the file contents
  for c in text:
    # only count letters (ignore spaces, punctuation, etc.)
    if c.isalpha():
      c = c.lower()
      letter_counts[c] += 1

  # get the most common letters and their counts
  most_common = letter_counts.most_common()

  # return the most common letters and their counts
  return most_common

def approximate_count(text, sample_size):
  # create a dictionary to store the counts of the letters in the sample
  counts = {}

  # initialize a variable to track the number of letters seen so far
  n = 0

  # iterate over each character in the text
  for c in text:
    # only count letters (ignore spaces, punctuation, etc.)
    if c.isalpha():
      c = c.lower()
      n += 1

      # with probability 1/n, add the letter to the sample and update its count
      if random.random() < 1.0 / n:
        if c in counts:
          counts[c] += 1
        else:
          counts[c] = 1

  # return the counts of the letters in the sample
  return counts


if __name__ == "__main__":
    file = open("collections/indianTailes.txt", "r")
    text = file.read()
    file.close()

    letters_freq = count_frequent_letters(text)
    most_frequent = letters_freq[:3]
    print("exact: " , most_frequent)


    letter_counts = approximate_count(text, 1000)
    print("Approximate: " , letter_counts)

    

