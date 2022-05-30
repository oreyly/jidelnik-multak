from __future__ import annotations
import os

os.environ['path'] += r';C:\Program Files\UniConvertor-2.0rc5\dlls'

import io
from tkinter import *
from tkinter import font

from PIL import ImageTk,Image
import cairosvg

class DataJidla():
    nazev:str
    alergeny: list[int]
    obr:str
    cena: int
    
    def  __init__(self, jidlo:list):
        self.nazev = jidlo[1]
        self.alergeny = jidlo[2].split(",") or []
        self.obr = jidlo[0]
        self.cena = jidlo[3]

class FramSVecma():
    @classmethod
    def PripravDefObr(self, cesta: str, zobrAlerg: bool, zobrCeny: bool, padd: int):
        self.defObrData = cairosvg.svg2png(url=cesta)
        self.defObr = Image.open(io.BytesIO(self.defObrData))
        
        self.zobrAlerg = zobrAlerg
        self.zobrCeny = zobrCeny
        
        self.padd = padd
    
    @staticmethod
    def RozdelMezerama(hodnota: any, delkaCasti: int = 3, separator: str = " ") -> (str):
        hodnota:str = str(hodnota)
        
        delka = len(hodnota)

        vys = ""
        
        for i in range(delka):
            if(i % delkaCasti == 0 and i > 0):
                vys = separator + vys
            
            vys = hodnota[delka - 1 - i] + vys

        return vys
    
    def __init__(self, mainWindow:Tk, fram: Frame, jidlo:DataJidla = None):
        self.fram = fram
        self.mainWindow = mainWindow
        self.VytvorFrame(jidlo)
    
    def VytvorFrame(self, jidlo: DataJidla):
        if(not jidlo):
            self.canv = None
            return
    
        if(os.path.isfile(f"img/{jidlo.obr}.jpeg")):
            self.obrO = Image.open(f"img/{jidlo.obr}.jpeg")
            self.pouzivaDefObr = False
        else:
            self.pouzivaDefObr = True
            self.obrO = self.defObr
            
        self.canv = Canvas(self.fram,highlightthickness=0, bg="black")
        self.canv.pack(anchor=NW)
        
        if(self.zobrAlerg or self.zobrCeny):
            self.alergcenaFram = Frame(self.fram)
            self.alergcenaFram.place(x=0,y=int(self.canv["height"]) - self.mainWindow.winfo_height() * 0.04)
            self.alergcenaFram.pack_propagate(False)
            
            self.alerg = Label(self.alergcenaFram, highlightthickness=0, text=(f"Alergeny: {', '.join([str(alergen) for alergen in jidlo.alergeny])}" if self.zobrAlerg else ""), fg="black", bg="white", anchor=W)
            self.alerg.pack(fill=BOTH, expand=True,anchor=NW,side=LEFT)
            
            self.cena = Label(self.alergcenaFram, highlightthickness=0, text=(f"{self.RozdelMezerama(jidlo.cena)} Kč" if self.zobrCeny else ""), fg="black", bg="white", anchor=E)
            self.cena.pack(fill=BOTH, expand=True,anchor=NW,side=LEFT)
        
        self.popisFram = Frame(self.fram)
        self.popisFram.pack(fill=BOTH, expand=True,anchor=NW)
    
        self.popis = Label(self.popisFram, highlightthickness=0, text=jidlo.nazev, fg="white", bg="black", anchor=NW, justify=LEFT)
        self.popis.pack(fill=BOTH, expand=True,anchor=NW)
    
    
    def ZmenilVelikost(self):
        if(not self.canv):
            return
    
        nov = (self.width - 2 - self.padd*2, int(self.height*0.75))
        
        novObr:tuple[int]
        sour:tuple[int]
        
        ratioO = self.obrO.width/self.obrO.height
        ratioN = nov[0]/nov[1]
        
        if(ratioO>ratioN or self.pouzivaDefObr):
            novObr = (int(nov[1] / self.obrO.height * self.obrO.width),nov[1])
            if(self.pouzivaDefObr):
                sour=(abs(nov[0] - novObr[0])/2,0)
            else:
                sour=(-abs(nov[0] - novObr[0])/2,0)
                
        else:
            novObr = (nov[0],int(nov[0] / self.obrO.width * self.obrO.height))
            sour = (0, -abs(nov[1] - novObr[1])/2)
            
        self.canv["width"]=nov[0]
        self.canv["height"]=nov[1]
        
        self.obrU = ImageTk.PhotoImage(self.obrO.resize(novObr))
        self.canv.create_image(sour[0], sour[1],image=self.obrU, anchor=NW)     
        
        if(self.zobrAlerg or self.zobrCeny):    
            self.alergcenaFram["height"] = self.mainWindow.winfo_height() * 0.04
            self.alergcenaFram["width"] = self.canv["width"]
            self.alergcenaFram.place(x=0,y=int(self.canv["height"]) - int(self.alergcenaFram["height"]))  
        
            self.cena["font"]=font.Font(family="Arial",size=int(self.mainWindow.winfo_height()*0.017/4*3),weight=font.BOLD)
            self.cena["wraplength"]=self.alergcenaFram["width"]
            
            self.alerg["font"]=font.Font(family="Arial",size=int(self.mainWindow.winfo_height()*0.017/4*3),weight=font.BOLD)
            self.alerg["wraplength"]=self.alergcenaFram["width"]
            
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