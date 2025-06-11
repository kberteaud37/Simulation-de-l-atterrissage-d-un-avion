import requests
import pandas as pd
from io import StringIO
import urllib3

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
