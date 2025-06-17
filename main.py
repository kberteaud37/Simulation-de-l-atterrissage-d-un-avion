"""--------Projet de session - Simulation de l'atterrissage d'un avion----------

    - Kilian Berteaud
    - Alexis Chenuet
    - Pierrick Loranchet

Cours MGA802, Session Été 2025
"""


#PROGRAMME PRINCIPAL
import classes
from classes.aeroports.fonctions_aeroport import recuperer_runways, recuperer_airports
from classes.meteos.fonctions_meteo import recuperer_meteo
from redirection_aeroport import compare
from affichages_graphiques import afficher_trajectoire_atterrissage, afficher_freinage
from classes.avions.fonction_avion import charger_donnees_avions
from choix_utilisateur import *

def main():
    print("\n" + "=" * 50)
    print("SIMULATEUR D'ATTERRISSAGE D'AVION - QUÉBEC")
    print("=" * 50 + "\n")

    # 1. Choix de l'aéroport
    runways_df = recuperer_runways()
    airports_df = recuperer_airports()
    print("\nListe des aéroports disponibles au Québec:")
    print(airports_df[["ident", "name"]].to_string(index=False))

    code_aeroport = code_aeroport_valide(airports_df)
    aeroport = classes.aeroports.Aeroport(code_aeroport, runways_df)
    aeroport.afficher_infos()

    # 2. Choix de la piste
    pistes_dispo = runways_df[runways_df["ident"] == code_aeroport]["runway_ident"].unique()
    print(f"\nPistes disponibles pour l'aéroport {code_aeroport}:")
    for i, piste in enumerate(pistes_dispo, 1):
        print(f"{i}. {piste}")

    piste_choisie = choisir_piste(pistes_dispo)
    piste = classes.aeroports.Piste(code_aeroport, runways_df, piste_choisie)

    # 3. Récupération des données météo
    print("\nRécupération des données météo en cours...")
    meteo = None  # Initialisation de la variable
    try:
        lat, lon = piste.latitude(), piste.longitude()
        meteo_data = recuperer_meteo(lat, lon)
        meteo = classes.meteos.Meteo(
            meteo_data["T"],
            meteo_data["P"],
            meteo_data["V_vent"],
            meteo_data["Dir_vent"],
            meteo_data["pluie"],
            meteo_data["glace"]
        )
        print("\nConditions météo actuelles:")
        print(f"- Température: {meteo_data['T']}°C")
        print(f"- Pression: {meteo_data['P']} hPa")
        print(f"- Vent: {meteo_data['V_vent']} km/h, direction {meteo_data['Dir_vent']}°")

        # Avertissements météo
        if meteo_data["pluie"]:
            print("\n⚠️ ATTENTION: Pluie détectée - le coefficient de friction sera réduit")
        if meteo_data["glace"]:
            print("\n⚠️ ATTENTION: Glace détectée - le coefficient de friction sera fortement réduit")
        if meteo_data["pluie"] and meteo_data["glace"]:
            print("\n⚠️ ATTENTION EXTREME: Conditions glacées avec pluie - coefficient de friction minimal")

    except Exception as e:
        print(f"\nErreur lors de la récupération des données météo: {e}")
        print("Utilisation de valeurs météo par défaut (15°C, 1013 hPa, vent calme)")
        meteo = classes.meteos.Meteo(15, 1013, 0, 0, False, False)

    # Maintenant que meteo est défini, on peut l'utiliser
    piste.afficher_infos_piste(meteo.pluie, meteo.glace)

    # 4. Choix du type d'avion
    print("\nTypes d'avion disponibles:")
    print("1. Commercial")
    print("2. Militaire")
    # Charger les données des avions avant de les filtrer
    choix_avion_df = charger_donnees_avions()
    if choix_avion_df.empty:
        print("ERREUR CRITIQUE: Impossible de charger les données avions. Vérifiez le fichier data_avions.csv")
        return

    while True:
        try:
            type_avion = int(input("\nChoisissez le type d'avion (1 ou 2): "))
            if type_avion in (1, 2):
                type_selectionne = "Commercial" if type_avion == 1 else "Militaire"
                avions_filtres = choix_avion_df[choix_avion_df['Type'] == type_selectionne]

                if avions_filtres.empty:
                    print(f"\nAucun avion {type_selectionne.lower()} disponible dans la base.")
                    print("Veuillez choisir un autre type ou ajouter des avions.")
                    continue

                break
        except ValueError:
            print("Choix invalide. Veuillez entrer 1 ou 2.")


        # 5. Sélection de l'avion
    print("\nAvions disponibles:")
    # Afficher une liste numérotée avec formatage pour aligner les numéros
    max_num_width = len(str(len(avions_filtres)))
    for i, (_, row) in enumerate(avions_filtres.iterrows(), 1):
        print(f"{i:{max_num_width}d}. {row['Code']}")
    print(f"{len(avions_filtres) + 1}. Saisie manuelle")

    choix_avion_obj = choisir_avion(avions_filtres)

    # 6. Paramètres de l'avion
    print("\nEntrez les paramètres de l'avion:")
    poids = get_float_input("- Poids à l'atterrissage (lb): ")


    # 7. Création de l'objet avion
    if type_avion == 1:
        avion = classes.avions.Commercial(poids, choix_avion_obj, meteo, piste)
    else:
        avion = classes.avions.Militaire(poids, choix_avion_obj, meteo, piste)

    # 8. Calculs et résultats
    print("\n" + "=" * 50)
    print(f"RÉSULTATS DE LA SIMULATION - {avion.code}")  # Ajout du code de l'avion ici
    print("=" * 50)

    # Comparaison piste/atterrissage
    piste_finale=compare(avion,piste)

    if recuperer_meteo(piste_finale.latitude(), piste_finale.longitude())['Dir_vent'] in range(0,180):
        print(f"Le vent à cet aéroport vient de l'Est, à {recuperer_meteo(piste_finale.latitude(), piste_finale.longitude())['Dir_vent']}° par rapport au Nord Magnétique")
        print(f"Vous devez atterrir sur la piste n°{piste_finale.orientation()[0]} pour être face au vent")
    elif recuperer_meteo(piste_finale.latitude(), piste_finale.longitude())['Dir_vent'] in range(181,360):
        print(f"Le vent à cet aéroport vient de l'Ouest, à {recuperer_meteo(piste_finale.latitude(), piste_finale.longitude())['Dir_vent']}° par rapport au Nord Magnétique")
        print(f"Vous devez atterrir sur la piste n°{piste_finale.orientation()[1]}° pour être face au vent")
    # Affichage des détails

    print("\nDétails des calculs:")
    print(f"- Vitesse de décrochage: {avion.calcul_V_stall():.2f} ft/s")
    print(f"- Distance d'approche (S_A): {avion.calcul_S_A():.2f} ft")
    print(f"- Distance de transition (S_TR): {avion.calcul_S_TR():.2f} ft")
    print(f"- Distance de roulement libre (S_FR): {avion.calcul_S_FR():.2f} ft")
    print(f"- Distance de freinage (S_B): {avion.calcul_S_B():.2f} ft")
    print(f"- Distance totale d'atterrissage: {avion.calcul_S_LA():.2f} ft")

    # 9. Visualisation
    # 9. Visualisation
    print("\nVoulez-vous voir la trajectoire d'atterrissage? (O/N)")
    if input().strip().upper() == "O":
        print("\nAffichage de la trajectoire...")
        afficher_trajectoire_atterrissage(avion)

        print("\nAffichage du profil de freinage...")
        afficher_freinage(avion)

    print("\nSimulation terminée. Bon vol!")


if __name__ == "__main__":
    main()