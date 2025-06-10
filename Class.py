from math import sqrt, cos, sin, tan, radians, log


class Avion:
    angle_de_descente = -3
    g = 32.2 #ft/s²
    temps_roue_libre = 3 #Secondes

    def __init__(self,code, poids_atterrissage, surface_alaire,
                 coefficient_portance_max_atterrissage,):
        self.code = code
        self.W_LA = poids_atterrissage
        self.S = surface_alaire
        self.Cl_max_LA = coefficient_portance_max_atterrissage
        self.charge_alaire = self.W_LA/self.S

    def calcul_V_stall(self):
        self.V_stall = sqrt(self.W_LA / (0.5 * self.density * self.S * self.Cl_max_LA))
        return self.V_stall

    def calcul_S_FR(self):
        self.V_TD = 1.15*self.V_stall
        self.S_FR = self.temps_roue_libre * self.V_TD
        return self.S_FR

    def calcul_f1(self):
        self.f1 = (self.T_sol/self.mu)+self.mu
        return self.f1

class Commercial(Avion):
    coef_transition = 1, 23
    n = 1.35 #Facteur de charge
    H_OBS = 35 #Hauteur d'obstacle

    def __init__(self, poids_atterrissage, surface_alaire,
                 coefficient_portance_max_atterrissage):
        super().__init__(poids_atterrissage, surface_alaire,
                         coefficient_portance_max_atterrissage)

    def calcul_V_TR(self):
        self.V_TR = self.coef_transition * self.V_stall
        return self.V_TR

    def calcul_R(self):
        self.R = (self.V_TR**2)/(self.g*(self.n-1))
        return self.R

    def calcul_H_TR(self):
        self.H_TR = self.R*(1-cos(radians(self.angle_de_descente)))
        return self.H_TR

    def calcul_S_A(self):
        self.S_A = (self.H_TR-self.H_OBS)/tan(radians(self.angle_de_descente))
        return self.S_A

    def calcul_S_TR(self):
        self.S_TR = -self.R*sin(radians(self.angle_de_descente))
        return self.S_TR



class Militaire(Avion):
    coef_transition = 1.15
    n = 2 #Facteur de charge
    H_OBS = 50 #Hauteur d'obstacle

    def calcul_V_TR(self):
        return self.coef_transition * self.V_stall

    def calcul_R(self):
        self.R = (self.V_TR ** 2) / (self.g * (self.n - 1))
        return self.R

    def calcul_H_TR(self):
        self.H_TR = self.R*(1-cos(radians(self.angle_de_descente)))
        return self.H_TR

    def calcul_S_A(self):
        self.S_A = (self.H_TR-self.H_OBS)/tan(radians(self.angle_de_descente))
        return self.S_A

    def calcul_S_TR(self):
        self.S_TR = -self.R*sin(radians(self.angle_de_descente))
        return self.S_TR