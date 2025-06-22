import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

def afficher_freinage(avion):
    """Affiche un graphique de la décélération d'un avion pendant le freinage.

    Cette fonction calcule et affiche la décélération de l'avion en fonction de la distance parcourue
    pendant le freinage. Elle utilise matplotlib pour tracer le graphique et Streamlit pour l'afficher.

    :param avion: Un objet de type Avion contenant les caractéristiques et conditions d'atterrissage.
    :type avion: Avion

    :return: None
    """
    distance_i = avion.calcul_S_FR()
    distance_f = avion.calcul_S_B()
    distances = np.linspace(distance_i, distance_f, 1000)

    decelerations = [avion.calcul_deceleration(d) for d in distances]

    fig, ax = plt.subplots()
    ax.plot(distances, decelerations)
    ax.set_xlabel('Distance (ft)')
    ax.set_ylabel('Décélération (ft/s²)')
    ax.set_title('Décélération en fonction de la distance')
    ax.grid(True)

    st.pyplot(fig)