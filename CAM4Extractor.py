#!/bin/python3.6
# Inspired by https://github.com/beaston02/CAM4Recorder
import os
import json
import time
import configparser
import sys
import requests
from ProfileAndFilter import Filter, Profile

config = configparser.ConfigParser()
settings = {}
modelsAddedSinceStart = []


# Direct copy from https://github.com/beaston02/CAM4Recorder
def getOnlineModels(page):
    i = 1
    while i < 5:
        try:
            sys.stdout.write("\033[K")
            print("Checking for models (page {})".format(page), end="\r")
            result = requests.get("https://www.cam4.com/directoryCams?directoryJson=true&online=true&url=true&page={}".format(page)).json()
            return result
        except:
            i = i + 1
            sys.stdout.write("\033[F")


def readConfig():
    global settings
    global config
    config.read("config.config")
    settings = {
        'cam4recorderwishlist': config.get('paths', 'cam4recorderwishlist'),
        'checkInterval': int(config.get('settings', 'checkInterval')),
        'filterfile': config.get('filter', 'filterfile'),
        'outputDir': config.get('paths', 'outputDir'),
        "verbose": config.getboolean('settings', 'verbose')
    }


def extractModelsByJson():
    modelsFound = []
    i = 1
    offline = False
    while not offline:
        results = getOnlineModels(i)
        if len(results['users']) >= 1:
            for u in results['users']:
                cProfile = Profile()
                cProfile.title = u['username']
                cProfile.url = u['username']
                cProfile.country = u['countryCode']
                cProfile.gender = u['gender']
                cProfile.orientation = u['sexPreference']
                modelsFound.append(cProfile)
        else:
            offline = True
        i += 1
    return modelsFound


def readFilters():
    # Read the filters
    filters = []
    filterFile = open(settings['filterfile'], 'r')
    try:
        filterStrings = json.load(filterFile)
    except:
        print("Your filters.json file is malformed. Please fix it (Hint: README.md)")
        exit(2)
    for filterString in filterStrings:
        filters.append(Filter.parseJson(filterString))
    filterFile.close()
    if len(filters) == 0:
        print("Your filters.json file is empty. Please add a filter (Hint: README.md)")
        exit(1)
    return filters


def readExcluded():
    if not os.path.isfile("exclude.txt"):
        return []
    with open("exclude.txt", "r") as ins:
        excludedList = []
        for line in ins:
            excludedList.append(line)
    excludedList = [x.strip("\n") for x in excludedList]
    return excludedList


def parseFiltersAndWriteFile(filters, modelsFound, excludedList):
    # For each filter, run through the models and determine if it should be added
    for filter in filters:
        # Open file for filter
        filename = settings['outputDir'] + "/" + filter.name + ".txt"
        if not os.path.isfile(filename):
            tf = open(filename, 'x+')
            tf.close()
        file = open(filename, 'r')
        fileContent = file.read()
        file.close()
        for model in modelsFound:
            if model.filtermatch(filter) and model.url not in fileContent and model.url not in excludedList:
                fileContent += model.url + "\n"
                modelsAddedSinceStart.append(model)
        file = open(filename, 'w')
        file.write(fileContent)
        file.close()


def parseFiltersAndExportToRec(filters, modelsFound, excludedList):
    for filter in filters:
        if filter.exportToCapture is False:
            continue
        file = open(settings['cam4recorderwishlist'], 'r')
        fileContent = file.read()
        file.close()
        for model in modelsFound:
            if model.filtermatch(filter) and model.url not in fileContent and model.url not in excludedList:
                fileContent += model.url + "\n"
        file = open(settings['cam4recorderwishlist'], 'w')
        file.write(fileContent)
        file.close()


def main():
    while True:
        readConfig()
        filters = readFilters()
        excluded = readExcluded()
        models = extractModelsByJson()
        parseFiltersAndWriteFile(filters, models, excluded)
        parseFiltersAndExportToRec(filters, models, excluded)
        for i in range(settings['checkInterval'], 0, -1):
            sys.stdout.write("\033[K")
            if settings['verbose']:
                print("Next check in {} seconds. Models added since start {}".format(i, modelsAddedSinceStart), end="\r")
            else:
                print("Next check in {} seconds".format(i), end="\r")
            time.sleep(1)


if __name__ == "__main__":
    main()
