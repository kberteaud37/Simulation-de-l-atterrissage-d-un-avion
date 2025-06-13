from math import cos, sin, tan, radians
from .avion import Avion

class Militaire(Avion):

    def __init__(self,poids_atterrissage, choix_avion, meteo, piste, vitesse_vent=0,
                 facteur_de_charge = 2,hauteur_obstacle = 50,
                 coef_transition = 1.15):
        super().__init__(poids_atterrissage, choix_avion,
                         meteo, piste, vitesse_vent)
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

    def calcul_S_LA(self):
        S_A = self.calcul_S_A()
        S_TR = self.calcul_S_TR()
        S_FR = self.calcul_S_FR()
        S_B = self.calcul_S_B()
        return 1.6*(S_A+S_TR+S_FR+S_B)