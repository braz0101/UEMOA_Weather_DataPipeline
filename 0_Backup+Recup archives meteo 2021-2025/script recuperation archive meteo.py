import os
import time
import logging
import requests 
import psycopg2 
import pandas as pd 
from datetime import datetime

# ------------------ Configuration Logging ------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# ------------------ Paramètres Base de Données ------------------
DB_CONFIG = {
    "dbname": "climat_uemoa",
    "user": "postgres",
    "password": "xxxxxx",
    "host": "localhost",
     "port": 5433
}

# ------------------ Paramètres Collecte ------------------
HOURLY_VARIABLES = [
    "temperature_2m", "relativehumidity_2m", "dewpoint_2m", "pressure_msl",
    "windspeed_10m", "winddirection_10m", "precipitation", "weathercode",
    "cloudcover", "visibility", "shortwave_radiation", "snowfall"
]

CSV_PATH = "archives_meteo_uemoa.csv"

# Régions à collecter
REGIONS = {
    "Sénégal": [
        {"nom": "Dakar", "latitude": 14.7167, "longitude": -17.4677, "altitude": 20, "pays": "Sénégal"},
        {"nom": "Diourbel", "latitude": 14.6589, "longitude": -16.2333, "altitude": 24, "pays": "Sénégal"},
        {"nom": "Fatick", "latitude": 14.3236, "longitude": -16.4149, "altitude": 11, "pays": "Sénégal"},
        {"nom": "Kaffrine", "latitude": 14.0964, "longitude": -15.5500, "altitude": 41, "pays": "Sénégal"},
        {"nom": "Kaolack", "latitude": 14.1476, "longitude": -16.0713, "altitude": 8, "pays": "Sénégal"},
        {"nom": "Kédougou", "latitude": 12.5574, "longitude": -12.1817, "altitude": 130, "pays": "Sénégal"},
        {"nom": "Kolda", "latitude": 12.8913, "longitude": -14.9601, "altitude": 26, "pays": "Sénégal"},
        {"nom": "Louga", "latitude": 15.6200, "longitude": -16.2167, "altitude": 29, "pays": "Sénégal"},
        {"nom": "Matam", "latitude": 15.6569, "longitude": -13.2527, "altitude": 28, "pays": "Sénégal"},
        {"nom": "Saint-Louis", "latitude": 16.0306, "longitude": -16.4886, "altitude": 2, "pays": "Sénégal"},
        {"nom": "Sédhiou", "latitude": 12.6963, "longitude": -15.5575, "altitude": 17, "pays": "Sénégal"},
        {"nom": "Tambacounda", "latitude": 13.7542, "longitude": -13.6661, "altitude": 26, "pays": "Sénégal"},
        {"nom": "Thiès", "latitude": 14.7931, "longitude": -16.9447, "altitude": 40, "pays": "Sénégal"},
        {"nom": "Ziguinchor", "latitude": 12.5733, "longitude": -16.2813, "altitude": 13, "pays": "Sénégal"}
    ],
    "Bénin": [
        {"nom": "Alibori", "latitude": 11.7325, "longitude": 2.3700, "altitude": 200, "pays": "Bénin"},
        {"nom": "Atacora", "latitude": 10.4540, "longitude": 1.6658, "altitude": 400, "pays": "Bénin"},
        {"nom": "Atlantique", "latitude": 6.3500, "longitude": 2.3333, "altitude": 50, "pays": "Bénin"},
        {"nom": "Borgou", "latitude": 9.7075, "longitude": 2.6386, "altitude": 300, "pays": "Bénin"},
        {"nom": "Collines", "latitude": 7.7333, "longitude": 2.2500, "altitude": 400, "pays": "Bénin"},
        {"nom": "Donga", "latitude": 9.9183, "longitude": 1.7072, "altitude": 350, "pays": "Bénin"},
        {"nom": "Kouffo", "latitude": 6.7167, "longitude": 1.8333, "altitude": 100, "pays": "Bénin"},
        {"nom": "Littoral", "latitude": 6.4231, "longitude": 2.6199, "altitude": 50, "pays": "Bénin"},
        {"nom": "Mono", "latitude": 6.7833, "longitude": 1.9833, "altitude": 20, "pays": "Bénin"},
        {"nom": "Ouémé", "latitude": 6.4833, "longitude": 2.6167, "altitude": 50, "pays": "Bénin"},
        {"nom": "Plateau", "latitude": 6.6167, "longitude": 2.6167, "altitude": 70, "pays": "Bénin"},
        {"nom": "Zou", "latitude": 7.3833, "longitude": 2.0833, "altitude": 200, "pays": "Bénin"}
    ],
    "Burkina Faso": [
        {"nom": "Boucle du Mouhoun", "latitude": 12.6700, "longitude": -3.0500, "altitude": 300, "pays": "Burkina Faso"},
        {"nom": "Cascades", "latitude": 10.5000, "longitude": -4.9167, "altitude": 200, "pays": "Burkina Faso"},
        {"nom": "Centre", "latitude": 12.3500, "longitude": -1.5333, "altitude": 300, "pays": "Burkina Faso"},
        {"nom": "Centre-Est", "latitude": 12.1000, "longitude": -0.3500, "altitude": 280, "pays": "Burkina Faso"},
        {"nom": "Centre-Nord", "latitude": 13.0000, "longitude": -1.1000, "altitude": 350, "pays": "Burkina Faso"},
        {"nom": "Centre-Ouest", "latitude": 12.3000, "longitude": -2.1500, "altitude": 320, "pays": "Burkina Faso"},
        {"nom": "Centre-Sud", "latitude": 11.4000, "longitude": -1.5000, "altitude": 330, "pays": "Burkina Faso"},
        {"nom": "Est", "latitude": 11.0000, "longitude": 0.5000, "altitude": 280, "pays": "Burkina Faso"},
        {"nom": "Hauts-Bassins", "latitude": 11.2000, "longitude": -4.2000, "altitude": 400, "pays": "Burkina Faso"},
        {"nom": "Nord", "latitude": 14.0000, "longitude": -1.2500, "altitude": 350, "pays": "Burkina Faso"},
        {"nom": "Plateau-Central", "latitude": 12.1500, "longitude": -1.3500, "altitude": 310, "pays": "Burkina Faso"},
        {"nom": "Sahel", "latitude": 14.1000, "longitude": -0.2500, "altitude": 380, "pays": "Burkina Faso"},
        {"nom": "Sud-Ouest", "latitude": 10.7000, "longitude": -3.1500, "altitude": 250, "pays": "Burkina Faso"}
    ],
    "Côte d'Ivoire": [
        {"nom": "Bas-Sassandra", "latitude": 5.3667, "longitude": -6.6333, "altitude": 20, "pays": "Côte d'Ivoire"},
        {"nom": "Comoé", "latitude": 8.2500, "longitude": -3.8500, "altitude": 200, "pays": "Côte d'Ivoire"},
        {"nom": "Denguélé", "latitude": 9.5000, "longitude": -7.2500, "altitude": 300, "pays": "Côte d'Ivoire"},
        {"nom": "Dix-Huit Montagnes", "latitude": 7.3667, "longitude": -8.1333, "altitude": 250, "pays": "Côte d'Ivoire"},
        {"nom": "Gôh", "latitude": 6.9333, "longitude": -5.7500, "altitude": 120, "pays": "Côte d'Ivoire"},
        {"nom": "Lacs", "latitude": 6.7833, "longitude": -4.9167, "altitude": 150, "pays": "Côte d'Ivoire"},
        {"nom": "Lagunes", "latitude": 5.3500, "longitude": -4.0833, "altitude": 10, "pays": "Côte d'Ivoire"},
        {"nom": "Montagnes", "latitude": 7.9167, "longitude": -7.6000, "altitude": 400, "pays": "Côte d'Ivoire"},
        {"nom": "Sassandra-Marahoué", "latitude": 6.3000, "longitude": -6.6333, "altitude": 120, "pays": "Côte d'Ivoire"},
        {"nom": "Savanes", "latitude": 9.7333, "longitude": -5.5667, "altitude": 250, "pays": "Côte d'Ivoire"},
        {"nom": "Vallée du Bandama", "latitude": 8.0833, "longitude": -5.3500, "altitude": 220, "pays": "Côte d'Ivoire"},
        {"nom": "Worodougou", "latitude": 8.1667, "longitude": -7.2500, "altitude": 300, "pays": "Côte d'Ivoire"},
        {"nom": "Yamoussoukro", "latitude": 6.8167, "longitude": -5.2833, "altitude": 200, "pays": "Côte d'Ivoire"},
        {"nom": "Haut-Sassandra", "latitude": 7.4333, "longitude": -6.9167, "altitude": 320, "pays": "Côte d'Ivoire"},
        {"nom": "Bélier", "latitude": 7.6000, "longitude": -5.2500, "altitude": 220, "pays": "Côte d'Ivoire"},
        {"nom": "Iffou", "latitude": 7.0833, "longitude": -5.1167, "altitude": 280, "pays": "Côte d'Ivoire"},
        {"nom": "Moronou", "latitude": 6.9000, "longitude": -3.9000, "altitude": 350, "pays": "Côte d'Ivoire"},
        {"nom": "Gbôklé", "latitude": 5.2167, "longitude": -6.4000, "altitude": 20, "pays": "Côte d'Ivoire"},
        {"nom": "Nawa", "latitude": 5.0167, "longitude": -6.6667, "altitude": 15, "pays": "Côte d'Ivoire"}
    ],
    "Guinée-Bissau": [
        {"nom": "Bafatá", "latitude": 12.1833, "longitude": -14.6667, "altitude": 60, "pays": "Guinée-Bissau"},
        {"nom": "Biombo", "latitude": 11.8333, "longitude": -15.5833, "altitude": 30, "pays": "Guinée-Bissau"},
        {"nom": "Bissau", "latitude": 11.8667, "longitude": -15.5833, "altitude": 5, "pays": "Guinée-Bissau"},
        {"nom": "Bolama", "latitude": 11.5833, "longitude": -15.4167, "altitude": 10, "pays": "Guinée-Bissau"},
        {"nom": "Cacheu", "latitude": 12.0667, "longitude": -16.1833, "altitude": 25, "pays": "Guinée-Bissau"},
        {"nom": "Gabú", "latitude": 12.2833, "longitude": -14.2333, "altitude": 100, "pays": "Guinée-Bissau"},
        {"nom": "Oio", "latitude": 12.1500, "longitude": -15.2500, "altitude": 80, "pays": "Guinée-Bissau"}
    ],
    "Mali": [
        {"nom": "Kayes", "latitude": 14.4500, "longitude": -11.4333, "altitude": 100, "pays": "Mali"},
        {"nom": "Koulikoro", "latitude": 12.8667, "longitude": -8.4333, "altitude": 350, "pays": "Mali"},
        {"nom": "Sikasso", "latitude": 11.3167, "longitude": -5.6667, "altitude": 400, "pays": "Mali"},
        {"nom": "Ségou", "latitude": 13.4500, "longitude": -6.2667, "altitude": 290, "pays": "Mali"},
        {"nom": "Mopti", "latitude": 14.4800, "longitude": -4.2000, "altitude": 300, "pays": "Mali"},
        {"nom": "Tombouctou", "latitude": 16.7667, "longitude": -3.0000, "altitude": 260, "pays": "Mali"},
        {"nom": "Gao", "latitude": 16.2667, "longitude": 0.0500, "altitude": 270, "pays": "Mali"},
        {"nom": "Kidal", "latitude": 18.4414, "longitude": 1.3958, "altitude": 600, "pays": "Mali"},
        {"nom": "Bamako", "latitude": 12.6392, "longitude": -8.0029, "altitude": 350, "pays": "Mali"}
    ],
    "Niger": [
        {"nom": "Agadez", "latitude": 16.9760, "longitude": 7.9833, "altitude": 480, "pays": "Niger"},
        {"nom": "Diffa", "latitude": 13.3156, "longitude": 12.6119, "altitude": 300, "pays": "Niger"},
        {"nom": "Dosso", "latitude": 13.0531, "longitude": 3.1833, "altitude": 230, "pays": "Niger"},
        {"nom": "Maradi", "latitude": 13.5000, "longitude": 7.1000, "altitude": 350, "pays": "Niger"},
        {"nom": "Tahoua", "latitude": 14.8967, "longitude": 5.2681, "altitude": 380, "pays": "Niger"},
        {"nom": "Tillabéri", "latitude": 14.2300, "longitude": 1.4500, "altitude": 280, "pays": "Niger"},
        {"nom": "Zinder", "latitude": 13.8000, "longitude": 8.9833, "altitude": 470, "pays": "Niger"},
        {"nom": "Niamey", "latitude": 13.5167, "longitude": 2.1167, "altitude": 207, "pays": "Niger"}
    ],
    "Togo": [
        {"nom": "Centrale", "latitude": 8.6167, "longitude": 1.1667, "altitude": 220, "pays": "Togo"},
        {"nom": "Kara", "latitude": 9.5500, "longitude": 1.2000, "altitude": 300, "pays": "Togo"},
        {"nom": "Maritime", "latitude": 6.1328, "longitude": 1.2158, "altitude": 70, "pays": "Togo"},
        {"nom": "Plateaux", "latitude": 7.5333, "longitude": 1.8500, "altitude": 350, "pays": "Togo"},
        {"nom": "Savanes", "latitude": 10.3500, "longitude": 0.8333, "altitude": 200, "pays": "Togo"}
    ]
}


