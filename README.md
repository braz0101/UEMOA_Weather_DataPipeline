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
- Téléchargement automatique des archives météo 2023–2025.  
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
├── 0_Backup+Recup archives meteo 2023-2025/
├── 1_Script_Création de la source de données/
├── 2_Modélisation de l'entrepot de données/
├── 3_Script_Création de l’entrepôt/
├── 4_Script_Chargement 1/
├── 5_Script_Chargement 2/
├── 6_Airflow_Chargement 3/
│   ├── dags/
│   ├── scripts/
│   └── docker-compose.yml
├── 7_RequetesValidationFonctionnelleEntrepot/
├── 8_TableauDeBordPowerBI/
└── Rapport détaillé du projet 6.pdf
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

- utilisateur : `admin`  
- mot de passe : `admin`

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
