"""Module contenant la classe Piste pour la simulation d'atterrissage."""

from .aeroport import Aeroport
import string


class Piste(Aeroport):
    """Classe représentant une piste d'atterrissage, héritant de Aeroport.

    :param code: Code OACI de l'aéroport
    :type code: str
    :param runways_df: DataFrame contenant les informations sur les pistes
    :type runways_df: pandas.DataFrame
    :param num_piste: Identifiant de la piste (ex: "08-26")
    :type num_piste: str
    """

    # Types de surfaces
    asphalte = ["concrete", "asphalt/gravel", "ASP", "asphalt", "ASPHALT", "ASPH"]
    gravier = ["Gravel", "gravel", "GRAVEL", "GRAVEL/TURF", "GVL", "SAND/GRAVEL", "GRAVEL/GRASS"]
    gazon = ["grass", "GRS", "GRASS", "EARTH/SNOW", "GRASS/SAND"]

    def __init__(self, code, runways_df, num_piste):
        """Initialise un objet Piste avec son aéroport parent et son numéro."""
        super().__init__(code, runways_df)
        self.n_piste = num_piste

    def longueur(self):
        """Retourne la longueur de la piste en pieds.

        :return: Longueur de la piste en pieds
        :rtype: float
        :raises: Affiche un message si la piste n'est pas trouvée
        """
        row = self.runway[(self.runway["ident"] == self.code) &
                          (self.runway["runway_ident"] == self.n_piste)]
        if not row.empty:
            longueur = row.iloc[0]["length_ft"]
            return float(longueur)
        else:
            print("Aéroport non trouvé")

    def largeur(self):
        """Retourne la largeur de la piste en pieds.

        :return: Largeur de la piste en pieds
        :rtype: float
        :raises: Affiche un message si la piste n'est pas trouvée
        """
        row = self.runway[(self.runway["ident"] == self.code) &
                          (self.runway["runway_ident"] == self.n_piste)]
        if not row.empty:
            largeur = row.iloc[0]["width_ft"]
            return float(largeur)
        else:
            print("Aéroport non trouvé")

    def surface(self):
        """Détermine le type de surface de la piste.

        :return: Type de surface (Asphalte, Gravier, Gazon ou Inconnue)
        :rtype: str
        :raises: Affiche un message si la piste n'est pas trouvée
        """
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

    def coeff_friction(self, pluie, glace):
        """Calcule le coefficient de friction de la piste.

        :param pluie: True s'il pleut, False sinon
        :type pluie: bool
        :param glace: True s'il y a de la glace, False sinon
        :type glace: bool
        :return: Coefficient de friction
        :rtype: float
        """
        if self.surface() == 'Asphalte':
            if glace is True:
                return 0.1
            elif pluie is True:
                return 0.3
            else:
                return 0.5
        elif self.surface() == 'Gravier':
            return 0.3
        elif self.surface() == 'Gazon':
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
        """Détermine l'orientation de la piste en degrés.

        :return: Liste des orientations des deux extrémités de la piste
        :rtype: list[int]
        """
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

    def afficher_infos_piste(self, pluie, glace):
        """Affiche les caractéristiques de la piste dans la console.

        :param pluie: True s'il pleut, False sinon
        :type pluie: bool
        :param glace: True s'il y a de la glace, False sinon
        :type glace: bool
        """
        print(f"\nCaracteristiques de la piste {self.n_piste}:")
        print(f"Matériau de la piste: {self.surface()}, f={self.coeff_friction(pluie, glace)}")
        print(f"Longueur: {self.longueur()}m")
        print(f"Largeur: {self.largeur()}m")