-- Création de la base de données climat_uemoa
-- (À exécuter dans psql ou pgAdmin, hors d'une connexion à une base spécifique)
-- CREATE DATABASE climat_uemoa;

-- Se connecter à la base climat_uemoa
-- \c climat_uemoa;

-- Création de la table brute source : meteo_uemoa
CREATE TABLE meteo_uemoa (
    id SERIAL PRIMARY KEY,
    pays VARCHAR(50) NOT NULL,
    region VARCHAR(100) NOT NULL,
    latitude NUMERIC(8,5) NOT NULL,
    longitude NUMERIC(8,5) NOT NULL,
    altitude INTEGER NOT NULL,
    observation_time TIMESTAMP NOT NULL,
    temperature_2m REAL,
    relativehumidity_2m REAL,
    dewpoint_2m REAL,
    pressure_msl REAL,
    windspeed_10m REAL,
    winddirection_10m REAL,
    precipitation REAL,
    weathercode INTEGER,
    cloudcover INTEGER,
    visibility REAL,
    shortwave_radiation REAL,
    snowfall REAL,
    collecte_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Création des index pour optimiser les recherches
CREATE INDEX idx_observation_time ON meteo_uemoa (observation_time);
CREATE INDEX idx_region ON meteo_uemoa (region);
CREATE INDEX idx_pays ON meteo_uemoa (pays);

-- Ajout d’une contrainte pour empêcher les doublons sur (pays, region, observation_time)
ALTER TABLE meteo_uemoa
ADD CONSTRAINT unique_station_time UNIQUE (pays, region, observation_time);
