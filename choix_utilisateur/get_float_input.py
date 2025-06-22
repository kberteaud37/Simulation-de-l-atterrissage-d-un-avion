def get_float_input(prompt):
    """Demande à l'utilisateur de saisir une valeur flottante valide.

    Cette fonction continue de demander à l'utilisateur de saisir une valeur jusqu'à ce qu'une
    valeur flottante valide soit entrée. Elle remplace également les virgules par des points
    pour faciliter la conversion en float.

    :param prompt: Message affiché à l'utilisateur pour lui demander de saisir une valeur.
    :type prompt: str

    :return: La valeur flottante saisie par l'utilisateur.
    :rtype: float
    """
    while True:
        # Constantly check if a value was entered followed by Enter
        try:
            value = input(prompt).replace(',', '.')  # Remplace les virgules par des points
            return float(value)
        except ValueError:
            # If input is not a float we get a ValueError
            print("Invalid input, please try again.")