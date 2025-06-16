"""Module contenant la classe Aeroport pour la simulation d'atterrissage."""
from fonctions_aeroport import *

class Aeroport:
    """Classe représentant un aéroport dans la simulation.

        :param code: Code OACI de l'aéroport
        :type code: str
        :param runways_df: DataFrame contenant les informations sur les pistes
        :type runways_df: pandas.DataFrame
    """
    def __init__(self, code,runways_df):
        """Initialise un objet Aeroport avec son code et les données des pistes."""
        self.code = code
        self.runway=runways_df

    def latitude(self):
        """Retourne la latitude de l'aéroport en degrés décimaux.

                :return: Latitude de l'aéroport
                :rtype: float
                :raises: Affiche un message si l'aéroport n'est pas trouvé
        """
        row = self.runway[self.runway["ident"] == self.code]
        if not row.empty:
            latitude = row.iloc[0]["latitude_deg"]
            return float(latitude)
        else:
            print("Aéroport non trouvé")

    def longitude(self):
        """Retourne la longitude de l'aéroport en degrés décimaux.

                :return: Longitude de l'aéroport
                :rtype: float
                :raises: Affiche un message si l'aéroport n'est pas trouvé
        """
        row = self.runway[self.runway["ident"] == self.code]
        if not row.empty:
            longitude = row.iloc[0]["longitude_deg"]
            return float(longitude)
        else:
            print("Aéroport non trouvé")

    def nom(self):
        """Retourne le nom complet de l'aéroport.

                :return: Nom de l'aéroport
                :rtype: str
                :raises: Affiche un message si l'aéroport n'est pas trouvé
        """
        row = self.runway[self.runway["ident"] == self.code]
        if not row.empty:
            nom = row.iloc[0]["name"]
            return str(nom)
        else:
            print("Aéroport non trouvé")

    def altitude(self):
        """Retourne l'altitude de l'aéroport en pieds.

                :return: Altitude en pieds
                :rtype: float
                :raises: Affiche un message si l'aéroport n'est pas trouvé
        """
        row = self.runway[self.runway["ident"] == self.code]
        if not row.empty:
            elevation = row.iloc[0]["elevation_ft"]
            return float(elevation)
        else:
            print("Aéroport non trouvé")

    def pistes(self):
        """Retourne la liste des identifiants de pistes disponibles.

                :return: Liste des identifiants de pistes
                :rtype: list[str]
                :raises: Affiche un message si l'aéroport n'est pas trouvé
        """
        filtre_code= self.runway[self.runway["ident"] == self.code]
        if not filtre_code.empty:
            pistes = [f"{row['runway_ident']}" for index, row in filtre_code.iterrows()]
            return pistes
        else:
            print("Aeroport non trouvé")

    def afficher_infos(self):
        """Affiche les informations principales de l'aéroport dans la console."""
        print(f"Aéroport: {self.nom()} ({self.code})")
        print(f"Coordonnées: {self.latitude()}, {self.longitude()}")
        print(f"Altitude: {self.altitude()} ft")
        print(f"La/les piste(s) de cet aéroport sont: {self.pistes()}")

