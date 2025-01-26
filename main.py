#---1 Setup---#
import tkinter as tk;from tkinter import ttk as ttk;import random;import time;from game_version import GameVersion;from tkinter import messagebox;from tkinter import *;import json;import os;

PointsInSession = 0

print(GameVersion)

url = 'https://raw.githubusercontent.com/ToMacMa/Matma/refs/heads/main/game_version.py'

def readFile(path):
    
    f = open(path, "r")
    output = f.read()
    f.close()
    return output

def writeToFile(path,whatToWrite):
    f = open(path, "w")
    f.write(whatToWrite)
    f.close()

def createFile(path):
    f = open(path, "a")
    f.close()

def loadJsonDataFromFile(path):
    return json.loads(readFile(path))

def createFolder(folder_name):
    try:
        os.mkdir(folder_name)
        print(f"Directory '{folder_name}' created successfully.")
    except FileExistsError:
        print(f"Directory '{folder_name}' already exists.")
    except PermissionError:
        print(f"Permission denied: Unable to create '{folder_name}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

def dumpJsonToFile(path,data):
    with open(path, "w") as file:
        json.dump(data, file)

createFile("saveData.json")
try:
    saveData = loadJsonDataFromFile('saveData.json')
    print(saveData)
except:
    dumpJsonToFile('saveData.json',{"points":0})
    saveData = loadJsonDataFromFile('saveData.json')

allTimePoints = saveData['points']
print(allTimePoints)

createFolder('users')

class updateWindow():
    def __init__(self):
        try:
            root = tk.Tk()
            root.title("Aktualizacja")
            #root.focus()
            root.geometry("600x500")
            root.config(bg='white')
            #widgets
            header = tk.Label(root,text="Aktualizacja\njest dostępna",font=('Arial',30),bg='white')
            #button1 = tk.Button(root,text="Aktualizuj",bg='white',relief='groove',command=lambda:webbrowser.open('https://github.com/ToMacMa/Matma', new = 2))
            button2 = tk.Button(root,text="Nie teraz",bg='white',relief='groove',command=lambda:root.destroy())


            #grid
            root.columnconfigure(0,weight=1000)
            root.columnconfigure(1,weight=1)
            root.columnconfigure(2,weight=1000)

            root.rowconfigure(0,weight=1)
            root.rowconfigure(1,weight=1)
            root.rowconfigure(2,weight=1)

            header.grid(row=0,column=1)
            #button1.grid(row=1,column=0,sticky='wesn')
            button2.grid(row=1,column=2,sticky='wesn')

            root.mainloop()
        except:
            print("error")
            #difficultySettings()
            #App('Matma', 1000)

class difficultySettings():

    def __init__(self):
        root = tk.Tk()
        root.geometry("600x600")
        root.title("Ustawianie trudności")
        root.config(bg='white')

        # widgets

        headerL = tk.Label(root,text="Ustawianie trudnośi",font=('Arial',40), bg='white')

        difficultySlider = tk.Scale(root, from_=1, to=4,orient='horizontal', bg='white', relief='groove')
        label1 = tk.Label(root,text=f"Wersja: {GameVersion}",font=('Arial',10), bg='white')
        label1.place(x=0,y=0)

        button1 = tk.Button(root,text="Gotowy?",font=('Arial',20), bg='white', relief='groove',command=lambda:setDifficulty())

        # setting up grid
        root.columnconfigure(0,weight=1)
        root.columnconfigure(1,weight=1)
        root.columnconfigure(2,weight=1)

        root.rowconfigure(0,weight=1)
        root.rowconfigure(1,weight=1)
        root.rowconfigure(2,weight=3)

        headerL.grid(row=0,column=1)
        difficultySlider.grid(row=1,column=1,sticky='we')
        button1.grid(row=2,column=1,sticky='wesn')

        def setDifficulty():
            global difficulty
            difficulty = difficultySlider.get()
            root.destroy()


        root.mainloop()

class App(tk.Tk):
    def __init__(self,title,size):
        rootSX = size
        rootSY = int(rootSX/4*2.5)
        #---1 Creating the window---#
        root = tk.Tk()
        root.title(title)
        root.geometry(f"{rootSX}x{rootSY}")
        root.config(bg='white', relief='groove')
        root.focus()
        global TimesUsed, CorrectAnswers
        CorrectAnswers = 0
        TimesUsed = 1
        #---2 Widgets---#

        headerL = tk.Label(root,text="MATMA",font=('Arial',90), bg='white')
        question = list()
        questionsAnswers = list()
        def createQuestion(ForcedOperation,RangeX,Rangey):
            global difficulty
            x = random.randint(RangeX[0],difficulty*RangeX[1])
            y = random.randint(Rangey[0],difficulty*Rangey[1])
            operation = random.randint(1,3)
            if ForcedOperation:
                operation = ForcedOperation
            if operation == 1:
                question.append(f"{x} + {y} ="); questionsAnswers.append(x+y)
            elif operation == 2:
                question.append(f"{x} x {y} ="); questionsAnswers.append(x*y)
            elif operation == 3 or operation == 4:
                if y > x:
                    if operation == 3:
                        question.append(f"{y} - {x} ="); questionsAnswers.append(y-x)
                    if operation == 4:
                        if x/y != int(x/y):
                            createQuestion(4)
                        else:
                            question.append(f"{x} / {y} ="); questionsAnswers.append(x/y)
                else:
                    if operation == 3:
                        question.append(f"{x} - {y} ="); questionsAnswers.append(x-y)
                    if operation == 4:
                        if y/x != int(y/x):
                            createQuestion(4)
                        else:
                            question.append(f"{y} / {x} ="); questionsAnswers.append(y/x)

        
        for i in range(0,1000):
            createQuestion(1,(1,30),(1,30))
            createQuestion(3,(1,60),(1,59))
            createQuestion(2,(0,15),(0,15))
            


        
        questionL1 = tk.Label(root, text=question[0],font=('Arial',30), bg='white')
        questionL2 = tk.Label(root, text=question[1],font=('Arial',30), bg='white')
        questionL3 = tk.Label(root, text=question[2],font=('Arial',30), bg='white')

        label2 = tk.Label(root,text=f"Punkty w tej sesji: {PointsInSession}, Punkty ogólnie: {allTimePoints}",font=('Arial',10), bg='white')

        input1 = tk.Entry(root, bg='white', relief='groove',font=('Arial',40))
        input2 = tk.Entry(root, bg='white', relief='groove',font=('Arial',40))
        input3 = tk.Entry(root, bg='white', relief='groove',font=('Arial',40))

        def newQuestions():
            global TimesUsed,CorrectAnswers
            if CorrectAnswers == 3:
                CorrectAnswers = 0
                tmp = TimesUsed
                TimesUsed = tmp + 1
                questionL1.config(text=question[0+TimesUsed*3-3])
                questionL2.config(text=question[1+TimesUsed*3-3])
                questionL3.config(text=question[2+TimesUsed*3-3])
                input1.delete(0, 'end')
                input2.delete(0, 'end')
                input3.delete(0, 'end')
        def saveSessionDataPoints():
            global allTimePoints,PointsInSession,difficulty

            allTimePoints = allTimePoints + difficulty

            dumpJsonToFile('saveData.json',{"points":allTimePoints})
            label2.config(text=f"Punkty w tej sesji: {PointsInSession}, Punkty ogólnie: {allTimePoints}")

        def checkAnswers(textFielId):
            global CorrectAnswers,PointsInSession,difficulty
            if textFielId == 1:
                answer = input1.get()
                if answer == str(questionsAnswers[0+TimesUsed*3-3]):
                    CorrectAnswers = CorrectAnswers + 1
                    PointsInSession = PointsInSession + difficulty
                    saveSessionDataPoints()
                    input1.delete(0, 'end')
                    input1.insert(0,"Poprawna odpowiedź!")
                    input1.config(fg='green')
                else:
                    input1.delete(0, 'end')
                    input1.insert(0,"Zła odpowiedź.")
                    input1.config(fg='red')
            if textFielId == 2:
                answer = input2.get()
                if answer == str(questionsAnswers[1+TimesUsed*3-3]):
                    CorrectAnswers = CorrectAnswers + 1
                    PointsInSession = PointsInSession + difficulty
                    saveSessionDataPoints()
                    input2.delete(0, 'end')
                    input2.insert(0,"Poprawna odpowiedź!")
                    input2.config(fg='green')
                else:
                    input2.delete(0, 'end')
                    input2.insert(0,"Zła odpowiedź.")
                    input2.config(fg='red')
            if textFielId == 3:
                answer = input3.get()
                if answer == str(questionsAnswers[2+TimesUsed*3-3]):
                    CorrectAnswers = CorrectAnswers + 1
                    PointsInSession = PointsInSession + difficulty
                    saveSessionDataPoints()
                    input3.delete(0, 'end')
                    input3.insert(0,"Poprawna odpowiedź!")
                    input3.config(fg='green')
                else:
                    input3.delete(0, 'end')
                    input3.insert(0,"Zła odpowiedź.")
                    input3.config(fg='red')

        button1 = tk.Button(root,text="Sprawdź odpowiedź", bg='white', relief='groove',command=lambda:checkAnswers(1))
        button2 = tk.Button(root,text="Sprawdź odpowiedź", bg='white', relief='groove',command=lambda:checkAnswers(2))
        button3 = tk.Button(root,text="Sprawdź odpowiedź", bg='white', relief='groove',command=lambda:checkAnswers(3))
        button4 = tk.Button(root,text="Nowe pytania", bg='white', relief='groove',command=lambda:newQuestions())

        #---3 Making the grid---#

        root.columnconfigure(0, weight=100)
        root.columnconfigure(1, weight=12)
        root.columnconfigure(2, weight=10)
        root.columnconfigure(3, weight=10)
        root.columnconfigure(4, weight=100)

        root.rowconfigure(0, weight=10)
        root.rowconfigure(1, weight=3)
        root.rowconfigure(2, weight=3)
        root.rowconfigure(3, weight=3)
        root.rowconfigure(4, weight=8)
        root.rowconfigure(5, weight=10)

        #---3 1 Placing widgets on the window---#

        headerL.grid(row=0,column=2)

        questionL1.grid(row=1,column=1,sticky='w')
        questionL2.grid(row=2,column=1,sticky='w')
        questionL3.grid(row=3,column=1,sticky='w')

        input1.grid(row=1,column=2,sticky='e')
        button1.grid(row=1,column=3,sticky='wesn')
        input2.grid(row=2,column=2,sticky='e')
        button2.grid(row=2,column=3,sticky='wesn')
        input3.grid(row=3,column=2,sticky='e')
        button3.grid(row=3,column=3,sticky='wesn')

        button4.grid(row=4,column=2,sticky='wesn')
        label1 = tk.Label(root,text=f"Wersja: {GameVersion}",font=('Arial',10), bg='white')
        label1.place(x=0,y=0)
        label2.grid(row=5,column=1)

        #---1 Run---#
        root.mainloop()

difficultySettings()
App('Matma', 1000)