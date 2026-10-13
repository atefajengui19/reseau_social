# Modélisation Ontologique Web 4.0 - Réseaux Sociaux

Ce projet propose une architecture complète pour extraire, sémantiser et visualiser les interactions issues de multiples réseaux sociaux. Il s'appuie sur les technologies du Web Sémantique (RDF, OWL, SPARQL) et l'analyse de graphes pour inférer de nouvelles connaissances, notamment la détection automatique de leaders d'opinion.

## Structure du Projet et Données

*   **Ontologie** : 
    *   `ontologie_modele.ttl` : Fichier contenant le modèle sémantique OWL décrivant les utilisateurs (`UtilisateurStandard`, `LeaderDOpinion`), les contenus (`Video360`, `Image`) et les interactions (`Like`, `Partage`)
*   **Scripts ETL (Extraction, Transformation, Load)** :
    *   `etl_facebook.py` : Extrait les publications via l'API Graph Facebook et les convertit en triplets RDF
    *   `etl_mastodon.py` : Capture les *toots* publics de Mastodon selon un hashtag cible, nettoie le HTML et génère les triplets RDF
    *   `etl_kaggle.py` : Sémantise un jeu de données tabulaire issu de `reseau_social.csv'.
    *   `etl_snap.py` : Importe la vérité terrain depuis `facebook_combined.txt` (dataset Stanford) pour modéliser les relations d'influence réelles.
*   **Interface Utilisateur** :
    *   `interface_streamlit.py` : Tableau de bord interactif permettant de lancer les ETL, d'explorer le graphe de connaissances (PyVis), de visualiser les métriques d'engagement et de comparer les algorithmes de centralité (PageRank, HITS, Betweenness) avec l'inférence OWL.

## 🛠️ Versions des Outils et Prérequis

Pour garantir la reproductibilité, voici les versions recommandées :
*   **Python** : Python 3.14.5
*   **Bibliothèques Python** : `Streamlit, version 1.57.0`, `requests`, `rdflib`, `networkx`, `pandas`, `plotly`, `pyvis`.
*   **Base de données orientée Graphe** : Apache Jena Fuseki (version 6.1.0).
*   **Éditeur d'Ontologie** : Protégé (version 5.6.9).

## 📥 Installation de Protégé 5.6.9 (Pour éditer l'ontologie)

Protégé est nécessaire pour visualiser ou modifier visuellement le fichier `ontologie_modele.ttl`.

1.  Rendez-vous sur le site officiel : [https://protege.stanford.edu/](https://protege.stanford.edu/)
2.  Téléchargez la version **Desktop** correspondant à votre système d'exploitation (Windows, macOS ou Linux).
3.  Installez l'application en suivant l'assistant d'installation (nécessite un environnement Java/JRE à jour).
4.  Ouvrez Protégé, cliquez sur **File > Open**, et sélectionnez le fichier `ontologie_modele.ttl` de ce dépôt pour visualiser la hiérarchie des classes et les propriétés.

## 🚀 Installation et Reproduction

### Étape 1 : Préparation de la base de données (Apache Jena Fuseki 6.1.0)
1.  Téléchargez et lancez le serveur **Apache Jena Fuseki**.
2.  Créez un nouveau dataset nommé **`master_social`**.
3.  Assurez-vous que le serveur tourne sur `http://localhost:3030` (port par défaut utilisé par les scripts)

### Étape 2 : Configuration de l'environnement Python
Dans le dossier racine du projet, exécutez les commandes suivantes :
```bash
# Créer un environnement virtuel (optionnel mais recommandé)
python -m venv env
source env/bin/activate  # Sur Windows : env\Scripts\activate

# Installer les dépendances
pip install streamlit requests rdflib networkx pandas plotly pyvis
