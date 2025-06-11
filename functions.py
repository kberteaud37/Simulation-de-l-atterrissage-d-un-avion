import requests
import pandas as pd
from io import StringIO
import urllib3
import certifi
# Coordonnées de Québec (ville) ou modifiable selon besoin
latitude = 45.5088
longitude = -73.5878

def recuperer_meteo(latitude,longitude):

    # URL de l'API avec les paramètres souhaités
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}"
        f"&longitude={longitude}"
        f"&current=temperature_2m,pressure_msl,wind_speed_10m,wind_direction_10m"
    )

    # Requête
    response = requests.get(url)

    # Vérification et affichage
    if response.status_code == 200:
        data = response.json()
        current_weather = data['current']
        #Température en °C
        temperature=current_weather['temperature_2m']
        #Pression en hPa
        pression=current_weather['pressure_msl']
        #Vitesse du vent en km/h
        vitesse_vent=current_weather['wind_speed_10m']
        #Orientation du vent en °
        orientation_vent=current_weather['wind_direction_10m']
    else:
        print("Erreur:", response.status_code)
    return (temperature, pression, vitesse_vent, orientation_vent)

def recuperer_runways():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    pd.set_option('display.max_columns', None)

    # Récupérer les fichiers csv en ligne
    url_airports = "https://ourairports.com/data/airports.csv"
    url_runways = "https://ourairports.com/data/runways.csv"
    airports_csv = requests.get(url_airports, verify=False).content.decode('utf-8')
    runways_csv = requests.get(url_runways, verify=False).content.decode('utf-8')

    # Créer des Data Frame à partir de ces fichiers
    airports_df = pd.read_csv(StringIO(airports_csv))
    runways_df = pd.read_csv(StringIO(runways_csv))

    #Nettoyer Airport
    # Filtrer les aéroports/aérodromes du QC
    qc_airports = airports_df[airports_df['iso_region'] == 'CA-QC']
    #Retiré les aéroports fermés et les héliports
    qc_airports = qc_airports[~qc_airports["type"].isin(["heliport", "closed"])]
    #Conserver uniquement les colonnes qui nous interesse
    qc_airports = qc_airports[["ident", "type", "name", "latitude_deg", "longitude_deg", "elevation_ft"]]

    #Nettoyer Runways
    #Conserver uniquement les colonnes qui nous interesse
    runways_df=runways_df[["airport_ident","length_ft","width_ft","surface"]]


    #Fusion des fichier Runways et Airports
    runways_fusion = pd.merge(qc_airports,runways_df,left_on="ident",right_on="airport_ident",how="inner")
    #Suppression de la colonne airport_ident en doublon
    runways_fusion = runways_fusion.drop(columns=["airport_ident"])
    return runways_fusion

