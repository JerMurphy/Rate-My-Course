DROP TABLE IF EXISTS reviews;

CREATE TABLE reviews (
	pk int NOT NULL AUTO_INCREMENT PRIMARY KEY, /*example: 4 */
	review varchar(500), /*example: this course sucks */
	tough_rating float NOT NULL, /*example: 4.87 */
	courseload_rating float NOT NULL,
	usefulness_rating float NOT NULL,
	exam_bool BOOLEAN NOT NULL, /*example: true/false */
	courseID varchar(10) NOT NULL, /*example: 1013 */
	postedBy varchar(100) NOT NULL, /*example: jmurphy1 (username) */
	CONSTRAINT 'fk_course_id' FOREIGN KEY (courseID) REFERENCES courses (id)
);
