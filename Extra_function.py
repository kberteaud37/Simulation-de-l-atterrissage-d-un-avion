
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

