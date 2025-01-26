#---1 Setup---#
import tkinter as tk
from tkinter import ttk as ttk
import random
import time
from game_version import GameVersion
from tkinter import messagebox
from tkinter import *
import json
import os
import os.path
from Crypto.Cipher import AES
from base64 import b64encode, b64decode
d2 = 'a'
class Crypt:

    def __init__(self, salt='SlTKeYOpHygTYkP3'):
        self.salt = salt.encode('utf8')
        self.enc_dec_method = 'utf-8'

    def encrypt(self, str_to_enc, str_key):
        try:
            aes_obj = AES.new(str_key.encode('utf-8'), AES.MODE_CFB, self.salt)
            hx_enc = aes_obj.encrypt(str_to_enc.encode('utf8'))
            mret = b64encode(hx_enc).decode(self.enc_dec_method)
            return mret
        except ValueError as value_error:
            if value_error.args[0] == 'IV must be 16 bytes long':
                raise ValueError('Encryption Error: SALT must be 16 characters long')
            elif value_error.args[0] == 'AES key must be either 16, 24, or 32 bytes long':
                raise ValueError('Encryption Error: Encryption key must be either 16, 24, or 32 characters long')
            else:
                raise ValueError(value_error)

    def decrypt(self, enc_str, str_key):
        try:
            aes_obj = AES.new(str_key.encode('utf8'), AES.MODE_CFB, self.salt)
            str_tmp = b64decode(enc_str.encode(self.enc_dec_method))
            str_dec = aes_obj.decrypt(str_tmp)
            mret = str_dec.decode(self.enc_dec_method)
            return mret
        except ValueError as value_error:
            if value_error.args[0] == 'IV must be 16 bytes long':
                raise ValueError('Decryption Error: SALT must be 16 characters long')
            elif value_error.args[0] == 'AES key must be either 16, 24, or 32 bytes long':
                raise ValueError('Decryption Error: Encryption key must be either 16, 24, or 32 characters long')
            else:
                raise ValueError(value_error)


PointsInSession = 0
SelectedAcount = ""
AccountPath = ""
allTimePoints = int()

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

def dumpJsonToFile(path,data):
    with open(path, "w") as file:
        json.dump(data, file)

