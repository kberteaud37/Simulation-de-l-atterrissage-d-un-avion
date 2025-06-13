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
        f"&current=temperature_2m,pressure_msl,wind_speed_10m,wind_direction_10m,precipitation,weather_code"
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
        #Qte de précipitations
        precipitation = current_weather.get('precipitation', 0)
        #Code Météo des précipitations
        weather_code = current_weather.get('weather_code', 0)
        #Detection Pluie
        # Détection de pluie (simplifiée)
        pluie = precipitation > 0 or weather_code in {51, 53, 55, 61, 63, 65, 80, 81, 82}
        glace = temperature<0 or weather_code in {56, 57,66,67,71,73,75,77,85,86}
        return {"T": temperature,"P": pression,"V_vent": vitesse_vent,"Dir_vent": orientation_vent,"pluie": pluie,"glace":glace}
    else:
        print("Erreur:", response.status_code)



