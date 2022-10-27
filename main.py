# Importerar alla nödvändiga bibliotek som används i projektet
from cProfile import label
from tkinter import *
#from traceback import print_tb
import pandas as pd
import regex as re

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

# Sätter dimensionerna på GUI:t
window_width = 1000
window_height = 600

root = Tk()

fig = Figure(figsize=(6, 4), dpi=200)

# Rutan som innehåller figuren
canvas = FigureCanvasTkAgg(fig, master=root) 
canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
toolbar = NavigationToolbar2Tk(canvas, root)

# Funktion som ritar ut och hittar alla förekomster
# Blir kallad varje gång som användaren klickar på knappen i GUI:t
def draw_chart():
    # Rensar rutan så att enbart ny data syns
    fig.clear()
    # Skapar en dict som datan från förekomsterna sparas i
    output = {None:None}

    # Ger användaren möjligheten att kunna läsa in filer som redan finns på systemet, användbart om man exempelvis vill kolla på den senaste datan igen
    if onlyPrint.get() == True:
        readCsv = pd.read_csv("data.csv")
        fig.add_subplot(111).plot(readCsv["Year"], readCsv["Occurences"])

    # Om användaren inte vill kolla på redan existerande data så genereras ny som skriver över det som redan finns (om det finns något)
    else:
        output = {int(yearEndEntry.get()):0}
        output = findOccurencesInpdDF(int(yearEndEntry.get()), int(yearStartEntry.get()), wordEntry.get(), output, caseSensitive.get(), pd.read_csv("elonmusk.csv"))

        # Skapar en pandas dataframe av dict:en där alla förekomster lagrades
        # Eftersom den nyligen skapta DF:en är felaktigt formaterad för att kunna användas väl måste dess index nollställas samt columner läggas till
        csvReadyDF = pd.DataFrame.from_dict(output, orient="index").reset_index()
        print(csvReadyDF)
        csvReadyDF.columns = ["Year", "Occurences"]

        # Skriver DF:en med all data till en .csv som kan användas i andra projekt, samt för att se antalet förekomster i mer detalj
        csvReadyDF.to_csv("data.csv", index=False)

        # Lägger till en graf genererad av matplotlib enligt formatet, 1 rad, 1 column på graf 1 (111)
        fig.add_subplot(111).plot(list(output.keys()), list(output.values()))
    
    # Ritar ut figuren 1 gång
    canvas.draw_idle()


def findOccurencesInpdDF(activeYear, yearStart, wordToCheck, outputDict, sensitiveOrNot, pdDFToCheck):
    for index, row in pdDFToCheck.iterrows():
        # Bara år som är mellan tidsramarna som användaren har valt kommer att kontrolleras
        if activeYear >= int(yearStart):
            # Kontrollerar om användaren användaren har valt kontroll av specifikt det som input:ades (känslig på stor och liten bokstav)
            # Om användaren vill kontrollera med känlighet på stor och liten bokstav så kommer ordet att direkt kollas av, annars kommer alla kombinationer av stor och liten bokstav att testas
            # Enda skillnaden är användningen av flaggan IGNORECASE som explicit säger till RegEx att ignorera om det är stor eller liten bokstav, därmed returnera får båda
            if sensitiveOrNot == True:
                # Kontrollerar om året tweeten tweetades på är samma som användaren matade in
                # Om inte kommer det årtalet som användaren matade in att minskas med 1 och förekomster på det året blir markerat som 0, då inga förekomster skedde
                # Om det finns förekomster på det året kommer antalet förekomster att loggas i dict:en
                if activeYear == int(row["Date Created"][:4]):
                    outputDict[activeYear] += len(re.findall(rf"\b{wordToCheck}\b", row["Tweets"])) 
                elif activeYear > int(row["Date Created"][:4]):
                    activeYear -= 1
                    outputDict[activeYear] = 0
            else:
                if activeYear == int(row["Date Created"][:4]):
                    outputDict[activeYear] += len(re.findall(rf"\b{wordToCheck}\b", row["Tweets"], re.IGNORECASE))
                elif activeYear > int(row["Date Created"][:4]):
                    activeYear -= 1
                    outputDict[activeYear] = 0
    
    return outputDict

# Rutor för vad som ska analyseras
wordEntry = Entry(root, width=5, font=("calibre", 10, "normal"))
yearStartEntry = Entry(root, width=5, font=("calibre", 10, "normal"))
yearEndEntry = Entry(root, width=5, font=("calibre", 10, "normal"))
# Gör en checkbox som ändrar variabeln nedan, variabeln används i huvudlogiken
# Eftersom att man inte direkt kan hämta datan från en checkbox så behöver vi först ändra på en variabel till checkboxens data, därmed varför ytterliggare variablar finns
caseSensitive = BooleanVar()
caseSensitiveEntry = Checkbutton(root, variable=caseSensitive, onvalue=True, offvalue=False)
onlyPrint = BooleanVar()
onlyPrintEntry = Checkbutton(root, variable=onlyPrint, onvalue=True, offvalue=False)
# Label för en "lapp" som säger något, varav i detta fall frågar användaren
# .pack() gör datan redo att presenteras i GUI:t, gör så att tkinter vet hur den ska skriva ut den
Label(root, text="Enter word").pack()
wordEntry.pack()
Label(root, text="Enter start year").pack()
yearStartEntry.pack()
Label(root, text="Enter end year").pack()
yearEndEntry.pack()
Label(root, text="Case sensitive?", width=20).pack()
caseSensitiveEntry.pack()
Label(root, text="Read from existing .csv?", width=20).pack()
onlyPrintEntry.pack()
# Knapp som startar logiken
Button(root,text="Draw", command=draw_chart).pack()

# Håller rutan igång och därmed programmet igång
# Tkinter kör om sålänge som rutan är öppen, därmed varför en while-loop in behövs/kan användas
root.mainloop()