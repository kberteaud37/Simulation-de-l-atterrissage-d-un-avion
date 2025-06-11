from math import sqrt, pi, log


class Avion:
    angle_de_descente = -3 #Degrés
    g = 32.2 #ft/s²
    temps_roue_libre = 3 #Secondes
    e = 0.8 #Coefficient D'Oswald

    def __init__(self,code, poids_atterrissage, allongement, hauteur_aile, surface_alaire,
                 coefficient_portance_max_atterrissage,meteo,piste
                 ,coefficient_trainee_train = 0.1,coefficient_trainee_volets = 0.02):
        self.code = code
        self.W_LA = poids_atterrissage
        self.A = allongement
        self.H = hauteur_aile
        self.S = surface_alaire
        self.Cl_max_LA = coefficient_portance_max_atterrissage
        self.C_LG = coefficient_trainee_train
        self.delta_C_D0_f = coefficient_trainee_volets
        self.charge_alaire = self.W_LA/self.S
        self.piste = piste
        self.mu = self.piste.ajout_coefficient_friction()
        self.meteo = meteo
        self.density = self.meteo.calcul_densite()
        # Poussée au sol pour l'instant nulle
        self.T_sol = 0

    def calcul_A_eff(self):
        return self.A/sqrt((2*self.H)/(sqrt(self.A*self.S)))

    def calcul_k_eff(self):
        A_eff = self.calcul_A_eff()
        return 1/(pi*A_eff*self.e)

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

    def calcul_f2(self):
        k_eff = self.calcul_k_eff()
        return (self.density/(2*self.charge_alaire))*(-self.mu*self.C_LG+k_eff*self.C_LG**2+self.delta_C_D0_f)

    def calcul_S_B(self):
        f1 = self.calcul_f1()
        f2 = self.calcul_f2()
        V_TD = self.calcul_V_TD()
        return (1/(2*self.g*f2))*log(1+((f2*V_TD**2)/f1))

    def calcul_deceleration(self):
        V_TD = self.calcul_V_TD()
        S_B = self.calcul_S_B()
        return - (V_TD**2)/(2*S_B)

