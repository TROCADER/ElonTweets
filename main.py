import pandas as pd
import regex as re
import seaborn as sns
import matplotlib.pyplot as plt

elonsTweets = pd.read_csv("elonmusk.csv")

userWord = input("Word: ")
head = userWord[0]
if len(userWord) > 1:
    tail = ""
    for i in range(1,len(userWord)):
        tail += userWord[i]

currentYear = "2022"
output = {currentYear:0}

for index, row in elonsTweets.iterrows():    
    if currentYear in row["Date Created"]:
        output[currentYear] += len(re.findall(rf"({head.upper()}|{head}){tail}(\.|\s)", row["Tweets"]))
    else:
        currentYear = row["Date Created"][0:4]
        output[currentYear] = 0


dataFrame2 = pd.DataFrame.from_dict(output, orient="index")

dataFrame2 = dataFrame2.reset_index()
dataFrame2.columns = ["Year", "Occurences"]

dataFrame2.to_csv("output.csv", index=False)


sns.barplot(x=list(output.keys()),y=list(output.values()))
plt.show()
