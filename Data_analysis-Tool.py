#%%#################################################################### Bibliotheken ####################################################################

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 
import easygui
from datetime import datetime
import datetime                                     #wichtig für funktion mmd
from scipy.stats import linregress
import folium
import os
import sys
import time

#%%#################################################################### Funktionen ######################################################################

def txt_to_pdf(name):
    from fpdf import FPDF 
    pdf = FPDF()   
    pdf.add_page()
    pdf.set_font("Arial", size = 10)
    f = open("./temp/" + name + ".txt", "r")
    for x in f:
        pdf.cell(500, 8, txt = x, ln = 1)#, align = 'C')
    f.close()
    pdf.output('./temp/' + name + '.pdf')

def output(name, start=False, end=False, PDF=False):
    global f, tem
    if start==True:
        if os.path.isdir('temp')==False:
            os.mkdir('temp')
        if os.path.exists('./temp/' + name + ".txt"):
            os.remove('./temp/' + name + ".txt")    
        tem = sys.stdout
        sys.stdout = f = open("./temp/" + name + ".txt", "a")
    if end==True:
        sys.stdout = tem
        f.close()
        if PDF==True:
            txt_to_pdf(name)
    return f, tem    

def count_graph():
    global g_num, g_lab                                         #für Benennung der PDF Ausgabe wichtig, damit diese in richtiger Reihenfolge gemerged werden
    if 'g_num' in globals():
        g_num = g_num + 1
    else:
        g_num = 1
    g_lab = str(g_num).zfill(2) + "_"
       
def plt_to_pdf(tit):
    if os.path.isdir('temp')==False:
        os.mkdir('temp')
    plt.savefig(fname=('temp/' + tit + '.pdf'), dpi='figure', format='pdf', facecolor='auto', edgecolor='auto')
    
def cnt_max(a, title=False):
    if "list_count_max" in globals():
        global list_count_max
        list_count_max.append(a.count().max())
    else:
        list_count_max = []
        list_count_max.append(a.count().max())
    if "list_names_delete" in globals():
        global list_names_delete
        list_names_delete.append(title)
    else:
        list_names_delete = []
        list_names_delete.append(title)
    print('\nAnzahl momentaner Datensätze: ', a.count().max(), "\n")
    return a

def delete(a, b, c=False, s=False, s2=False, w=False, title=False):
    """
    Parameters
    ----------
    a : Dataframe
        Datenbank (hier z.B. WKA)
    b : string
        s>=s2 löscht alle Werte wo größergleich s2; s<=s2 löscht alle Werte wo kleinergleich s2; s<=w löscht alle Spalten wo der Wert unter oder gleich w ist; s>=w löscht alle Spalten wo der Wert größer oder gleich w ist;
        s<w löscht alle Spalten wo der Wert unter w ist; s>w löscht alle Spalten wo der Wert größer w ist;
    s : string, optional
    c : string, optional
        anzugebender Wert mit dem die zweite Spalte multipliziert wird
    s2 : string, optional
        Anzugebende zweite Spalte s2 mit welcher verglichen werden soll. Schreibweise wird automatisch korrigiert.
    w : integer, optional
        Anzugebender Wert w der gefiltert werden soll.

    Returns
    -------
    a : TYPE
        DESCRIPTION.

    """
    if b=='dropna':
        a.dropna(inplace=True) 
    if b!='dropna':
        if b=='s>=s2':
            indexNames = a[a[s.upper()] >= a[s2.upper()]].index
        if b=='s<=s2':
            indexNames = a[a[s.upper()] <= a[s2.upper()]].index
        if b=='s>s2*c':
            indexNames = a[(a[s.upper()]*c) >= (a[s2.upper()])].index
        if b=='s<s2*c':
            indexNames = a[(a[s.upper()]*c) <= (a[s2.upper()])].index
        if b=='s<=w':
            indexNames = a[(a[s.upper()] <= w)].index
        if b=='s<w':
            indexNames = a[(a[s.upper()] < w)].index
        if b=='s>=w':
            indexNames = a[(a[s.upper()] >= w)].index
        if b=='s>w':
            indexNames = a[(a[s.upper()] > w)].index
        a.drop(indexNames, inplace=True)
    cnt_max(a, title=title)
    return a

