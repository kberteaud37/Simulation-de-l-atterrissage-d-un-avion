"""Module utilitaire pour la récupération et le traitement des données d'aéroports."""

import requests
import pandas as pd
from io import StringIO
import urllib3

def recuperer_runways():
    """Récupère et nettoie les données des aéroports et pistes du Québec.

        :return: DataFrame fusionné contenant les informations des aéroports et pistes
        :rtype: pandas.DataFrame
        :raises: Désactive les avertissements SSL pour les requêtes HTTP
    """
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
    # Filtrer les aéroports/aérodromes du CA
    qc_airports = airports_df[airports_df['iso_region'] == 'CA-QC']
    #Retiré les aéroports fermés et les héliports
    qc_airports = qc_airports[~qc_airports["type"].isin(["heliport", "closed"])]
    #Conserver uniquement les colonnes qui nous intéressent
    qc_airports = qc_airports[["ident", "type", "name", "latitude_deg", "longitude_deg", "elevation_ft"]]

    #Nettoyer Runways
    #Conserver uniquement les colonnes qui nous intéressent
    runways_df=runways_df[["airport_ident","length_ft","width_ft","surface","le_ident","he_ident"]]

    # Fusionner les identifiants de piste avec un tiret
    runways_df["runway_ident"] = runways_df["le_ident"] + "-" + runways_df["he_ident"]

    # Nettoyage des identifiants pour éviter les erreurs de comparaison

    qc_airports["ident"] = qc_airports["ident"].astype(str).str.strip()
    runways_df["airport_ident"] = runways_df["airport_ident"].astype(str).str.strip()

    #Fusion des fichier Runways et Airports
    runways_fusion = pd.merge(qc_airports,runways_df,left_on="ident",right_on="airport_ident",how="inner")
    #Suppression de la colonne airport_ident en doublon
    runways_fusion = runways_fusion.drop(columns=["airport_ident"])
    return runways_fusion

# Fonction qui filtre et ne garde que les aéroports en une seule instance
def recuperer_airports():
    """Récupère la liste des aéroports du Québec sans doublons.

        :return: DataFrame contenant les informations de base des aéroports
        :rtype: pandas.DataFrame
    """
    df_runways = recuperer_runways()
    # Sélectionne colonnes utiles
    df = df_runways[["ident", "latitude_deg", "longitude_deg", "name"]]
    # Supprime doublons sur 'ident', en gardant la première occurrence
    df_airports = df.drop_duplicates(subset=["ident"])
    return df_airports.reset_index(drop=True)

