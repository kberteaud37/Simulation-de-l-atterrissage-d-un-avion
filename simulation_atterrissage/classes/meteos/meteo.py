class Meteo:
    """Classe représentant les conditions météorologiques pour la simulation d'atterrissage.

    Cette classe calcule et fournit les paramètres météorologiques nécessaires à la simulation,
    y compris la densité de l'air en fonction de la température et de la pression.

    :param temperature: Température en degrés Celsius.
    :type temperature: float
    :param pression: Pression atmosphérique en hPa.
    :type pression: float
    :param vitesse_vent: Vitesse du vent en km/h.
    :type vitesse_vent: float
    :param orientation_vent: Orientation du vent en degrés.
    :type orientation_vent: float
    :param pluie: Indique s'il pleut.
    :type pluie: bool
    :param glace: Indique s'il y a de la glace.
    :type glace: bool
    """
    #Constante des gaz parfaits
    R = 287
    def __init__(self,temperature,pression,vitesse_vent,orientation_vent,pluie,glace):
        """Initialise un objet Meteo avec les conditions météorologiques."""
        self.T = temperature
        self.P = pression
        self.V_vent = vitesse_vent
        self.orientation_vent = orientation_vent
        self.pluie = pluie
        self.glace = glace

    #Calcul de la densité avec loi des gaz parfaits
    def calcul_densite(self):
        """Calcule la densité de l'air en utilisant la loi des gaz parfaits.

        :return: Densité de l'air en slug/ft³.
        :rtype: float
        """
        T_K=self.T+273.15
        P_Pa=self.P*100
        densite=P_Pa/(T_K*self.R) #kg/m3
        densite = densite * 0.00194032 #slug/ft3
        return densite
