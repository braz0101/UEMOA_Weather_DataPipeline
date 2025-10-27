------------------------------------------
-- Requêtes d’Analyse pour validation fonctionnelle de l’entrepôt
------------------------------------------

-- 1. Température moyenne & précipitations totales par région
SELECT 
    ds.region,
    ROUND(AVG(f.temperature_2m)::NUMERIC, 2) AS "Température moyenne (°C)",
    ROUND(SUM(f.precipitation)::NUMERIC, 2) AS "Précipitations totales (mm)"
FROM fact_meteo f
JOIN dimension_station ds ON f.id_dim_station = ds.id_dim_station
GROUP BY ds.region
ORDER BY ds.region;

-- 2. Top 3 des stations les plus chaudes
SELECT 
    ds.region, 
    ds.pays, 
    MAX(f.temperature_2m) AS "Température max enregistrée (°C)"
FROM fact_meteo f
JOIN dimension_station ds ON f.id_dim_station = ds.id_dim_station
GROUP BY ds.region, ds.pays
ORDER BY "Température max enregistrée (°C)" DESC
LIMIT 3;

-- 3. Mois les plus pluvieux en 2023
SELECT 
    dd.mois,
    ROUND(SUM(f.precipitation)::NUMERIC, 2) AS "Total précipitations (mm)"
FROM fact_meteo f
JOIN dimension_date dd ON f.date = dd.date
WHERE dd.annee = 2023
GROUP BY dd.mois
ORDER BY "Total précipitations (mm)" DESC
LIMIT 3;

-- 4. Vitesse moyenne du vent par région et saison (2023)
SELECT 
    ds.region,
    dd.saison,
    ROUND(AVG(f.windspeed_10m)::NUMERIC, 2) AS "Vitesse moyenne du vent (m/s)"
FROM fact_meteo f
JOIN dimension_station ds ON f.id_dim_station = ds.id_dim_station
JOIN dimension_date dd ON f.date = dd.date
WHERE dd.annee = 2023
GROUP BY ds.region, dd.saison
ORDER BY ds.region, dd.saison;

-- 5. Nombre total de jours avec précipitations > 0 par région en 2023
SELECT 
    ds.region,
    COUNT(DISTINCT dd.date) AS "Nombre de jours pluvieux"
FROM fact_meteo f
JOIN dimension_station ds ON f.id_dim_station = ds.id_dim_station
JOIN dimension_date dd ON f.date = dd.date
WHERE f.precipitation > 0 AND dd.annee = 2023
GROUP BY ds.region
ORDER BY "Nombre de jours pluvieux" DESC;

-- 6. Température minimale enregistrée par pays et région en 2023
SELECT 
    ds.pays,
    ds.region,
    MIN(f.temperature_2m) AS "Température minimale (°C)"
FROM fact_meteo f
JOIN dimension_station ds ON f.id_dim_station = ds.id_dim_station
JOIN dimension_date dd ON f.date = dd.date
WHERE dd.annee = 2023
GROUP BY ds.pays, ds.region
ORDER BY "Température minimale (°C)";

-- 7. Moyenne de la couverture nuageuse par région par mois en 2023
SELECT 
    ds.region,
    dd.mois,
    ROUND(AVG(f.cloudcover)::NUMERIC, 2) AS "Couverture nuageuse moyenne (%)"
FROM fact_meteo f
JOIN dimension_station ds ON f.id_dim_station = ds.id_dim_station
JOIN dimension_date dd ON f.date = dd.date
WHERE dd.annee = 2023
GROUP BY ds.region, dd.mois
ORDER BY ds.region, dd.mois;

-- 8. Somme totale de l’énergie radiative reçue (shortwave radiation) par région en 2023
SELECT 
    ds.region,
    ROUND(SUM(f.shortwave_radiation)::NUMERIC, 2) AS "Énergie radiative totale (W/m²)"
FROM fact_meteo f
JOIN dimension_station ds ON f.id_dim_station = ds.id_dim_station
JOIN dimension_date dd ON f.date = dd.date
WHERE dd.annee = 2023
GROUP BY ds.region
ORDER BY "Énergie radiative totale (W/m²)" DESC;

-- 9. Analyse des conditions météorologiques par région avec description (2023)
SELECT
    ds.region,
    f.weathercode,
    dc.description AS "Condition météo",
    COUNT(*) AS occurrences
FROM fact_meteo f
JOIN dimension_station ds ON f.id_dim_station = ds.id_dim_station
JOIN dimension_date dd ON f.date = dd.date
JOIN dimension_condition dc ON f.weathercode = dc.weathercode
WHERE dd.annee = 2023
GROUP BY ds.region, f.weathercode, dc.description
ORDER BY ds.region, occurrences DESC;