def mmd(a, x, y=False, e=False, e2=False, Title=False):
    """
    Maximum, Minimum und Durschnitt von ein oder zwei Spalten
    
    Parameters
    ----------
    a : Datenbank (z.B. WKA)
        Dataframe
    x : String
        Spalte die auf max, min und Durchschnitt analysiert werden soll. Bei Datum auch noch Abstand in Jahren zum heutigen Datum.
    y : String, optional
        Zweite Spalte die auf max, min und Durchschnitt analysiert werden soll. Bei Datum auch noch Abstand in Jahren zum heutigen Datum. Falls leer wird nur die erste analysiert.
    e : Einheit, optional
        Einheit die hinter max, min und Durchschnitt stehen soll. Bei Jahren wird <= 1 Jahr ausgegeben.
    e2 : Einheit, optional
        Einheit die hinter y max, min und Durchschnitt stehen soll. Bei Jahren wird <= 1 Jahr ausgegeben.
    e2 : string, optional
        Möglicher Titel bzw. Text der über der Ausgabe von min, max und Durchschnittsermittlung angegeben angezeigt wird.
    Returns
    -------
    None.

    """
    mi = a[x.upper()].min()                                 #für die Überprüfung ob Datum wichtig
    if isinstance(mi, datetime.date) == True:
        if Title==False:
            if y==False:
                print("\nMinimum, Maximum, Durchschnitt & jeweiliges Alter von", str(x.capitalize()))
            else:
                print("\nMinimum, Maximum, Durchschnitt & jeweiliges Alter von", str(x.capitalize()), "und", str((y.capitalize())))
        else:
            if y==False:
                print("\nMinimum, Maximum, Durchschnitt & jeweiliges Alter von", str(x.capitalize()), Title)
            else:
                print("\nMinimum, Maximum, Durchschnitt & jeweiliges Alter von", str(x.capitalize()), "und", str((y.capitalize())), Title)
        e = 'Jahre'
        mi = a[x.upper()].min().strftime("%d.%m.%Y")
        ma = a[x.upper()].max().strftime("%d.%m.%Y")
        du = a[x.upper()].mean().strftime("%d.%m.%Y")
        dage = round(((datetime.datetime.now() - a[x.upper()].mean()).total_seconds()/(365.25*24*60*60)),)
        if dage > 1:
            dage_e = e
        else:
            dage_e = 'Jahr'
        miage = round(((datetime.datetime.now() - a[x.upper()].min()).total_seconds()/(365.25*24*60*60)),)
        if miage > 1:
            miage_e = e
        else:
            miage_e = 'Jahr'
        maage = round(((datetime.datetime.now() - a[x.upper()].max()).total_seconds()/(365.25*24*60*60)),)
        if maage > 1:
            maage_e = e
        else:
            maage_e = 'Jahr'
        print("\n", x.capitalize(), ":\n\nMinimum: ", mi, "\nMaximum: ", ma, "\nDurchschnitt: ", du, 
              "\n\njüngste: ", maage, maage_e, "\nälteste: ", miage, miage_e, "\nDurchschnitt: ", dage, dage_e)
    else:
        if Title==False:
            if y==False:
                print("\nMinimum, Maximum & Durchschnitt von", str(x.capitalize()))
            else:
                print("\nMinimum, Maximum & Durchschnitt von", str(x.capitalize()), "und", str((y.capitalize())))
        else:
            if y==False:
                print("\nMinimum, Maximum & Durchschnitt von", str(x.capitalize()), Title)
            else:
                print("\nMinimum, Maximum & Durchschnitt von", str(x.capitalize()), "und", str((y.capitalize())), Title)
        mi = a[x.upper()].min()
        ma = a[x.upper()].max()
        du = round(a[x.upper()].mean(),2)
        print("\n", x.capitalize(), ":\n\nMinimum: ", mi, e, "\nMaximum: ", ma, e, "\nDurchschnitt: ", du, e)
    
    if y!=False:
        mi = a[x.upper()].min()
        if isinstance(mi, datetime.date) == True:
            e = ' Jahre'
            mi = a[y.upper()].min().strftime("%d.%m.%Y")
            ma = a[y.upper()].max().strftime("%d.%m.%Y")
            du = a[y.upper()].mean().strftime("%d.%m.%Y")
            dage = round(((datetime.datetime.now() - a[y.upper()].mean()).total_seconds()/(365.25*24*60*60)),)
            if dage > 1:
                dage_e = e
            else:
                dage_e = 'Jahr'
            miage = round(((datetime.datetime.now() - a[y.upper()].min()).total_seconds()/(365.25*24*60*60)),)
            if miage > 1:
                miage_e = e
            else:
                miage_e = 'Jahr'
            maage = round(((datetime.datetime.now() - a[y.upper()].max()).total_seconds()/(365.25*24*60*60)),)
            if maage > 1:
                maage_e = e
            else:
                maage_e = 'Jahr'
            print("\n", y.capitalize(), ":\n\nMinimum: ", mi, "\nMaximum: ", ma, "\nDurchschnitt: ", du,
                  "\n\njüngste: ", maage, e, "\nälteste: ", miage, e, "\nDurchschnitt: ", dage, e)
        else:
            if e2==False:
                e2 = e
            mi = a[y.upper()].min()
            ma = a[y.upper()].max()
            du = round(a[y.upper()].mean(),2)
            print("\n", y.capitalize(), ":\n\nMinimum: ", mi, e2, "\nMaximum: ", ma, e2, "\nDurchschnitt: ", du, e2)

