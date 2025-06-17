import streamlit as st
import pandas as pd
import contextlib
from classes.aeroports.piste import Piste
import classes
from classes.aeroports.fonctions_aeroport import recuperer_runways, recuperer_airports

from classes.meteos.fonctions_meteo import recuperer_meteo

# 🔄 Pour afficher dans Streamlit des print() d'objets avec .afficher_infos()
import io
import sys


# Initialiser les états de session
if "step" not in st.session_state:
    st.session_state.step = 1

if "code_aeroport" not in st.session_state:
    st.session_state.code_aeroport = None

if "piste_choisie" not in st.session_state:
    st.session_state.piste_choisie = None

if "meteo_data" not in st.session_state:
    st.session_state.meteo_data = None


# Chargement des données
runways_df = recuperer_runways()
airports_df = recuperer_airports()


# === ÉTAPE 1 : Sélection Aéroport & Piste ===
if st.session_state.step == 1:
    st.title("🛬 Étape 1 : Choix de l'aéroport et de la piste")

    airport_codes = airports_df["ident"].tolist()
    selected_code = st.selectbox("Choisissez un aéroport (code ICAO)", options=airport_codes)
    if selected_code:
        aeroport = classes.aeroports.Aeroport(selected_code, runways_df)

        # Rediriger la sortie de print vers un buffer
        buffer = io.StringIO()
        sys.stdout = buffer
        aeroport.afficher_infos()
        sys.stdout = sys.__stdout__
        st.text(buffer.getvalue())

        pistes_dispo = runways_df[runways_df["ident"] == selected_code]["runway_ident"].unique()
        selected_piste = st.selectbox("Choisissez une piste", options=pistes_dispo)

        code = st.session_state.code_aeroport
        piste_id = st.session_state.piste_choisie
        piste = classes.aeroports.Piste(code, runways_df, piste_id)

        st.session_state.piste = piste


        piste_obj = Piste(code=selected_code, runways_df=runways_df, num_piste=selected_piste)


        # Enregistrer en session
        st.session_state.code_aeroport = selected_code
        st.session_state.piste_choisie = selected_piste

        if st.button("➡️ Suivant"):
            st.session_state.step = 2
            st.rerun()


# === ÉTAPE 2 : Affichage météo ===
elif st.session_state.step == 2:
    st.title("🌤️ Étape 2 : Conditions météo")

    code = st.session_state.code_aeroport
    piste_id = st.session_state.piste_choisie
    piste = classes.aeroports.Piste(code, runways_df, piste_id)

    st.session_state.piste = piste

    try:
        # Récupération des données météo
        lat, lon = piste.latitude(), piste.longitude()
        meteo_data = recuperer_meteo(lat, lon)

        pluie = meteo_data["pluie"]
        glace = meteo_data["glace"]

        # Création de l'objet Météo
        meteo = classes.meteos.Meteo(
            meteo_data["T"],
            meteo_data["P"],
            meteo_data["V_vent"],
            meteo_data["Dir_vent"],
            pluie,
            glace
        )

        st.session_state.meteo = meteo  # stockage pour les étapes suivantes

        # Affichage météo
        st.subheader("Conditions météo actuelles :")
        st.markdown(f"- 🌡️ Température : **{meteo_data['T']}°C**")
        st.markdown(f"- 📈 Pression : **{meteo_data['P']} hPa**")
        st.markdown(f"- 💨 Vent : **{meteo_data['V_vent']} km/h**, direction **{meteo_data['Dir_vent']}°**")

        if pluie and glace:
            st.error("⚠️ ATTENTION CONDITIONS EXTRÊMES : Conditions glacées avec pluie – Coefficient de friction minimal.")
        elif glace:
            st.warning("⚠️ ATTENTION : Glace détectée – Le coefficient de friction sera fortement réduit.")
        elif pluie:
            st.warning("⚠️ ATTENTION : Pluie détectée – Le coefficient de friction sera réduit.")

    except Exception as e:
        st.error(f"Erreur météo : {e}")
        st.info("Valeurs météo par défaut utilisées.")
        meteo_data = {
            "T": 15, "P": 1013, "V_vent": 0, "Dir_vent": 0, "pluie": False, "glace": False
        }
        pluie = meteo_data["pluie"]
        glace = meteo_data["glace"]

    st.subheader("Caractéristiques de la piste :")
    # Affichage des infos piste (utilise pluie/glace)
    buffer = io.StringIO()
    sys.stdout = buffer
    piste.afficher_infos_piste(pluie=pluie, glace=glace)
    sys.stdout = sys.__stdout__
    st.text(buffer.getvalue())

    # Navigation
    col1, col2 = st.columns(2)
    if col1.button("⬅️ Retour"):
        st.session_state.step = 1
        st.rerun()

    if col2.button("➡️ Étape suivante"):
        st.session_state.step = 3
        st.rerun()

