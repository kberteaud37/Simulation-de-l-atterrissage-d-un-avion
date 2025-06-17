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
                break
        except ValueError:
            pass
        print("Choix invalide. Veuillez réessayer.")