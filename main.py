import pandas as pd
import matplotlib as plt
import seaborn as sns
import pathlib as pl

dataFrame = pd.read_csv("elonmusk.csv")

userWord = input("Word: ")
userYear = input("Year: ")

occurencesDict = {}

for index, row in dataFrame.iterrows():
    if userYear in row["Date Created"] and userWord in row["Tweets"]:
        if userYear in occurencesDict:
            occurencesDict[userYear] += 1
        else:
            occurencesDict[userYear] = 1

for year in occurencesDict:
    print(f"{year}: {occurencesDict[year]}")

dataFrame2 = pd.DataFrame.from_dict(occurencesDict, orient="index")

dataFrame2 = dataFrame2.reset_index()
dataFrame2.columns = ["Year", "Occurences"] #range(dataFrame2.columns.size)

dataFrame2.to_csv("output.csv", index=False)

print(dataFrame2)


