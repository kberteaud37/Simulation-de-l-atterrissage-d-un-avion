import matplotlib.pyplot as plt
import numpy as np
import classes
import affichages_graphiques
from scipy.spatial import KDTree
from classes.aeroports.fonctions_aeroport import recuperer_runways,recuperer_airports
from classes.avions.choix_avion import ChoixAvion


#Fonction forçant l'utilisateur à entrer une valeur acceptable
def get_float_input(prompt):
    while True:
        # Constantly check if a value was entered followed by Enter
        try:
            value = input(prompt).replace(',', '.')  # Remplace les virgules par des points
            return float(value)
            break
        except ValueError:
            # If input is not a float we get a ValueError
            print("Invalid input, please try again.")
    return value

# Fonction qui compare la longueur des pistes avec la distance nécessaire à l'atterrissage
def compare(avion, piste, coef_secu=1.67):
    distance_necessaire = (avion.calcul_S_B()+avion.calcul_S_FR()+avion.calcul_S_TR()) * coef_secu
    print(f"La distance nécessaire est : {distance_necessaire : .2f} ft")
    print(f"La longueur de la piste est : {piste.longueur()} ft")

    df_runways = recuperer_runways()
    aeroport = [piste]
    code_aeroport_courant = piste.code
    pistes = df_runways[df_runways["ident"] == code_aeroport_courant]

    max_recherches = 20
    nb_recherches = 0
    print(f"Test pour l'aéroport {piste.nom()}...")

    while distance_necessaire >= piste.longueur():
        if nb_recherches >= max_recherches:
            raise RuntimeError("Trop de recherches effectuées, aucun aéroport viable trouvé.")
        nb_recherches += 1

        for num_piste in pistes["runway_ident"]:
            piste_test = classes.aeroports.Piste(code_aeroport_courant, df_runways, num_piste)
            if distance_necessaire < piste_test.longueur():
                piste = piste_test
                break
        else:
            print("Atterrissage non sûr : la distance nécessaire dépasse la longueur de la piste.\n"
                  "Recherche d'une piste d'atterrissage sûre en cours...")
            aeroport_proche = trouver_aeroport_proche(aeroport)
            code_aeroport_courant = aeroport_proche["ident"]
            pistes = df_runways[df_runways["ident"] == code_aeroport_courant]

            ligne = pistes.iloc[0]
            nouvelle_piste = classes.aeroports.Piste(ligne["ident"], df_runways, ligne["runway_ident"])
            aeroport.append(nouvelle_piste)
            print(f"Test pour l'aéroport {nouvelle_piste.nom()}...")
            continue  # relance le while
        break  # sortie si piste compatible trouvée

    print(f"Vous pouvez atterrir à {piste.nom()} sur la piste {piste.n_piste}")
    print(f"La longueur de la piste est {piste.longueur()} ft et la distance nécessaire de {distance_necessaire:.2f} ft")


def trouver_aeroport_proche(exclusions):
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

"""
piste = classes.Piste("CYUL", recuperer_runways(),"10-28")
meteo = classes.meteos.Meteo(15+273.15,1013,10,270,0,0)
choix_avion = ChoixAvion("A320")
avion = classes.avions.Commercial(120000,choix_avion,meteo,piste)
affichages_graphiques.afficher_trajectoire_atterrissage(avion)
affichages_graphiques.afficher_freinage(avion)

# Exemple de la fonction compare()
piste = classes.Piste("CSP6", recuperer_runways(),"07-25")
"""


def code_aeroport_valide(airports_df):
    """
    Demande à l'utilisateur un code d'aéroport valide jusqu'à ce qu'un code valide soit entré

    Args:
        airports_df (DataFrame): DataFrame contenant les données des aéroports avec une colonne 'ident'

    Returns:
        str: Code d'aéroport valide
    """
    while True:
        code_aeroport = input("\nEntrez le code de l'aéroport (ex: CYUL): ").strip().upper()
        if code_aeroport in airports_df["ident"].values:
            return code_aeroport
        print("Code d'aéroport invalide. Veuillez réessayer.")


