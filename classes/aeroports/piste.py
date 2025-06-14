from aeroport import Aeroport
from fonctions_aeroport import *
import string

# Class Piste

class Piste(Aeroport):
    asphalte=["concrete","asphalt/gravel","ASP","asphalt","ASPHALT","ASPH"]
    gravier=["Gravel","gravel","GRAVEL","GRAVEL/TURF","GVL","SAND/GRAVEL","GRAVEL/GRASS"]
    gazon=["grass","GRS","GRASS","EARTH/SNOW","GRASS/SAND"]
    def __init__(self,code,runways_df,num_piste):

        # Appel du constructeur parent
        super().__init__(code,runways_df)
        self.n_piste=num_piste

        # Dictionnaire des coefficients de friction
        """
        self.coef_friction = {
            'asphalte': 0.5,
            'asphalte mouillee': 0.3,
            'asphalte glacee': 0.10,
            'gazon solide': 0.4,
            'poussiere solide': 0.3,
            'gazon mouille': 0.2,
        }
        """
    def longueur(self):
        row = self.runway[(self.runway["ident"] == self.code) &
                         (self.runway["runway_ident"] == self.n_piste)]
        if not row.empty:
            longueur = row.iloc[0]["length_ft"]
            return float(longueur)
        else:
            print("Aéroport non trouvé")

    def largeur(self):
        row = self.runway[(self.runway["ident"] == self.code) &
                          (self.runway["runway_ident"] == self.n_piste)]
        if not row.empty:
            largeur = row.iloc[0]["width_ft"]
            return float(largeur)
        else:
            print("Aéroport non trouvé")

    def surface(self):
        row = self.runway[(self.runway["ident"] == self.code)]
        if not row.empty:
            surface = row.iloc[0]["surface"]
            if surface in self.asphalte:
                return 'Asphalte'
            elif surface in self.gravier:
                return 'Gravier'
            elif surface in self.gazon:
                return 'Gazon'
            else:
                return 'Inconnue'
        else:
            print("Aéroport non trouvé")

    def coeff_friction(self,pluie,glace):
        if self.surface()=='Asphalte':
            if glace is True:
                return 0.1
            elif pluie is True:
                return 0.3
            else:
                return 0.5
        elif self.surface()=='Gravier':
            return 0.3
        elif self.surface()=='Gazon':
            if pluie is True:
                return 0.2
            else:
                return 0.4
        else:
            if glace is True:
                return 0.1
            else:
                return 0.3

    def orientation(self):
        alphabet_min = string.ascii_lowercase + "-"
        orientation_piste = ""
        for lettre in self.n_piste.lower():
            if lettre not in alphabet_min:
                orientation_piste += lettre
            elif lettre == "-":
                orientation_piste += ","
        orientation_str = orientation_piste.split(",")
        orientation = []
        for num in orientation_str:
            orientation.append(int(num) * 10)
        return orientation
    def afficher_infos_piste(self,pluie,glace):
        print(f"\nCaracteristiques de la piste {self.n_piste}:")
        print(f"Matériau de la piste: {self.surface()}, f={self.coeff_friction(pluie,glace)}")
        print(f"Longueur: {self.longueur()}m")
        print(f"Largeur: {self.largeur()}m")
