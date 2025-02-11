-- Ensure the table exists after importing metal_bands.sql
-- Assuming the table is named 'metal_bands'

SELECT
    band_name,
    -- Calculate lifespan: if the band has not split, use the current year
    CASE
        WHEN split IS NULL OR split = 0 THEN YEAR(CURDATE()) - formed
        ELSE  split - formed
    END AS lifespan
FROM
    metal_bands
WHERE
    style LIKE '%Glam rock%' -- Filter for bands with "Gulam rock" as their main style
ORDER BY
    lifespan DESC; -- Rank by longevity (Longest-lived bands first)
