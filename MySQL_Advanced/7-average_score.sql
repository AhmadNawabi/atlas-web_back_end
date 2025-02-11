-- Task 7 cerates a sotred procedure ComputeAverageScoreForUser that computes
-- and store the average score for a student. An average score can be a decimal
DELIMITER //
CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
    DECLARE average_score FLOAT;
    -- Compute the average score
    SELECT AVG(score) INTO average_score FROM corrections WHERE corrections.user_id = user_id;
    -- Update the average score
    UPDATE users SET average_score = average_score WHERE id = user_id;
END;
//
DELIMITER ;
