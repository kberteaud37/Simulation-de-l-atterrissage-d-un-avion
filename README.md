# ✈️ Simulation d'atterrissage d'un avion

**Projet de session MGA802 — Été 2025**  
Auteurs : Kilian Berteaud, Alexis Chenuet, Pierrick Loranchet  

---

## 📌 Description

Cette application Streamlit propose une **simulation réaliste d’atterrissage d’un avion** en prenant en compte :

- Les données réelles des **aéroports et pistes**,
- Les **conditions météorologiques** dynamiques,
- Le **type d’avion** sélectionné ou personnalisé,
- Une **analyse complète de l'atterrissage** : distance d’approche, transition, freinage, etc.

Un affichage interactif (cartes, métriques, visualisations) guide l’utilisateur à travers **quatre étapes** pour réaliser la simulation.

---

## 🖼️ Aperçu de l’interface

![Aperçu de l’application](b67e27fa-68ef-4b58-921a-722e67348a7e.png)

---

## 🚀 Déploiement en ligne

Accédez à l’application sans rien installer :

👉 **[simulateur-avion.streamlit.app](https://simulateur-avion.streamlit.app)**

---

## 🛠️ Installation locale

### 📦 Prérequis

- Python 3.8+
- pip
- (Optionnel mais recommandé) Environnement virtuel

### 💻 Méthode 1 : via `requirements.txt`

```bash
# Cloner le dépôt
git clone https://github.com/kberteaud37/Simulation-de-l-atterrissage-d-un-avion.git
cd Simulation-de-l-atterrissage-d-un-avion

# Créer et activer un environnement virtuel
python -m venv venv
source venv/bin/activate        # Linux/Mac
.\venv\Scripts\activate         # Windows

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
streamlit run main.py
