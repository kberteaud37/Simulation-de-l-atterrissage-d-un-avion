import pandas as pd
from classes.avions.fonction_avion import charger_donnees_avions


class ChoixAvion:
    """Classe adaptée pour gérer les unités converties"""

    def __init__(self, code_avion,  custom_data=None):
        self.code = code_avion
        self._donnees_avions = None  # Cache pour les données des avions
        self._custom_data = custom_data  # Stocke les données personnalisées

    def _importation_donnees(self):
        if self.code == "CUSTOM" and self._custom_data is not None:
            return self._custom_data
        """Charge les données des avions une seule fois et les met en cache"""
        if self._donnees_avions is None:
            self._donnees_avions = charger_donnees_avions()
        return self._donnees_avions

    def _get_avion_data(self):
        """Récupère les données de l'avion spécifique"""
        if self.code == "CUSTOM" and self._custom_data is not None:
            return self._custom_data

        if self._donnees_avions is None:
            self._donnees_avions = charger_donnees_avions()

        # Correction pour éviter le KeyError
        try:
            avion_data = self._donnees_avions[self._donnees_avions['Code'] == self.code]
            if not avion_data.empty:
                return avion_data.iloc[0]
        except Exception as e:
            print(f"Erreur lors de la récupération des données: {e}")

        raise ValueError(f"Avion {self.code} non trouvé dans la base de données")

    def hauteur(self, en_pieds=True):
        avion = self._get_avion_data()
        if en_pieds:
            return float(avion['Hauteur_aile_ft'])  # Utilise directement la valeur convertie
        return float(avion['Hauteur_aile_m'])

    def surface(self, en_pieds_carres=True):
        avion = self._get_avion_data()
        if en_pieds_carres:
            return float(avion['Surface_alaire_ft2'])  # Utilise directement la valeur convertie
        return float(avion['Surface_alaire_m2'])

    def allongement(self):
        avion = self._get_avion_data()
        return float(avion['Allongement']) if avion is not None else None

    def portance(self):
        avion = self._get_avion_data()
        return float(avion['CL_max_atterrissage']) if avion is not None else None

    def trainee_train(self):
        avion = self._get_avion_data()
        return float(avion['Cd_train']) if avion is not None else None

    def trainee_volets(self):
        avion = self._get_avion_data()
        return float(avion['Cd_volets']) if avion is not None else None

    def type_avion(self):
        """Retourne le type d'avion (Commercial/Militaire)"""
        avion = self._get_avion_data()
        try:
            # Essayer de récupérer le type directement
            return avion['Type']
        except KeyError:
            # Fallback si la colonne Type n'existe pas
            militaires = ['F-', 'AH-', 'B-', 'Rafale', 'Eurofighter', 'Su-', 'Mirage']
            if any(mil in self.code for mil in militaires):
                return 'Militaire'
            return 'Commercial'




