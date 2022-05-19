import textwrap
from tkinter import *
from tkinter import font
from PIL import ImageFont

def Radku():
    global i
    fo = ImageFont.truetype('arial.ttf', i)
    
    delky:list[int] = []
    maxi = int(f["width"])
    slova = l["text"].split(" ")
    delkaMezery = fo.getsize(" ")[0]
    
    for slovo in slova:
        delky.append(fo.getsize(slovo)[0])
    
    radky = 1
    delka = 0
    
    index = 0
    while(index < len(delky)):
        delkaSlova = delky[index]
        
        if(delkaSlova>maxi):
            while(delkaSlova>maxi):
                radky+=1
                delkaSlova-=maxi
            else:
                radky+=1
                delka = delkaSlova + delkaMezery if delkaSlova > 0 else 0
                index+=1
                continue
        
        delka+=delkaSlova
        
        if(delka>maxi):
            delka-=delkaSlova
            
            if(delka>0):
                radky+=1
                delka = delkaSlova
    
    print(delky)
    
    #print(f"Řádků: {}")

def Plus(event):
    global i
    i+=1
    l["font"] = font.Font(family="Arial", size=i)
    Radku()
    
    
def Minus(event):
    global i
    i-=1
    l["font"] = font.Font(family="Arial", size=i)
    Radku()


global i
i=10
okno = Tk()
okno.geometry("300x500")

f = Frame(okno, height=100, width=300)
f.grid(row=0,column=0)
f.pack_propagate(False)
l = Label(f, bg="green", wraplength=int(f["width"]), font=("Arial",i), text="Docelahodněvelkejatakévelicedlouhejtext,Docelahodně velkej a také velice dlouhej text, Docela hodně velkej a také velice dlouhej text")
l.pack(fill=BOTH, expand=True)

b1 = Button(okno, text="+")
b1.grid(row=1,column=0)
b1.bind("<Button-1>", Plus)

b2 = Button(okno, text="-")
b2.grid(row=2, column=0)
b2.bind("<Button-1>", Minus)

okno.mainloop()