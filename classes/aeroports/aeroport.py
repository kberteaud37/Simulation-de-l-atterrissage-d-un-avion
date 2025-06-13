# Class Aeroport
class Aeroport:
    def __init__(self, code,runways_df):
        self.code = code
        self.runway=runways_df

    def latitude(self):
        row = self.runway[self.runway["ident"] == self.code]
        if not row.empty:
            latitude = row.iloc[0]["latitude_deg"]
            return float(latitude)
        else:
            print("Aéroport non trouvé")

    def longitude(self):
        row = self.runway[self.runway["ident"] == self.code]
        if not row.empty:
            longitude = row.iloc[0]["longitude_deg"]
            return float(longitude)
        else:
            print("Aéroport non trouvé")

    def nom(self):
        row = self.runway[self.runway["ident"] == self.code]
        if not row.empty:
            nom = row.iloc[0]["name"]
            return str(nom)
        else:
            print("Aéroport non trouvé")

    def altitude(self):
        row = self.runway[self.runway["ident"] == self.code]
        if not row.empty:
            elevation = row.iloc[0]["elevation_ft"]
            return float(elevation)
        else:
            print("Aéroport non trouvé")

    def pistes(self):
        filtre_code= self.runway[self.runway["ident"] == self.code]
        if not filtre_code.empty:
            pistes = [f"{row['runway_ident']}" for index, row in filtre_code.iterrows()]
            return pistes
        else:
            print("Aeroport non trouvé")

    def afficher_infos(self):
        print(f"Aéroport: {self.nom()} ({self.code})")
        print(f"Coordonnées: {self.latitude()}, {self.longitude()}")
        print(f"Altitude: {self.altitude()} ft")
        print(f"La/les piste(s) de cet aéroport sont: {self.pistes()}")