def createFolder(folder):
    nested_directory = folder
    try:
        os.makedirs(nested_directory)
        print(f"Nested directories '{nested_directory}' created successfully.")
    except FileExistsError:
        print(f"One or more directories in '{nested_directory}' already exist.")
    except PermissionError:
        print(f"Permission denied: Unable to create '{nested_directory}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

def createUser(username,password):
    if not os.path.isfile(f"users/{username}.json"):
        createFolder('users')
        createFile(f"users/{username}.json")
        dumpJsonToFile(f"users/{username}.json",{"points":0,"password": password})

createUser('gość','')

class AccountSelection():
    def __init__(self):
        root = tk.Tk()
        root.config(bg='white')
        root.geometry("800x700")
        root.title("Wybieranie konta")

        accounts = list()
        for i in os.listdir('users'):
            accounts.append(i.removesuffix('.json'))
        print(accounts)
        def accountPasswordVerifying(account):
            def signIn(password,account,window):
                global d2
                test_crpt = Crypt()
                enc_password = loadJsonDataFromFile(f'users/{account}.json')['password']
                test_key = 'MyKey4TestingYnP'
                test_dec_text = test_crpt.decrypt(enc_password, test_key)
                if test_dec_text == password:
                    d2 = enc_password
                    window.destroy()
                    selectAccount(account)

            if account == "gość":
                selectAccount('gość')
            else:
                print(account)
                window = Tk()
                window.geometry("500x400")
                window.focus()
                window.config(bg='white')

                header = Label(window,text="Wpisz hasło",font=('Arial',30),bg='white')
                input1 = Entry(window,font=('Arial',30),bg='white',borderwidth=2,relief='groove')
                button1 = Button(window,text="Zaloguj się",font=('Arial', 30),bg='white',relief='groove',command=lambda account=account:signIn(input1.get(),account,window))
                
                window.rowconfigure(0,weight=1)
                window.rowconfigure(1,weight=1)
                window.rowconfigure(2,weight=1)
                window.columnconfigure(0,weight=1)
                window.columnconfigure(1,weight=1)
                window.columnconfigure(2,weight=1)

                header.grid(row=0,column=1)
                input1.grid(row=1,column=1,sticky='we')
                button1.grid(row=2,column=1,sticky='wesn')

                window.mainloop()
        def selectAccount(account):
            global SelectedAcount,AccountPath,allTimePoints
            print(account)
            path = f"users/{account}.json"
            try:
                saveData = loadJsonDataFromFile(path)
                print(saveData)
            except:
                dumpJsonToFile(path,{"points":0})
                saveData = loadJsonDataFromFile(path)

            SelectedAcount = account
            AccountPath = path
            #print(saveData['points'])
            allTimePoints = saveData['points']
            #print(allTimePoints)
            root.destroy()
        i2 = 0
        label = tk.Label(root,text='gość',font=('Arial',20),bg='white',relief='groove')
        button = Button(root,text='Wybierz\nkonto',font=('Arial',20),bg='white'
                        ,relief='groove',command=lambda:accountPasswordVerifying('gość'))

        label.place_configure(x=0,y=0+(i2*122))
        button.place_configure(x=0,y=35+(i2*122))
        i2 = i2 + 1
        for i in accounts:
            if not i == "gość":
                label = tk.Label(root,text=i,font=('Arial',20),bg='white',relief='groove')
                button = Button(root,text='Wybierz\nkonto',font=('Arial',20),bg='white'
                                ,relief='groove',command=lambda i=i:accountPasswordVerifying(i))

                label.place_configure(x=0,y=0+(i2*122))
                button.place_configure(x=0,y=35+(i2*122))
                i2 = i2 + 1

        def AccountCreationWindow(root):
            window = tk.Tk()
            window.title("Tworzenie nowego konta")
            window.config(bg='white')
            window.geometry("600x500")
            window.focus()


            header = Label(window,text="Tworzenie konta",font=('Arial',30),bg='white')

            input1 = tk.Entry(window,bg='white',relief='groove',borderwidth=2,font=('Arial',15))
            input2 = tk.Entry(window,bg='white',relief='groove',borderwidth=2,font=('Arial',15))

            label1 = Label(window,text="Nazwa:",font=('Arial',15),bg='white')
            label2 = Label(window,text="Hasło:",font=('Arial',15),bg='white')
            label3 = Label(window,text="",font=('Arial',15),bg='white')

            def CheckInfoAndCreateAccount(root,window):
                global d2
                d1 = str(input1.get())
                d2 = str(input2.get())
                label3.config(fg='red')
                d1 = d1.replace('.', '')
                test_crpt = Crypt()
                test_text = str(d2)

                test_key = 'MyKey4TestingYnP'
                test_enc_text = test_crpt.encrypt(test_text, test_key)
                if len(d1)>10 or len(d1)<3:
                    label3.config(text="Nazwa zbyt krótka lub zbyt długa")
                    return
                else:
                    if len(d2)>16 or len(d2)<8:
                        label3.config(text="Hasło zbyt krótkie lub zbyt długie")
                        return
                    else:
                        createUser(d1,test_enc_text)
                        label3.config(text="Konto utworzone!")
                        window.destroy()
                        root.destroy()
                        AccountSelection()
                try:     
                    label3.config(fg='black')
                    label3.config(text="")
                except:
                    pass

            button1 = Button(window,text="Stwórz konto",font=('Arial',15),bg='white',relief='groove'
                             ,command=lambda:CheckInfoAndCreateAccount(root,window))

            window.columnconfigure(0,weight=1)
            window.columnconfigure(1,weight=1)
            window.columnconfigure(2,weight=1)

            window.rowconfigure(0,weight=1)
            window.rowconfigure(1,weight=10)
            window.rowconfigure(2,weight=10)
            window.rowconfigure(3,weight=10)
            window.rowconfigure(4,weight=10)

            header.grid(row=0,column=1)
            input1.grid(row=1,column=1,sticky='we')
            input2.grid(row=2,column=1,sticky='we')
            label1.grid(row=1,column=0,sticky='e')
            label2.grid(row=2,column=0,sticky='e')
            label3.grid(row=4,column=1)
            button1.grid(row=3,column=1,sticky='wesn')

            window.mainloop()

        button1 = Button(root,text="Utwórz nowe konto",font=('Arial',20),bg='white',
                        relief='groove',command=lambda:AccountCreationWindow(root))
        button1.pack()

        root.mainloop()

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

        difficultySlider = tk.Scale(root, from_=1, to=5,orient='horizontal', bg='white', relief='groove')
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
            App('Matma', 1000)


        root.mainloop()
class App(tk.Tk):
    def __init__(self,title,size):
        global allTimePoints
        rootSX = size
        rootSY = int(rootSX/4*2.5)
        #---1 Creating the root---#
        root = tk.Tk()
        root.title(title)
        root.geometry(f"{rootSX}x{rootSY}")
        root.config(bg='white', relief='groove')
        root.focus_force()
        global TimesUsed, CorrectAnswers
        CorrectAnswers = 0
        TimesUsed = 1
        #---2 Widgets---#

        headerL = tk.Label(root,text="MATMA",font=('Arial',90), bg='white')
        question = list()
        questionsAnswers = list()
        def createQuestion(ForcedOperation,RangeX,RangeY):
            try:
                global difficulty
                x = random.randint(RangeX[0],difficulty*RangeX[1])
                y = random.randint(RangeY[0],difficulty*RangeY[1])
                z = random.randint(1,random.randint(15,random.randint(25,35)))
                operation = random.randint(1,3)
                if ForcedOperation:
                    operation = ForcedOperation
                if operation == 4:
                    if x == 0:
                        x = random.randint(2,12)
                    if y == 0:
                        y = random.randint(2,12)
                    if z == 0:
                        z = random.randint(2,12)
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
                                try:
                                    createQuestion(4,RangeX,RangeY)
                                except:
                                    createQuestion(4,RangeX,RangeY)
                            else:
                                question.append(f"{z*x} / {y} ="); questionsAnswers.append(int((z*x)/y))
                    else:
                        if operation == 3:
                            question.append(f"{x} - {y} ="); questionsAnswers.append(x-y)
                        if operation == 4:
                            if y/x != int(y/x):
                                try:
                                    createQuestion(4,RangeX,RangeY)
                                except:
                                    createQuestion(4,RangeX,RangeY)
                            else:
                                question.append(f"{z*y} / {x} ="); questionsAnswers.append(int((z*y)/x))
            except ZeroDivisionError as e:
                createQuestion(4,RangeX,RangeY)

        
        for i in range(0,1000):
            createQuestion(random.randint(1,3),(1,30),(1,30))
            createQuestion(random.randint(2,2),(0,15),(0,15))
            createQuestion(random.randint(3,4),(1,60),(1,59))
            


        
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
                button1.config(state='normal')
                button2.config(state='normal')
                button3.config(state='normal')
                input1.config(state='normal')
                input2.config(state='normal')
                input3.config(state='normal')
                input1.delete(0, 'end')
                input2.delete(0, 'end')
                input3.delete(0, 'end')

        def saveSessionDataPoints():
            global allTimePoints,PointsInSession,difficulty,AccountPath,SelectedAcount,d2

            allTimePoints = allTimePoints + difficulty
            
            dumpJsonToFile(AccountPath,{"points":allTimePoints,"password":d2})
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
                    button1.config(state='disabled')
                    input1.config(state='readonly')
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
                    button2.config(state='disabled')
                    input2.config(state='readonly')
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
                    button3.config(state='disabled')
                    input3.config(state='readonly')
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

        #---3 1 Placing widgets on the root---#

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

AccountSelection()
if not AccountPath == "":
    difficultySettings()