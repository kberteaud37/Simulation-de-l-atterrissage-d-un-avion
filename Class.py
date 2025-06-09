#class aéroport

class Aeroport:
    def __init__(self, nom, code, ville, pays, coordonnees, altitude):
        self.nom = nom
        self.code = code
        self.ville = ville
        self.pays = pays
        self.coordonnees = coordonnees  # Tuple (latitude, longitude)
        self.altitude = altitude  # en mètres

    def afficher_infos(self):
        print(f"Aéroport: {self.nom} ({self.code})")
        print(f"Localisation: {self.ville}, {self.pays}")
        print(f"Coordonnées: {self.coordonnees[0]}°N, {self.coordonnees[1]}°E")
        print(f"Altitude: {self.altitude} mètres")


# Création d'un aéroport
cdg = Aeroport(
    nom="Charles de Gaulle",
    code="CDG",
    ville="Paris",
    pays="France",
    coordonnees=(49.0128, 2.5500),
    altitude=119
)


# Affichage complet
cdg.afficher_infos()