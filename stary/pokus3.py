from tkinter import *

ws = Tk()
ws.title('PythonGuides')
ws.geometry('400x300')
ws.config(bg='black')

frame = Frame(ws, bg='yellow', width=100, height=100)

frame.grid(column=0, row=0)
frame.grid_propagate(False)

Button(frame, text="another line").grid(row=0, sticky=EW)

ws.mainloop()