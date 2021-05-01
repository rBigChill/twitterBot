import time
import json
import os

# File Locations
FRONT_PAGE = "frontPage.txt"
NEW_FRIENDS = "friends.txt"
HNFRONT_PAGE = "hnFrontPage.txt"

# API Limits
LIMIT = 900

# Query List
QUERY = ["python programming","go programming","bjj","ufc","programming","webdev"]

def clear():
    """
        Clear Screen
    """
    #os.system("clear")
    pass

def pause(sleep):
    """
        Pause Program
    """
    time.sleep(sleep)

def printTime():
    #date = time.strftime(f"%d %B %Y")
    now = time.strftime(f"%H:%M:%S")
    return f"[{now}]"

def saveData(dataToSave, fileLocation):
    """
        Save Data
    """
    with open(fileLocation, "w", encoding="utf-8") as fl:
        json.dump(dataToSave, fl, ensure_ascii=False, indent=4)

def openData(fileLocation):
    """
        Open Data
    """
    while True:
        try:
            with open(fileLocation, "r", encoding="utf-8") as fl:
                loadedData = json.load(fl)
        except FileNotFoundError:
            print("\n\t~ FileNotFoundError ~")
        else:
            return loadedData

def saveDataTXT(dataToSave, fileLocation):
    """
        Save Data
    """
    with open(fileLocation, "a") as fl:
        fl.write(f"{str(dataToSave)}\n")

def openDataTXT(fileLocation):
    """
        Open Data
    """
    friends = []

    with open(fileLocation, "r") as fl:
        loadedData = fl.readlines()

    for i in loadedData:
        friends.append(int(i.strip()))
    return friends

def deleteDataTXT(fileLocation):
    """
        Delete Data
    """
    with open(fileLocation, "w") as fl:
        pass
