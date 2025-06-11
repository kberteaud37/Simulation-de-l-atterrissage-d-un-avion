import pandas as pd
import fonction_avion as charger_donnees_avions


class ChoixAvion:
    """Classe pour accéder aux paramètres d'un avion à partir d'un DataFrame global"""

    def __init__(self, code_avion):
        """Initialise avec le code de l'avion"""
        self.code = code_avion

    def _get_avion_data(self, donnees):
        """Filtre le DataFrame pour l'avion courant"""
        if not isinstance(donnees, pd.DataFrame):
            raise ValueError("Le paramètre 'donnees' doit être un DataFrame pandas")

        avion_data = donnees[donnees['Code'] == self.code]
        return avion_data.iloc[0] if not avion_data.empty else None

    # Méthodes pour chaque paramètre
    def allongement(self, donnees):
        avion = self._get_avion_data(donnees)
        return avion['Allongement'] if avion is not None else None

    def hauteur(self, donnees):
        avion = self._get_avion_data(donnees)
        return avion['Hauteur_aile_m'] if avion is not None else None

    def surface(self, donnees):
        avion = self._get_avion_data(donnees)
        return avion['Surface_alaire_m2'] if avion is not None else None

    def portance(self, donnees):
        avion = self._get_avion_data(donnees)
        return avion['CL_max_atterrissage'] if avion is not None else None

    def trainee_train(self, donnees):
        avion = self._get_avion_data(donnees)
        return avion['Cd_train'] if avion is not None else None

    def trainee_volets(self, donnees):
        avion = self._get_avion_data(donnees)
        return avion['Cd_volets'] if avion is not None else None