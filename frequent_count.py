import sys, getopt
import os
from collections import defaultdict
import unicodedata
import random
import string
import time


def letter_count(text):
    """function used to implement the basic counter algorithm"""
    counters = defaultdict(int)
    for char in text:
        if char.isalpha() and char != "":
            char = remove_accents(char)
            counters[char] += 1
    sorted_counters = sorted(counters.items(), key=lambda x: x[1], reverse=True)
    return sorted_counters


def frequent_count(text, k):
    """function used to implement the frequent counter algorithm"""
    counts = {}
    for element in text:
        if element.isalpha():
            element = remove_accents(element)
            if element in counts:
                counts[element] += 1
            elif len(counts) < k - 1:
                counts[element] = 1
            else:
                for i in list(counts.keys()):
                    counts[i] -= 1
                    if counts[i] == 0:
                        del counts[i]

    if len(counts) > 0:
        return max(counts, key=counts.get), sorted(
            counts.items(), key=lambda x: x[1], reverse=True
        )
    else:
        return None, None


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

    sorted_letters = sorted(letter_count.items(), key=lambda x: x[1], reverse=True)
    return sorted_letters


# remove accents from a string
def remove_accents(letter):
    """function used to remove accents from a letter"""
    return unicodedata.normalize("NFD", letter).encode("ascii", "ignore").decode()


def remove_punctuation(text):
    """function used to remove punctuation from a text"""
    translator = str.maketrans("", "", string.punctuation)

    return text.translate(translator)


def getArgs(argv):
    folder = "collections/"
    opts, args = getopt.getopt(argv, "hf:", ["folder="])
    for opt, arg in opts:
        if opt == "-h":
            print("python3 frequent_count.py -f <folderToFiles>")
            sys.exit()
        elif opt in ("-f", "--folder"):
            folder += arg
    return folder


def getAllFiles(folder):
    all_files = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(".txt"):
                tmp = root + "/" + file
                all_files.append(tmp)
    return all_files


