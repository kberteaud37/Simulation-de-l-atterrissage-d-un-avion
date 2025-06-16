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

# Exemple d'utilisation
piste = classes.Piste("CYUL", recuperer_runways(),"10-28")
meteo = classes.meteos.Meteo(15+273.15,1013,10,270,0,0)
choix_avion = ChoixAvion("A320")
avion = classes.avions.Commercial(120000,choix_avion,meteo,piste)
affichages_graphiques.afficher_trajectoire_atterrissage(avion)
affichages_graphiques.afficher_freinage(avion)

# Exemple de la fonction compare()
piste = classes.Piste("CSP6", recuperer_runways(),"07-25")
compare(avion,piste)
