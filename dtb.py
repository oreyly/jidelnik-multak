import fdb 
from fdb import fbcore
import pandas as pd

def Vsechno(i = 10):
    kurzor.execute("select rdb$field_name from rdb$relation_fields where rdb$relation_name='TFIRMA_TELEVIZE'")

    zahlavi = [str(nazev)[2:-3].strip() for nazev in kurzor.fetchall()]
    co = ", ".join(zahlavi)
    #zahlavi = ["FIRMA_NR", "LFD_JIDELNA"]
    kurzor.execute(f"SELECT {co} FROM TFIRMA_TELEVIZE")

    tabulka = pd.DataFrame(kurzor.fetchall()[:])
    tabulka.columns = zahlavi
    tabulka.to_excel("tab3.xlsx")

    print(tabulka)
    
pripojeni:fbcore.Connection = fdb.connect(
    dsn="192.168.100.203:SKLADPOS",
    user="praxe",
    password="praxe",
    role="user_admin",
    charset="UTF-8"
)

kurzor:fbcore.Cursor = pripojeni.cursor()

kurzor.execute("SELECT * from JIDELNA_JIDELAK_VYPIS_DW(?,?,?,?,?,?,?)",("18.5.2022",1,4,1,402,0,"NOW"))

for cislo in [vec[0] for vec in kurzor.fetchall()]:
    print(cislo)
    kurzor.execute("SELECT * FROM MULTIMEDIA_SKLAD(?,?) WHERE NN0 = 1", (cislo, "O"))
    x = kurzor.fetchall()
    print(x)
    l = x[0][-2]
    soub = open(f"{cislo}.jpeg","wb")
    try:
        soub.write(l)
    except:
        soub.write(l.read())
    soub.close()



#input()
"""
vypis = []

for datum in ["5.5.2022","11.5.2022"]:
    for i in range(3):
        for j in range(10):
            for k in range(3):
                for l in range(10):
                    for m in range(3):
                        kurzor.execute("SELECT * from JIDELNA_JIDELAK_VYPIS_DW(?,?,?,?,?,?,?)",(datum,i,j,k,l,m,"NOW"))
                        vypis.append(str(kurzor.fetchone()))
                        s = datum + " -> " + "/".join([str(clen) for clen in [i,j,k,l,m]]) + "\t->\t" + str(vypis[-1])
                        print(s)


print(len(vypis))
neco = [zapis for zapis in vypis if zapis != "None"]
print(len(neco))
print(neco)
"""
''' for i in range(1,30):
    for j in range(3):
        kurzor.execute("SELECT * from JIDELNA_JIDELAK_VYPIS_DW(?,?,?,?,?,?,?)",("16.5.2022",1,i,1,i*100+j,0,"NOW"))
        data = kurzor.fetchall()
        print(f"{j}/{i*100+1})")
        print(data)
        
        try:
            tab = pd.DataFrame(data[:])
            tab.columns = "JIDELAK_NR, DATUM, LFD_NN, SKLD_NR, SKLAD_NR, CENA, CENADPH, SKLD_NAZEV, SKLD_CENADPH".split(", ")
            print(tab)
            print()
        except:
            pass '''
        
pripojeni.commit()
