"""--------Projet de session - Simulation de l'atterrissage d'un avion----------

    - Kilian Berteaud
    - Alexis Chenuet
    - Pierrick Loranchet

Cours MGA802, Session Été 2025
"""


#PROGRAMME PRINCIPAL

import classes
from classes.aeroports.fonctions_aeroport import recuperer_runways, recuperer_airports
from classes.avions.choix_avion import ChoixAvion
from classes.meteos.fonctions_meteo import recuperer_meteo
from Extra_function import get_float_input, afficher_trajectoire_atterrissage, compare
import matplotlib.pyplot as plt
try:
    from classes.avions.fonction_avion import charger_donnees_avions
except ImportError:
    # Fallback si la structure des packages ne fonctionne pas
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent))
    from fonction_avion import charger_donnees_avions

def main():
    print("\n" + "=" * 50)
    print("SIMULATEUR D'ATTERRISSAGE D'AVION - QUÉBEC")
    print("=" * 50 + "\n")

    # 1. Choix de l'aéroport
    runways_df = recuperer_runways()
    airports_df = recuperer_airports()

    print("\nListe des aéroports disponibles au Québec:")
    print(airports_df[["ident", "name"]].to_string(index=False))

    while True:
        code_aeroport = input("\nEntrez le code de l'aéroport (ex: CYUL): ").strip().upper()
        if code_aeroport in airports_df["ident"].values:
            break
        print("Code d'aéroport invalide. Veuillez réessayer.")

    # 2. Choix de la piste
    pistes_dispo = runways_df[runways_df["ident"] == code_aeroport]["runway_ident"].unique()
    print(f"\nPistes disponibles pour l'aéroport {code_aeroport}:")
    for i, piste in enumerate(pistes_dispo, 1):
        print(f"{i}. {piste}")

    while True:
        try:
            choix = int(input("\nChoisissez une piste (numéro): "))
            if 1 <= choix <= len(pistes_dispo):
                num_piste = pistes_dispo[choix - 1]
                break
        except ValueError:
            pass
        print("Choix invalide. Veuillez réessayer.")

    piste = classes.aeroports.Piste(code_aeroport, runways_df, num_piste)
    piste.afficher_infos()
    piste.afficher_infos_piste()

    # 3. Récupération des données météo
    print("\nRécupération des données météo en cours...")
    try:
        lat, lon = piste.latitude(), piste.longitude()
        temp, pression, vent_vitesse, vent_direction = recuperer_meteo(lat, lon)
        meteo = classes.meteos.Meteo(temp, pression, vent_vitesse, vent_direction)
        print("\nConditions météo actuelles:")
        print(f"- Température: {temp}°C")
        print(f"- Pression: {pression} hPa")
        print(f"- Vent: {vent_vitesse} km/h, direction {vent_direction}°")
    except Exception as e:
        print(f"\nErreur lors de la récupération des données météo: {e}")
        print("Utilisation de valeurs météo par défaut (15°C, 1013 hPa, vent calme)")
        meteo = classes.meteos.Meteo(15, 1013, 0, 0)

    # 4. Choix du type d'avion
    print("\nTypes d'avion disponibles:")
    print("1. Commercial")
    print("2. Militaire")

    while True:
        try:
            type_avion = int(input("\nChoisissez le type d'avion (1 ou 2): "))
            if type_avion in (1, 2):
                break
        except ValueError:
            pass
        print("Choix invalide. Veuillez réessayer.")

    # 5. Sélection de l'avion
    print("\nChargement des modèles d'avion disponibles...")
    choix_avion_df = charger_donnees_avions()  # Utilisez la fonction directement
    print("\nAvions disponibles:")
    print(choix_avion_df[["Code"]].to_string(index=False, header=False))

    while True:
        code_avion = input("\nEntrez le code de l'avion (ex: A320): ").strip().upper()
        if code_avion in choix_avion_df["Code"].values:
            break
        print("Code d'avion invalide. Veuillez réessayer.")

    choix_avion_obj = ChoixAvion(code_avion)

    # 6. Paramètres de l'avion
    print("\nEntrez les paramètres de l'avion:")
    poids = get_float_input("- Poids à l'atterrissage (kg): ")
    vitesse_vent = get_float_input("- Vitesse du vent (km/h, 0 si déjà dans les données météo): ")

    # 7. Création de l'objet avion
    if type_avion == 1:
        avion = classes.avions.Commercial(poids, choix_avion_obj, meteo, piste, vitesse_vent)
    else:
        avion = classes.avions.Militaire(poids, choix_avion_obj, meteo, piste, vitesse_vent)

    # 8. Calculs et résultats
    print("\n" + "=" * 50)
    print("RÉSULTATS DE LA SIMULATION")
    print("=" * 50)

    # Comparaison piste/atterrissage
    compare(avion, piste)

    # Affichage des détails
    print("\nDétails des calculs:")
    print(f"- Vitesse de décrochage: {avion.calcul_V_stall():.2f} ft/s")
    print(f"- Distance d'approche (S_A): {avion.calcul_S_A():.2f} ft")
    print(f"- Distance de transition (S_TR): {avion.calcul_S_TR():.2f} ft")
    print(f"- Distance de roulement libre (S_FR): {avion.calcul_S_FR():.2f} ft")
    print(f"- Distance de freinage (S_B): {avion.calcul_S_B():.2f} ft")
    print(f"- Distance totale d'atterrissage: {avion.calcul_S_LA():.2f} ft")

    # 9. Visualisation
    print("\nVoulez-vous voir la trajectoire d'atterrissage? (O/N)")
    if input().strip().upper() == "O":
        afficher_trajectoire_atterrissage(avion)
        plt.show()

    print("\nSimulation terminée. Bon vol!")


if __name__ == "__main__":
    main()