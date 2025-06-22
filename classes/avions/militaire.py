from math import cos, sin, tan, radians
from classes.avions.avion import Avion

class Militaire(Avion):
    """Classe représentant un avion militaire pour la simulation d'atterrissage.

        Hérite de la classe Avion de base et implémente les calculs spécifiques
        aux avions militaires selon les normes de l'aviation militaire.

        :param poids_atterrissage: Poids de l'avion à l'atterrissage (lbs)
        :type poids_atterrissage: float
        :param choix_avion: Objet contenant les caractéristiques techniques de l'avion
        :type choix_avion: ChoixAvion
        :param meteo: Objet contenant les conditions météorologiques
        :type meteo: Meteo
        :param piste: Objet représentant la piste d'atterrissage
        :type piste: Piste
        :param vitesse_vent: Vitesse du vent de face (ft/s), defaults to 0
        :type vitesse_vent: float, optional
        :param facteur_de_charge: Facteur de charge pour les calculs de trajectoire, defaults to 2
        :type facteur_de_charge: float, optional
        :param hauteur_obstacle: Hauteur de l'obstacle à franchir (ft), defaults to 50
        :type hauteur_obstacle: float, optional
        :param coef_transition: Coefficient pour le calcul de la vitesse de transition, defaults to 1.15
        :type coef_transition: float, optional
        """
    def __init__(self,poids_atterrissage, choix_avion, meteo, piste, vitesse_vent=0,
                 facteur_de_charge = 2,hauteur_obstacle = 50,
                 coef_transition = 1.15):
        super().__init__(poids_atterrissage, choix_avion,
                         meteo, piste, vitesse_vent)
        self.n = facteur_de_charge
        self.H_OBS = hauteur_obstacle
        self.coef_TR = coef_transition

    def calcul_V_TR(self):
        """Calcule la vitesse de transition pendant l'arrondi.

               :return: Vitesse de transition (ft/s)
               :rtype: float
               """
        V_stall = self.calcul_V_stall()
        return self.coef_TR * V_stall

    def calcul_R(self):
        """Calcule le rayon de la trajectoire circulaire pendant l'arrondi.

                :return: Rayon de la trajectoire circulaire (ft)
                :rtype: float
                """
        V_TR = self.calcul_V_TR()
        return (V_TR ** 2) / (self.g * (self.n - 1))

    def calcul_H_TR(self):
        """Calcule la hauteur perdue pendant la phase de transition.

                :return: Hauteur perdue durant la transition (ft)
                :rtype: float
                """
        R = self.calcul_R()
        return R * (1 - cos(radians(self.angle_de_descente)))

    def calcul_S_A(self):
        """Calcule la distance horizontale de la phase d'approche.

                :return: Distance d'approche (ft)
                :rtype: float
                """
        H_TR = self.calcul_H_TR()
        return (H_TR - self.H_OBS) / tan(radians(self.angle_de_descente))

    def calcul_S_TR(self):
        """Calcule la distance horizontale de la phase de transition.

                :return: Distance de transition (ft)
                :rtype: float
                """
        R = self.calcul_R()
        return -R * sin(radians(self.angle_de_descente))

    def calcul_S_LA(self):
        """Calcule la distance totale d'atterrissage avec marge de sécurité.

                Applique un facteur de sécurité de 1.6 selon les normes aéronautiques.

                :return: Distance totale d'atterrissage avec marge (ft)
                :rtype: float
                """
        S_A = self.calcul_S_A()
        S_TR = self.calcul_S_TR()
        S_FR = self.calcul_S_FR()
        S_B = self.calcul_S_B()
        return 1.6*(S_A+S_TR+S_FR+S_B)