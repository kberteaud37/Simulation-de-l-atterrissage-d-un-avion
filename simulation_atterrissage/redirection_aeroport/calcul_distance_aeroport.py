import numpy as np
from simulation_atterrissage.classes.aeroports.fonctions_aeroport import recuperer_airports

def calcul_distance_aeroport(code_depart, code_arrivee):
    df_airports = recuperer_airports()

    # Récupération des coordonnées
    row_depart = df_airports[df_airports["ident"] == code_depart].iloc[0]
    row_arrivee = df_airports[df_airports["ident"] == code_arrivee].iloc[0]

    lat1, lon1 = np.radians([row_depart["latitude_deg"], row_depart["longitude_deg"]])
    lat2, lon2 = np.radians([row_arrivee["latitude_deg"], row_arrivee["longitude_deg"]])

    # Formule de Haversine
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    rayon_terre_nm = 3440  # rayon terrestre en milles nautiques
    distance_nm = rayon_terre_nm * c

    return distance_nm