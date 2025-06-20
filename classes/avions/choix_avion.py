from classes.avions.fonction_avion import charger_donnees_avions


class ChoixAvion:
    """Classe pour la gestion et la sélection des caractéristiques techniques des avions.

        Cette classe permet d'accéder aux paramètres techniques d'un avion spécifique
        à partir de son code identifiant, avec conversion automatique des unités.
        Supporte également la création d'avions personnalisés via le code "CUSTOM".

        :param code_avion: Code identifiant de l'avion (ex : "B737", "A320")
        :type code_avion: str
        :param custom_data: Données personnalisées pour un avion CUSTOM, defaults to None
        :type custom_data: dict, optional
        """
    def __init__(self, code_avion, custom_data=None):
        """Initialise un objet ChoixAvion avec le code de l'avion et des données optionnelles."""
        self.code = code_avion  # Stocke directement le code sans transformation
        self._donnees_avions = None
        self._custom_data = custom_data

    def _importation_donnees(self):
        """Charge les données des avions depuis la source externe.

                :return: DataFrame contenant les données techniques des avions
                :rtype: pandas.DataFrame
                """
        if self.code == "CUSTOM" and self._custom_data is not None:
            return self._custom_data
        """Charge les données des avions une seule fois et les met en cache"""
        if self._donnees_avions is None:
            self._donnees_avions = charger_donnees_avions()
        return self._donnees_avions

    def _get_avion_data(self):
        """Récupère les données techniques de l'avion spécifié.

                :return: Série pandas contenant les données de l'avion
                :rtype: pandas.Series
                :raises ValueError: Si l'avion n'est pas trouvé dans la base de données
                """
        if self.code == "CUSTOM" and self._custom_data is not None:
            return self._custom_data

        if self._donnees_avions is None:
            self._donnees_avions = charger_donnees_avions()

        # Recherche insensible à la casse et aux espaces
        avion_data = self._donnees_avions[
            self._donnees_avions['Code'].str.upper().str.strip() == self.code.upper().strip()
            ]

        if not avion_data.empty:
            return avion_data.iloc[0]

        raise ValueError(f"Avion {self.code} non trouvé dans la base de données")

    def hauteur(self, en_pieds=True):
        """Retourne la hauteur de l'aile de l'avion.

                :param en_pieds: Si True, retourne en pieds; si False, en mètres, defaults to True
                :type en_pieds: bool, optional
                :return: Hauteur de l'aile
                :rtype: float
                """

        avion = self._get_avion_data()
        if en_pieds:
            return float(avion['Hauteur_aile_ft'])  # Utilise directement la valeur convertie
        return float(avion['Hauteur_aile_m'])

    def surface(self, en_pieds_carres=True):
        """Retourne la surface alaire de l'avion.

                :param en_pieds_carres: Si True, retourne en pieds carrés; si False, en mètres carrés, defaults to True
                :type en_pieds_carres: bool, optional
                :return: Surface alaire
                :rtype: float
                """

        avion = self._get_avion_data()
        if en_pieds_carres:
            return float(avion['Surface_alaire_ft2'])  # Utilise directement la valeur convertie
        return float(avion['Surface_alaire_m2'])

    def allongement(self):
        """Retourne l'allongement de l'aile (ratio envergure/surface).

                :return: Allongement de l'aile
                :rtype: float
                """

        avion = self._get_avion_data()
        return float(avion['Allongement']) if avion is not None else None

    def portance(self):
        """Retourne le coefficient de portance maximal à l'atterrissage.

                :return: Coefficient de portance maximal (CL_max)
                :rtype: float
                """

        avion = self._get_avion_data()
        return float(avion['CL_max_atterrissage']) if avion is not None else None

    def trainee_train(self):
        """Retourne le coefficient de traînée du train d'atterrissage.

                :return: Coefficient de traînée du train (Cd_train)
                :rtype: float
                """

        avion = self._get_avion_data()
        return float(avion['Cd_train']) if avion is not None else None

    def trainee_volets(self):
        """Retourne l'incrément de traînée dû aux volets.

                :return: Delta coefficient de traînée des volets (ΔCd_volets)
                :rtype: float
                """

        avion = self._get_avion_data()
        return float(avion['Cd_volets']) if avion is not None else None

    def type_avion(self):
        """Détermine le type d'avion (Commercial ou Militaire).

                :return: Type d'avion ("Commercial" ou "Militaire")
                :rtype: str
                :raises KeyError: Si la colonne Type n'existe pas et qu'on ne peut pas déterminer le type
                """
        avion = self._get_avion_data()
        try:
            # Essayer de récupérer le type directement
            return avion['Type']
        except KeyError:
            # Fallback si la colonne Type n'existe pas
            militaires = ['F-', 'AH-', 'B-', 'Rafale', 'Eurofighter', 'Su-', 'Mirage']
            if any(mil in self.code for mil in militaires):
                return 'Militaire'
            return 'Commercial'




