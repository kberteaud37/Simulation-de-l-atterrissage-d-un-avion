from .aeroport import Aeroport

# Class Piste

class Piste(Aeroport):
    def __init__(self,code,num_piste):

        # Appel du constructeur parent
        super().__init__(code)
        self.n_piste=num_piste

        # Dictionnaire des coefficients de friction
        """
        self.coef_friction = {
            'asphalte': 0.5,
            'asphalte mouillee': 0.3,
            'asphalte glacee': 0.10,
            'gazon solide': 0.4,
            'poussiere solide': 0.3,
            'gazon mou': 0.2,
            'gazon mouille': 0.2,
        }
        """
    def longueur(self, runways_df):
        row = runways_df[runways_df["ident"] == self.code]
        if not row.empty:
            longueur = row.iloc[0]["length_ft"]
            return float(longueur)
        else:
            print("Aéroport non trouvé")

    def largeur(self, runways_df):
        row = runways_df[runways_df["ident"] == self.code]
        if not row.empty:
            largeur = row.iloc[0]["width_ft"]
            return float(largeur)
        else:
            print("Aéroport non trouvé")

    def surface(self, runways_df):
        row = runways_df[runways_df["ident"] == self.code]
        if not row.empty:
            longueur = row.iloc[0]["length_ft"]
            largeur = row.iloc[0]["width_ft"]
            surface = row.iloc[0]["surface"]
            return (float(longueur), float(largeur), str(surface))
        else:
            print("Aéroport non trouvé")

    def ajout_coefficient_friction(self):
        return self.coef_friction.get(self.surface, 0.5)

    def afficher_infos_piste(self):
        print(f"\nInformations de la piste {self.numero_piste}:")
        print(f"Surface: {self.surface.capitalize()} (Coeff. friction: {self.ajout_coefficient_friction()})")
        print(f"Dimensions: {self.longueur}m x {self.largeur}m")
        print(f"Orientation: {self.orientation}°")
        print(f"Localisation: {self.nom} ({self.code}), {self.ville}")


