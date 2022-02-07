from datetime import date
from numpy.lib.function_base import average
import pandas as pd
import numpy as np
from pandas.core.indexes.interval import interval_range
from tabulate import TableFormat, tabulate
from prettytable import PrettyTable
import math
import statistics
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick


      
#------------------------------------------------------------Haefigkeitstabellen------------------------------------------------------------------

#Die Mehtode bekommt die Daten unerer Datei mit Name des Merkmals, das der benutzer ausgewaehlt hat.
#Es wird eine haeufigkeitstabelle zurueckgegben
def haefigkeitstabelle(merkmal, daten):    

    #zaehle wie haefig jedes betrag in unserer Merkmal-Spalte aufgetreten ist
    tab = daten[merkmal].value_counts(ascending=True)  
    
    #erstelle eine Tabelle fuer das Merkmal mit Spalten: ai und Hn(ai)
    tab = pd.DataFrame({'ai': tab.keys(), 'Hn(ai)': tab.values})

    #sortiere die Zeilen nach ai
    tab = tab.sort_values(by=['ai'])
    tab = tab.reset_index(drop=True)

    #berechne und fuege neue Spalte hn(ai) ein
    tab['hn(ai)'] = round(tab['Hn(ai)']/len(daten)*100).astype(str) + ' %'

    #berechne und fuege neue Spalte H(i) ein 
    tab['H(i)'] = tab['Hn(ai)'].cumsum()

    #berechne und fuege neue Spalte h(i) ein 
    tab['h(i)'] = round (tab['H(i)']/len(daten)*100).astype(str) + ' %'

    return tab
 
#------------------------------------------------------------KlassenHaefigkeitstabellen----------------------------------------------------------

#Die Mehtode bekommt die Daten unerer Datei mit Name des Merkmals, das der benutzer ausgewaehlt hat.
#wir schneiden die gezielte Spalte und erstellen eine Klassenhaefigkeitstabelle
#Es wird eine Klassenhaefigkeitstabelle zurueckgegben, zusaetzlich wird k, b, und a1_u zurueckgegeben
def klassenHaefigkeitstabelle(merkmal, daten, eps): 
    
    #konvertiere die Zahlen unserer Spalte wie '2,13', die als string gelesen werden, zu dieser Form '2.13' ---> float getrennt durch Punkt 
    tab = konvertiere_string_float(daten[merkmal])

    #berechne, zu wie viel Intervalls werden die Beitraege zugeoerdnet 
    k = round(np.sqrt(len(daten)))

    #Berechne Anfangspunkt vom ersten Intervall
    a1_u = round (tab.min() - (eps/2) , 2 )

    #Berechne die Breite von jedem Intervall
    b = round( ( (tab.max()- tab.min() + eps) / k ) + 0.04, 1)

    #Klassifizire die Beitraege unserer Spalte im jeweiligen Intervall, und zaehle wie viel Beitraege jedes Intervall inthaelt
    tab = tab.groupby(pd.cut(tab, np.arange(a1_u, (a1_u+b*5)+0.1, b))).count()

    #gebe unsere Tabelle eine Ueberschrift
    tab = pd.DataFrame({'Ki': tab.keys(), 'Hn(Ki)': tab.values})

    #add new column for hn(Ki)
    tab['hn(Ki)'] = round(tab['Hn(Ki)']/len(daten)*100).astype(str) + ' %'

    #berechne und fuege neue Spalte H(i) ein 
    tab['H(i)'] = tab['Hn(Ki)'].cumsum()

    #berechne und fuege neue Spalte h(i) ein 
    tab['h(i)'] = round (tab['H(i)']/len(daten)*100).astype(str) + ' %'

    return tab, k , b ,a1_u

#------------------------------------------------------------Diagramme fuer Haefigkeitstabellen--------------------------------------------------------

