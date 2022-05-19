from __future__ import annotations
from random import randint
from tkinter import *
from tkinter import font
from PIL import ImageTk,Image

class DataJidla():
    nazev:str
    alergeny: list[int]
    obr:str
    
    def  __init__(self, jidlo:list):
        self.nazev = jidlo[1]
        self.alergeny = jidlo[2] or []
        self.obr = jidlo[0]

class FramSVecma():
    def __init__(self, mainWindow:Tk, fram: Frame, jidlo:DataJidla = None):
        self.fram = fram
        self.mainWindow = mainWindow
        self.VytvorFrame(jidlo)
    
    def VytvorFrame(self, jidlo: DataJidla):
        if(not jidlo):
            self.canv = None
            return
    
        self.obrO = Image.open(f"img/{jidlo.obr}.jpeg")
        self.canv = Canvas(self.fram,highlightthickness=0, bg="red")
        self.canv.pack(anchor=NW)
    
        self.alergFram = Frame(self.fram)
        self.alergFram.place(x=0,y=int(self.canv["height"]) - self.mainWindow.winfo_height() * 0.04)
        self.alergFram.pack_propagate(False)
    
        self.alerg = Label(self.alergFram, highlightthickness=0, text=f"Alergeny: {', '.join(jidlo.alergeny)}", fg="black", bg="white", anchor=W)
        self.alerg.pack(fill=BOTH, expand=True,anchor=NW)
    
        self.popisFram = Frame(self.fram)
        self.popisFram.pack(fill=BOTH, expand=True,anchor=NW)
    
        self.popis = Label(self.popisFram, highlightthickness=0, text=jidlo.nazev*5, fg="white", bg="black", anchor=NW)
        self.popis.pack(fill=BOTH, expand=True,anchor=NW)
    
    
    def ZmenilVelikost(self):
        if(not self.canv):
            return
    
        self.canv["height"]=int(self.height*0.8)
        self.canv["width"]=self.width-6
        #self.canv["width"]=500
        self.obrU = ImageTk.PhotoImage(self.obrO.resize((int(self.canv["width"]),int(self.canv["height"]))))
        #self.obrO.resize((int(self.canv["width"]),int(self.canv["height"]))).save(f"sesBuran{randint(0,100000)}.jpeg")
        self.canv.create_image(0,0,image=self.obrU,anchor=NW)     
        self.alergFram["height"] = self.mainWindow.winfo_height() * 0.04
        self.alergFram["width"] = self.canv["width"]
        print(self.alergFram["width"])
        print(self.canv["width"])
        self.alergFram.place(x=0,y=int(self.canv["height"]) - int(self.alergFram["height"]))  
    
    
        self.popis["font"]=font.Font(family="Arial",size=int(self.mainWindow.winfo_height()*0.019/4*3),weight=font.BOLD)
        self.popis["wraplength"]=self.canv["width"]
    

    @property
    def width(self):
        return self.fram["width"]

    @width.setter
    def width(self, value: int):
        self.fram["width"] = value
    
        self.ZmenilVelikost()
        
    @property
    def height(self):
        return self.fram["height"]
    
    @height.setter
    def height(self, value: int):
        self.fram["height"] = value
        
        self.ZmenilVelikost()
        
    @property
    def size(self):
        return (self.fram["width"], self.fram["height"])
    
    @size.setter
    def size(self, value):
        self.fram["width"] = value[0]
        self.fram["height"] = value[1]
        
        self.ZmenilVelikost()
        
if( __name__ == "__main__"):
    import Nacteni