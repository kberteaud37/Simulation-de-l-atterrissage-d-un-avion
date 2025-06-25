import numpy as np
from simulation_atterrissage.classes.aeroports.fonctions_aeroport import recuperer_airports

def calcul_distance_aeroport(code_depart, code_arrivee):
    df_airports = recuperer_airports()
    """Calcule la distance entre deux aéroports en milles nautiques (NM) en utilisant la formule de Haversine.

        Cette fonction calcule la distance orthodromique (grand cercle) entre deux aéroports
        à partir de leurs coordonnées géographiques, en utilisant la formule mathématique de Haversine.

        :param code_depart: Code OACI de l'aéroport de départ (ex: 'CYUL')
        :type code_depart: str
        :param code_arrivee: Code OACI de l'aéroport d'arrivée (ex: 'KJFK')
        :type code_arrivee: str
        :return: Distance entre les deux aéroports en milles nautiques (NM)
        :rtype: float
        :raises IndexError: Si l'un des codes aéroport n'est pas trouvé dans la base de données
        :raises ValueError: Si les codes départ/arrivée sont identiques

        Note:
            - 1 mille nautique (NM) = 1.852 km
            - Utilise le rayon terrestre moyen de 3440 NM (6,371 km)
            - La précision est d'environ ±0.3% en raison de l'hypothèse de sphéricité terrestre
        """

    # Récupération des coordonnées
    row_depart = df_airports[df_airports["ident"] == code_depart].iloc[0]
    row_arrivee = df_airports[df_airports["ident"] == code_arrivee].iloc[0]

    #Conversion des degrés decimaux en radians
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