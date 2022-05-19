from __future__ import annotations
from datetime import datetime
import string
import fdb 
from fdb import fbcore
import configparser
import os

from Multak import Multak
from Jidelnik import Jidelnik
from FramSVecma import DataJidla

def NactiObrazky(NRka):
    if(not os.path.isdir("img")):
        os.mkdir("img")
        
    if(len(NRka)==0):
        raise Exception("Nic není")
    
    for NR in NRka:
        kurzor.execute("SELECT * FROM MULTIMEDIA_SKLAD(?,?) WHERE NN0 = 1", (NR, "O"))
        
        l = kurzor.fetchall()[0][-2]
        
        if(not os.path.isfile(f"img/{NR}.jpeg")):
            soub = open(f"img/{NR}.jpeg","wb")
            
            try:
                soub.write(l)
            except:
                soub.write(l.read())
            
            soub.close()

def ZpracujDulezite(jidla):
    vys = []
    for jidlo in jidla:
        vys.append(DataJidla([jidlo[i] for i in [3, 7, 8]]))
        
    return vys

config = configparser.ConfigParser()
config.read("conf.ini")

conf = dict(config.items("data"))

pripojeni:fbcore.Connection = fdb.connect(
    dsn="192.168.100.203:SKLADPOS",
    user=conf["user"],
    password=conf["pswd"],
    role=conf["role"],
    charset=conf["charset"]
)

kurzor:fbcore.Cursor = pripojeni.cursor()

kurzor.execute(f"SELECT first 1 FIRMA_NR, LFD_JIDELNA, ROZMER_ZOBRAZENI, NAZEV_JIDELNA FROM TFIRMA_TELEVIZE WHERE LFD_JIDELNA={conf['lfd']}")

data = kurzor.fetchone()

if (data[2] == None):
    Multak("")
else:
    kurzor.execute("SELECT * from JIDELNA_JIDELAK_VYPIS_DW(?,?,?,?,?,?,?)",(datetime.today(),1,data[0],1,data[1],0,"NOW"))
    
    jidla:list[DataJidla] = ZpracujDulezite(kurzor.fetchall())
    
    print(jidla[0])
    
    NactiObrazky([jidlo.obr for jidlo in jidla])
    
    rozmery = [int(x) for x in data[2].split("x")]
    
    Jidelnik(data[3], "logo.png", rozmery[0],rozmery[1],True, jidla)