import pandas as pd
import fonction_avion as charger_donnees_avions

class Choix_Avion:
    """Classe simple pour récupérer les paramètres d'un avion"""


    def __init__(self, code_avion):
        """Initialise avec le code de l'avion"""
        self.code = code_avion
        # Trouve l'avion correspondant
        self.avion = self.donnees[self.donnees['Code'] == self.code].iloc[0] if not self.donnees[
            self.donnees['Code'] == self.code].empty else None

    # Méthodes pour chaque paramètre
    def allongement(self, donnees):
        return self.avion['Allongement'] if self.avion is not None else None

    def hauteur(self, donnees):
        return self.avion['Hauteur_aile_m'] if self.avion is not None else None

    def surface(self, donnees):
        return self.avion['Surface_alaire_m2'] if self.avion is not None else None

    def portance(self, donnees):
        return self.avion['CL_max_atterrissage'] if self.avion is not None else None

    def trainee_train(self, donnees):
        return self.avion['Cd_train'] if self.avion is not None else None

    def trainee_volets(self, donnees):
        return self.avion['Cd_volets'] if self.avion is not None else None



a320 = ChoixAvion("A320")

print(f"Coefficient de traînée du train (A320): {a320.trainee_train()}")


b747 = ChoixAvion("B747-400")
print(f"Surface alaire du B747: {b747.surface()} m²")

avion = ChoixAvion("A320")

cd_train = avion.trainee_train()
surface = avion.surface()

print(cd_train)
print(surface)