.. _installation:

Installation
============

Configuration requise
---------------------
- Python 3.8+ (avec pip inclus)
- Git (pour le clonage)
- Streamlit 1.33+ (installé automatiquement)

Méthodes d'installation
-----------------------

1. Mode développeur (installation éditable)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Idéal pour contribuer au projet ou modifier la simulation :

.. code-block:: bash

   # Clonage du dépôt
   git clone https://github.com/kberteaud37/simulation-atterrissage.git
   cd simulation-atterrissage

   # Installation en mode éditable avec dépendances
   pip install -e ".[dev]"  # Inclut les outils de test et linting

2. Installation comme package Python
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Pour une utilisation comme bibliothèque dans d'autres projets :

.. code-block:: bash

   # Depuis GitHub
   pip install git+https://github.com/kberteaud37/simulation-atterrissage.git

   # Depuis une archive locale
   pip install .

3. Via requirements.txt (méthode historique)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Alternative simple :

.. code-block:: bash

   pip install -r requirements.txt

Lancement de l'application
--------------------------

.. code-block:: bash

   streamlit run simulation_atterrissage/main.py

Accès en ligne (sans installation)
----------------------------------
Version hébergée disponible : |badge_streamlit|

.. |badge_streamlit| image:: https://static.streamlit.io/badges/streamlit_badge_black_white.svg
   :target: https://simulateur-avion.streamlit.app
   :alt: Open in Streamlit

Vérification
------------

Testez l'installation avec :

.. code-block:: bash

   python -c """
   from simulation_atterrissage.core import Simulation
   print('Package fonctionnel! Version:', Simulation.version)
   """

Dépannage
---------

+------------------------------+-----------------------------------------------+
| Problème                     | Solution                                      |
+==============================+===============================================+
| Erreurs de dépendances       | ``pip install --upgrade pip wheel setuptools``|
+------------------------------+-----------------------------------------------+
| Module non trouvé            | Vérifiez votre PYTHONPATH ou réinstallez avec |
|                              | ``pip install -e .``                          |
+------------------------------+-----------------------------------------------+
| Erreurs Streamlit            | ``streamlit cache clear``                     |
+------------------------------+-----------------------------------------------+