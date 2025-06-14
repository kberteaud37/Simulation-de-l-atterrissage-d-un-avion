from .aeroport import Aeroport
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

    def orientation_1(self):
        row= self.runway[(self.runway["ident"] == self.code) &
                          (self.runway["runway_ident"] == self.n_piste)]
        alphabet_min = string.ascii_lowercase
        if not row.empty:
            num_piste = row.iloc[0]["le_ident"]
            orientation_1=""
            for lettre in num_piste.lower():
                if lettre not in alphabet_min:
                    orientation_1 += lettre
            return int(orientation_1)*10
        else:
            print("Aéroport non trouvé")

    def orientation_2(self):
        row= self.runway[(self.runway["ident"] == self.code) &
                          (self.runway["runway_ident"] == self.n_piste)]
        alphabet_min = string.ascii_lowercase
        if not row.empty:
            num_piste = row.iloc[0]["he_ident"]
            orientation_2=""
            for lettre in num_piste.lower():
                if lettre not in alphabet_min:
                    orientation_2 += lettre
            return int(orientation_2)*10
        else:
            print("Aéroport non trouvé")

    def afficher_infos_piste(self,pluie,glace):
        print(f"\nCaracteristiques de la piste {self.n_piste}:")
        print(f"Matériau de la piste: {self.surface()}, f={self.coeff_friction(pluie,glace)}")
        print(f"Longueur: {self.longueur()}m")
        print(f"Largeur: {self.largeur()}m")

