import sys, getopt
import os
from collections import defaultdict
import unicodedata
import random
import string
import time

NUM_REPETITIONS = 5


def letter_count(text):
    """function used to implement the basic counter algorithm"""
    counters = defaultdict(int)
    for char in text:
        if char.isalpha() and char != "":
            char = remove_accents(char)
            counters[char] += 1
    sorted_counters = sorted(counters.items(), key=lambda x: x[1], reverse=True)
    return sorted_counters


def MisraGriesAlgorithm(text, k):
    """frequent counter algorithm"""
    A = {}
    for j in text:
        if j.isalpha():
            j = remove_accents(j)
            if j in A:
                A[j] = A[j] + 1
            else:
                if len(A) < k - 1:
                    A[j] = 1
                else:
                    for i in list(A.keys()):
                        A[i] = A[i] - 1
                        if A[i] == 0:
                            del A[i]
    return sorted(A.items(), key=lambda x: x[1], reverse=True)


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

    csuros_counter = sorted(letter_count.items(), key=lambda x: x[1], reverse=True)
    return csuros_counter


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
    K = 10
    opts, args = getopt.getopt(argv, "hf:k:", ["folder="])
    for opt, arg in opts:
        if opt == "-h":
            print("python3 frequent_count.py -f <folderToFiles> -k <number of K>")
            sys.exit()
        elif opt in ("-f", "--folder"):
            folder += arg
        elif opt == "-k":
            K = arg
    return (folder, int(K))


def getAllFiles(folder):
    all_files = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(".txt"):
                tmp = root + "/" + file
                all_files.append(tmp)
    return all_files


if __name__ == "__main__":

    folder, K = getArgs(sys.argv[1:])

    absoluteErrorCsurosCounterAvg = 0
    absoluteErrorFrequentCounterAvg = 0
    relativeErrorCsurosCounterAvg = 0
    relativeErrorFrequentCounterAvg = 0

    all_text_files = getAllFiles(folder)
    numFiles = len(all_text_files)

    if not os.path.isdir("results"):
        os.mkdir("results")

    for file in all_text_files:
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
        csuros_counter = estimate_frequent_letters(text, 5000)
        for letter, freq in csuros_counter:
            resultsFile.write("%5s : %3d\n" % (letter, freq))

        totalElapsedTime = time.time() - startAlgorithm + elapsedTimeTreatingFile
        resultsFile.write(
            "{:s} : {:f}\n".format("Total Elapsed Time", totalElapsedTime)
        )
        #

        # Frequent counter
        startAlgorithm = time.time()
        resultsFile.write("\n{:s}\n".format("Frequent Counter"))
        frequent_counter = MisraGriesAlgorithm(text, K)

        for letter, freq in frequent_counter:
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

        exact_counter = dict(exact_counter)

        for letter, app_freq in csuros_counter:
            if letter in exact_counter:
                real_count = exact_counter[letter]
                if app_freq != real_count:
                    absoluteErrorsCsurosCounter[letter] = abs(real_count - app_freq)
                    relativeErrorsCsurosCounter[letter] = (
                        abs(real_count - app_freq)
                    ) / real_count

        for letter, app_freq in frequent_counter:
            if letter in exact_counter:
                real_count = exact_counter[letter]
                if app_freq != real_count:
                    absoluteErrorsFrequentCounter[letter] = abs(real_count - app_freq)
                    relativeErrorsFrequentCounter[letter] = (
                        abs(real_count - app_freq)
                    ) / real_count

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
        if len(absoluteErrorsCsurosCounter) > 0:
            absoluteErrorCsurosCounterAvg += sum(
                absoluteErrorsCsurosCounter.values()
            ) / len(absoluteErrorsCsurosCounter)

        if len(absoluteErrorsFrequentCounter) > 0:
            absoluteErrorFrequentCounterAvg += sum(
                absoluteErrorsFrequentCounter.values()
            ) / len(absoluteErrorsFrequentCounter)

        if len(relativeErrorsCsurosCounter) > 0:
            relativeErrorCsurosCounterAvg += sum(
                relativeErrorsCsurosCounter.values()
            ) / len(relativeErrorsCsurosCounter)

        if len(relativeErrorsFrequentCounter) > 0:
            relativeErrorFrequentCounterAvg += sum(
                relativeErrorsFrequentCounter.values()
            ) / len(relativeErrorsFrequentCounter)

        resultsFile.write(
            f"{dict(exact_counter).keys()} {dict(csuros_counter).keys()} {dict(frequent_counter).keys()}"
        )
        resultsFile.close()

    # calcular o erro absoluto e relativo médio de todos os ficheiros
    absoluteErrorCsurosCounterAvg = absoluteErrorCsurosCounterAvg / numFiles
    absoluteErrorFrequentCounterAvg = absoluteErrorFrequentCounterAvg / numFiles

    relativeErrorCsurosCounterAvg = relativeErrorCsurosCounterAvg / numFiles
    relativeErrorFrequentCounterAvg = relativeErrorFrequentCounterAvg / numFiles

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
