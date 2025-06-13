import matplotlib.pyplot as plt
import numpy as np

def afficher_trajectoire_atterrissage(avion):
    # Initialisation des valeurs
    S_A = avion.calcul_S_A()
    S_TR = avion.calcul_S_TR()
    S_FR = avion.calcul_S_FR()
    S_B = avion.calcul_S_B()
    angle_rad = np.radians(avion.angle_de_descente)
    h_obstacle = avion.H_OBS
    R = avion.calcul_R()
    H_TR = avion.calcul_H_TR()

    # Création des données pour la trajectoire
    x_A = np.linspace(0, S_A, 100)
    y_A = avion.H_OBS + x_A * np.tan(angle_rad)

    # Centre du cercle
    center_x = S_A + S_TR
    center_y = R

    # Création des points du cercle
    theta = np.linspace(0, np.pi, 1000)
    x_circle = center_x - R * np.sin(theta)
    y_circle = center_y - R * np.cos(theta)

    # Filtrer les points pour les intervalles souhaités
    mask = (x_circle >= S_A) & (x_circle <= S_A + S_TR) & (y_circle >= 0) & (y_circle <= H_TR)
    x_filtered = x_circle[mask]
    y_filtered = y_circle[mask]

    # Roulement libre et freinage
    x_FR = np.linspace(S_A + S_TR, S_A + S_TR + S_FR, 100)
    y_FR = np.zeros_like(x_FR) + 0.1 # La droite est juste au-dessus de l'axe des 0

    x_B = np.linspace(S_A + S_TR + S_FR, S_A + S_TR + S_FR + S_B, 100)
    y_B = np.zeros_like(x_B) + 0.1

    # Tracer la trajectoire
    plt.figure(figsize=(12, 6))
    plt.plot(x_A, y_A, label='Approche initiale', color='blue')
    plt.plot(x_filtered, y_filtered, label='Transition', color='orange')
    plt.plot(x_FR, y_FR, label='Roulement libre', color='green')
    plt.plot(x_B, y_B, label='Freinage', color='red')
    # Tracer la piste

    # Ajouter des labels et une légende
    plt.title("Trajectoire d'atterrissage de l'avion")
    plt.xlabel('Distance')
    plt.ylabel('Altitude')
    plt.legend()
    plt.grid(True)
    plt.ylim(-h_obstacle-10, h_obstacle+10)
    plt.show()


