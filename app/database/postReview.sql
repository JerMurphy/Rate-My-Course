DELIMITER //
DROP PROCEDURE IF EXISTS postReview;

CREATE PROCEDURE postReview(IN reviewIN varchar(500), IN tough_ratingIn int, IN courseload_ratingIn int, IN usefulness_ratingIn int, IN exam_boolIn BOOLEAN, IN courseIdIn varchar(10), IN postedByIn varchar(64))
BEGIN
 INSERT INTO reviews(review, tough_rating, courseload_rating, usefulness_rating, exam_bool, courseId, postedBy) 
        VALUES (reviewIn, tough_ratingIn, courseload_ratingIn, usefulness_ratingIn, exam_boolIn, courseIdIn, postedByIn);
END //
DELIMITER ;
