import pandas as pd
from fonction_avion import charger_donnees_avions


class Choix_Avion:
    """Classe adaptée pour gérer les unités converties"""

    def __init__(self, code_avion):
        self.code = code_avion

    def _get_avion_data(self, donnees):
        avion_data = donnees[donnees['Code'] == self.code]
        return avion_data.iloc[0] if not avion_data.empty else None

    def hauteur(self, donnees, en_pieds=True):
        avion = self._get_avion_data(donnees)
        if avion is None:
            return None
        return avion['Hauteur_aile_ft'] if en_pieds else avion.get('Hauteur_aile_m')

    def surface(self, donnees, en_pieds_carres=True):
        avion = self._get_avion_data(donnees)
        if avion is None:
            return None
        return avion['Surface_alaire_ft2'] if en_pieds_carres else avion.get('Surface_alaire_m2')

    def allongement(self, donnees):
        avion = self._get_avion_data(donnees)
        return float(avion['Allongement']) if avion is not None else None

    def portance(self, donnees):
        avion = self._get_avion_data(donnees)
        return float(avion['CL_max_atterrissage']) if avion is not None else None

    def trainee_train(self, donnees):
        avion = self._get_avion_data(donnees)
        return float(avion['Cd_train']) if avion is not None else None

    def trainee_volets(self, donnees):
        avion = self._get_avion_data(donnees)
        return float(avion['Cd_volets']) if avion is not None else None

donnees_avions = charger_donnees_avions()
a320 = Choix_Avion("A320")
print(f"Surface alaire: {a320.surface(donnees_avions)} ft²")
print(f"Coeff de traînée: {a320.trainee_train(donnees_avions)}")