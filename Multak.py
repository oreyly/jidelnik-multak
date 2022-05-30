from ast import Mult
from tkinter import *
import vlc
import pafy

class Multak():
    def __init__(self, zdroj, zvuk = False, URL = False):
        self.VytvorOknoMultaku(zdroj, zvuk, URL)
     
    def NastavSirky(self):         
        if(self.mainWindow.winfo_height() != self.poslVys or self.mainWindow.winfo_width() != self.poslSir):
            self.poslVys = self.mainWindow.winfo_height()
            self.poslSir = self.mainWindow.winfo_width()
            
            self.zahlaviFram["width"] = self.poslSir
            self.zahlaviFram["height"] = self.poslVys * 0.08
            
            self.videoCan["width"] = self.poslSir
            self.videoCan["height"] = self.poslVys * 0.9

            self.butFram["width"] = self.poslSir
            self.butFram["height"] = self.poslVys * 0.02
    
    def UpravilOkno(self, event):
        self.NastavSirky()

    def VytvorVideo(self):
        self.videoCan.destroy()
        self.videoCan = Canvas(self.mainWindow, width = self.poslSir, height = int(self.poslVys * 0.9), bg="black", highlightthickness = 0)
        self.videoCan.grid(row=1,column=0)
        self.play()
    
    def GetHandle(self):
        return self.videoCan.winfo_id()
    
    def play(self):
        self.VLCprehravac:vlc.MediaPlayer = vlc.MediaPlayer(self.zdroj)  
        self.VLCprehravac.audio_set_mute(self.zvuk)

        self.VLCprehravac.set_hwnd(self.GetHandle())
        
        em = self.VLCprehravac.event_manager()
        em.event_attach(vlc.EventType.MediaPlayerEndReached, self.onEnd)

        self.VLCprehravac.play()
    
    def hej(self, event):
        if(self.VLCprehravac and self.VLCprehravac.is_playing()):
            self.pauza = True
            self.VLCprehravac.pause()
        elif(self.pauza):
            self.VLCprehravac.pause()
        else:
            self.VytvorVideo()
    
    def onEnd(self, event:vlc.Event):
        if event.type == vlc.EventType.MediaPlayerEndReached:
            self.VytvorVideo()

    def VytvorOknoMultaku(self, zdroj, zvuk, URL):
        self.poslVys = 0
        self.poslSir = 0
        
        if(URL):
            video = pafy.new(zdroj)
            videolink = video.getbest()
            self.zdroj = videolink.url
        else:
            self.zdroj = zdroj
        
        self.zvuk = zvuk
        self.pauza = False
        self.VLCprehravac = None
        
        self.mainWindow = Tk()
        self.mainWindow.geometry("800x800")
        
        self.zahlaviFram = Frame(self.mainWindow, width=100, height=10, bg="green")
        self.zahlaviFram.grid(row=0, column=0)
        self.zahlaviFram.pack_propagate(False)
        
        self.zahlavi = Label(self.zahlaviFram, text="La Freska", bg="black", fg="white", highlightthickness=0)
        self.zahlavi.pack(fill=BOTH, expand=True)
        
        self.videoCan = Canvas(self.mainWindow, width = self.poslSir, height = int(self.poslVys * 0.9), bg="green", highlightthickness = 0)
        self.videoCan.grid(row=1, column=0)
        
        self.butFram = Frame(self.mainWindow, width=100, height=10, bg="green")
        self.butFram.grid(row=2, column=0)
        self.butFram.pack_propagate(False)
        
        self.but = Button(self.butFram, text="Start\Stop", bg="brown", highlightthickness=0)
        self.but.pack(fill=BOTH, expand=True)
        self.but.bind("<Button>", self.hej)
        
        self.mainWindow.bind("<Configure>", self.UpravilOkno)
        
        mainloop()