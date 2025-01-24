import tkinter as tk

GameVersion = 1.0

root = tk.Tk()
root.config(bg='white')

label1 = tk.Label(root,text=f"Wersja: {GameVersion}",font=('Arial',20), bg='white')
label1.place(x=0,y=0)

root.mainloop()