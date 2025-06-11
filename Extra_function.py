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
    S_TR = avion.calcul_S_TR()
    S_FR = avion.calcul_S_FR()
    S_B = avion.calcul_S_B()
    angle_descente = avion.angle_de_descente

    # Phase 1: Approche initiale
    x_A = np.linspace(0, S_A, 100)
    y_A = np.tan(angle_descente) * x_A

    # Phase 2: Transition
    x_TR = np.linspace(S_A, S_A + S_TR, 100)
    y_TR = np.tan(angle_descente) * S_A + (0 - np.tan(angle_descente) * S_A) * (x_TR - S_A) / S_TR

    # Phase 3: Roulement libre
    x_FR = np.linspace(S_A + S_TR, S_A + S_TR + S_FR, 100)
    y_FR = np.zeros_like(x_FR)

    # Phase 4: Freinage
    x_B = np.linspace(S_A + S_TR + S_FR, S_A + S_TR + S_FR + S_B, 100)
    y_B = np.zeros_like(x_B)

    # Tracer la trajectoire
    plt.figure(figsize=(10, 5))
    plt.plot(x_A, y_A, label='Approche initiale')
    plt.plot(x_TR, y_TR, label='Transition')
    plt.plot(x_FR, y_FR, label='Roulement libre')
    plt.plot(x_B, y_B, label='Freinage')
    plt.axhline(0, color='black', linewidth=0.8)  # Ligne de la piste
    plt.xlabel('Distance')
    plt.ylabel('Altitude')
    plt.title('Trajectoire d\'atterrissage de l\'avion')
    plt.legend()
    plt.grid(True)
    plt.axis('equal')
    plt.show()

# Exemple d'utilisation
piste = classes.aeroports.Piste("YUL", "code", "ville", (45.67, -73.75), 1700,
                 2, "Asphalte", 45, 3000, 105)
meteo = classes.meteos.Meteo(15+273.15,1013,10,270)
avion = classes.avions.Militaire("A320",17918,8,60,396.1,2.62,meteo,piste)
afficher_trajectoire_atterrissage(avion)

compare(avion,piste)

