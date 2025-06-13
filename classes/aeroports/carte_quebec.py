import folium
import webbrowser
import os
from fonctions_aeroport import *
# Récupérer les données des aéroports
runways_data = recuperer_runways()

# Créer une carte centrée sur le Québec
qc_map = folium.Map(location=[46.8, -71.2], zoom_start=7)

# Ajouter chaque aéroport comme un marqueur
for index, row in runways_data.iterrows():
    folium.Marker(
        location=[row['latitude_deg'], row['longitude_deg']],
        popup=f"{row['name']} (Code: {row['ident']})",
        tooltip=row['name']
    ).add_to(qc_map)

# Afficher la carte
file_path = "quebec_airports_map.html"
qc_map.save(file_path)
webbrowser.open('file://' + os.path.realpath(file_path))