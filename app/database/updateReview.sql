DELIMITER //
DROP PROCEDURE IF EXISTS updateReview;

CREATE PROCEDURE updateReview(IN reviewIN varchar(500), IN tough_ratingIn int, IN courseload_ratingIn int, IN usefulness_ratingIn int, IN exam_boolIn BOOLEAN, IN courseIdIn varchar(10),IN reviewIdIn int)
BEGIN
 UPDATE reviews SET review = reviewIn, tough_rating = tough_ratingIN, courseload_rating = courseload_ratingIn, usefulness_rating = usefulness_ratingIn, exam_bool = exam_boolIn, courseId = courseIdIn 
	WHERE id = reviewIdIn;
END //
DELIMITER ;