elif st.session_state.step == 3:
    st.title("✈️ Étape 3 : Choix de l'avion et paramètres")

    from classes.avions.fonction_avion import charger_donnees_avions

    try:
        choix_avion_df = charger_donnees_avions()
    except Exception as e:
        st.error(f"❌ Impossible de charger les données avions : {e}")
        st.stop()

    if choix_avion_df.empty:
        st.error("❌ Aucune donnée avion chargée. Vérifie `data_avions.csv`.")
        st.stop()

    # Choix du type d'avion
    type_avion = st.selectbox("Sélectionnez le type d'avion :", options=["Commercial", "Militaire"])
    avions_filtres = choix_avion_df[choix_avion_df["Type"] == type_avion].copy()

    # Ajouter l'option personnalisée
    avions_filtres = avions_filtres.copy()
    avion_codes = avions_filtres["Code"].tolist() + ["Autre"]
    selected_code = st.selectbox("Choisissez un avion :", options=avion_codes)

    custom_avion_data = None

    if selected_code == "Autre":
        st.markdown("### ✏️ Caractéristiques personnalisées de l’avion")

        hauteur_m = st.number_input("Hauteur de l’aile (m)", min_value=0.0, step=0.1, format="%.2f")
        surface_m2 = st.number_input("Surface alaire (m²)", min_value=0.0, step=0.5, format="%.2f")

        allongement = st.number_input("Allongement", min_value=0.0, step=0.1, format="%.2f")
        cl_max = st.number_input("Coefficient de portance max à l’atterrissage", min_value=0.0, step=0.1, format="%.2f")
        cd_train = st.number_input("Coefficient de trainée du train d’atterrissage", min_value=0.0, step=0.01, format="%.3f")
        cd_volets = st.number_input("Coefficient de trainée des volets", min_value=0.0, step=0.01, format="%.3f")

        custom_avion_data = {
            'Code': 'CUSTOM',
            'Allongement': allongement,
            'Hauteur_aile_m': hauteur_m,
            'Hauteur_aile_ft': hauteur_m * 3.28084,
            'Surface_alaire_m2': surface_m2,
            'Surface_alaire_ft2': surface_m2 * 10.7639,
            'CL_max_atterrissage': cl_max,
            'Cd_train': cd_train,
            'Cd_volets': cd_volets
        }

    # Poids à l’atterrissage
    poids = st.number_input("💡 Entrez le poids à l’atterrissage (lb)", min_value=0.0, step=1000.0, format="%.0f")

    # Sauvegarde en session
    st.session_state.type_avion = type_avion
    st.session_state.avion_code = selected_code
    st.session_state.poids = poids
    if custom_avion_data:
        st.session_state.custom_avion_data = custom_avion_data

    # Navigation
    col1, col2 = st.columns(2)
    if col1.button("⬅️ Retour"):
        st.session_state.step = 2
        st.rerun()

    if col2.button("➡️ Étape suivante"):
        st.session_state.step = 4
        st.rerun()

elif st.session_state.step == 4:
    st.title("📊 Étape 4 : Résultats de la simulation")

    import time
    from classes.avions import Commercial, Militaire, ChoixAvion
    from redirection_aeroport import *
    from classes.meteos import Meteo
    from classes.avions.fonction_avion import charger_donnees_avions
    from affichages_graphiques import afficher_trajectoire_atterrissage, afficher_freinage
    # Récupération des variables de session
    poids = st.session_state.poids
    meteo = st.session_state.meteo
    piste = st.session_state.piste
    type_avion = st.session_state.type_avion
    avion_code = st.session_state.avion_code

    # Choix de l'avion (objet)
    if avion_code == "Autre (personnalisé)":
        choix_avion_obj = ChoixAvion('CUSTOM', custom_data=st.session_state.custom_avion_data)
    else:
        choix_avion_obj = ChoixAvion(avion_code)

    # Création de l'objet avion
    if type_avion == "Commercial":
        avion = Commercial(poids, choix_avion_obj, meteo, piste)
    else:
        avion = Militaire(poids, choix_avion_obj, meteo, piste)

    # Calcul et logs
    piste_finale, logs = compare(avion, piste)

    # Affichage ligne par ligne
    st.subheader("Vérification et recherche de pistes :")
    for log_type, message in logs:
        if log_type == "error":
            st.error(message)
        elif log_type == "success":
            st.success(message)
        elif log_type == "info":
            st.info(message)
        else:
            st.write(message)
        time.sleep(1)

    # Direction du vent
    dir_vent = recuperer_meteo(piste_finale.latitude(), piste_finale.longitude())["Dir_vent"]

    st.write("---")
    st.subheader(f"🛬 Résultats pour l'avion : `{avion.code}`")

    if dir_vent in range(0, 180):
        st.info(f"💨 Le vent vient de l'Est ({dir_vent}°)\n\n➡️ Atterrissage recommandé sur la piste **{piste_finale.orientation()[0]}**")
    elif dir_vent in range(181, 360):
        st.info(f"💨 Le vent vient de l'Ouest ({dir_vent}°)\n\n➡️ Atterrissage recommandé sur la piste **{piste_finale.orientation()[1]}**")
    else:
        st.warning("⚠️ Direction du vent non déterminée")

    # Résultats de calculs
    st.markdown("### 📐 Détails des distances calculées (en pieds)")
    st.metric("Vitesse de décrochage", f"{avion.calcul_V_stall():.2f} ft/s")
    st.metric("Distance d'approche (S_A)", f"{avion.calcul_S_A():.2f} ft")
    st.metric("Distance de transition (S_TR)", f"{avion.calcul_S_TR():.2f} ft")
    st.metric("Distance de roulement libre (S_FR)", f"{avion.calcul_S_FR():.2f} ft")
    st.metric("Distance de freinage (S_B)", f"{avion.calcul_S_B():.2f} ft")
    st.success(f"✈️ **Distance totale d'atterrissage**: {avion.calcul_S_LA():.2f} ft")

    st.write("---")
    st.markdown("### 📊 Visualisations")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("📈 Afficher la trajectoire d’atterrissage"):
            afficher_trajectoire_atterrissage(avion)

    with col2:
        if st.button("📉 Afficher le profil de freinage"):
            afficher_freinage(avion)
