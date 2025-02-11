-- Task 3: Lists all bands with Glam rock as their style.
-- Ranked by their longevity (lifespan), ordered by lifespan in descending order.

SELECT 
    band_name,
    -- Calculate lifespan: Use 2022 as the current year for active bands
    CASE 
        WHEN split IS NULL OR split = 0 THEN 2022 - formed
        ELSE split - formed
    END AS lifespan
FROM 
    metal_bands
WHERE 
    style LIKE '%Glam rock%' -- Filter for bands with "Glam rock" as their main style
ORDER BY 
    lifespan DESC; -- Rank by longevity (longest-lived bands first)
