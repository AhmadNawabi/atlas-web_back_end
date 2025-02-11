-- Task 3 lists all bands with Glam rock as their style.
-- ranked by their longevity, order by the number of fans.
SELECT band_name, (IFNULL(split, 2020) - formed) AS lifespan
FROM metal_bands
WHERE style LIKE "%Glam rock%"
ORDER BY lifespan DESC;
