-- Lists all bands with Glam rock as their main style, ranked by longevity

SELECT band_name, 
       COALESCE(YEAR(split) - YEAR(formed), YEAR(NOW()) - YEAR(formed)) AS lifespan
FROM metal_bands
WHERE main_style = 'Glam rock'
ORDER BY lifespan DESC;
