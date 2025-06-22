import requests

def recuperer_meteo(latitude,longitude):
    """Récupère les données météorologiques actuelles pour des coordonnées géographiques données.

    Cette fonction interroge l'API Open-Meteo pour obtenir les conditions météo actuelles
    et retourne les données pertinentes pour l'aviation, notamment :

    - Température, pression, vitesse et direction du vent
    - Indicateurs de conditions météorologiques critiques (pluie, glace)

    Args:

        - latitude (float): Latitude du point à interroger (de -90 à 90)
        - longitude (float): Longitude du point à interroger (de -180 à 180)

    Returns:
        dict: Dictionnaire contenant les données météorologiques avec les clés suivantes :
            - "T" (float): Température à 2m en °C
            - "P" (float): Pression au niveau de la mer en hPa
            - "V_vent" (float): Vitesse du vent à 10m en km/h
            - "Dir_vent" (float): Direction du vent magnétique (orientation réelle - 15°)
            - "pluie" (bool): True si précipitations ou codes météo de pluie détectés
            - "glace" (bool): True si température <0°C ou codes météo de gel détectés
        str: Message d'erreur si la requête échoue (format "Erreur: [code_statut]")

    Raises:
        ValueError: Si les coordonnées fournies sont hors des plages valides
        requests.exceptions.RequestException: Pour les erreurs de connexion ou de timeout

    Notes:
        - Les codes météo (WMO) utilisés pour détecter pluie/glace correspondent à :

          * Pluie : 51,53,55,61,63,65,80,81,82
          * Glace : 56,57,66,67,71-77,85,86
        - La direction du vent est ajustée de -15° pour obtenir l'orientation magnétique
        - En cas d'absence de données de précipitations/code météo, elles sont initialisées à 0
    """
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
        orientation_mag=orientation_vent-15
        #Qte de précipitations
        precipitation = current_weather.get('precipitation', 0)

        #Code Météo des précipitations
        weather_code = current_weather.get('weather_code', 0)

        #Detection Pluie
        pluie = precipitation > 0 or weather_code in {51, 53, 55, 61, 63, 65, 80, 81, 82}

        #Detection Glace
        glace = temperature<0 or weather_code in {56, 57,66,67,71,73,75,77,85,86}
        return {"T": temperature,"P": pression,"V_vent": vitesse_vent,"Dir_vent": orientation_mag,"pluie": pluie,"glace":glace}
    else:
        return "Erreur:", response.status_code



