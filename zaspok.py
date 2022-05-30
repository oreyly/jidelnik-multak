from tkinter import *

okno = Tk()

okno.geometry("400x400")

lab = Label(okno, width=50, height=2, bg="red", fg="white", text="T"*50)
lab.wm_a
lab.grid(row=0, column=0)

okno.mainloop()