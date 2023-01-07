import os
import sys
import matplotlib.pyplot as plt


ALL_INFORMATIONS = {}

METRICS = [
    "CSUROS_COUNTER_ABSOLUTE_ERROR",
    "FREQ_COUNTER_ABSOLUTE_ERROR",
    "CSUROS_COUNTER_RELATIVE_ERROR",
    "FREQ_COUNTER_RELATIVE_ERROR",
]


def drawGraph():

    # Data to plot

    data = [
        78.6154,
        99.9775,
        99.9843,
        99.9757,
        99.9916,
        99.9910,
    ]
    xValues = [
        "E",
        "T",
        "A",
        "D",
        "H",
        "N",
    ]

    # Create a figure and an axis
    fig, ax = plt.subplots()

    # Plot a bar chart
    ax.bar(xValues, data)

    ax.set_title("Relative Error - FREQ COUNTER")
    ax.set_xlabel("Letters")
    ax.set_ylabel("Percentage (%)")

    # Show the plot
    plt.show()


if __name__ == "__main__":
    drawGraph()
    sys.exit(-1)
    contador = 0
    allFiles = os.listdir("basicCount/")

    for file in allFiles:
        f = open("basicCount/" + file, "r")
        allLines = f.readlines()
        f.close()

        language = file.split("_")[1].replace(".txt", "")
        if language not in ALL_INFORMATIONS:
            ALL_INFORMATIONS[language] = {}

        data = [i.replace("\n", "") for i in allLines]

        for i in data:
            if i != "":
                if METRICS[contador] not in ALL_INFORMATIONS[language]:
                    ALL_INFORMATIONS[language][METRICS[contador]] = {}

                letter, number = i.split(":")
                if letter not in ALL_INFORMATIONS[language][METRICS[contador]]:
                    ALL_INFORMATIONS[language][METRICS[contador]][letter] = float(
                        number
                    )
                else:
                    ALL_INFORMATIONS[language][METRICS[contador]][letter] += float(
                        number
                    )
            else:
                contador += 1
        contador = 0

    for language in ALL_INFORMATIONS:
        print("\n>>>>", language, "<<<<")
        for metric in ALL_INFORMATIONS[language]:
            print(">>>>", metric, "<<<<")
            for letter in ALL_INFORMATIONS[language][metric]:
                print(letter, ALL_INFORMATIONS[language][metric][letter])
