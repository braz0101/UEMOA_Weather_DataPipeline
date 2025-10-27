-- Chargement dimension station (extrait unique des stations)
INSERT INTO dimension_station (pays, region, latitude, longitude, altitude)
SELECT DISTINCT pays, region, latitude, longitude, altitude
FROM meteo_uemoa
ON CONFLICT (pays, region) DO NOTHING;

-- Chargement dimension date (extrait unique des dates, calcul attributs)
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

-- Chargement dimension condition météo (à faire une fois) --

INSERT INTO dimension_condition (weathercode, description) VALUES
(0, 'Ciel dégagé'),
(1, 'Principalement ensoleillé'),
(2, 'Partiellement nuageux'),
(3, 'Couvert'),
(45, 'Brouillard'),
(48, 'Brouillard givrant'),
(51, 'Bruine légère'),
(53, 'Bruine modérée'),
(55, 'Bruine dense'),
(56, 'Bruine verglaçante légère'),
(57, 'Bruine verglaçante dense'),
(61, 'Pluie faible'),
(63, 'Pluie modérée'),
(65, 'Pluie forte'),
(66, 'Pluie verglaçante légère'),
(67, 'Pluie verglaçante forte'),
(71, 'Neige faible'),
(73, 'Neige modérée'),
(75, 'Neige forte'),
(77, 'Grains de neige'),
(80, 'Averses de pluie faibles'),
(81, 'Averses de pluie modérées'),
(82, 'Averses de pluie violentes'),
(85, 'Averses de neige faibles'),
(86, 'Averses de neige fortes'),
(95, 'Orage (léger ou modéré)'),
(96, 'Orage avec grêle légère'),
(99, 'Orage avec grêle forte');

-- Chargement de la table de faits
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
JOIN dimension_date d ON DATE(m.observation_time) = d.date;

-- Après pour charger des données actualisées tout en évitant les doublons, on utilise ON CONFLICT DO NOTHING --

-- Ajoute une contrainte d’unicité sur la table de faits (Faire une fois) --
ALTER TABLE fact_meteo
ADD CONSTRAINT unique_fait_station_time UNIQUE (id_dim_station, observation_time);