#Balkendiagramm fuer dikrete Daten (Darstellung der Haufigkeitstabelle)
def balkendiagramm_diskret(merkmal, tab):
    x_pos = np.arange(len(tab['ai']))
    plt.bar(x_pos, tab['Hn(ai)'], color = (0.5,0.1,0.5,0.6))

    plt.title(merkmal)        #fuege Ueberschrift der Tabelle ein (Name des Merkmal)
    plt.xlabel('Merkmalsauspraegungen')    #fuege das Wort 'Merkmalsauspraegungen' auf x-Achse   
    plt.ylabel('hn(ai)/Hn(ai)')          #fuege hn(ai)/Hn(ai) auf x-Achse  
    plt.xticks(x_pos, tab['ai'])   #drucke die Merkmalsauspraegungen auf x-Achse (die Beitraege)
    plt.show()                      #druecke Diagramm
    

#Tortendiagramm fuer dikrete Daten (Darstellung der Haufigkeitstabelle)
def tortendiagramm_diskret(tab):  
    x_pos = tab['hn(ai)'].apply(lambda x: float(x.replace('%','')))
    plt.pie(x_pos, labels = tab['ai'], autopct='%1.0f%%', pctdistance=0.5, labeldistance=1.2)
    plt.show()


#--------------------------------------------------------Diagramme fuer KlassenHaefigkeitstabellen--------------------------------------------------------

#Balkendiagramm fuer stetigte Daten (Darstellung der Klassenhaufigkeitstabelle)
def balkendiagramm_stetig(merkmal, tab):
    x_pos = np.arange(len(tab['Ki']))
    plt.bar(x_pos, tab['Hn(Ki)'], color = (0.5,0.1,0.5,0.6))
    
    plt.title(merkmal)        #fuege Ueberschrift der Tabelle ein (Name des Merkmal)
    plt.xlabel('Intervalls')    #fuege das Wort 'Intervalls' auf x-Achse   
    plt.ylabel('hn(Ki)/Hn(Ki)')       #fuege hn(Ki)/Hn(Ki) auf x-Achse  
    plt.xticks(x_pos, tab['Ki'])  #drucke die Intervalls auf x-Achse
    plt.show()                      #druecke Diagramm

    
#Tortendiagramm fuer stetigte Daten (Darstellung der Klassenhaufigkeitstabelle)
def tortendiagramm_stetig(tab):
    x_pos = tab['hn(Ki)'].apply(lambda x: float(x.replace('%','')))
    plt.pie(x_pos, labels = tab['Ki'], autopct='%1.0f%%', pctdistance=0.5, labeldistance=1.2)
    plt.show()
   
#------------------------------------------------------Stichprobenkennwerte auf Basis der Stichprobendaten----------------------------------------------------------

#berechne arithmetisches Mittelwert auf Basis der Stichprobendaten
def arithMittel_basis_Stichprobendaten(spalte):
    avg_value = round ( average(spalte) , 2)
    return avg_value

#berechne Median auf Basis der Stichprobendaten
def median_basis_Stichprobendaten(spalte):
    return statistics.median(spalte)

#berechne Median auf Basis der Stichprobendaten  
def quantile_basis_stichprobendaten(spalte):   
    erste = np.quantile(spalte, .25)
    zweite = np.quantile(spalte, .5)
    dritte = np.quantile(spalte, .75)
    return erste,zweite, dritte

#berechne Modus auf Basis der Stichprobendaten  
def modus_basis_Stichprobendaten(spalte):
    if len(set(spalte)) != len(spalte):       #pruefe ob die Laenge von set von spalte (gibt die Spalte ohne Duplikate), nicht gleich die Laenge der Spalte mit Duplikaten
        return statistics.mode(spalte)         
    else:                                      
        return "Kein Modus wurde gefunden"    #else beide haben die gleiche Laenge => kein Modus 

#berechne Spannweite auf Basis der Stichprobendaten 
def spannweite_basis_Stichprobendaten(spalte):
    return round(spalte.max() - spalte.min(), 3)

def quartilsabstand_basis_Stichprobendaten(spalte):
    return spalte.quantile(q=0.75) - spalte.quantile(q=0.25)

#berechne Streuung auf Basis der Stichprobendaten 
def streuung_basis_Stichprobendaten(daten, spalte, median):  
    sum = 0                 
    for wert in spalte:
        sum += (wert - median)**2
    return round( sum / (len(daten)-1) , 3)    

#berechne Standardabweichung auf Basis der Stichprobendaten     
def standardabweichung__basis_Stichprobendaten(streuung):
    return round( math.sqrt(streuung)  , 3)    


