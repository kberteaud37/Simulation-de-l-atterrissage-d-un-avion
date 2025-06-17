import matplotlib.pyplot as plt
import numpy as np

def afficher_freinage(avion):
    """
        Affiche un graphique de la décélération en fonction de la distance de freinage.

        Cette fonction calcule et affiche la courbe de décélération d'un avion entre sa distance
        de freinage initiale (S_FR) et sa distance de freinage finale (S_B).

        :param avion: Objet avion contenant les méthodes de calcul de freinage
        :type avion: object
        :return: None (affiche directement le graphique)

    """
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

