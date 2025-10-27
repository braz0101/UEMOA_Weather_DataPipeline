-- Dimension Station (stations météo de l'UEMOA)
CREATE TABLE dimension_station (
    id_dim_station SERIAL PRIMARY KEY,
    pays VARCHAR(50),
    region VARCHAR(100),
    latitude NUMERIC(8,5),
    longitude NUMERIC(8,5),
    altitude INTEGER,
    UNIQUE (pays, region) -- Garantie d'une station unique par région
);

-- Dimension Date (analyse temporelle)
CREATE TABLE dimension_date (
    date DATE PRIMARY KEY,
    jour INTEGER,
    mois INTEGER,
    annee INTEGER,
    trimestre INTEGER,
    saison VARCHAR(20)
);

-- Dimension Condition (codes météo standardisés)
CREATE TABLE dimension_condition (
    weathercode INTEGER PRIMARY KEY,
    description VARCHAR(100)
);

-- Table de Faits Météo (mesures consolidées)
CREATE TABLE fact_meteo (
    id_fact SERIAL PRIMARY KEY,
    id_dim_station INTEGER REFERENCES dimension_station(id_dim_station),
    date DATE REFERENCES dimension_date(date),
    weathercode INTEGER REFERENCES dimension_condition(weathercode),
    observation_time TIMESTAMP,
    temperature_2m REAL,
    relativehumidity_2m REAL,
    dewpoint_2m REAL,
    pressure_msl REAL,
    windspeed_10m REAL,
    winddirection_10m REAL,
    precipitation REAL,
    cloudcover INTEGER,
    visibility REAL,
    shortwave_radiation REAL,
    snowfall REAL
);

