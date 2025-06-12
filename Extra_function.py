import matplotlib.pyplot as plt
import numpy as np
import classes

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

def compare(avion,piste,coef_secu = 1.67):
    distance_necessaire = avion.calcul_S_B() * coef_secu
    if piste.longueur() <= distance_necessaire:
        print("Atterrissage sûr : la distance nécessaire est inférieure ou égale à la longueur de la piste")
        return True
    else:
        print("Atterrissage non sûr : la distance nécessaire dépasse la longueur de la piste.\n"
              "Recherche d'une piste d'atterrissage sûre en cours...")
        return False

def afficher_trajectoire_atterrissage(avion):
    # Initialisation des valeurs
    S_A = avion.calcul_S_A()
    print(f"S_A = {S_A}")
    S_TR = avion.calcul_S_TR()
    print(f"S_TR = {S_TR}")
    S_FR = avion.calcul_S_FR()
    print(f"S_FR = {S_FR}")
    S_B = avion.calcul_S_B()
    print(f"S_B = {S_B}")
    angle_rad = np.radians(avion.angle_de_descente)
    print(angle_rad)
    h_obstacle = avion.H_OBS

    # Création des données pour la trajectoire
    x_A = np.linspace(0, S_A, 100)
    y_A = avion.H_OBS + x_A * np.tan(angle_rad)

    # Calculer les coordonnées pour la phase de transition
    # Rayon de courbure pour la transition
    rayon = abs(h_obstacle / np.sin(angle_rad))

    # Centre du cercle de transition
    x_center = S_A
    y_center = h_obstacle + S_A * np.tan(angle_rad) - rayon

    # Angle pour l'arc de cercle
    theta = np.linspace(np.pi / 2, np.pi, 100)
    x_TR = x_center + rayon * np.cos(theta)
    y_TR = y_center + rayon * np.sin(theta)

    # Roulement libre et freinage
    x_FR = np.linspace(S_A + S_TR, S_A + S_TR + S_FR, 100)
    y_FR = np.zeros_like(x_FR)

    x_B = np.linspace(S_A + S_TR + S_FR, S_A + S_TR + S_FR + S_B, 100)
    y_B = np.zeros_like(x_B)

    # Tracer la trajectoire
    plt.figure(figsize=(12, 6))
    plt.plot(x_A, y_A, label='Approche initiale', color='blue')
    plt.plot(x_TR, y_TR, label='Transition', color='orange')
    plt.plot(x_FR, y_FR, label='Roulement libre', color='green',linewidth=3)
    plt.plot(x_B, y_B, label='Freinage', color='red',linewidth=3)
    # Tracer la piste

    # Ajouter des labels et une légende
    plt.title("Trajectoire d'atterrissage de l'avion")
    plt.xlabel('Distance')
    plt.ylabel('Altitude')
    plt.legend()
    plt.grid(True)
    plt.ylim(-h_obstacle-10, h_obstacle+10)
    plt.show()

# Exemple d'utilisation
piste = classes.aeroports.Piste("YUL", "code", "ville", (45.67, -73.75), 1700,
                 2, "Asphalte", 45, 3000, 105)
meteo = classes.meteos.Meteo(15+273.15,1013,10,270)
avion = classes.avions.Commercial("A320",17918,8,60,396.1,2.62,meteo,piste,45)
afficher_trajectoire_atterrissage(avion)

compare(avion,piste)

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
