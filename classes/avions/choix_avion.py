import pandas as pd
from .fonction_avion import charger_donnees_avions


class ChoixAvion:
    """Classe adaptée pour gérer les unités converties"""

    def __init__(self, code_avion):
        self.code = code_avion
        self._donnees_avions = None  # Cache pour les données des avions

    def _importation_donnees(self):
        """Charge les données des avions une seule fois et les met en cache"""
        if self._donnees_avions is None:
            self._donnees_avions = charger_donnees_avions()
        return self._donnees_avions

    def _get_avion_data(self):
        """Récupère les données de l'avion spécifique"""
        donnees = self._importation_donnees()
        avion_data = donnees[donnees['Code'] == self.code]
        return avion_data.iloc[0] if not avion_data.empty else None

    def hauteur(self, en_pieds=True):
        avion = self._get_avion_data()
        if avion is None:
            return None
        return avion['Hauteur_aile_ft'] if en_pieds else avion.get('Hauteur_aile_m')

    def surface(self, en_pieds_carres=True):
        avion = self._get_avion_data()
        if avion is None:
            return None
        return avion['Surface_alaire_ft2'] if en_pieds_carres else avion.get('Surface_alaire_m2')

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


"""# Exemple d'utilisation
a320 = ChoixAvion("A320")
print(f"Surface alaire: {a320.surface()} ft²")  # Par défaut en pieds carrés
print(f"Surface alaire: {a320.surface(en_pieds_carres=False)} m²")  # En mètres carrés
print(f"Coeff de traînée: {a320.trainee_train()}")"""