import pytest
from classes.avion import Avion
from classes.aeroport import Aeroport, Piste
from simulation_atterrissage import simuler_atterrissage


def test_simulation_complete():
    """Test d'intégration complet avec conditions normales"""
    # 1. Configuration
    avion = Avion(
        modele="A320",
        poids=65000,  # kg
        coefficient_freinage=0.3
    )

    piste = Piste(
        longueur=2500,  # mètres
        condition="sec",
        pente=0.02
    )

    aeroport = Aeroport(
        nom="Montréal-Trudeau",
        pistes=[piste]
    )

    # 2. Exécution
    resultat = simuler_atterrissage(
        avion=avion,
        aeroport=aeroport,
        vent=10,  # noeuds
        temperature=15  # °C
    )

    # 3. Vérifications
    assert resultat.reussi is True
    assert resultat.distance_utilisee < piste.longueur
    assert "A320" in resultat.message