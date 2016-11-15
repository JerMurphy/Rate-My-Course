DROP TABLE IF EXISTS courses;

CREATE TABLE courses (
  id varchar(8) NOT NULL PRIMARY KEY,
	subject varchar(4) NOT NULL, /* example: CS1013 */ 
	num varchar(4) NOT NULL, /* example: Intro to Java I */
	name varchar(64) NOT NULL /* example: Natalie Webber, we should try and make this a list somehow */
);