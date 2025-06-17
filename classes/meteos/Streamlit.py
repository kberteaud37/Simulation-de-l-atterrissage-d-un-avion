import streamlit as st
import classes
from classes.aeroports.fonctions_aeroport import recuperer_runways, recuperer_airports

st.set_page_config(page_title="Sélecteur d'Aéroport", layout="centered")

st.title("🛬 Sélection d'un aéroport et d'une piste")

# Récupération des données
runways_df = recuperer_runways()
airports_df = recuperer_airports()

# Liste des codes aéroports disponibles
airport_codes = airports_df["ident"].tolist()

# Sélection d'un aéroport (filtrable)
code_aeroport = st.selectbox("Choisissez un aéroport (code ICAO)", options=airport_codes)

if code_aeroport:
    # Création de l'objet aéroport
    aeroport = classes.aeroports.Aeroport(code_aeroport, runways_df)

    # Affichage des infos aéroport
    st.subheader("🛫 Informations sur l'aéroport sélectionné")
    aeroport_info = aeroport.afficher_infos()  # Cette méthode affiche dans la console

    # Si la méthode afficher_infos() imprime juste au lieu de retourner une string, on la redirige :
    import io
    import sys
    buffer = io.StringIO()
    sys.stdout = buffer
    aeroport.afficher_infos()
    sys.stdout = sys.__stdout__
    infos_texte = buffer.getvalue()
    st.text(infos_texte)

    # Pistes disponibles pour cet aéroport
    pistes_dispo = runways_df[runways_df["ident"] == code_aeroport]["runway_ident"].unique()
    piste_choisie = st.selectbox("Choisissez une piste", options=pistes_dispo)

    if piste_choisie:
        st.success(f"Piste sélectionnée : {piste_choisie}")