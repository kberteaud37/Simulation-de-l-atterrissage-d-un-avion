from math import sqrt, pi, log


class Avion:
    angle_de_descente = -2 #Degrés
    g = 32.2 #ft/s²
    temps_roue_libre = 3 #Secondes
    e = 0.8 #Coefficient D'Oswald

    def __init__(self,poids_atterrissage, choix_avion, meteo, piste, vitesse_vent=0):
        self.code = choix_avion.code
        self.W_LA = poids_atterrissage
        self.A = choix_avion.allongement()
        self.H = choix_avion.hauteur()
        self.S = choix_avion.surface()
        self.Cl_max_LA = choix_avion.portance()
        self.C_LG = choix_avion.trainee_train()
        self.delta_C_D0_f = choix_avion.trainee_volets()
        self.charge_alaire = self.W_LA/self.S
        self.piste = piste
        self.pluie = meteo.pluie
        self.glace = meteo.glace
        self.mu = self.piste.coeff_friction(self.pluie,self.glace)
        self.meteo = meteo
        self.density = self.meteo.calcul_densite()
        self.V_vent = vitesse_vent
        # Poussée au sol pour l'instant nulle
        self.T_sol = 0

    def calcul_A_eff(self):
        return self.A/sqrt((2*self.H)/(sqrt(self.A*self.S)))

    def calcul_k_eff(self):
        A_eff = self.calcul_A_eff()
        return 1/(pi*A_eff*self.e)

    def calcul_V_stall(self):
        return sqrt(self.W_LA / (0.5 * self.density * self.S * self.Cl_max_LA)) + self.V_vent

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

    def calcul_deceleration(self, distance):
        V_TD = self.calcul_V_TD()
        return - (V_TD**2)/(2*distance)

