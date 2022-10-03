from re import U
import numpy
import pandas

dataFrame = pandas.read_csv("elonmusk.csv")

userWord = input("Word: ")
userYear = input("Year: ")

#startYear = input("Start year: ")
#endYear = input("End year: ")
#currentYear = startYear

occurencesDict = {}

occurences = 0
for index, row in dataFrame.iterrows():
    if userYear in row["Date Created"] and userWord in row["Tweets"]:
        #occurences += 1

        if userYear in occurencesDict:
            occurencesDict[userYear] += 1
        else:
            occurencesDict[userYear] = 1

for year in occurencesDict:
    print(f"{year}: {occurencesDict[year]}")