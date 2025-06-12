import requests
import pandas as pd
from io import StringIO
import urllib3

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
    # Filtrer les aéroports/aérodromes du CA
    qc_airports = airports_df[airports_df['iso_region'] == 'CA-QC']
    #Retiré les aéroports fermés et les héliports
    qc_airports = qc_airports[~qc_airports["type"].isin(["heliport", "closed"])]
    #Conserver uniquement les colonnes qui nous interesse
    qc_airports = qc_airports[["ident", "type", "name", "latitude_deg", "longitude_deg", "elevation_ft"]]

    #Nettoyer Runways
    #Conserver uniquement les colonnes qui nous interesse
    runways_df=runways_df[["airport_ident","length_ft","width_ft","surface","le_ident","he_ident"]]

    # Nettoyage des identifiants pour éviter les erreurs de comparaison

    qc_airports["ident"] = qc_airports["ident"].astype(str).str.strip()
    runways_df["airport_ident"] = runways_df["airport_ident"].astype(str).str.strip()

    #Fusion des fichier Runways et Airports
    runways_fusion = pd.merge(qc_airports,runways_df,left_on="ident",right_on="airport_ident",how="inner")
    #Suppression de la colonne airport_ident en doublon
    runways_fusion = runways_fusion.drop(columns=["airport_ident"])
    return runways_fusion


