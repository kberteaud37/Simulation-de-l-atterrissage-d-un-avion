from .aeroport import Aeroport

# Class Piste

class Piste(Aeroport):
    def __init__(self, nom, code, ville, coordonnees, altitude,
                 numero_piste, surface, largeur, longueur, orientation):

        # Appel du constructeur parent
        super().__init__(nom, code, ville, coordonnees, altitude)

        self.numero_piste = numero_piste
        self.surface = surface.lower()  # Normalisation en minuscules
        self.largeur = largeur  # en mètres
        self.longueur = longueur  # en mètres
        self.orientation = orientation  # en degrés

        # Dictionnaire des coefficients de friction
        self.coef_friction = {
            'asphalte': 0.5,
            'asphalte mouillee': 0.3,
            'asphalte glacee': 0.10,
            'gazon solide': 0.4,
            'poussiere solide': 0.3,
            'gazon mou': 0.2,
            'gazon mouille': 0.2,
        }

    def ajout_coefficient_friction(self):
        return self.coef_friction.get(self.surface, 0.5)

    def afficher_infos_piste(self):
        print(f"\nInformations de la piste {self.numero_piste}:")
        print(f"Surface: {self.surface.capitalize()} (Coeff. friction: {self.ajout_coefficient_friction()})")
        print(f"Dimensions: {self.longueur}m x {self.largeur}m")
        print(f"Orientation: {self.orientation}°")
        print(f"Localisation: {self.nom} ({self.code}), {self.ville}")


piste1 = Piste(
    nom="Charles de Gaulle",
    code="CDG",
    ville="Paris",
    coordonnees=(49.0128, 2.5500),
    altitude=119,
    numero_piste="09L/27R",
    surface="asphalte",
    largeur=45,
    longueur=2700,
    orientation=90
)



piste1.afficher_infos_piste()