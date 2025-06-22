.. _installation:

Installation
============

Ce guide vous montre comment installer et configurer le projet Simulation d'atterrissage.

Prérequis
---------

Avant de commencer, assurez-vous d'avoir installé les logiciels suivants :

- Python 3.8 ou supérieur (https://www.python.org/downloads/)
- pip (gestionnaire de paquets Python)
- Git (optionnel pour la version contrôle)

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

Vérification de l'installation
-----------------------------

Après installation, exécutez :

.. code-block:: bash

   python -c "from simulation_atterrissage import main; print('Installation réussie !')"

Dépannage
---------

Problèmes courants :

* **Erreurs de dépendances** :

     # Solution 1 : Mettez à jour pip
     python -m pip install --upgrade pip

     # Solution 2 : Installation forcée
     pip install --ignore-installed -r requirements.txt