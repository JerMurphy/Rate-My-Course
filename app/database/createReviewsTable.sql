DROP TABLE IF EXISTS reviews;

CREATE TABLE reviews (
  id int NOT NULL AUTO_INCREMENT,
  review varchar(500), /*example: this course sucks */
  tough_rating int NOT NULL, /*example: 4/5 */
  courseload_rating int NOT NULL, /*example: 2/5 */
  usefulness_rating int NOT NULL, /*example: 3/5 */
  exam_bool BOOLEAN NOT NULL, /*example: true/false */
  courseId varchar(8) NOT NULL, /*example: CS1073 */
  postedBy varchar(64) NOT NULL, /*example: jmurphy1 (username) */
  PRIMARY KEY (id),
  FOREIGN KEY (courseId) REFERENCES courses(id)
);
