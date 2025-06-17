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