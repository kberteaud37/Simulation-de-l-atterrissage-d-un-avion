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