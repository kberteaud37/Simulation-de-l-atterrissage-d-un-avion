import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

def afficher_freinage(avion):
    decelerations = []
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