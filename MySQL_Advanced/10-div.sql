-- 10-div.sql
DELIMITER $$

CREATE FUNCTION SafeDive(a INT, b INT) RETURNS FLOAT DETERMINISTIC
BEGIN
    -- Check if the dicisor is 0
    IF b = 0 THEN
        RETURN 0;
    ELSE
        RETURN a / b;
    END IF;
END$$

DELIMITER;
