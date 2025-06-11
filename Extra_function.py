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
