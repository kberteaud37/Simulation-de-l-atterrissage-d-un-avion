import matplotlib.pyplot as plt
import numpy as np
import classes
from classes.aeroports.fonctions_aeroport import recuperer_runways
from classes.avions.choix_avion import ChoixAvion


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
    print(f"La distance nécessaire est : {distance_necessaire}")
    print(f"La longueur de la piste est : {piste.longueur()}")
    while distance_necessaire >= piste.longueur():
        print("Atterrissage non sûr : la distance nécessaire dépasse la longueur de la piste.\n"
              "Recherche d'une piste d'atterrissage sûre en cours...")
        pistes = recuperer_runways()[recuperer_runways()["ident"] == piste.code]
        for num_piste in pistes["runway_ident"]:
            piste = classes.aeroports.Piste("CYUL", recuperer_runways(), num_piste)
            print(piste.n_piste)
    print(f"Atterrissage sûr : la distance nécessaire est inférieure ou égale à la longueur "
          f"de la piste {piste.n_piste} à l'aéroport {piste.nom()}")

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
piste = classes.aeroports.Piste("CYUL", recuperer_runways(),"10-28")
meteo = classes.meteos.Meteo(15+273.15,1013,10,270)
choix_avion = ChoixAvion("A320")
avion = classes.avions.Commercial(17918,choix_avion,meteo,piste,45)
afficher_trajectoire_atterrissage(avion)

compare(avion,piste)

code = "CYUL"
num_p = "06L-24R"
row = recuperer_runways()[(recuperer_runways()["ident"] == code) & (recuperer_runways()["runway_ident"] == num_p)]