def choisir_piste(pistes_dispo):
    """
    Demande à l'utilisateur de choisir une piste valide parmi les options disponibles

    Args:
        pistes_dispo (list): Liste des pistes disponibles

    Returns:
        str: Numéro/identifiant de la piste choisie
    """
    while True:
        try:
            choix = int(input("\nChoisissez une piste (numéro): "))
            if 1 <= choix <= len(pistes_dispo):
                return pistes_dispo[choix - 1]
        except ValueError:
            pass
        print("Choix invalide. Veuillez réessayer.")


def choisir_avion(avions_filtres):
    """
    Permet à l'utilisateur de choisir un avion parmi une liste ou de créer un avion personnalisé

    Args:
        avions_filtres (DataFrame): DataFrame contenant les avions disponibles

    Returns:
        ChoixAvion: Objet ChoixAvion configuré selon le choix de l'utilisateur
    """
    while True:
        choix = input("\nEntrez le numero de l'avion: ").strip()

        try:
            choix_num = int(choix)

            # Choix d'un avion existant
            if 1 <= choix_num <= len(avions_filtres):
                code_avion = avions_filtres.iloc[choix_num - 1]['Code']
                print(f"\nVous avez sélectionné l'avion: {code_avion}")
                return ChoixAvion(code_avion)

            # Option pour créer un avion personnalisé
            elif choix_num == len(avions_filtres) + 1:
                print("\nSaisie des caractéristiques de l'avion:")
                hauteur_m = get_float_input("Hauteur de l'aile (m): ")
                surface_m2 = get_float_input("Surface alaire (m²): ")

                custom_data = {
                    'Code': 'CUSTOM',
                    'Allongement': get_float_input("Allongement: "),
                    'Hauteur_aile_m': hauteur_m,
                    'Hauteur_aile_ft': hauteur_m * 3.28084,
                    'Surface_alaire_m2': surface_m2,
                    'Surface_alaire_ft2': surface_m2 * 10.7639,
                    'CL_max_atterrissage': get_float_input("Coefficient de portance max (CL_max): "),
                    'Cd_train': get_float_input("Coefficient de traînée du train (Cd_train): "),
                    'Cd_volets': get_float_input("Coefficient de traînée des volets (Cd_volets): ")
                }
                print("\nVous avez créé un avion personnalisé: CUSTOM")
                return ChoixAvion('CUSTOM', custom_data=custom_data)

            else:
                print(f"Veuillez entrer un nombre entre 1 et {len(avions_filtres) + 1}")

        except ValueError:
            print("Entrée invalide. Veuillez entrer uniquement le numéro de l'avion.")


def choisir_type_avion(choix_avion_df):
    """
    Permet à l'utilisateur de choisir entre avion commercial ou militaire

    Args:
        choix_avion_df (DataFrame): DataFrame contenant tous les avions disponibles

    Returns:
        tuple: (type_selectionne, avions_filtres) où:
            - type_selectionne: str ("Commercial" ou "Militaire")
            - avions_filtres: DataFrame filtré selon le type choisi
    """
    while True:
        try:
            type_avion = int(input("\nChoisissez le type d'avion (1 ou 2):  "))

            if type_avion == 1:
                type_selectionne = "Commercial"
            elif type_avion == 2:
                type_selectionne = "Militaire"
            else:
                print("Veuillez entrer 1 ou 2.")
                continue

            avions_filtres = choix_avion_df[choix_avion_df['Type'] == type_selectionne]

            if avions_filtres.empty:
                print(f"\nAucun avion {type_selectionne.lower()} disponible dans la base.")
                print("Veuillez choisir un autre type ou ajouter des avions.")
                continue

            return type_selectionne, avions_filtres

        except ValueError:
            print("Choix invalide. Veuillez entrer 1 ou 2.")