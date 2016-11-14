DROP TABLE IF EXISTS courses;

CREATE TABLE courses (
  pk int NOT NULL AUTO_INCREMENT,
	id varchar(10) NOT NULL, /* example: CS1013 */ 
	name varchar(64) NOT NULL, /* example: Intro to Java I */
	prof varchar(500) NOT NULL, /* example: Natalie Webber, we should try and make this a list somehow */
	PRIMARY KEY (pk)
);
