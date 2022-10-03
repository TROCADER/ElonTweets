import numpy
import pandas

dataFrame = pandas.read_csv("elonmusk.csv")

userWord = input("Word: ")
userYear = input("Year: ")

occurences = 0
for index, row in dataFrame.iterrows():
    if userYear in row["Date Created"] and userWord in row["Tweets"]:
        occurences += 1

print(occurences)