# ------------------ Fonctions Utilitaires ------------------

def fetch_historical_weather(lat, lon, start_date, end_date):
    """
    Interroge l'API Open-Meteo Archive pour récupérer les données météo historiques.
    """
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "hourly": ",".join(HOURLY_VARIABLES),
        "timezone": "Africa/Abidjan"
    }
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logging.error(f"Erreur lors de la requête API pour [{lat}, {lon}] : {e}")
        return None


def insert_record(conn, record):
    """
    Insère un enregistrement météo en base, sans doublon.
    """
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO meteo_uemoa (
                    pays, region, latitude, longitude, altitude, observation_time,
                    temperature_2m, relativehumidity_2m, dewpoint_2m, pressure_msl,
                    windspeed_10m, winddirection_10m, precipitation, weathercode,
                    cloudcover, visibility, shortwave_radiation, snowfall
                ) VALUES (
                    %(pays)s, %(region)s, %(latitude)s, %(longitude)s, %(altitude)s, %(observation_time)s,
                    %(temperature_2m)s, %(relativehumidity_2m)s, %(dewpoint_2m)s, %(pressure_msl)s,
                    %(windspeed_10m)s, %(winddirection_10m)s, %(precipitation)s, %(weathercode)s,
                    %(cloudcover)s, %(visibility)s, %(shortwave_radiation)s, %(snowfall)s
                )
                ON CONFLICT (pays, region, observation_time) DO NOTHING
            """, record)
    except Exception as e:
        logging.error(f"Erreur insertion en base : {e}")


def export_to_csv(records, csv_path):
    """
    Exporte les données consolidées dans un fichier CSV sans doublon.
    """
    try:
        df_new = pd.DataFrame(records)

        if os.path.exists(csv_path):
            df_existing = pd.read_csv(csv_path)
            df_combined = pd.concat([df_existing, df_new], ignore_index=True)
            df_combined.drop_duplicates(subset=["pays", "region", "observation_time"], inplace=True)
        else:
            df_combined = df_new

        df_combined.to_csv(csv_path, index=False)
        logging.info(f"Export CSV terminé : {len(df_combined)} lignes dans '{csv_path}'")

    except Exception as e:
        logging.error(f"Erreur lors de l'export CSV : {e}")


# ------------------ Fonction Principale ------------------

def main():
    """
    Orchestrateur du processus de collecte et de stockage des données météo archivées.
    """
    logging.info("Démarrage de la collecte historique météo UEMOA...")

    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = True
    except Exception as e:
        logging.error(f"Connexion à la base échouée : {e}")
        return
    

    start_date = datetime(2021, 1, 1)
    end_date = datetime(2025, 10, 27)
    all_records = []



    try:
        for pays, regions in REGIONS.items():
            for region in regions:
                logging.info(f"Collecte {pays} - {region['nom']} en cours...")

                data = fetch_historical_weather(
                    region["latitude"], region["longitude"], start_date, end_date
                )

                if not data or "hourly" not in data:
                    logging.warning(f"Aucune donnée pour {region['nom']}")
                    continue

                times = data["hourly"].get("time", [])

                for idx, obs_time in enumerate(times):
                    record = {
                        "pays": pays,
                        "region": region["nom"],
                        "latitude": region["latitude"],
                        "longitude": region["longitude"],
                        "altitude": region["altitude"],
                        "observation_time": obs_time
                    }
                    for var in HOURLY_VARIABLES:
                        record[var] = data["hourly"].get(var, [None] * len(times))[idx]

                    insert_record(conn, record)
                    all_records.append(record)

                logging.info(f"Collecte terminée pour {region['nom']}")
                time.sleep(1)

    except Exception as e:
        logging.error(f"Erreur lors du traitement : {e}")

    finally:
        conn.close()
        logging.info("Connexion à la base fermée")

    if all_records:
        export_to_csv(all_records, CSV_PATH)
    else:
        logging.warning("Aucune donnée à exporter")


# ------------------ Point d'entrée ------------------

if __name__ == "__main__":
   main()