if __name__ == "__main__":

    folder = getArgs(sys.argv[1:])

    absoluteErrorCsurosCounterAvg = 0
    absoluteErrorFrequentCounterAvg = 0
    relativeErrorCsurosCounterAvg = 0
    relativeErrorFrequentCounterAvg = 0
    numFiles = 0

    all_text_files = getAllFiles(folder)

    if not os.path.isdir("results"):
        os.mkdir("results")

    for file in all_text_files:
        numFiles += 1
        start = time.time()

        # abre o ficheiro de texto
        f = open(file, "r")
        # lê o ficheiro, remove espaços em branco e converte para maiúsculas
        text = f.read().strip().upper()
        # remove pontuação
        text = remove_punctuation(text)
        # converte o texto numa lista de palavras
        text = text.split(" ")

        # remove os \n e espaços em branco
        text = [word.replace("\n", "") for word in text if word != ""]
        # fecha o ficheiro
        f.close()

        # vê qual o idioma do ficheiro para abrir o ficheiro de stopwords correto
        name, language = file.split("/")[-1].split("_")
        language = language.replace(".txt", "")

        print(file.upper(), end="\r")
        # abre o ficheiro de stopwords
        f = open("stopwords/stopwords_" + language + ".txt", "r")
        # lê o ficheiro, remove espaços em branco, converte para maiúsculas e guarda numa lista
        stopWords = f.read().strip().upper().split("\n")

        # remove os espaços em branco
        stopWords = [word for word in text if word != ""]
        # fecha o ficheiro
        f.close()

        # remove as stopwords do texto
        for word in text:
            if word in stopWords:
                text.remove(word)

        text = " ".join(text)

        elapsedTimeTreatingFile = time.time() - start

        resultsFile = open(f"results/{name}_{language}.txt", "w")

        resultsFile.write("{:s}\n".format("Basic Counter"))

        # Exact counter
        startAlgorithm = time.time()
        exact_counter = letter_count(text)
        for letter, freq in exact_counter:
            resultsFile.write("%5s : %3d\n" % (letter, freq))

        totalElapsedTime = time.time() - startAlgorithm + elapsedTimeTreatingFile
        resultsFile.write(
            "{:s} : {:f}\n".format("Total Elapsed Time", totalElapsedTime)
        )
        #

        # Csuros counter
        startAlgorithm = time.time()
        resultsFile.write("\n{:s}\n".format("Csuros Counter"))
        sorted_letters = estimate_frequent_letters(text, 5000)
        for letter, freq in sorted_letters:
            resultsFile.write("%5s : %3d\n" % (letter, freq))

        totalElapsedTime = time.time() - startAlgorithm + elapsedTimeTreatingFile
        resultsFile.write(
            "{:s} : {:f}\n".format("Total Elapsed Time", totalElapsedTime)
        )
        #

        # Frequent counter
        startAlgorithm = time.time()
        resultsFile.write("\n{:s}\n".format("Frequent Counter"))
        frequent, dict_freq = frequent_count(text, 10)
        for letter, freq in dict_freq:
            resultsFile.write("%5s : %3d\n" % (letter, freq))

        totalElapsedTime = time.time() - startAlgorithm + elapsedTimeTreatingFile
        resultsFile.write(
            "{:s} : {:f}\n".format("Total Elapsed Time", totalElapsedTime)
        )

        # guarda os erros absolutos e relativos em dicionários
        absoluteErrorsCsurosCounter = {}
        absoluteErrorsFrequentCounter = {}
        relativeErrorsCsurosCounter = {}
        relativeErrorsFrequentCounter = {}

        for letter, freq in exact_counter:
            for letter2, freq2 in sorted_letters:
                if letter == letter2 and freq != freq2:
                    absoluteErrorsCsurosCounter[letter] = abs(freq - freq2)
                    relativeErrorsCsurosCounter[letter] = (abs(freq - freq2)) / freq

        for letter, freq in exact_counter:
            for letter2, freq2 in dict_freq:
                if letter == letter2 and freq != freq2:
                    absoluteErrorsFrequentCounter[letter] = abs(freq - freq2)
                    relativeErrorsFrequentCounter[letter] = (abs(freq - freq2)) / freq

        resultsFile.write("\n{:^s}\n".format("Absolute error csuros' counter"))
        for letter, freq in absoluteErrorsCsurosCounter.items():
            resultsFile.write("%5s : %3d\n" % (letter, freq))

        resultsFile.write("\n{:s}\n".format("Absolute error frequent counter"))
        for letter, freq in absoluteErrorsFrequentCounter.items():
            resultsFile.write("%5s : %3d\n" % (letter, freq))

        resultsFile.write("\n{:s}\n".format("Relative error csuros' counter"))
        for letter, freq in relativeErrorsCsurosCounter.items():
            resultsFile.write("%5s : %3f\n" % (letter, freq))

        resultsFile.write("\n{:s}\n".format("Relative error frequent counter"))
        for letter, freq in relativeErrorsFrequentCounter.items():
            resultsFile.write("%5s : %3f\n" % (letter, freq))

        # calcular o erro absoluto e relativo médio
        absoluteErrorCsurosCounterAvg += sum(
            absoluteErrorsCsurosCounter.values()
        ) / len(absoluteErrorsFrequentCounter)

        absoluteErrorFrequentCounterAvg += sum(
            absoluteErrorsFrequentCounter.values()
        ) / len(absoluteErrorsFrequentCounter)

        relativeErrorCsurosCounterAvg += sum(
            relativeErrorsCsurosCounter.values()
        ) / len(relativeErrorsFrequentCounter)
        relativeErrorFrequentCounterAvg += sum(
            relativeErrorsFrequentCounter.values()
        ) / len(relativeErrorsFrequentCounter)

        resultsFile.close()

    # calcular o erro absoluto e relativo médio de todos os ficheiros
    absoluteErrorCsurosCounterAvg = absoluteErrorCsurosCounterAvg / numFiles
    absoluteErrorFrequentCounterAvg = absoluteErrorFrequentCounterAvg / numFiles
    relativeErrorCsurosCounterAvg = relativeErrorCsurosCounterAvg / numFiles
    relativeErrorFrequentCounterAvg = relativeErrorFrequentCounterAvg / numFiles
    time.sleep(1)
    print(
        "\
        %3d : %s\n\
        %5f : %s\n\
        %5f : %s\n\
        %5f : %s\n\
        %5f : %s\
        "
        % (
            numFiles,
            "Number of files analysed",
            absoluteErrorCsurosCounterAvg,
            "Csuros' Counter Absolute Error",
            absoluteErrorFrequentCounterAvg,
            "Frequent Counter Absolute Error",
            relativeErrorCsurosCounterAvg,
            "Csuros' Counter Relative Error",
            relativeErrorFrequentCounterAvg,
            "Frequent Counter Relative Error",
        )
    )
