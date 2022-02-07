from enum import Enum
from matplotlib.pyplot import close 
import core as cr



#finde und lese die Datei. Falls nicht gefunden, frage nochmal.
def frage_nach_Dateiname():
    bedingung = True
    while bedingung:
        #table = input('Geben Sie die Name Bzw. Pfad der Datei ein, die Sie analysieren moechten: ') 
        #Obige Zeile ist kommentiert, damit man nicht immer wieder "Motoren.csv" eingeben muss
        table = "Motoren.csv"
        if (bedingung != 0):
            daten = cr.FileCheck(table)
            bedingung=False
            return daten

#frage den den Benutzer fuer welches Merkmal er eine Haeufigkeitstabelle erstellen moechte
#fuer Merkmale MOD, Fehler, DZ wird die funktion haefigkeitstabelle(merkmal, daten) aufgerufen
#fuer Merkmale MOD, Fehler, DZ wird die funktion klassenHaefigkeitstabelle(merkmal, daten, eps) aufgerufen  
def frage_welches_Merkmal(merkmale):
    i = 0
    for x in merkmale:
        i+=1
        print( i,':', x )
    print("0 : beenden")

    wahl = input("\nWaehlen Sie, welches Merkmal moechten Sie gerne analysieren: ")
    wahl = cr.InputIntCheck(wahl)
    
    return wahl


#drucke die Menue um den Benutzer zu fragen welche Kennwerte zu berechnen sind
def frage_welche_Stichprobenkennwerte():   
    print("Stichprobenkennwerte berechnen:\n")
    kennwerte = ["Mittelwert", "Median", "Quantile", "Modus", "Spannweite", "Quartilabstand", "Streuung", "Standardabweichung", "Alles"]
    i = 0
    for x in kennwerte:
        i+=1
        print( [i] , x )
    print("\nGeben Sie die Nummer der Werte ein, drucken Sie auf Enter nach jeder Eingabe")
    print("Um die Eingabe zu beenden, muessen Sie irgendeinen Buchstaben eingeben.")
    
    try:
        werte = []
        while True:
            w = int(input())
            if w == 9:
                return [1,2,3,4,5,6,7,8]
            if w > 0 and w < 9 :
               werte.append(w)       
    except:
        return(werte)

#drucke die Menue um den Benutzer zu fragen welche Kennwerte zu berechnen sind
def frage_welche_Stichprobenkennwerte_basis_Klasse():
    print("Stichprobenkennwerte berechnen:\n")
    kennwerte = ["Mittelwert", "Median", "Quantile", "Streuung", "Standardabweichung", "Alles"]
    i = 0
    for x in kennwerte:
        i+=1
        print( [i] , x )
    print("\nGeben Sie die Nummer der Werte ein, drucken Sie auf Enter nach jeder Eingabe")
    print("Um die Eingabe zu beenden, muessen Sie irgendeinen Buchstaben eingeben.")
    
    try:
        werte = []
        while True:
            w = int(input())
            if w == 6:
                return [1,2,3,4,5]
            if w > 0 and w < 6 :
               werte.append(w)       
    except:
        return(werte)

#Frage den Benutzer, ob er die Stichprobenkennwerte fuer Stetige Daten auf Basis der Stichprobendaten oder auf Basis der klassifizierten Daten berechnen moechte.
def frage_nach_Basis():
    print("Stichprobenkennwerte:\n----------------------")
    print("1: auf Basis der Stichprobendaten.")
    print("2: auf Basis der klassifizierten Daten.") 
    while True:
        basis = input("Basis:") 
        if basis in ('1','2'):
                break
    return (basis)

#Frage den Benutzer, ob er Balkendiagramm oder Tortendiagramm fuer ein Merkmal erstellen moechte
def frage_Welches_Diagramm():
    while True:
        wahl = input("Welches Diagramm?\n------------------\n1: Balkendiagramm.\n2: Tortendiagramm.\n0: ueberspringen.\n----------------->  ")
        if wahl in ('1','2','0'):
            break
    return wahl

#Hilfsmethode, um run() Methode in einer Schleife zu laufen bis der benutzer beenden moechte
#Die Methode bekommt eine Methode als Eingabe
def schleife(method):
    method()
    while True:
        while True:
            wahl = str(input('\nMenue wieder zeigen? (y/n): '))
            PrintLine()
            if wahl in ('y','Y', 'n', 'N'):
                break
            print("Falsche Eingabe.")
        if wahl == 'y' or wahl == 'Y':              
            method()
        else:
            break

#Hilfsmethode, um schneller und Kompakter eine Linie zu ducken 
def PrintLine():
    print ("==========================================\n")