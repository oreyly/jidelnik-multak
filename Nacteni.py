from __future__ import annotations
from datetime import datetime
import fdb 
from fdb import fbcore
import configparser
import os

from Multak import Multak
from Jidelnik import DataJidelniku, Jidelnik
from FramSVecma import DataJidla


def englise(SKLD_NR: str, target_SKLD: int = 1):
    SKLD_NR = str(SKLD_NR)
    
    if (len(SKLD_NR) >= 7 ):
        over = len(SKLD_NR) - 5
        SKLD_NR = int(SKLD_NR[over:])
    else:
        SKLD_NR = int(SKLD_NR[1:]);

    return ((target_SKLD * 100000) + SKLD_NR);

def NactiObrazky(NRka):
    if(not os.path.isdir("img")):
        os.mkdir("img")
        
    if(len(NRka)==0):
        raise Exception("Nic není")
    
    for NR in NRka:
        if(os.path.isfile(f"img/{NR}.jpeg")):
            continue
        
        kurzor.execute("SELECT * FROM MULTIMEDIA_SKLAD(?,?) WHERE NN0 = 1", (NR, "O"))
        
        dt = kurzor.fetchall()
        
        if(len(dt)==0):
            novNR = englise(NR)
            kurzor.execute("SELECT * FROM MULTIMEDIA_SKLAD(?,?) WHERE NN0 = 1", (novNR, "O"))
            
            dt = kurzor.fetchall()
            
            if(len(dt)==0):
                continue
            
        l = dt[0][-2]
        
        soub = open(f"img/{NR}.jpeg","wb")
        
        try:
            soub.write(l)
        except:
            soub.write(l.read())
        
        soub.close()
    
    print("Hotovo")

def ZpracujDulezite(jidla):
    vys = []
    for jidlo in jidla:
        vys.append(DataJidla([jidlo[i] for i in [3, 7, 8, 6]]))
        
    return vys

config = configparser.ConfigParser()
config.read("conf.ini")

conf = dict(config.items("data"))

pripojeni:fbcore.Connection = fdb.connect(
    dsn=conf["dsn"],
    user=conf["user"],
    password=conf["pswd"],
    role=conf["role"],
    charset=conf["charset"]
)

kurzor:fbcore.Cursor = pripojeni.cursor()

kurzor.execute(f"SELECT first 1 FIRMA_NR, LFD_JIDELNA, ROZMER_ZOBRAZENI, NAZEV_JIDELNA, ZOB_CENA, ZOB_ALERGENY, BANER_FORMAT FROM TFIRMA_TELEVIZE WHERE LFD_JIDELNA={conf['lfd']}")

data:list = [dato for dato in kurzor.fetchone()]

data[-1] = data[-1] in [1, 2]

data.append("pokus.jpg")
data.append("logo.png")

if (data[2] == None):
    Multak("")
else:
    kurzor.execute("SELECT * from JIDELNA_JIDELAK_VYPIS_DW(?,?,?,?,?,?,?)",(datetime.today(),1,data[0],1,data[1],0,"NOW"))
    
    jidla:list[DataJidla] = ZpracujDulezite(kurzor.fetchall())
    
    print(jidla[0])
    
    NactiObrazky([jidlo.obr for jidlo in jidla])
    
    Jidelnik(DataJidelniku([data[x] for x in [3,-1, 2, 6, -2, 4, 5]]), jidla)