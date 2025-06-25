from classes.avions import Avion


def test_freinage_urgence():
    """Test unitaire sur le calcul de freinage"""
    avion = Avion(
        modele="B737",
        poids=50000,
        coefficient_freinage=0.4  # Freinage urgent
    )

    distance = avion.calculer_distance_freinage(
        vitesse_initiale=60,  # m/s
        condition_piste="mouille"
    )

    assert 400 <= distance <= 600  # Vérification plage réaliste