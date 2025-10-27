import psycopg2
import logging

# Logging basique
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Connexion BDD
DB_NAME = "climat_uemoa"
DB_USER = "postgres"
DB_PASSWORD = "passer"
DB_HOST = "host.docker.internal"
DB_PORT = 5433 

# Requêtes séparées
sql_dimension_date = """
INSERT INTO dimension_date (date, jour, mois, annee, trimestre, saison)
SELECT DISTINCT 
    DATE(observation_time),
    EXTRACT(DAY FROM observation_time)::INT,
    EXTRACT(MONTH FROM observation_time)::INT,
    EXTRACT(YEAR FROM observation_time)::INT,
    EXTRACT(QUARTER FROM observation_time)::INT,
    CASE 
        WHEN EXTRACT(MONTH FROM observation_time) IN (12, 1, 2) THEN 'Hiver'
        WHEN EXTRACT(MONTH FROM observation_time) IN (3, 4, 5) THEN 'Printemps'
        WHEN EXTRACT(MONTH FROM observation_time) IN (6, 7, 8) THEN 'Été'
        ELSE 'Automne'
    END AS saison
FROM meteo_uemoa
ON CONFLICT (date) DO NOTHING;
"""

sql_fact_meteo = """
INSERT INTO fact_meteo (
    id_dim_station, date, weathercode, observation_time,
    temperature_2m, relativehumidity_2m, dewpoint_2m, pressure_msl,
    windspeed_10m, winddirection_10m, precipitation, cloudcover,
    visibility, shortwave_radiation, snowfall
)
SELECT
    s.id_dim_station,
    DATE(m.observation_time),
    m.weathercode,
    m.observation_time,
    m.temperature_2m, m.relativehumidity_2m, m.dewpoint_2m, m.pressure_msl,
    m.windspeed_10m, m.winddirection_10m, m.precipitation, m.cloudcover,
    m.visibility, m.shortwave_radiation, m.snowfall
FROM meteo_uemoa m
JOIN dimension_station s ON m.pays = s.pays AND m.region = s.region
JOIN dimension_date d ON DATE(m.observation_time) = d.date
ON CONFLICT (id_dim_station, observation_time) DO NOTHING;
"""

def update_dimensions_facts(cible='all'):
    """Mise à jour ciblée : dimension_date, fact_meteo ou les deux."""
    conn = None
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
        )
        conn.autocommit = True
        with conn.cursor() as cur:
            if cible in ('dimension_date', 'all'):
                cur.execute(sql_dimension_date)
                logging.info("Dimension date mise à jour avec succès.")
            
            if cible in ('fact_meteo', 'all'):
                cur.execute(sql_fact_meteo)
                logging.info("Faits météo mis à jour avec succès.")
    
    except Exception as e:
        logging.error(f"Erreur lors de la mise à jour : {e}")
        raise
    finally:
        if conn:
            conn.close()

# Test/debug local
if __name__ == "__main__":
    update_dimensions_facts('all')