def pdf_merge(name, date=False, operation_folder=False, delete_folder=True):
    """
    Fasst alle PDFs in dem Unterordner /temp in eine PDF im Arbeitsordner zusammen

    Parameters
    ----------
    name : string
        Benennung der Datei
    date : True/False, optional
        Fügt dem Dateinamen das aktuelle Datum und Uhrzeit hinzu. The default is False.
    delete_folder : True/False, optional
        Löscht oder löscht nicht den Unterordner temp

    Returns
    -------
    None.

    """
    from PyPDF2 import PdfMerger
    import shutil
    from datetime import datetime
    if operation_folder==False:
        if os.path.isdir('temp')==False:
            os.mkdir('temp')
        os.chdir('./temp')       
    merger = PdfMerger()    
    for item in os.listdir():
        if item.endswith('pdf'):
            merger.append(item)
    os.chdir("..")
    if date==True:
        merger.write(name + '_' + str(datetime.now().strftime("%Y-%m-%d %H-%M-%S") + '.pdf'))
    else:
        merger.write(name + '.pdf')
    merger.close()
    if delete_folder==True:
        shutil.rmtree('./temp')

def plt_xy_r(a, x, y, e1=False, e2=False, title=False, PDF=False):
    """
    Stellt x zu y Werte in Punkten mit einer Regressgeraden dar

    Parameters
    ----------
    a : dataframeDataframe
        Datenbank (hier z.B. WKA)
    x : string
        Name der Spalte für die x-Werte (Schreibweise egal, wird automatisch geändert)
    y : string
        Name der Spalte für die y-Werte (Schreibweise egal, wird automatisch geändert)
    e1 : string, optional
        Einheit für die x-Achse.
    e2 : string, optional
        Einheit für die y-Achse. Falls leer, bzw. false wird der Wert von e1 genommen.
    title : String, optional
        Der Standardtitel setzt sich aus x-Achse zu Y-Achse zusammen. Falls zusätzliche Infos mitgegeben werden sollen, werden diese darunter geschrieben.

    Returns
    -------
    None.

    """
    count_graph()
    xlabel = x.capitalize()
    ylabel = y.capitalize()
    a=a.dropna()                                            # WKA.dropna() wichtig für Regress-Gerade
    xdatensatz = a[x.upper()]
    ydatensatz = a[y.upper()]
    if title==False:
        tit = xlabel + ' zu ' + ylabel
        plt.title(tit,fontweight="bold")
    else:
        tit = xlabel + ' zu ' + ylabel + "\n(" + title + ")"
        plt.title(tit,fontweight="bold")
    if e1==False:
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
    else:
        if e2==False:
            plt.xlabel(xlabel + " ["+ e1 + "]")
            plt.ylabel(ylabel + " ["+ e1 + "]")
        else:
            plt.xlabel(xlabel + " ["+ e1 + "]")
            plt.ylabel(ylabel + " ["+ e2 + "]")
    plt.grid(visible=True)
    plt.plot(xdatensatz, ydatensatz, 'bo')
    b, a, r, p, std= linregress(xdatensatz, ydatensatz)    
    x = np.linspace(xdatensatz.min(), xdatensatz.max())
    y = a + b*x
    a_neu= str(round(a,0))
    b_neu= str(round(b,2))
    plt.plot(x,y, 'r', label= 'Regressionsgerade y = '+b_neu+'x '+ a_neu)
    plt.legend(loc="upper left")
    if PDF==True:
        plt_to_pdf(g_lab + tit)
    plt.show()  

