from math import sqrt


class Avion:
    angle_de_descente = -3

    def __init__(self, poids_atterrissage, surface_alaire,
                 coefficient_portance_max_atterrissage):
        self.W_LA = poids_atterrissage
        self.S = surface_alaire
        self.Cl_max_LA = coefficient_portance_max_atterrissage

    def V_stall(self):
        self.V_stall = sqrt(self.W_LA / (0, 5 * self.density * self.S * self.Cl_max_LA))
        return self.V_stall


class Commercial(Avion):
    coef_transition = 1, 23
    n = 1, 35

    def __init__(self, poids_atterrissage, surface_alaire,
                 coefficient_portance_max_atterrissage):
        super().__init__(poids_atterrissage, surface_alaire,
                         coefficient_portance_max_atterrissage)

    def V_TR(self):
        return self.coef_transition * self.V_stall


class Militaire(Avion):
    coef_transition = 1, 15

    def V_TR(self):
        return self.coef_transition * self.V_stall

