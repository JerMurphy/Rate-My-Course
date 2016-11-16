DELIMITER //
DROP PROCEDURE IF EXISTS getSpecReviews;

CREATE PROCEDURE getSpecReviews(IN courseIdIn varchar(10))
BEGIN
  SELECT *
    FROM reviews
          WHERE courseID = courseIdIn;
END //
DELIMITER ;
