import matplotlib.pyplot as plt
import numpy as np

def afficher_freinage(avion):
    decelerations = []
    distance_i = avion.calcul_S_FR()
    distance_f = avion.calcul_S_B()
    distances = np.linspace(distance_i, distance_f, 1000)  # 1000 distances autour de la valeur donnée

    for _ in distances:
        decelerations = [avion.calcul_deceleration(d) for d in distances]

    plt.plot(distances, decelerations)
    plt.xlabel('Distance (ft)')
    plt.ylabel('Décélération (ft/s²)')
    plt.title('Décélération en fonction de la distance')
    plt.grid(True)
    plt.show()
