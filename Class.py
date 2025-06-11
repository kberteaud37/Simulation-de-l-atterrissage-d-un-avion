from math import sqrt, cos, sin, tan, radians


class Avion:
    angle_de_descente = -3 #Degrés
    g = 32.2 #ft/s²
    temps_roue_libre = 3 #Secondes

    def __init__(self,code, poids_atterrissage, surface_alaire,
                 coefficient_portance_max_atterrissage,meteo,piste):
        self.code = code
        self.W_LA = poids_atterrissage
        self.S = surface_alaire
        self.Cl_max_LA = coefficient_portance_max_atterrissage
        self.charge_alaire = self.W_LA/self.S
        self.piste = piste
        self.mu = self.piste.ajout_coefficient_friction()
        self.meteo = meteo
        self.density = self.meteo.density()
        # Poussée au sol pour l'instant nulle
        self.T_sol = 0

    def calcul_V_stall(self):
        return sqrt(self.W_LA / (0.5 * self.density * self.S * self.Cl_max_LA))

    def calcul_V_TD(self):
        V_stall = self.calcul_V_stall()
        return 1.15*V_stall

    def calcul_S_FR(self):
        V_TD = self.calcul_V_TD()
        return self.temps_roue_libre * V_TD

    def calcul_f1(self):
        return (self.T_sol/self.mu)+self.mu

class Commercial(Avion):

    def __init__(self,code, poids_atterrissage, surface_alaire,
                 coefficient_portance_max_atterrissage,meteo,piste,
                 facteur_de_charge = 1.35,hauteur_obstacle = 35,
                 coef_transition = 1.23):
        super().__init__(code, poids_atterrissage, surface_alaire,
                 coefficient_portance_max_atterrissage,meteo,piste)
        self.n = facteur_de_charge
        self.H_OBS = hauteur_obstacle
        self.coef_TR = coef_transition

    def calcul_V_TR(self):
        V_stall = self.calcul_V_stall()
        return self.coef_TR * V_stall

    def calcul_R(self):
        V_TR = self.calcul_V_TR()
        return (V_TR**2)/(self.g*(self.n-1))

    def calcul_H_TR(self):
        R = self.calcul_R()
        return R*(1-cos(radians(self.angle_de_descente)))

    def calcul_S_A(self):
        H_TR = self.calcul_H_TR()
        return (H_TR-self.H_OBS)/tan(radians(self.angle_de_descente))

    def calcul_S_TR(self):
        R = self.calcul_R()
        return -R*sin(radians(self.angle_de_descente))



class Militaire(Avion):

    def __init__(self, code, poids_atterrissage, surface_alaire,
                 coefficient_portance_max_atterrissage, meteo, piste,
                 facteur_de_charge = 2,hauteur_obstacle = 50,
                 coef_transition = 1.15):
        super().__init__(code, poids_atterrissage, surface_alaire,
                         coefficient_portance_max_atterrissage, meteo, piste)
        self.n = facteur_de_charge
        self.H_OBS = hauteur_obstacle
        self.coef_TR = coef_transition

    def calcul_V_TR(self):
        V_stall = self.calcul_V_stall()
        return self.coef_TR * V_stall

    def calcul_R(self):
        V_TR = self.calcul_V_TR()
        return (V_TR ** 2) / (self.g * (self.n - 1))

    def calcul_H_TR(self):
        R = self.calcul_R()
        return R * (1 - cos(radians(self.angle_de_descente)))

    def calcul_S_A(self):
        H_TR = self.calcul_H_TR()
        return (H_TR - self.H_OBS) / tan(radians(self.angle_de_descente))

    def calcul_S_TR(self):
        R = self.calcul_R()
        return -R * sin(radians(self.angle_de_descente))


# Class aéroport

class Aeroport:
    def __init__(self, nom, code, ville, coordonnees, altitude):
        self.nom = nom
        self.code = code
        self.ville = ville
        self.coordonnees = coordonnees  # Tuple (latitude, longitude)
        self.altitude = altitude  # en mètres

    def afficher_infos(self):
        print(f"Aéroport: {self.nom} ({self.code})")
        print(f"Localisation: {self.ville}")
        print(f"Coordonnées: {self.coordonnees[0]}°N, {self.coordonnees[1]}°E")
        print(f"Altitude: {self.altitude} mètres")



cdg = Aeroport(
    nom="Charles de Gaulle",
    code="CDG",
    ville="Paris",
    coordonnees=(49.0128, 2.5500),
    altitude=119
)


cdg.afficher_infos()

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