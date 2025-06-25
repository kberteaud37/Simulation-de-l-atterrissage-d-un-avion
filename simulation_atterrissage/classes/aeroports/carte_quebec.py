"""
Module de visualisation cartographique des aéroports du Québec.

Fournit la fonction creer_carte_quebec() pour générer une carte interactive
des aéroports à l'aide de la bibliothèque Folium.

Exemple:
- from carte_quebec import creer_carte_quebec
- creer_carte_quebec()  # Génère et ouvre la carte
"""

import folium
import webbrowser
import os
from .fonctions_aeroport import *

def creer_carte_quebec():
    """Génère une carte interactive Folium des aéroports du Québec et l'ouvre dans le navigateur.

    Récupère les données des pistes d'aéroports via `recuperer_runways()`, crée une carte centrée
    sur le Québec (46.8°N, 71.2°W) avec zoom=7, et ajoute un marqueur par aéroport avec :
    - Position : latitude/longitude
    - Popup : Nom et code OACI
    - Infobulle : Nom de l'aéroport

    La carte est sauvegardée sous 'quebec_airports_map.html' et ouverte automatiquement.

    Returns:
        None
    """
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