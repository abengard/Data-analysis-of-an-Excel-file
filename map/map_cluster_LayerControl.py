import pandas as pd 
from datetime import datetime
import folium
import easygui
from folium.plugins import MarkerCluster
from folium.plugins import HeatMap


###################################################################### Allgemein ######################################################################

WKA = pd.read_excel(easygui.fileopenbox()) #Dialog-Fenster                              # liest den Datensatz ein 
 

print(WKA.head())

#Bereinigen 
datensatz_01=WKA['BREITENGRAD'].count()             # für Kontrolle von nan-Einträgen
WKA=WKA.dropna()                                    # Nulleinträge bereinigen
datensatz_02=WKA['BREITENGRAD'].count() 

today=datetime.now().strftime("%Y-%m-%d %H-%M-%S")  #Datum für Dateinamen


print("\n\n\nBreitengrad\n\nMinimum: " ,WKA["BREITENGRAD"].min(),"\nMaximum: ", WKA["BREITENGRAD"].max())
print("\n\nLängengrad\n\nMinimum: " ,WKA["LAENGENGRAD"].min(),"\nMaximum: ", WKA["LAENGENGRAD"].max())
print("\n\nAnzahl Koordinaten:", len(WKA))

d_power= round(WKA["LEISTUNG"].mean(),0)
iconsource = "./icon.png"
print("Nennleistungsdurchschnitt:", d_power, "kW")

m = folium.Map(location=[54.219367 , 9.696117], tiles='OpenStreetMap' , zoom_start=8, control_scale=True) #location is der Mittelpunkt von SH

#Satellitenansicht

folium.TileLayer(
        tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr = 'Esri',
        name = 'Satellite',
        overlay = False,
        control = True
       ).add_to(m)

#FeatureGroup 1 - personalisierte Icons

fg1=folium.FeatureGroup(name='WKA Icons', show=True)
m.add_child(fg1)
markerCluster = MarkerCluster().add_to(fg1)

for i, row in WKA.iterrows():
    lat = WKA.at[i, 'BREITENGRAD']
    lon = WKA.at[i, 'LAENGENGRAD']
    popup = "<strong>Hersteller: </strong>"+str(WKA.at[i, 'HERSTELLER'])+ "<br>" + "<strong>Modell: </strong>"+str(WKA.at[i, 'TYP']) + "<br>" + "<strong>Nennleistung: </strong>"+str(WKA.at[i, 'LEISTUNG'])+ " kW" + "<br>" + "<strong>Nabenhöhe: </strong>" +str(WKA.at[i, 'NABENHOEHE']) + " m" + "<br>" + "<strong>Rotordurchmesser: </strong>" +str(WKA.at[i, 'ROTORDURCHMESSER']) + " m"+ "<br>" + "<strong>Schallleistungspegel: </strong>" +str(WKA.at[i, 'SCHALLLEISTUNGSPEGEL']) + " dB(A)" 
 
    folium.Marker(location=[lat,lon], popup=popup , tooltip="Klicken Sie hier für mehr Informationen zur WKA" , icon = folium.features.CustomIcon(iconsource, icon_size=(100,100))).add_to(markerCluster)

#FeatureGroup 2 - Icon blau/rot nach Durchschnittsleistung ohne Cluster    

fg3=folium.FeatureGroup(name='Leistung in blau/rot (ohne Cluster)' + "<br>" + 'Durchschnittsleistung (DSL): ' + str(d_power) + "kW" + '<br>' + 'blau > DSL' + "<br>" + 'rot < DSL', show=False)
m.add_child(fg3) 

for i, row in WKA.iterrows():
    lat = WKA.at[i, 'BREITENGRAD']
    lon = WKA.at[i, 'LAENGENGRAD']
    power = WKA.at[i, 'LEISTUNG']
    popup = "<strong>Hersteller: </strong>"+str(WKA.at[i, 'HERSTELLER'])+ "<br>" + "<strong>Modell: </strong>"+str(WKA.at[i, 'TYP']) + "<br>" + "<strong>Nennleistung: </strong>"+str(WKA.at[i, 'LEISTUNG'])+ " kW" + "<br>" + "<strong>Nabenhöhe: </strong>" +str(WKA.at[i, 'NABENHOEHE']) + " m" + "<br>" + "<strong>Rotordurchmesser: </strong>" +str(WKA.at[i, 'ROTORDURCHMESSER']) + " m"+ "<br>" + "<strong>Schallleistungspegel: </strong>" +str(WKA.at[i, 'SCHALLLEISTUNGSPEGEL']) + " dB(A)" 
   
    if power >= d_power:
       color = 'blue'
       
    else:
       color = 'red'
  
    folium.Marker(location=[lat,lon], popup=popup , tooltip="Klicken Sie hier für mehr Informationen zur WKA" , icon = folium.Icon(color=color)).add_to(fg3)

#FeatureGroup 3 - Icon blau/rot nach Durchschnittsleistung mit Cluster

fg3=folium.FeatureGroup(name='Leistung in blau/rot (mit Cluster)' + "<br>" + 'Durchschnittsleistung (DSL): ' + str(d_power) + "kW" + '<br>' + 'blau > DSL' + "<br>" + 'rot < DSL', show=False)
m.add_child(fg3)
markerCluster = MarkerCluster().add_to(fg3)    

for i, row in WKA.iterrows():
    lat = WKA.at[i, 'BREITENGRAD']
    lon = WKA.at[i, 'LAENGENGRAD']
    power = WKA.at[i, 'LEISTUNG']
    popup = "<strong>Hersteller: </strong>"+str(WKA.at[i, 'HERSTELLER'])+ "<br>" + "<strong>Modell: </strong>"+str(WKA.at[i, 'TYP']) + "<br>" + "<strong>Nennleistung: </strong>"+str(WKA.at[i, 'LEISTUNG'])+ " kW" + "<br>" + "<strong>Nabenhöhe: </strong>" +str(WKA.at[i, 'NABENHOEHE']) + " m" + "<br>" + "<strong>Rotordurchmesser: </strong>" +str(WKA.at[i, 'ROTORDURCHMESSER']) + " m"+ "<br>" + "<strong>Schallleistungspegel: </strong>" +str(WKA.at[i, 'SCHALLLEISTUNGSPEGEL']) + " dB(A)" 
   
    if power >= d_power:
       color = 'blue'
       
    else:
       color = 'red'
  
    folium.Marker(location=[lat,lon], popup=popup , tooltip="Klicken Sie hier für mehr Informationen zur WKA" , icon = folium.Icon(color=color)).add_to(markerCluster)

#FeatureGroup 4 - Heatmap Leistung

fg4=folium.FeatureGroup(name='Heatmap Leistung', show=False)
m.add_child(fg4)
markerCluster = MarkerCluster().add_to(fg4)
hml = pd.DataFrame(WKA, columns=['BREITENGRAD' , 'LAENGENGRAD' , 'LEISTUNG']) 
HeatMap(hml).add_to(markerCluster)

#FeatureGroup 5 - Heatmap Schalleistungspegel

fg5=folium.FeatureGroup(name='Heatmap Schallleistungspegel', show=True)
m.add_child(fg5)
markerCluster = MarkerCluster().add_to(fg5)
hms = pd.DataFrame(WKA, columns=['BREITENGRAD' , 'LAENGENGRAD' , 'SCHALLLEISTUNGSPEGEL']) 
HeatMap(hms).add_to(markerCluster)

m.add_child(folium.LayerControl())
m.save('WKA_map_cluster_LayerControl_' + str(today) + '.html')

