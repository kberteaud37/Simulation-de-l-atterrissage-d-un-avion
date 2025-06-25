from .. import classes
from simulation_atterrissage.classes.aeroports.fonctions_aeroport import recuperer_runways
from .trouver_aeroport_proche import trouver_aeroport_proche
from .calcul_distance_aeroport import calcul_distance_aeroport

# Fonction qui compare la longueur des pistes avec la distance nécessaire à l'atterrissage
def compare(monavion, piste, coef_secu=1.67):
    """Compare la longueur des pistes avec la distance nécessaire à l'atterrissage et trouve une solution viable.

    Cette fonction effectue une analyse de sécurité pour l'atterrissage en comparant :
    - La distance totale nécessaire (approche + transition + freinage) avec coefficient de sécurité
    - La longueur disponible des pistes

    Si la piste initiale est trop courte, recherche automatiquement des alternatives :
    1. D'abord d'autres pistes du même aéroport
    2. Puis des aéroports voisins si nécessaire

    :param monavion: Objet avion contenant les caractéristiques et méthodes de calcul
    :type monavion: Avion
    :param piste: Piste d'atterrissage initialement prévue
    :type piste: Piste
    :param coef_secu: Coefficient de sécurité (1.67 par défaut selon normes aéronautiques)
    :type coef_secu: float, optional
    :return: Tuple contenant (piste sélectionnée, logs détaillés, distance nécessaire)
    :rtype: tuple
    :raises RuntimeError: Si aucun aéroport viable n'est trouvé après 20 recherches

    Le tuple retourné contient :
        - piste (Piste): La piste sélectionnée (peut différer de la piste initiale)
        - logs (list): Liste de messages structurés (type, message) pour le suivi :
            - "info": Informations techniques
            - "error": Problèmes détectés
            - "success": Solution trouvée
            - "text": Messages de progression
        - distance_necessaire (float): Distance totale requise avec coefficient de sécurité

    """

    logs = []  # <-- liste de logs [(type, message)]
    avion = monavion

    # Calcul initial de la distance nécessaire
    distance_necessaire = (avion.calcul_S_B()+avion.calcul_S_FR()+avion.calcul_S_TR()) * coef_secu
    logs.append(("info", f"La distance nécessaire est : {distance_necessaire:.2f} ft"))
    logs.append(("info", f"La longueur de la piste est : {piste.longueur()} ft"))

    # Récupération des données des pistes
    df_runways = recuperer_runways()
    aeroport = [piste]
    code_aeroport_courant = piste.code
    pistes = df_runways[df_runways["ident"] == code_aeroport_courant]

    # Paramètres de contrôle
    max_recherches = 20
    nb_recherches = 0
    logs.append(("text", f"Test pour l'aéroport {piste.nom()}..."))

    # Boucle de recherche de piste viable
    while distance_necessaire >= piste.longueur():
        if nb_recherches >= max_recherches:
            raise RuntimeError("Trop de recherches effectuées, aucun aéroport viable trouvé.")
        nb_recherches += 1

        # 1. Test des autres pistes du même aéroport
        for num_piste in pistes["runway_ident"]:
            piste_test = classes.aeroports.Piste(code_aeroport_courant, df_runways, num_piste)
            avion.piste = piste_test
            distance_necessaire_test = (avion.calcul_S_B() + avion.calcul_S_FR() + avion.calcul_S_TR()) * coef_secu
            if distance_necessaire_test < piste_test.longueur():
                piste = piste_test
                distance_necessaire = distance_necessaire_test
                break
        else:
            # 2. Si aucune piste viable, recherche d'un nouvel aéroport
            logs.append(("error", "⚠️ Atterrissage non sûr : la distance nécessaire dépasse la longueur de la piste.\nRecherche d'une piste d'atterrissage sûre en cours..."))
            aeroport_proche = trouver_aeroport_proche(aeroport)
            code_aeroport_courant = aeroport_proche["ident"]
            pistes = df_runways[df_runways["ident"] == code_aeroport_courant]

            ligne = pistes.iloc[0]
            nouvelle_piste = classes.aeroports.Piste(ligne["ident"], df_runways, ligne["runway_ident"])
            aeroport.append(nouvelle_piste)
            logs.append(("text", f"Test pour l'aéroport {nouvelle_piste.nom()}..."))
            continue
        break
    # Résultats finaux
    distance_nm = calcul_distance_aeroport(aeroport[0].code, piste.code)
    logs.append(("success", f"🛬 Vous pouvez atterrir à {piste.nom()} (piste {piste.n_piste}), situé à {distance_nm:.2f} NM de {aeroport[0].nom()}."))
    logs.append(("info", f"La longueur de la nouvelle piste est {piste.longueur()} ft"))

    return piste, logs, distance_necessaire