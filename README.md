📊 E-commerce Data Analysis & A/B Testing Project

 Présentation

Ce projet analyse des données issues d’un site e-commerce afin de :

comprendre le comportement des utilisateurs

analyser la performance des produits et catégories

identifier les points de friction du funnel de conversion

évaluer une variation produit via un A/B test

 Le projet peut être lu et compris sans aucune installation.
 L’installation est uniquement nécessaire si vous souhaitez exécuter le code.

🎯 Objectifs

Analyse exploratoire des données (EDA)

Analyse du parcours utilisateur

Identification des leviers business

Mise en place d’un A/B test

Visualisation via un dashboard interactif

 Données utilisées 

```bash
 DataSet: (https://www.kaggle.com/datasets/retailrocket/ecommerce-dataset)
```
```bash
events.csv — événements utilisateurs

item_properties_part1.csv, item_properties_part2.csv — propriétés produits

category_tree.csv — hiérarchie des catégories
```
 Analyses réalisées (lecture sans code)

Activité utilisateur dans le temps

Funnel de conversion (View → Add to Cart → Transaction)

Produits et catégories générateurs de revenu

Analyse A/B basée sur un KPI principal

 Toutes les analyses sont expliquées en langage clair dans les notebooks et les graphiques.

⚙️ Installation & Exécution (OPTIONNELLE)

!!! Cette section est uniquement destinée aux personnes souhaitant exécuter le projet localement.
Si vous souhaitez seulement comprendre les résultats, vous pouvez ignorer cette partie.

1️/ Prérequis
```bash
Python 3.9+
Python 3.12.7
```
pip (installé avec Python)

Un terminal (Windows / macOS / Linux)

 Aucun compte cloud requis
 Aucun environnement complexe imposé

2️/ Cloner le projet
```bash
git clone https://github.com/votre-repo/ecommerce-analysis.git
cd ecommerce-analysis
```
3️/ (Optionnel mais recommandé) Créer un environnement virtuel
Windows
```bash
python -m venv venv
```
```bash
venv\Scripts\activate
```
macOS / Linux
```bash
python3 -m venv venv
```
```bash
source venv/bin/activate
```
4️/ Installer les dépendances

📦 Dépendances principales
```bash
pandas

numpy

matplotlib

plotly

streamlit

statsmodels
```
Installation en une commande
```bash
pip install -r requirements.txt

```

 Si requirements.txt n’existe pas, utilisez :
```bash
pip install pandas numpy matplotlib plotly streamlit statsmodels
```
5️/ Lancer les notebooks (optionnel)
```bash
jupyter notebook
```
Puis ouvrir les fichiers dans le dossier notebooks/.

6️/ Lancer le dashboard Streamlit
```bash
streamlit run app.py
```
 Le dashboard s’ouvre automatiquement dans le navigateur.

📁 Structure du projet
```bash
ecommerce-analysis/
│
├── data/
│   ├── # Données brutes  
│
├── notebooks/ # Analyses étape par étape
├── rapport/
├── scripts/ # A/B test          
├── app.py     # Dashboard Streamlit
├── requirements.txt  # Dépendances
├── README.md
└── .gitignore

```

🧪 A/B Test (résumé)

KPI principal : Purchase Conversion Rate

Méthode : test de proportion (Z-test)

Résultat : différence non significative

Décision : aucune preuve d’amélioration statistique

🧠 Enseignements clés

Le trafic est élevé mais la conversion reste faible

Le principal point de friction est avant l’ajout au panier

Le revenu est concentré sur peu de produits et catégories

Les décisions doivent être validées statistiquement

🏁 Conclusion

Ce projet illustre une démarche data complète, depuis l’exploration des données jusqu’à la prise de décision business.

Il est conçu pour :

✅ être compris sans installation

✅ être exécuté facilement si besoin

✅ être présenté en contexte professionnel ou académique