def plt_xy_m(a, x, y, Gerade=False, m=False, e1=False, e2=False, title=False, PDF=False): 
    """
    Stellt x zu y Werte in Punkten mit einer Geraden der Steigung m dar

    Parameters
    ----------
    a : dataframeDataframe
        Datenbank (hier z.B. WKA)
    x : string
        Name der Spalte für die x-Werte (Schreibweise egal, wird automatisch geändert)
    y : string
        Name der Spalte für die y-Werte (Schreibweise egal, wird automatisch geändert)
    Gerade : String, optional
        Zeichnet eine Gerade. Steigung siehe m.
    m : float, optional
        Setzt den Wert der Steigung m fest. Falls false oder leer, Gerade aber True, wird die Steigung per Abfrage definiert.
    e1 : string, optional
        Einheit für die x-Achse.
    e2 : string, optional
        Einheit für die y-Achse. Falls leer, bzw. false wird der Wert von e1 genommen.
    title : String, optional
        Der Standardtitel setzt sich aus x-Achse zu Y-Achse zusammen. Falls zusätzliche Infos mitgegeben werden sollen, werden diese darunter geschrieben.

    Returns
    -------
    None.

    """    
    count_graph()                             
    xlabel = x.capitalize()
    ylabel = y.capitalize()
    xdatensatz = a[x.upper()]
    ydatensatz = a[y.upper()]
    if title==False:
        tit = xlabel + ' zu ' + ylabel
        plt.title(tit,fontweight="bold")
    else:
        tit = xlabel + ' zu ' + ylabel + "\n(" + title + ")"
        plt.title(tit,fontweight="bold")
        tit = xlabel + ' zu ' + ylabel + " (" + title + ")"             # für die PDF Ausgabe
    if e1==False:
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
    else:
        if e2==False:
            plt.xlabel(xlabel + " ["+ e1 + "]")
            plt.ylabel(ylabel + " ["+ e1 + "]")
        else:
            plt.xlabel(xlabel + " ["+ e1 + "]")
            plt.ylabel(ylabel + " ["+ e2 + "]")
    plt.grid(visible=True)
    plt.plot(xdatensatz, ydatensatz, 'bo')
    mi = a[x.upper()].min()
    if Gerade == True:
        if m == False:
            m = float(input("Steigung m = "))
        else:
            m = m
        if isinstance(mi, datetime.date) == True:
            x = np.linspace(19000,7500)
        else:
            x = np.linspace(xdatensatz.min(), xdatensatz.max() , 100)
        y = x * m
        plt.plot(x,y, 'r')
    if PDF==True:
        plt_to_pdf(g_lab + tit)
    plt.show()
    
def plt_pie(a, x, most=False, fontsize=7, PDF=False):
    """
    Parameters
    ----------
    a : Dataframe
        Datenbank (hier z.B. WKA)
    x : string
        Zu darstellende Spalte (z.B. Hersteller)
    most : integer, optional
        direkte Mitgabe der zu darstellenden Stücke. Falls false, bzw. leer gelassen, wird die Anzahl per Abfrage definiert

    Returns
    -------
    None.

    """
    count_graph()
    manu = a[x.upper()].value_counts()
    if most==False:
        best = input("Anzahl eingeben: ")
    else:
        best = most
    top = int(best)
    sonst = sum(manu) - sum(manu[0:top])
    pie = (manu[0:top])
    pie['sonstige'] = sonst
    explode = pie.size * (0.1, )                                                # rückt die Kuchenstücke aus
    def func(pct, allvalues):
        absolute = int(pct / 100.*np.sum(allvalues))
        return "{:d} ({:.1f}%)".format(absolute, pct)
    plt.pie(pie, labels = pie.index, startangle=90, shadow=True, autopct = lambda pct: func(pct, pie), textprops={'fontsize': fontsize}, explode=explode)
    tit = 'Die '+ str(best) +' häufigst verwendeten Hersteller'
    plt.title(tit,fontweight="bold")
    if PDF==True:
        plt_to_pdf(g_lab + tit)
    plt.show()

