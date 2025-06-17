from classes.avions.choix_avion import ChoixAvion
from choix_utilisateur import get_float_input

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