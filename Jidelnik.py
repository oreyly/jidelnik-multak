from __future__ import annotations
from datetime import datetime
from doctest import NORMALIZE_WHITESPACE
from random import randint
from tkinter import *
import tkinter
from PIL import ImageTk,Image
from FramSVecma import FramSVecma, DataJidla

class Jidelnik():    
    def __init__(self, nazev, logo, radky, sloupce, ban, jidla:list[DataJidla]):
        self.VytvorOknoJidelniku(nazev, logo, radky, sloupce, ban, jidla)

    def NastavSirky(self):         
        if(self.mainWindow.winfo_height() != self.poslVys or self.mainWindow.winfo_width() != self.poslSir):
            self.poslVys = self.mainWindow.winfo_height()
            self.poslSir = self.mainWindow.winfo_width()

            self.zahlaviFram["width"] = self.poslSir
            self.zahlaviFram["height"] = self.poslVys * 0.08
            self.logoU = ImageTk.PhotoImage(self.logoO.resize((int(int(self.zahlaviFram["height"]) / self.logoO.height * self.logoO.width)-4, int(self.zahlaviFram["height"])-4)))
            self.zahlaviL.create_image(0,0,image=self.logoU, anchor=NW)
            
            self.zahlaviS["font"]=("Arial",self.zahlaviFram["height"]//4//4*3)
            
            self.zahlaviP["font"]=("Arial",self.zahlaviFram["height"]//3//4*3)

            

            framVel = [self.poslSir / (self.sloupce + 1 if self.baner != None else self.sloupce) - 4, self.poslVys * 0.92 / self.radky - 4]
            
            for radek in self.framy:
                for fr in radek:
                    fr.size = framVel
                    
                    #if(radek*self.sloupce+sloupec<len(self.obrazkyU)):
                    #    self.obrazkyU[radek*self.sloupce+sloupec] = ImageTk.PhotoImage(self.obrazkyO[radek*self.sloupce+sloupec].resize(int(framVel[0]),int(framVel[1])))
                    #    self.framy[radek][sloupec].create_image(0,0,image=self.obrazkyU[radek*self.sloupce+sloupec], anchor="nw")
                    
            
            if(self.baner!=None):
                    self.baner["width"] = framVel[0]
                    self.baner["height"] = self.poslVys * 0.92
                    self.i = ImageTk.PhotoImage(self.obr.resize((int(self.baner["width"]),int(self.baner["height"]))))
                    self.baner.create_image(0,0,image=self.i, anchor="nw")

    def UpravilOkno(self, event):
        self.NastavSirky()
        
    def Nacti(self, event):
        self.NastavSirky()

    def rgb_hack(rgb):
        return "#%02x%02x%02x" % rgb

    def VytvorBanner(self, okno):        
        self.obr = Image.open("img/102843.jpeg")
        
        can = Canvas(okno, bg="green", width=50, height=100, highlightthickness=0)
        
        return can

    def Konec(self, event:tkinter.Event):
        self.mainWindow.destroy()
    
    def Full(self, event:tkinter.Event):
        self.mainWindow.attributes("-fullscreen", not self.mainWindow.wm_attributes("-fullscreen"))
    
    def VytvorOknoJidelniku(self, nazev, logo, radky, sloupce, ban: bool, jidla:list[DataJidla]):
        self.poslVys = 0
        self.poslSir = 0
        
        self.sloupce = sloupce
        self.radky = radky
        
        self.framy:list[list[FramSVecma]] = []
        
        self.mainWindow = Tk()
        self.mainWindow.title(nazev)
        self.mainWindow["bg"]="black"
        self.mainWindow.geometry("1600x900")
        
        self.zahlaviFram = Frame(self.mainWindow, width=100, height=10, bg="green")
        self.zahlaviFram.grid(row=0, column=0, columnspan=sloupce + (1 if ban else 0))
        self.zahlaviFram.pack_propagate(False)
        
        
        self.zahlaviLFram = Frame(self.zahlaviFram, bg="black")
        self.zahlaviLFram.pack(fill=BOTH, expand=True, side=LEFT)
        self.zahlaviLFram.pack_propagate(False)
        
        self.logoO = Image.open(logo)
        self.zahlaviL = Canvas(self.zahlaviLFram, bg="black", highlightthickness=0)
        self.zahlaviL.pack(fill=BOTH, expand=True, side=LEFT, padx=10, pady=10)
        
        
        self.zahlaviSFram = Frame(self.zahlaviFram)
        self.zahlaviSFram.pack(fill=BOTH, expand=True, side=LEFT)
        self.zahlaviSFram.pack_propagate(False)
        
        self.zahlaviS = Label(self.zahlaviSFram, text=datetime.now().strftime("%d. %m. %Y - %H:%M:%S"), bg="black", fg="white", highlightthickness=0)
        self.zahlaviS.pack(fill=BOTH, expand=True, side=LEFT)
        
        
        self.zahlaviPFram = Frame(self.zahlaviFram)
        self.zahlaviPFram.pack(fill=BOTH, expand=True, side=LEFT)
        self.zahlaviPFram.pack_propagate(False)
        
        self.zahlaviP = Label(self.zahlaviPFram, text=nazev, bg="black", fg="white", highlightthickness=0, anchor=E)
        self.zahlaviP.pack(fill=BOTH, expand=True, side=LEFT)
        
        for radek in range(radky):
            self.framy.append([])
            for sloupec in range(sloupce):                
                fr = Frame(self.mainWindow, bg="black", width=30, height=30, highlightthickness=1, highlightbackground="white", padx=2, pady=2)
                fr.grid(row=(radek + 1),column=sloupec) #+1 Kvůli nadpisu
                fr.pack_propagate(False)
                
                if(radek*sloupce+sloupec<len(jidla)):
                    self.framy[radek].append(FramSVecma(self.mainWindow, fr, jidla[radek*sloupce+sloupec]))
                else:
                    self.framy[radek].append(FramSVecma(self.mainWindow, fr))
            
        if(ban):
            self.baner = self.VytvorBanner(self.mainWindow)
            self.baner.grid(row=1,column=sloupce,rowspan=radky)
        else:
            self.baner = None
            
        self.mainWindow.bind("<Configure>", self.Nacti)
        self.mainWindow.bind("<Escape>", self.Konec)
        self.mainWindow.bind("q", self.Full)
        
        mainloop()
        
if( __name__ == "__main__"):
    import Nacteni