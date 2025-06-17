import classes
from classes.aeroports.fonctions_aeroport import recuperer_runways
from .trouver_aeroport_proche import trouver_aeroport_proche
from .calcul_distance_aeroport import calcul_distance_aeroport

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

    distance_nm = calcul_distance_aeroport(aeroport[0].code, piste.code)
    print(f"Vous pouvez atterrir à {piste.nom()} (piste {piste.n_piste}), situé à {distance_nm:.2f} NM de {aeroport[0].nom()}.")
    print(f"La longueur de la piste est {piste.longueur()} ft et la distance nécessaire de {distance_necessaire:.2f} ft")

    return piste