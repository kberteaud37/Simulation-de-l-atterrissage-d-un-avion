import numpy as np
from scipy.spatial import KDTree
from simulation_atterrissage.classes.aeroports.fonctions_aeroport import recuperer_airports

def trouver_aeroport_proche(exclusions):
    """Trouve l'aéroport le plus proche en évitant les aéroports exclus.

    Cette fonction utilise un arbre KD (K-Dimension) pour trouver efficacement l'aéroport
    le plus proche (distance orthodromique) qui n'est pas dans la liste d'exclusion.

    :param exclusions: Liste des aéroports à exclure de la recherche (doit contenir au moins l'aéroport de départ)
    :type exclusions: list[Piste]
    :return: DataFrame pandas contenant les informations de l'aéroport le plus proche
    :rtype: pandas.Series
    :raises ValueError:
        - Si l'aéroport de départ n'est pas trouvé dans la base de données
        - Si tous les aéroports valides sont exclus
        - Si la liste d'exclusion est vide

    Note:
        - Utilise la formule de distance grand cercle via conversion en radians
        - La recherche est optimisée via KDTree pour des performances O(log n)
        - Les coordonnées sont converties en radians pour le calcul de distance

    """
    df_airports = recuperer_airports()
    code_depart = exclusions[0].code
    a_exclure = set(p.code for p in exclusions)  # pour éviter les doublons et rendre la recherche rapide

    # Aéroport de départ
    row_depart = df_airports[df_airports["ident"] == code_depart]
    if row_depart.empty:
        raise ValueError(f"Aéroport avec ident = {code_depart} introuvable.")
    row_depart = row_depart.iloc[0]
    coord_depart = np.radians([row_depart["latitude_deg"], row_depart["longitude_deg"]])

    # Filtrage des aéroports à exclure
    df_filtre = df_airports[~df_airports["ident"].isin(a_exclure)].copy()

    if df_filtre.empty:
        raise ValueError("Tous les aéroports ont été exclus, impossible de continuer la recherche.")

    coords = np.radians(df_filtre[["latitude_deg", "longitude_deg"]])
    tree = KDTree(coords)

    dist, idx = tree.query(coord_depart)
    plus_proche = df_filtre.iloc[idx]

    return plus_proche