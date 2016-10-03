DROP TABLE IF EXISTS courses
CREATE TABLE courses (
	id varchar(8) NOT NULL,
	name varchar(32) NOT NULL,
	professor varchar(32) NOT NULL,
	PRIMARY KEY (courseID)
);