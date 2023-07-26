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
    foundText = get_text_between_substrings(text, "Norte", "DIAS").replace(".", "").replace("  ", " ").replace("ANO TODO", "ANO_TODO").replace("*", "NAO_RECOMENDADO")
    listOfWords = foundText.split(" ")

    validPattern = re.compile(r"^(JAN|FEV|MAR|ABR|MAI|JUN|JUL|AGO|SET|OUT|NOV|DEZ|JANEIRO|FEVEREIRO|MARÇO|ABRIL|MAIO|JUNHO|JULHO|AGOSTO|SETEMBRO|OUTUBRO|NOVEMBRO|DEZEMBRO)/(JAN|FEV|MAR|ABR|MAI|JUN|JUL|AGO|SET|OUT|NOV|DEZ|JANEIRO|FEVEREIRO|MARÇO|ABRIL|MAIO|JUNHO|JULHO|AGOSTO|SETEMBRO|OUTUBRO|NOVEMBRO|DEZEMBRO)$", re.IGNORECASE)
    allMonths = [
        "JANEIRO",
        "FEVEREIRO",
        "MARÇO",
        "ABRIL",
        "MAIO",
        "JUNHO",
        "JULHO",
        "AGOSTO",
        "SETEMBRO",
        "OUTUBRO",
        "NOVEMBRO",
        "DEZEMBRO",
        "JAN",
        "FEV",
        "MAR",
        "ABR",
        "MAI",
        "JUN",
        "JUL",
        "AGO",
        "SET",
        "OUT",
        "NOV",
        "DEZ",
    ]

    processedData = []
    
    for i in range(len(listOfWords)):
        if (listOfWords[i] == "ANO_TODO" or listOfWords[i] == "NAO_RECOMENDADO" or re.match(validPattern, listOfWords[i]) or listOfWords[i] in allMonths):
            processedData.append(listOfWords[i].upper())

    return {
        "south": processedData[0],
        "southeast": processedData[1],
        "northeast": processedData[2],
        "midwest": processedData[3],
        "north": processedData[4]
    }

def get_best_ways_to_use(text):
    bestWaysToUse = text[text.find("Recomendações de aproveitamento"):].replace("  ", " ")

    if (bestWaysToUse[len(bestWaysToUse) - 1].isnumeric()):
        return bestWaysToUse.replace("– ", "").replace("\n", " ").strip()[:-1]

    return bestWaysToUse.replace("– ", "").replace("\n", " ").strip()

id = 0
rawText = ""
dataArray = []

for n in range(7, 57):
    rawText += reader.pages[n].extract_text()
    text = reader.pages[n].extract_text()

    data = {
        "id": id,
        "popularNames": get_plant_popular_names(text),
        "scientificName": get_plant_scientific_name(text).replace("  ", " "),
        "description": get_plant_description(text),
        "bestWayToPlant": get_plant_best_way_to_plant(text),
        "bestTimeToPlant": get_best_time_to_plant(text),
        "bestWaysToUse": get_best_ways_to_use(text),
    }

    dataArray.append(data)

    id += 1

    textFromPdf += str(data)

print(textFromPdf)

# write the textFromPdf variable to a txt file
with open("hortalicas.txt", "w", encoding='utf-8') as f:
    f.write(rawText)

with open("hortalicas.js", "w", encoding='utf-8') as f:
    f.write("export const data = " + str(dataArray) + ";")
