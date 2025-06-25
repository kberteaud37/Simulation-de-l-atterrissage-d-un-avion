# ✈️ Simulation d'atterrissage d'un avion

**Projet de session MGA802 — Été 2025**

Auteurs : Kilian Berteaud, Alexis Chenuet, Pierrick Loranchet

---

## 📌 Description

Application Streamlit pour **simuler un atterrissage** avec :
- 🏗️ Données réelles d'aéroports/pistes
- 🌦️ Conditions météo dynamiques
- ✈️ Modèles d'avion paramétrables
- 📊 Analyse complète (distance, freinage, etc.)

---

## 🚀 Démo en ligne

Accédez sans installer :
👉 [simulateur-avion.streamlit.app](https://simulateur-avion.streamlit.app)

---

## 📖 Documentation

Pour consulter la documentation complète du projet, ouvrez le fichier `build/html/index.html` dans votre navigateur web après avoir généré la documentation. Pour générer la documentation, utilisez la commande suivante :

```bash
.\make.bat html
```
Cela générera la documentation HTML dans le répertoire docs/build/html.

---

## 🛠️ Installation
Prérequis
- Python 3.8+
- Git
- pip

### 📦 Méthode 1 : Comme package (recommandé)
```bash
git clone https://github.com/kberteaud37/Simulation-de-l-atterrissage-d-un-avion.git

# Installation en mode éditable (+ dépendances)
pip install -e .

# Lancer l'application
cd simulation_atterrissage
streamlit run main.py
consulter la documentation complète du projet, ouvrez le fichier `build/html/index.html` dans votre navigateur web après avoir généré la documentation. 

```

### 📦 Méthode 2 : Installation via requirements.txt
Si vous préférez installer uniquement les dépendances nécessaires sans le mode éditable :

```bash
git clone https://github.com/kberteaud37/Simulation-de-l-atterrissage-d-un-avion.git

# Installation des dépendances
pip install -r requirements.txt

# Lancer l'application
cd simulation_atterrissage
streamlit run main.py
```

---

## 🧪 Tests

### Prérequis
```bash
pip install pytest pytest-cov
```

### Exécution des tests
```bash
# Tous les tests avec couverture
pytest --cov=simulation_atterrissage --cov-report=html tests/

# Test spécifique
pytest tests/test_avion.py -v

# Générer le rapport de couverture
open htmlcov/index.html  # Sur Mac/Linux
start htmlcov/index.html # Sur Windows
```
--- 

## 📚 Références et API
Ce projet s'appuie sur le cours MEC 671 pour les calculs de performances des avions, offrant une base théorique solide pour les simulations d'atterrissage.

Les données et fonctionnalités sont enrichies grâce à plusieurs API et bibliothèques :

- **Meteo** : Fournit des données météorologiques en temps réel, telles que la température, la pression et la vitesse du vent, essentielles pour les calculs de densité de l'air.
- **OurAirports** : Base de données complète des aéroports, utilisée pour obtenir les coordonnées et les caractéristiques des pistes au Québec.
- **Streamlit** : Utilisé pour créer une interface web interactive permettant aux utilisateurs de visualiser et d'interagir avec les résultats de la simulation.
- **Folium** : Génère des cartes interactives pour visualiser les aéroports et les pistes sélectionnées.

---

## 🤝 Contribution
Les contributions sont les bienvenues ! Pour contribuer :

1. Fork le projet
2. Créez votre branche (git checkout -b feature/ma-nouvelle-fonctionnalité)
3. Committez vos changements (git commit -am 'Ajout d'une nouvelle fonctionnalité')
4. Poussez sur la branche (git push origin feature/ma-nouvelle-fonctionnalité)
5. Ouvrez une Pull Request

---

## 📜 Licence
Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.