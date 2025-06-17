import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

def afficher_trajectoire_atterrissage(avion):
    S_A = avion.calcul_S_A()
    S_TR = avion.calcul_S_TR()
    S_FR = avion.calcul_S_FR()
    S_B = avion.calcul_S_B()
    angle_rad = np.radians(avion.angle_de_descente)
    h_obstacle = avion.H_OBS
    R = avion.calcul_R()
    H_TR = avion.calcul_H_TR()

    x_A = np.linspace(0, S_A, 100)
    y_A = avion.H_OBS + x_A * np.tan(angle_rad)

    center_x = S_A + S_TR
    center_y = R
    theta = np.linspace(0, np.pi, 1000)
    x_circle = center_x - R * np.sin(theta)
    y_circle = center_y - R * np.cos(theta)
    mask = (x_circle >= S_A) & (x_circle <= S_A + S_TR) & (y_circle >= 0) & (y_circle <= H_TR)
    x_filtered = x_circle[mask]
    y_filtered = y_circle[mask]

    x_FR = np.linspace(S_A + S_TR, S_A + S_TR + S_FR, 100)
    y_FR = np.zeros_like(x_FR) + 0.1

    x_B = np.linspace(S_A + S_TR + S_FR, S_A + S_TR + S_FR + S_B, 100)
    y_B = np.zeros_like(x_B) + 0.1

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(x_A, y_A, label='Approche initiale', color='blue')
    ax.plot(x_filtered, y_filtered, label='Transition', color='orange')
    ax.plot(x_FR, y_FR, label='Roulement libre', color='green')
    ax.plot(x_B, y_B, label='Freinage', color='red')
    ax.set_title("Trajectoire d'atterrissage de l'avion")
    ax.set_xlabel('Distance')
    ax.set_ylabel('Altitude')
    ax.legend()
    ax.grid(True)
    ax.set_ylim(-h_obstacle-10, h_obstacle+10)

    st.pyplot(fig)