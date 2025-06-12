import pandas as pd


def charger_donnees_avions(convertir_en_pieds=True):
    """Charge et nettoie rigoureusement les données avions"""
    chemin_fichier = r'.\Ressources\data_avions.csv'

    try:
        # Coefficients de conversion
        PIEDS_PAR_METRE = 3.28084
        PIEDS_CARRE_PAR_METRE_CARRE = 10.7639

        # 1. Chargement des données
        df = pd.read_csv(chemin_fichier, sep=';', encoding='utf-8')

        # 2. Nettoyage approfondi
        # a. Suppression des doublons
        df = df.drop_duplicates(subset=['Code'], keep='first')

        # b. Filtrage des données problématiques
        df = df[df['Code'].notna()]  # Enlève les lignes sans code avion

        # c. Conversion des types
        df = df.convert_dtypes()  # Conversion automatique aux types optimaux

        # 3. Gestion des unités
        if convertir_en_pieds:
            # Conversion et création des nouvelles colonnes
            df['Hauteur_aile_ft'] = df['Hauteur_aile_m'] * PIEDS_PAR_METRE
            df['Surface_alaire_ft2'] = df['Surface_alaire_m2'] * PIEDS_CARRE_PAR_METRE_CARRE

            # Formatage des valeurs converties
            df['Hauteur_aile_ft'] = df['Hauteur_aile_ft'].round(2)  # 2 décimales
            df['Surface_alaire_ft2'] = df['Surface_alaire_ft2'].round(1)  # 1 décimale

            # Colonnes finales (version avec gestion propre des unités)
            colonnes_finales = [
                'Code', 'Allongement',
                'Hauteur_aile_m', 'Hauteur_aile_ft',
                'Surface_alaire_m2', 'Surface_alaire_ft2',
                'CL_max_atterrissage', 'Cd_train', 'Cd_volets'
            ]
        else:
            colonnes_finales = [
                'Code', 'Allongement', 'Hauteur_aile_m',
                'Surface_alaire_m2', 'CL_max_atterrissage',
                'Cd_train', 'Cd_volets'
            ]

        # 4. Sélection et ordre des colonnes
        df_clean = df[colonnes_finales]

        # 5. Vérification finale
        if df_clean.empty:
            raise ValueError("Aucune donnée valide après nettoyage")

        return df_clean

    except Exception as e:
        print(f"Erreur lors du nettoyage: {e}")
        return pd.DataFrame()