# coding: utf-8
from gpt4free import Provider, Completion
from PyPDF2 import PdfReader
import re

reader = PdfReader("hortalicas.pdf")

textFromPdf = ""


def get_text_between_substrings(text, start, end):
    idx1 = text.find(start)
    idx2 = text.find(end)

    # length of substring 1 is added to
    # get string from next character
    return text[idx1 + len(start) + 1 : idx2]


def get_plant_popular_names(text):
    popularNames = get_text_between_substrings(text, "Nome popular", "Nome científico")

    return list(
        map(
            lambda x: x.strip().capitalize().replace("\n", " "),
            popularNames.replace("– ", "").split(", "),
        )
    )
    return None


def get_plant_scientific_name(text):
    scientificName = get_text_between_substrings(text, "Nome científico", "Descrição")

    return scientificName.replace("– ", "").replace("\n", " ").strip()


def get_plant_description(text):
    description = get_text_between_substrings(
        text, "Descrição", "Época e regiões para plantio"
    )

    return description.replace("– ", "").replace("\n", " ").strip()


def get_plant_best_way_to_plant(text):
    bestWayToPlant = get_text_between_substrings(
        text, "Época e regiões para plantio", "ESPÉCIE"
    )

    return bestWayToPlant.replace("– ", "").replace("\n", " ").strip()


def get_best_time_to_plant(text):
    bestTimeToPlant = get_text_between_substrings(text, "Norte", "DIAS").split(" ")

    data = {
        "south": bestTimeToPlant[1].strip(),
        "southeast": bestTimeToPlant[2].strip(),
        "northeast": bestTimeToPlant[3].strip(),
        "midwest": bestTimeToPlant[4].strip(),
        "north": bestTimeToPlant[5].strip(),
    }

    return data


id = 0
rawText = ""
dataArray = []

for n in range(7, 57):
    rawText += reader.pages[n].extract_text()
    text = reader.pages[n].extract_text()

    # print(get_plant_popular_names(text))

    data = {
        "id": id,
        "popularNames": get_plant_popular_names(text),
        "scientificName": get_plant_scientific_name(text),
        "description": get_plant_description(text),
        "bestWayToPlant": get_plant_best_way_to_plant(text),
        "bestTimeToPlant": get_best_time_to_plant(text),
    }

    dataArray.append(data)

    id += 1

    textFromPdf += str(data)

print(textFromPdf)

# write the textFromPdf variable to a txt file
with open("hortalicas.txt", "w") as f:
    f.write(rawText)

with open("hortalicas.js", "w") as f:
    f.write("export const data = " + str(dataArray) + ";")
