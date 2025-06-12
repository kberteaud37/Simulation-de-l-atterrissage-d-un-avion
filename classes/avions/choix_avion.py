import pandas as pd
import fonction_avion as charger_donnees_avions


class ChoixAvion:
    """Classe pour accéder aux paramètres d'un avion à partir d'un DataFrame global"""

    def __init__(self, code_avion):
        """Initialise avec le code de l'avion"""
        self.code = code_avion

    def avion_data(self, donnees):
        avion_data = donnees[donnees['Code'] == self.code]
        cod= avion_data.iloc[0]['Code'] if not avion_data.empty else None

    # Méthodes pour chaque paramètre
    def allongement(self, donnees):
        avion_data = donnees[donnees['Code'] == self.code]
        allongement = avion_data.iloc[0]['Allongement'] if avion_data.empty is not None else None
        return float(allongement)

    def hauteur(self, donnees):
        avion_data = donnees[donnees['Code'] == self.code]
        hauteur = avion_data.iloc[0]['Hauteur_aile_m'] if avion_data.empty is not None else None
        return float(hauteur)

    def surface(self, donnees):
        avion_data = donnees[donnees['Code'] == self.code]
        surface = avion_data.iloc[0]['Surface_alaire_m2'] if avion_data.empty is not None else None
        return float(surface)

    def portance(self, donnees):
        avion_data = donnees[donnees['Code'] == self.code]
        portance = avion_data.iloc[0]['CL_max_atterrissage'] if avion_data.empty is not None else None
        return float(portance)

    def trainee_train(self, donnees):
        avion_data = donnees[donnees['Code'] == self.code]
        trainee_train = avion_data.iloc[0]['Cd_train'] if avion_data.empty is not None else None
        return float(trainee_train)

    def trainee_volets(self, donnees):
        avion_data = donnees[donnees['Code'] == self.code]
        trainee_volets = avion_data.iloc[0]['Cd_volets'] if avion_data.empty is not None else None
        return float(trainee_volets)


avion = ChoixAvion.trainee_volets()