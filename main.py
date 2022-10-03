import pandas

dataFrame = pandas.read_csv("elonmusk.csv")

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