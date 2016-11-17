DELIMITER //
DROP PROCEDURE IF EXISTS getSpecCourses;

CREATE PROCEDURE getSpecCourses(IN subjectIn varchar(4))
BEGIN
  SELECT *
    FROM courses
          WHERE subject = subjectIn;
END //
DELIMITER ;
