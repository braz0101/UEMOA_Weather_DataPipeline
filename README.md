# 🌦️ UEMOA_Weather_DataPipeline  

Projet complet d’ingénierie des données sur la météo dans la zone **UEMOA** : pipeline **ETL automatisé** avec **Python** et **Apache Airflow**, entrepôt de données **PostgreSQL**, et tableau de bord analytique sous **Power BI**.

---

## 🧩 Sommaire  
1. [Contexte du projet](#-contexte-du-projet)  
2. [Objectifs](#-objectifs)  
3. [Architecture globale](#-architecture-globale)  
4. [Technologies utilisées](#-technologies-utilisées)  
5. [Étapes du pipeline](#-étapes-du-pipeline)  
6. [Structure du projet](#-structure-du-projet)  
7. [Validation & Tableau de bord](#-validation--tableau-de-bord)  
8. [Exécution avec Docker & Airflow](#-exécution-avec-docker--airflow)  
9. [Résultats & Visualisations](#-résultats--visualisations)  
10. [Auteurs](#-auteurs)

---

## 🌍 Contexte du projet  
Ce projet s’inscrit dans une démarche de **valorisation des données météorologiques** collectées dans la zone **UEMOA** (Union Économique et Monétaire Ouest Africaine).  
L’objectif principal est de construire un **entrepôt de données (Data Warehouse)** pour centraliser, historiser et analyser les données issues de différentes stations météo.

---

## 🎯 Objectifs  
- Collecter automatiquement les données météo historiques et en temps réel.  
- Construire un **pipeline ETL** robuste et automatisé (Airflow).  
- Concevoir un **modèle en étoile** pour l’analyse décisionnelle.  
- Charger les données consolidées dans un entrepôt PostgreSQL.  
- Mettre en place un **tableau de bord Power BI** pour le suivi des indicateurs météo.  

---

## 🏗️ Architecture globale  

```
+------------------+       +-------------------+       +---------------------+
| Données Sources  | --->  |  Pipeline ETL     | --->  | Entrepôt PostgreSQL |
| (archives météo) |       | (Python + Airflow)|       |  (modèle en étoile) |
+------------------+       +-------------------+       +---------------------+
                                                          |
                                                          v
                                                  +-----------------+
                                                  |  Power BI       |
                                                  |  Tableau de bord|
                                                  +-----------------+
```

---

## ⚙️ Technologies utilisées  
| Catégorie | Outil / Technologie |
|------------|--------------------|
| Langage principal | Python 3.11 |
| Orchestration | Apache Airflow |
| Base de données | PostgreSQL |
| Conteneurisation | Docker |
| Visualisation | Power BI |
| Gestion de version | Git / GitHub |

---

## 🔄 Étapes du pipeline  

1️⃣ **Collecte des données**  
- Téléchargement automatique des archives météo 2021–2025 (avec possibilité de sélectionner une plage de dates spécifique dans le script).
- Nettoyage et standardisation (script Python).  

2️⃣ **Création de la base source**  
- Tables brutes créées via `1_ScriptCreation_BaseDeDonnees_Et_TableBruteSource.sql`.  

3️⃣ **Modélisation de l’entrepôt**  
- Modèle en étoile avec tables de dimensions et table de faits (`3_Script_SQL_CreationEntrepotDonnees.sql`).  

4️⃣ **Chargement initial et incrémental**  
- `script1.sql` : premier chargement.  
- `script2.sql` : actualisation.  

5️⃣ **Pipeline Airflow automatisé (Docker)**  
- `etl_meteo.py` : collecte et insertion.  
- `update_dimensions_facts.py` : mise à jour automatique des faits et dimensions.  
- DAGs : `meteo_uemoa_hourly_dag.py`, `update_dimensions_facts_dag.py`.

---

## 🗂️ Structure du projet  

```
📦 UEMOA_Weather_DataPipeline
├── 0_Backup+Recup_archives_meteo_2021-2025/
│ └── script_recuperation_archive_meteo.py
├── 1_Script_Creation_de_la_source_de_donnees/
│ └── 1_ScriptCreation_BaseDeDonnees_Et_TableBruteSource.sql
├── 2_Modelisation_de_l_entrepot_de_donnees/
│ ├── 2_ModeleEntrepotMeteoUemoa.drawio
│ └── modele.png
├── 3_Script_Creation_de_l_entrepot/
│ └── 3_Script_SQL_CreationEntrepotDonnees.sql
├── 4_Script_Chargement_1/
│ └── script1.sql
├── 5_Script_Chargement_2/
│ └── script2.sql
├── 6_Airflow_Chargement_3/
│ ├── dags/
│ │ ├── meteo_uemoa_hourly_dag.py
│ │ └── update_dimensions_facts_dag.py
│ ├── exports/
│ │ └── meteo_uemoa.csv
│ ├── scripts/
│ │ ├── etl_meteo.py
│ │ └── update_dimensions_facts.py
│ └── docker-compose.yml
├── 7_RequetesValidationFonctionnelleEntrepot/
│ └── RequetesPourValidationFonctionnelleEntrepot.sql
├── 8_TableauDeBordPowerBI/
│ └── Visualisations (tableau de bord).pbix
└── Rapport_detaillé_du_projet.pdf
```

---

## ✅ Validation & Tableau de bord  
Les requêtes de validation (`7_RequetesValidationFonctionnelleEntrepot.sql`) ont permis de confirmer la cohérence des données.  
Un tableau de bord Power BI présente :  
- Les températures moyennes par pays et station.  
- L’évolution temporelle des précipitations.  
- Des cartes interactives et indicateurs clés.  

---

## 🐳 Exécution avec Docker & Airflow  

### 1️⃣ Lancer les services :
```bash
docker-compose up -d
```

### 2️⃣ Accéder à l’interface Airflow :
👉 [http://localhost:8081](http://localhost:8081)

- utilisateur : `admin`  (à changer)
- mot de passe : `admin` (à changer)

### 3️⃣ Exécuter les DAGs :
- `meteo_uemoa_hourly_dag`
- `update_dimensions_facts_dag`

---

## 📊 Résultats & Visualisations  

Le tableau de bord Power BI offre une vision complète des tendances météo :  

- 🌡️ Températures moyennes par pays  
- ☔ Précipitations journalières  
- 💨 Vitesse du vent moyenne  
- 🗺️ Carte géographique interactive (UEMOA)

---

## 👨‍💻 Auteurs  

**Ibrahima FALL**  
🎓 Master 1 – Systèmes, Réseaux & Télécommunications  
📧 ibrahimafall3110@gmail.com  
🖥️ Projet académique dans le cadre du module *Data Engineering*  

---

## ⭐ Suggestions d’améliorations futures  
- Intégration d’un module **IA / Machine Learning** pour la prévision météo.  
- Automatisation des dashboards Power BI avec API.  
- Déploiement cloud (AWS / GCP) pour la scalabilité.
