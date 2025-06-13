from .aeroport import Aeroport
# Class Piste

class Piste(Aeroport):
    asphalte=["concrete","asphalt/gravel","ASP","asphalt","ASPHALT","ASPH"]
    gravier=["Gravel","gravel","GRAVEL","GRAVEL/TURF","GVL","SAND/GRAVEL","GRAVEL/GRASS"]
    gazon=["grass","GRS","GRASS","EARTH/SNOW","GRASS/SAND"]
    def __init__(self,code,runways_df,num_piste_le,num_piste_he):

        # Appel du constructeur parent
        super().__init__(code,runways_df)
        self.n_le_piste=num_piste_le
        self.n_he_piste=num_piste_he

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
                         (self.runway["le_ident"] == self.n_le_piste) &
                         (self.runway["he_ident"] == self.n_he_piste)]
        if not row.empty:
            longueur = row.iloc[0]["length_ft"]
            return float(longueur)
        else:
            print("Aéroport non trouvé")

    def largeur(self):
        row = self.runway[(self.runway["ident"] == self.code)&
                         (self.runway["le_ident"] == self.n_le_piste) &
                         (self.runway["he_ident"] == self.n_he_piste)]
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

    def coeff_friction(self):
        if self.surface()=='Asphalte':
            return 0.5
        elif self.surface()=='Gravier':
            return 0.3
        elif self.surface()=='Gazon':
            return 0.4
        else:
            return 0.3

    def afficher_infos_piste(self,numero_piste):
        print(f"\nCaracteristiques de la piste {numero_piste}:")
        print(f"Matériau de la piste: {self.surface()}, f={self.coeff_friction()}")
        print(f"Longueur: {self.longueur()}m")
        print(f"Largeur: {self.largeur()}m")