#-----------------------------------------------------Stichprobenkennwerte auf basis klassifizierten Daten----------------------------------------------------------

#berechne Klassenmitte fuer stetige Daten auf Basis der KlassenHaefigkeitstabellen     
def klassenmitte(tab):
    tab['xi'] = (pd.IntervalIndex(tab['Ki']).right + pd.IntervalIndex(tab['Ki']).left) / 2
    return tab

#berechne das arithmetische Mittel fuer stetige Daten auf Basis der KlassenHaefigkeitstabellen   
def arithmetisches_Mittel_basis_Tabelle(tab):
    x = 0
    for index, row in tab.iterrows():
        x += row['xi'] * row['Hn(Ki)']   
    return round(x/30, 3)     

#berechne Median fuer stetige Daten auf Basis der KlassenHaefigkeitstabellen
def median_basis_Tabelle(daten, tab, b):  
    x = len(daten) * 0.5   
    for index, row in tab.iterrows():      #finde i, also welche Zeile
        if(row['H(i)'] >= x):
            i = index
            break
    
    ai_u = pd.IntervalIndex(tab['Ki']).left.__getitem__(i)
    h_i = tab['H(i)'].__getitem__(i-1) / len(daten)
    hn_Ki = tab['Hn(Ki)'].__getitem__(i) / len(daten)
   
    med = ai_u + ( (0.5 - h_i)/hn_Ki ) * b
    return round(med, 3)

#berechne Quantile fuer stetige Daten auf Basis der KlassenHaefigkeitstabellen
def quantile_basis_Tabelle(daten, tab, b, alpha): 
    x = len(daten) * alpha
    for index, row in tab.iterrows():   #finde i, also welche Zeile
        if(row['H(i)'] >= x):
            i = index
            break
    
    ai_u = pd.IntervalIndex(tab['Ki']).left.__getitem__(i)
    if(i<1):     #wenn i=0, dann ist die Zeile i-1 nicht in der Tabelle vorhanden.
        return
    h_i = tab['H(i)'].__getitem__(i-1) / len(daten)
    hn_Ki = tab['Hn(Ki)'].__getitem__(i) / len(daten)
   
    quantile = ai_u + ( (alpha - h_i)/hn_Ki ) * b
    return round(quantile, 3)

#berechne Streuung fuer stetige Daten auf Basis der KlassenHaefigkeitstabellen
def streuung_basis_Tabelle(med, tab):
    x = 0
    for index, row in tab.iterrows():
         x += (row['xi'] - med)**2 * row['Hn(Ki)'] 
    return round( x / (len(tab)-1) , 3)

#berechne Standardabweichung fuer stetige Daten auf Basis der KlassenHaefigkeitstabellen
def standardabweichung__basis_Tabelle(streuung):
    return round( math.sqrt(streuung)  , 3)    

#-----------------------------------------------------------------------Hilfsmethoden------------------------------------------------------------------------

#Versuche es, die Datei zu lesen und betrachte ';' als Trenner
#drucke error falls die Datei nciht gefunden ist 
#alle Daten der Datei werden zurueckgegeben als dataframe 
def FileCheck(table):
    try:
        return pd.read_csv(table, sep=';',na_values='.')
    except IOError: 
        print ("Error: Datei wuerde nicht gefunden. Versuchen Sie nochmal")
        return 0  

#Hilfsmethode
#pruefe, ob die Einagbe der Benutzer eine valide Nummer ist, also wenn eine Nummer gefragt ist, muss nicht ein Buchstabe eingegeben wird
def InputIntCheck(eingabe):
    try: 
        eingabe = int(eingabe)
    except ValueError as e: 
        print("\n****** Fehler: Sie duerfen nur Zahlen eingeben ******") 
    return eingabe

#In unserer Datei gibt es einige float-Zahlen, die durch ',' anstatt '.' getrennt sind
#diese Zahlen werden deswegen als String betrachtet
#die Funktion konvertiere_string_float wird das Problem loesen durch Ersetzung von  ',' durch '.'
def konvertiere_string_float(daten): 
    return daten.apply(lambda x: float(x.replace(',','.')))

    







