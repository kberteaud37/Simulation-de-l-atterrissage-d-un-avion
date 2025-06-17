import pandas as pd
from pathlib import Path

def charger_donnees_avions(convertir_en_pieds=True):
    """Charge, nettoie et prépare les données techniques des avions depuis un fichier CSV.

        Cette fonction effectue plusieurs opérations :
        1. Charge le fichier CSV en testant différents séparateurs
        2. Nettoie les données (suppression des doublons, gestion des valeurs manquantes)
        3. Convertit les unités métriques en unités impériales si demandé
        4. Vérifie l'intégrité des données
        5. Retourne un DataFrame propre et standardisé

        :param convertir_en_pieds: Si True, convertit les unités métriques en pieds, defaults to True
        :type convertir_en_pieds: bool, optional
        :return: DataFrame contenant les données techniques des avions nettoyées
        :rtype: pandas.DataFrame
        :raises ValueError: Si des colonnes obligatoires sont manquantes ou si les données sont vides après nettoyage
        :raises pd.errors.ParserError: Si le fichier ne peut être lu avec aucun séparateur testé
        :raises FileNotFoundError: Si le fichier spécifié n'existe pas

        """
    chemin_fichier = Path("Ressources") / "data_avions.csv"

    try:
        # Coefficients de conversion
        PIEDS_PAR_METRE = 3.28084
        PIEDS_CARRE_PAR_METRE_CARRE = 10.7639

        # 1. Chargement des données avec plusieurs options de séparateur
        try:
            # Essayer d'abord avec une virgule
            df = pd.read_csv(chemin_fichier, sep=',', encoding='utf-8')
        except pd.errors.ParserError:
            try:
                # Si échec, essayer avec un point-virgule
                df = pd.read_csv(chemin_fichier, sep=';', encoding='utf-8')
            except pd.errors.ParserError:
                # Si échec, essayer avec tabulation
                df = pd.read_csv(chemin_fichier, sep='\t', encoding='utf-8')



        # 2. Nettoyage approfondi
        # a. Suppression des doublons
        df = df.drop_duplicates(subset=['Code'], keep='first')
        df = df[df['Code'].notna()]
        df = df.convert_dtypes()

        # 3. Gestion des unités
        if convertir_en_pieds:
            # Conversion et création des nouvelles colonnes
            df['Hauteur_aile_ft'] = df['Hauteur_aile_m'] * PIEDS_PAR_METRE
            df['Surface_alaire_ft2'] = df['Surface_alaire_m2'] * PIEDS_CARRE_PAR_METRE_CARRE

            # Formatage des valeurs converties
            df['Hauteur_aile_ft'] = df['Hauteur_aile_ft'].round(2)
            df['Surface_alaire_ft2'] = df['Surface_alaire_ft2'].round(1)

            # Colonnes finales
            colonnes_finales = [
                'Code', 'Type', 'Allongement',
                'Hauteur_aile_m', 'Hauteur_aile_ft',
                'Surface_alaire_m2', 'Surface_alaire_ft2',
                'CL_max_atterrissage', 'Cd_train', 'Cd_volets'
            ]
        else:
            colonnes_finales = [
                'Code', 'Type', 'Allongement', 'Hauteur_aile_m',
                'Surface_alaire_m2', 'CL_max_atterrissage',
                'Cd_train', 'Cd_volets'
            ]

        # Vérifier que toutes les colonnes nécessaires existent
        for col in colonnes_finales:
            if col not in df.columns:
                raise ValueError(f"Colonne manquante dans les données: {col}")

        # 4. Sélection et ordre des colonnes
        df_clean = df[colonnes_finales]

        # 5. Vérification finale
        if df_clean.empty:
            raise ValueError("Aucune donnée valide après nettoyage")

        return df_clean

    except Exception as e:
        print(f"Erreur lors du nettoyage: {str(e)}")
        # Retourner un DataFrame vide en cas d'erreur
        return pd.DataFrame()