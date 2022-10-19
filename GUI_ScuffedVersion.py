from tkinter import *
from traceback import print_tb
import pandas as pd
import regex as re

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

window_width = 1000
window_height = 600

elonsTweets = pd.read_csv("elonmusk.csv")

root = Tk()

fig = Figure(figsize=(6, 4), dpi=200)

canvas = FigureCanvasTkAgg(fig, master=root) 
canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
toolbar = NavigationToolbar2Tk(canvas, root)

def draw_chart():
    fig.clear()
    userWord = wordEntry.get()
    currentYear = int(yearEndEntry.get())
    output = {currentYear:0}
    head = userWord[0]


    for index, row in elonsTweets.iterrows():
        if currentYear >= int(yearStartEntry.get()):
            if caseSensitive.get() == True:
                if currentYear == int(row["Date Created"][:4]):
                    output[currentYear] += len(re.findall(rf"\b{userWord}\b", row["Tweets"])) 
                elif currentYear > int(row["Date Created"][:4]):
                    currentYear -= 1
                    output[currentYear] = 0
            else:
                userWord = userWord.lower()
                if len(userWord) > 1:
                    tail = ""
                for i in range(1,len(userWord)):
                    tail += userWord[i]

                if currentYear == int(row["Date Created"][:4]):
                    output[currentYear] += len(re.findall(rf"\b({head.upper()}|{head}){tail}\b", row["Tweets"]))
                elif currentYear > int(row["Date Created"][:4]):
                    currentYear -= 1
                    output[currentYear] = 0
    
    fig.add_subplot(111).plot(list(output.keys()), list(output.values()))
    canvas.draw_idle()

    csvReadyDF = pd.DataFrame.from_dict(output, orient="index").reset_index()
    csvReadyDF.columns = ["Year", "Occurences"]

    csvReadyDF.to_csv("output.csv", index=False)

wordEntry = Entry(root, width=5, font=("calibre", 10, "normal"))
yearStartEntry = Entry(root, width=5, font=("calibre", 10, "normal"))
yearEndEntry = Entry(root, width=5, font=("calibre", 10, "normal"))
caseSensitive = BooleanVar()
caseSensitiveEntry = Checkbutton(root, variable=caseSensitive, onvalue=True, offvalue=False)
Label(root, text="Enter word").pack()
wordEntry.pack()
Label(root, text="Enter start date").pack()
yearStartEntry.pack()
Label(root, text="Enter end date").pack()
yearEndEntry.pack()
Label(root, text="Case sensitive?", width=20).pack()
caseSensitiveEntry.pack()
Button(root,text="Draw", command=draw_chart).pack()

root.mainloop()

