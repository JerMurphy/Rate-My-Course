DELIMITER //
DROP PROCEDURE IF EXISTS deleteReview;

CREATE PROCEDURE deleteReview(IN id_in int)
BEGIN
  DELETE
    FROM reviews
      WHERE id = id_in;
END //
DELIMITER ;
