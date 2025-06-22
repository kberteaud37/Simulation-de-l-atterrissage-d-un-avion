.. _installation:

Installation
============

Ce guide vous montre comment installer et configurer le projet Simulation d'atterrissage.

Prérequis
---------

Avant de commencer, assurez-vous d'avoir installé les logiciels suivants :

- Python 3.8 ou supérieur (https://www.python.org/downloads/)
- pip (gestionnaire de paquets Python)
- Git (optionnel pour le versionnage)

Méthodes d'installation
-----------------------

1. **Installation via requirements.txt (recommandé pour le développement)** :

   .. code-block:: bash

      # 1. Clonez le dépôt (ou téléchargez les sources)
      git clone https://github.com/kberteaud37/simulation-atterrissage.git
      cd simulation-atterrissage

      # 2. Créez un environnement virtuel (optionnel mais recommandé)
      python -m venv venv
      source venv/bin/activate  # Linux/Mac
      venv\Scripts\activate     # Windows

      # 3. Installez les dépendances
      pip install -r requirements.txt

2. **Installation comme package (pour une utilisation en production)** :

   .. code-block:: bash

      pip install git+https://github.com/kberteaud37/simulation-atterrissage.git
      # ou pour une installation locale
      pip install .

Exécution de l’application
--------------------------

Une fois l'installation terminée, lancez l'application Streamlit avec la commande suivante :

.. code-block:: bash

   streamlit run main.py

Cela ouvrira automatiquement l'application dans votre navigateur par défaut.

Utilisation en ligne (optionnel)
--------------------------------

Une version hébergée de l'application est également accessible (si disponible) via Streamlit Cloud :

`https://simulateur-avion.streamlit.app <https://simulateur-avion.streamlit.app>`_

Cette méthode ne nécessite aucune installation et est recommandée pour une utilisation rapide ou une démonstration.

Vérification de l'installation
------------------------------

Après installation, vous pouvez vérifier que tout est bien installé en exécutant :

.. code-block:: bash

   python -c "from simulation_atterrissage import main; print('Installation réussie !')"

Dépannage
---------

Problèmes courants :

* **Erreurs de dépendances** :

     .. code-block:: bash

        # Solution 1 : Mettez à jour pip
        python -m pip install --upgrade pip

        # Solution 2 : Installation forcée
        pip install --ignore-installed -r requirements.txt
