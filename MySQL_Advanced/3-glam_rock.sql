-- Old school band
SELECT band_name, 
       COALESCE(YEAR(split), YEAR(NOW())) - YEAR(formed) AS lifespan
FROM metal_bands
WHERE main_style LIKE '%Glam rock%'
ORDER BY lifespan DESC;
