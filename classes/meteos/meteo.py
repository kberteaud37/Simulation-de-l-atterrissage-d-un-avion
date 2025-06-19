class Meteo:
    #Constante des gaz parfaits
    R = 287
    def __init__(self,temperature,pression,vitesse_vent,orientation_vent,pluie,glace):
        self.T = temperature
        self.P = pression
        self.V_vent = vitesse_vent
        self.orientation_vent = orientation_vent
        self.pluie = pluie
        self.glace = glace

    #Calcul de la densité avec loi des gaz parfaits
    def calcul_densite(self):
        T_K=self.T+273.15
        P_Pa=self.P*100
        densite=P_Pa/(T_K*self.R) #kg/m3
        densite = densite * 0.00194032 #slug/ft3
        return densite
