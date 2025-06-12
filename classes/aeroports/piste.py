from aeroport import Aeroport
from fonctions_aeroport import *
# Class Piste

class Piste(Aeroport):
    def __init__(self,code,num_piste_le,num_piste_he):

        # Appel du constructeur parent
        super().__init__(code)
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
            'gazon mou': 0.2,
            'gazon mouille': 0.2,
        }
        """
    def longueur(self, runways_df):
        row = runways_df[(runways_df["ident"] == self.code) &
                         (runways_df["le_ident"] == self.n_le_piste) &
                         (runways_df["he_ident"] == self.n_he_piste)]
        if not row.empty:
            longueur = row.iloc[0]["length_ft"]
            return float(longueur)
        else:
            print("Aéroport non trouvé")

    def largeur(self, runways_df):
        row = runways_df[(runways_df["ident"] == self.code)&
                         (runways_df["le_ident"] == self.n_le_piste) &
                         (runways_df["he_ident"] == self.n_he_piste)]
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

    def afficher_infos_piste(self,numero_piste,runways_df):
        print(f"\nCaracteristiques de la piste {numero_piste}:")
        #print(f"Surface: {self.surface.capitalize()} (Coeff. friction: {self.ajout_coefficient_friction()})")
        print(f"Longueur: {self.longueur(runways_df)}m")
        print(f"Largeur: {self.largeur(runways_df)}m")


mtl=Aeroport("CYUL")
piste1=mtl.pistes(recuperer_runways())[0][2]
piste2=mtl.pistes(recuperer_runways())[1][2]
piste_mtl=Piste("CYUL",piste1,piste2)
piste_mtl.afficher_infos_piste(mtl.afficher_pistes(recuperer_runways())[2],recuperer_runways())
