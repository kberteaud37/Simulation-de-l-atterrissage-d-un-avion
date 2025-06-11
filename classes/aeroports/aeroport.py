# Class Aeroport
from fonctions_aeroport import *
class Aeroport:
    def __init__(self, code):
        self.code = code

    def latitude(self, runways_df):
        row = runways_df[runways_df["ident"] == self.code]
        if not row.empty:
            latitude = row.iloc[0]["latitude_deg"]
            return float(latitude)
        else:
            print("Aéroport non trouvé")

    def longitude(self, runways_df):
        row = runways_df[runways_df["ident"] == self.code]
        if not row.empty:
            longitude = row.iloc[0]["longitude_deg"]
            return float(longitude)
        else:
            print("Aéroport non trouvé")

    def nom(self, runways_df):
        row = runways_df[runways_df["ident"] == self.code]
        if not row.empty:
            nom = row.iloc[0]["name"]
            return str(nom)
        else:
            print("Aéroport non trouvé")

    def altitude(self, runways_df):
        row = runways_df[runways_df["ident"] == self.code]
        if not row.empty:
            elevation = row.iloc[0]["elevation_ft"]
            return float(elevation)
        else:
            print("Aéroport non trouvé")


    def afficher_infos(self,runways_df):
        print(f"Aéroport: {self.nom(runways_df)} ({self.code})")
        print(f"Coordonnées: {self.latitude(runways_df)}, {self.longitude(runways_df)}")
        print(f"Altitude: {self.altitude(runways_df)} ft")
