from matplotlib import pyplot as plt
from numpy.lib.function_base import quantile
from tabulate import tabulate
import core as cr
import prints as pr
import math


#Triggering the entire Project
#Do this by python run.py

def run():
    daten = pr.frage_nach_Dateiname()
    wahl = pr.frage_welches_Merkmal(daten.columns)
   
    if wahl in [1, 2, 6]:
        merkmal = daten.columns[wahl-1]   
        tab = cr.haefigkeitstabelle(merkmal, daten)                                    #erstelle Tabelle
        print(tabulate(tab, headers=tab.keys(), tablefmt='fancy_grid'))                #drucke Tabelle
        pr.PrintLine()

        diagamm_diskret(merkmal, tab)                                                 #erstelle diagramm 
        pr.PrintLine()

        if wahl in [1,6]:
            kennwerte = pr.frage_welche_Stichprobenkennwerte()
            stichprobenkennwerte_basis_Stichprobendaten(merkmal, daten, kennwerte)
        else:
            pr.schleife(run)

    elif wahl in [3,4,5]:
        merkmal = daten.columns[wahl-1]
        epsilon = input("Geben Sie die Messgenauigkeit ein (epsilon): ")
            
        #return Werte der Mehtode klassenHaefigkeitstabelle sind folgendes: ret[0]=tab , ret[1]=k , ret[2]=b , ret[3]=a1_u
        ret = cr.klassenHaefigkeitstabelle(merkmal, daten, float(epsilon))
        tab = ret[0]
        b = ret [2]
        print(tabulate(tab, headers=tab.keys(), tablefmt='fancy_grid'))
        pr.PrintLine()     
        
        diagamm_stetig(merkmal, tab)      #erstelle diagramm 
        pr.PrintLine() 
        
        basis = pr.frage_nach_Basis()       #Auf welche Basis?
        pr.PrintLine()

        if(basis == '1'):
            kennwerte = pr.frage_welche_Stichprobenkennwerte()    
            stichprobenkennwerte_basis_Stichprobendaten(merkmal, daten, kennwerte)      
        elif(basis == '2'):
            kennwerte = pr.frage_welche_Stichprobenkennwerte_basis_Klasse()    
            stichprobenkennwerte_basis_klassifizierten_Daten(daten, tab, b, kennwerte)
            

    elif wahl == 0:
        return


#Verwalte die Erstellung einer Diagramm fuer diskrete Daten
def diagamm_diskret(merkmal, tab):
    wahl = pr.frage_Welches_Diagramm()
    if wahl == '1':
        cr.balkendiagramm_diskret(merkmal, tab)
    elif wahl == '2':
        cr.tortendiagramm_diskret(tab)
    elif wahl == '0':
        return
 
 
#Verwalte die Erstellung einer Diagramm fuer stetige Daten
def diagamm_stetig(merkmal, tab):
    wahl = pr.frage_Welches_Diagramm()
    if wahl == '1':
        cr.balkendiagramm_stetig(merkmal, tab)
    elif wahl == '2':
        cr.tortendiagramm_stetig(tab)
    elif wahl == '0':
        return


#Verwalte die Berchnung von stichprobenkennwerte auf Basis der Stichprobendaten
def stichprobenkennwerte_basis_Stichprobendaten(merkmal, daten, kennwerte):
    spalte = daten[merkmal]
    if merkmal in ["Lebensdauer", "T0", "T30"]:
        spalte = cr.konvertiere_string_float(spalte)
    pr.PrintLine()
    for wert in kennwerte:
        if wert == 1:
            mittel = cr.arithMittel_basis_Stichprobendaten(spalte)
            print ("Arithmetisches Mittel: ", mittel, "\n")   
        elif wert == 2:
            median = cr.median_basis_Stichprobendaten(spalte)
            print ("Median: ", median,"\n")    
        elif wert == 3:
            quantile = cr.quantile_basis_stichprobendaten(spalte)
            print("Quantile: 1-Qunatile:", quantile[0],",2-Qunatile:",quantile[1],",3-Qunatile:",quantile[2], "\n")
        elif wert == 4:
            modus = cr.modus_basis_Stichprobendaten(spalte)
            print("Modus: ", modus, "\n")     
        elif wert == 5:
            spannweite = cr.spannweite_basis_Stichprobendaten(spalte)
            print("Spannweite: ", spannweite, "\n")
        elif wert == 6:
            quartilsabstand = cr.quartilsabstand_basis_Stichprobendaten(spalte)
            print("Quartilsabstand: ", quartilsabstand, "\n")
        elif wert == 7:
            median = cr.median_basis_Stichprobendaten(spalte)
            streuung= cr.streuung_basis_Stichprobendaten(daten, spalte, median)
            print ("Streuung: ", streuung, "\n")   
        elif wert == 8:   
            stdAbw= cr.standardabweichung__basis_Stichprobendaten(streuung)
            print ("Standardabweichung: ", stdAbw, "\n")

            
#Verwalte die Berchnung von stichprobenkennwerte auf Basis der klassifizierten Daten
def stichprobenkennwerte_basis_klassifizierten_Daten(daten, tab, b, kennwerte):
    tab = cr.klassenmitte(tab)
    print ("==========================================\n"
            + "==========================================\n "
            + "Neue Tabelle mit einer neuen Spalte (Klassenmitte) xi:")
    print(tabulate(tab, headers=tab.keys(), tablefmt='fancy_grid'))
    pr.PrintLine()

    for wert in kennwerte:
        if wert == 1:
            mittel = cr.arithmetisches_Mittel_basis_Tabelle(tab)
            print ("Arithmetisches Mittel: ", mittel, "\n")
        elif wert == 2:
            median = cr.median_basis_Tabelle(daten, tab, b)
            print ("Median: ", median,"\n")
        elif wert == 3:
            quantile_1 = cr.quantile_basis_Tabelle(daten, tab, b, 0.25)
            quantile_2 = cr.quantile_basis_Tabelle(daten, tab, b, 0.5)
            quantile_3 = cr.quantile_basis_Tabelle(daten, tab, b, 0.75)
            print("Quantile: 1-Qunatile:", quantile_1,",2-Qunatile:",quantile_2,",3-Qunatile:",quantile_3, "\n")
        elif wert == 4:
            streuung= cr.streuung_basis_Tabelle(mittel, tab)
            print ("Streuung: ", streuung, "\n")
        elif wert == 5:   
            streuung= cr.streuung_basis_Tabelle(mittel, tab)
            stdAbw= cr.standardabweichung__basis_Tabelle(streuung)
            print ("Standardabweichung: ", stdAbw, "\n")

    
########

#run Methode fuehrt das ganze Programm aus.     
pr.schleife(run)