def plt_box(a, x, y=False, PDF=False):
    """
    Parameters
    ----------
    a : Dataframe
        Datenbank (hier z.B. WKA)
    x : string
        Zu darstellende Spalte (z.B. Nabenhöhe)
    y : string
        Zweite zu darstellende Spalte (z.B. Rotordurchmesser). Falls false oder leer, wird nur x dargestellt.

    Returns
    -------
    None.

    """
    count_graph()
    if y == False:
        a.boxplot(column=[x.upper()])
        
    else:
        a.boxplot(column=[x.upper(), y.upper()])
        tit = tit = 'Boxplot von ' + x.capitalize() + ' und ' + y.capitalize()
    plt.title(tit,fontweight="bold")
    if PDF==True:
        plt_to_pdf(g_lab + tit)
    plt.show()

def plt_vb(a, x, v=False, b=False, PDF=False):
    count_graph()
    if v==False:
        v = (input("von: "))
    if b==False:
        b = (input("bis: "))
    if b <= v:
        print("von v muss größer sein als bis b!")
        return
    v_label = str(v).capitalize()
    b_label = str(b).capitalize()
    tit = "Anzahl " + x.capitalize() + "n von " + v_label + " bis " + b_label
    plt.title(tit,fontweight="bold")
    mask = (a[x.upper()] >= str(v)+'-01-01') & (a[x.upper()] <= str(b)+'-01-01')
    filtered=a.loc[mask]
    plt.hist(filtered[x.upper()])
    #plt.gcf().set_size_inches(12, 6)
    plt.tight_layout()
    if PDF==True:
        plt_to_pdf(g_lab + tit)
    plt.show()
    
def plt_dif(b, xlabel, Title=False, PDF=False):
    count_graph()
    if Title!= False:
        Title = str(Title)
    y = b[::-1]                    
    fig, ax = plt.subplots()
    ax.barh(xlabel[::-1], y)
    tit = 'Anzahl Daten in Datensatz ' + Title
    plt.xlim(0 , (max(list_count_max)+500))                                             #damit Label nicht über den Rahmen gehen
    plt.title(tit,fontweight="bold")
    plt.xlabel('Anzahl Daten')
    plt.ylabel('Löschvorgang')
    ax.bar_label(ax.containers[0])
    plt.tight_layout()
    if PDF==True:
        plt_to_pdf(g_lab + tit)
    plt.show()
     
#%%##################################################################### Allgemein ######################################################################

output('Windkraftanlagenanalyse', start=True)                                           # startet die Dokumentation in eine txt im Pfad ./temp

WKA = pd.read_excel(easygui.fileopenbox()) #Dialog-Fenster                              # liest den Datensatz ein 


print(WKA.head(10))                                                                     # stellt die ersten 10 Datensätze dar

#Bereinigen 
cnt_max(WKA, title='WKA unbereinigt')                                                   # Anfangszahl WKA (unbereinigt), erzeugt Zählerliste "count_list_max", Wert/Index 0 in Zählerliste
delete(WKA, 'dropna', title='Nulleinträge bereinigt')                                   # Nulleinträge bereinigen; Wert/Index 1 in Zählerliste                                                 

#%%#################################################################### Aufgabe 1a ######################################################################

a1a_x = 'rotordurchmesser'
a1a_y = 'nabenhoehe'
a1a_m = 0.5
a1a_e = 'm'                                                                             # Rotordurchmesser darf max 0.5x so groß wie Nabenhöhe sein

mmd(WKA, a1a_x, a1a_y, a1a_e, Title='nach dem Löschen von Nan-Einträgen')
   
#Plot Rotordurchmesser zu Nabenhöhe    
plt_xy_m(WKA, a1a_x, a1a_y, e1=a1a_e, PDF=True)

#Plot Rotordurchmesser zu Nabenhöhe mit Gerade
plt_xy_m(WKA, a1a_x, a1a_y, Gerade=True, m=a1a_m, e1=a1a_e, title='mit Gerade', PDF=True)

#Bereinigen
delete(WKA, 's>s2*c', c=0.5, s=a1a_x, s2=a1a_y, title='Nabenhöhe <= halber Rotordurchmesser') # löscht alle Nabenhöhe <= 0,5*Rotordurchmesser, da Nabenhöhe größer sein muss als 0,5*Rotordurchmesser

