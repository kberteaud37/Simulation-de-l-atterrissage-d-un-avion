import matplotlib.pyplot as plt
import numpy as np
import classes
from scipy.spatial import KDTree
from classes.aeroports.fonctions_aeroport import recuperer_runways,recuperer_airports
from classes.avions.choix_avion import ChoixAvion


#Fonction forçant l'utilisateur à entrer une valeur acceptable
def get_float_input(prompt):
    while True:
        # Constantly check if a value was entered followed by Enter
        try:
            # Put the value entered by user in "entrée"
            value = float(input(prompt))
            break
        except ValueError:
            # If input is not a float we get a ValueError
            print("Invalid input, please try again.")
    return value

# Fonction qui compare la longueur des pistes avec la distance nécessaire à l'atterrissage
def compare(avion, piste, coef_secu=1.67):
    distance_necessaire = (avion.calcul_S_B()+avion.calcul_S_FR()+avion.calcul_S_TR()) * coef_secu
    print(f"La distance nécessaire est : {distance_necessaire} ft")
    print(f"La longueur de la piste est : {piste.longueur()} ft")

    df_runways = recuperer_runways()
    aeroport = [piste]
    code_aeroport_courant = piste.code
    pistes = df_runways[df_runways["ident"] == code_aeroport_courant]

    max_recherches = 20
    nb_recherches = 0

    while distance_necessaire >= piste.longueur():
        if nb_recherches >= max_recherches:
            raise RuntimeError("Trop de recherches effectuées, aucun aéroport viable trouvé.")
        nb_recherches += 1
        print("Atterrissage non sûr : la distance nécessaire dépasse la longueur de la piste.\n"
              "Recherche d'une piste d'atterrissage sûre en cours...")

        for num_piste in pistes["runway_ident"]:
            piste_test = classes.aeroports.Piste(code_aeroport_courant, df_runways, num_piste)
            if distance_necessaire < piste_test.longueur():
                piste = piste_test
                break
        else:
            aeroport_proche = trouver_aeroport_proche(aeroport)
            code_aeroport_courant = aeroport_proche["ident"]
            pistes = df_runways[df_runways["ident"] == code_aeroport_courant]

            ligne = pistes.iloc[0]
            nouvelle_piste = classes.aeroports.Piste(ligne["ident"], df_runways, ligne["runway_ident"])
            aeroport.append(nouvelle_piste)
            continue  # relance le while
        break  # sortie si piste compatible trouvée

    print(f"Vous pouvez atterrir à {piste.nom()} sur la piste {piste.n_piste}")
    print(f"La longueur de la piste est {piste.longueur()} ft et la distance nécessaire de {distance_necessaire} ft")


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

    print(f"Aéroport le plus proche (hors exclusions) : {plus_proche['ident']} à {dist * 6371:.2f} km")
    return plus_proche


def afficher_trajectoire_atterrissage(avion):
    # Initialisation des valeurs
    S_A = avion.calcul_S_A()
    print(f"S_A = {S_A}")
    S_TR = avion.calcul_S_TR()
    print(f"S_TR = {S_TR}")
    S_FR = avion.calcul_S_FR()
    print(f"S_FR = {S_FR}")
    S_B = avion.calcul_S_B()
    print(f"S_B = {S_B}")
    angle_rad = np.radians(avion.angle_de_descente)
    print(angle_rad)
    h_obstacle = avion.H_OBS

    # Création des données pour la trajectoire
    x_A = np.linspace(0, S_A, 100)
    y_A = avion.H_OBS + x_A * np.tan(angle_rad)

    # Calculer les coordonnées pour la phase de transition
    # Rayon de courbure pour la transition
    rayon = abs(h_obstacle / np.sin(angle_rad))

    # Centre du cercle de transition
    x_center = S_A
    y_center = h_obstacle + S_A * np.tan(angle_rad) - rayon

    # Angle pour l'arc de cercle
    theta = np.linspace(np.pi / 2, np.pi, 100)
    x_TR = x_center + rayon * np.cos(theta)
    y_TR = y_center + rayon * np.sin(theta)

    # Roulement libre et freinage
    x_FR = np.linspace(S_A + S_TR, S_A + S_TR + S_FR, 100)
    y_FR = np.zeros_like(x_FR)

    x_B = np.linspace(S_A + S_TR + S_FR, S_A + S_TR + S_FR + S_B, 100)
    y_B = np.zeros_like(x_B)

    # Tracer la trajectoire
    plt.figure(figsize=(12, 6))
    plt.plot(x_A, y_A, label='Approche initiale', color='blue')
    plt.plot(x_TR, y_TR, label='Transition', color='orange')
    plt.plot(x_FR, y_FR, label='Roulement libre', color='green',linewidth=3)
    plt.plot(x_B, y_B, label='Freinage', color='red',linewidth=3)
    # Tracer la piste

    # Ajouter des labels et une légende
    plt.title("Trajectoire d'atterrissage de l'avion")
    plt.xlabel('Distance')
    plt.ylabel('Altitude')
    plt.legend()
    plt.grid(True)
    plt.ylim(-h_obstacle-10, h_obstacle+10)
    plt.show()

# Exemple d'utilisation
piste = classes.Piste("CYUL", recuperer_runways(),"10-28")
meteo = classes.meteos.Meteo(15+273.15,1013,10,270)
choix_avion = ChoixAvion("A320")
avion = classes.avions.Commercial(158732,choix_avion,meteo,piste,45)
"""afficher_trajectoire_atterrissage(avion)"""

# Exemple de la fonction compare()
piste = classes.Piste("CSP6", recuperer_runways(),"07-25")
compare(avion,piste)