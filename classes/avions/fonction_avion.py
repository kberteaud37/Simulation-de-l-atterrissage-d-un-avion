import pandas as pd


def charger_donnees_avions():
    """Charge les données avions depuis le CSV et retourne un dictionnaire"""
    chemin_fichier = r'.\Ressources\data_avions.csv'

    try:
        # Lecture du fichier
        df = pd.read_csv(chemin_fichier, sep=';')

        # Conversion en dictionnaire
        donnees = {}
        for _, row in df.iterrows():
            code = row['Code']
            donnees[code] = {
                'Allongement': row['Allongement'],
                'Hauteur': row['Hauteur_aile_ft'],
                'Surface': row['Surface_alaire_ft2'],
                'Portance_max': row['CL_max_atterrissage'],
                'Cd_train': row['Cd_train'],
                'Cd_volets': row['Cd_volets']
            }
        return donnees

    except FileNotFoundError:
        print(f"Erreur: Fichier introuvable à l'emplacement {chemin_fichier}")
        return None
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier: {e}")
        return None