#Check nach Bereinigen 
mmd(WKA, a1a_x, a1a_y, a1a_e, Title='nach dem Löschen Nabenhöhe <= halber Rotordurchmesser')
plt_xy_m(WKA, a1a_x, a1a_y, Gerade=True, m=a1a_m, e1=a1a_e, title='bereinigt', PDF=True)
  
#%%#################################################################### Aufgabe 1b ######################################################################

a1b_x = 'inbetriebnahme'
a1b_y = 'genehmigt_am'
a1b_m = 1

mmd(WKA, a1b_x, a1b_y)
plt_xy_m(WKA, a1b_x, a1b_y, PDF=True)

#Bereinigen
delete(WKA, 's<=w', s=a1b_x, w='1980', title='Inbetriebn. <= 1980')                       # löscht alle Inbetriebnahmen <= 1980, da unsinnig        
delete(WKA, 's<=w', s=a1b_y, w='1980', title='genehmigt_am <= 1980')                      # löscht alle genehmigt_am <= 1980, da unsinnig; Wert/Index 4 in Zählerliste  

#Check nach Bereinigen
mmd(WKA, a1b_x, a1b_y, Title='nach dem Löschen von Einträgen <= 1980')
plt_xy_m(WKA, a1b_x, a1b_y, title='unter 1980 gelöscht', PDF=True)

#nur Inbetriebnahme > genehmigt an
delete(WKA, 's<=s2', s=a1b_x, s2=a1b_y, title='Inbetriebn. <= genehmigt')               # löscht alle Inbetriebnahmen <= genehmigt_am, da unsinnig; Wert/Index 5 in Zählerliste  
plt_xy_m(WKA, a1b_x, a1b_y, Gerade=True, m=a1b_m, title="Inbetriebnahme größer genehmigt an", PDF=True)

#%%#################################################################### Aufgabe 2 #######################################################################

a2 = 'hersteller'
a2_a = 6

plt_pie(WKA, a2, a2_a, fontsize=8, PDF=True)

#%%#################################################################### Aufgabe 3 ######################################################################

a3_x = 'rotordurchmesser'
a3_x2 = 'nabenhoehe'
a3_y = 'leistung'
a3_x_e = a3_x2_e = 'm'
a3_y_e = 'kW'

mmd(WKA, a3_x, a3_y, a3_x_e, a3_y_e)
plt_xy_r(WKA, a3_x, a3_y, a3_x_e, a3_y_e, PDF=True)
mmd(WKA, a3_x2, a3_y, a3_x2_e, a3_y_e)
plt_xy_r(WKA, a3_x2, a3_y, e1=a3_x2_e, e2=a3_y_e, PDF=True)
plt_box(WKA, a3_x, a3_x2, PDF=True)

#%%#################################################################### Aufgabe 4 ######################################################################

a4='inbetriebnahme'

mmd(WKA, a4)
plt_vb(WKA, a4, 2010, 2012, PDF=True)

#%%#################################################################### Aufgabe 5 ######################################################################

a5 = 'leistung'
a5_e = 'kW'                                                                             # entscheidet über den Inhalt des popups
SH = [54.219367 , 9.696117]                                                             # Mittelpunkt von SH
i = 5                                                                                   # Index einer beliebigen WKA
                                                      
pop = (a5.capitalize() + ": " + str(WKA.at[i, a5.upper()]) + a5_e)                      # definiert den Inhalt des Popup Fensters

m = folium.Map(location=SH, tiles='OpenStreetMap' , zoom_start=8, control_scale=True)   # location is der Mittelpunkt von SH
folium.Marker(location=[WKA['BREITENGRAD'][i] , WKA['LAENGENGRAD'][i]], popup=str(pop) , tooltip="Klicken Sie hier für mehr Informationen zur WKA").add_to(m)
m.save('map_' + a5.capitalize() + ' und Ort von ' + str(i) + 'ter WKA.html')

#%%#################################################################### Datensatz ######################################################################

plt_dif(list_count_max, list_names_delete, Title='WKA', PDF=True)

#%%#################################################################### sonstiges ######################################################################

output(name='Windkraftanlagenanalyse', end=True, PDF=True)                              # beendet die Dokumentation in eine txt im Pfad ./temp

pdf_merge('Windkraftanlagenanalyse', date=True, delete_folder=True)                    # wandelt die PDF Ausgaben (Graphen und Dokumentation) in eine einzelnde PDF um