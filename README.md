# 🌦️ UEMOA_Weather_DataPipeline  

Projet complet d’ingénierie des données sur la météo dans la zone **UEMOA** : pipeline **ETL automatisé** avec **Python** et **Apache Airflow**, entrepôt de données **PostgreSQL**, et tableau de bord analytique sous **Power BI**.

---

## 🔹 Résumé du projet
Le projet **UEMOA_Weather_DataPipeline** vise à construire un **pipeline ETL complet** pour collecter, transformer et analyser les données météo de la zone UEMOA, permettant de produire des tableaux de bord interactifs pour la prise de décision.

---

## 🔹 Prérequis logiciel / environnement
Avant de lancer le projet avec Docker et Airflow, assurez-vous d’avoir installé et configuré :
- **Python 3.11**
- **PostgreSQL** (base de données locale ou serveur distant)
- **Docker & Docker Compose**
- **WSL 2** (recommandé pour exécuter Docker et Airflow sous Windows)
- **Power BI** (pour visualiser les fichiers `.pbix`)
- **Git** (pour cloner le dépôt et gérer les versions)

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
│ └── Visualisations (tableau de bord).pdf
└── Rapport_detaillé_du_projet.pdf
```

---

## ✅ Validation & Tableau de bord  
Les requêtes de validation (`7_RequetesValidationFonctionnelleEntrepot.sql`) ont permis de confirmer la cohérence des données ainsi que le tableau de bord.    

# - Température moyenne & précipitations totales par région :
<img width="1175" height="912" alt="image" src="https://github.com/user-attachments/assets/31e14a97-11ed-422c-ac12-646b33756438" />

<img width="1318" height="781" alt="image" src="https://github.com/user-attachments/assets/9ada9c36-6994-4f0d-aac8-c91b119be084" />


# - Top 3 des stations les plus chaudes :
<img width="1102" height="616" alt="image" src="https://github.com/user-attachments/assets/591f9252-182d-4560-beeb-92a087a7404c" />

<img width="1255" height="831" alt="image" src="https://github.com/user-attachments/assets/94167685-8651-4dd7-b069-b8d6ce8bf590" />

---

## 🐳 Exécution avec Docker & Airflow  

### 1️⃣ Lancer les services :
```bash
docker-compose up -d
```
<img width="1467" height="714" alt="image" src="https://github.com/user-attachments/assets/7f5ba31c-3566-44a8-92e6-d05c35eddb32" />

### 2️⃣ Accéder à l’interface Airflow :
👉 [http://localhost:8081](http://localhost:8081)

<img width="955" height="814" alt="image" src="https://github.com/user-attachments/assets/bd86b17f-3e8b-4ddc-bcd1-a8476aabc1b0" />

- utilisateur : `admin`  (à changer)
- mot de passe : `admin` (à changer)

### 3️⃣ Exécuter les DAGs :

<img width="1904" height="882" alt="image" src="https://github.com/user-attachments/assets/68b197cf-0c14-4d39-b7f5-0569ac334841" />

- `meteo_uemoa_hourly_dag`
- `update_dimensions_facts_dag`

---

## 📊 Résultats & Visualisations  

Le tableau de bord Power BI offre une vision complète des tendances météo :  

- 🌡️ Températures moyennes par pays   
- 💨 Vitesse du vent moyenne, et d'autres tendances météo (Visualisations (tableau de bord).pdf)

---

## 👨‍💻 Auteurs  

**Ibrahima FALL**  
🎓 Master – Systèmes, Réseaux & Télécommunications à l'Ecole Supérieure Polytechnique de Dakar (ESP-UCAD)  
📧 ibrahimafall3110@gmail.com  
🖥️ Projet réalisé dans le cadre de la certification Data Engineering – FORCE-N Sénégal
 
---

## ⭐ Suggestions d’améliorations futures
- Intégration d’un module **IA / Machine Learning** pour la prévision météo (régression, séries temporelles, réseaux de neurones, LSTM, Prophet, etc.).  
- Détection d’anomalies météorologiques avec **IA** pour identifier des événements extrêmes ou erreurs de capteurs.  
- Automatisation des dashboards Power BI avec API.  
- Déploiement cloud (**AWS**, **GCP**, ou **Azure**) pour la scalabilité et la haute disponibilité.  
- Utilisation de **Talend** ou d’un autre ETL pour simplifier l’orchestration et la transformation des données.  
- Création de dashboards interactifs avec **Apache Superset** pour une alternative open-source à Power BI.  
- Ajout de **tests automatisés** et de monitoring pour le pipeline ETL (alertes en cas d’échec ou de données manquantes).  
- Optimisation des requêtes SQL et de l’entrepôt pour gérer de plus gros volumes de données.  
- Mise en place d’un **workflow CI/CD** pour déployer automatiquement les scripts ETL et les dashboards.  
- Intégration d’**API météo externes** pour enrichir les données historiques avec des informations en temps réel.  
- Visualisation des tendances météo avec **cartographie interactive** avancée (Leaflet, Plotly, etc.).  
- Prédiction des tendances climatiques à long terme via **modèles d’apprentissage profond**.  
- Analyse corrélative entre données météo et autres indicateurs socio-économiques à l’aide de **machine learning multivarié**.

