DROP TABLE IF EXISTS courses;

CREATE TABLE courses (
  id varchar(8) NOT NULL PRIMARY KEY, /* example: CS1073 */ 
	subject varchar(4) NOT NULL, /* example: CS */ 
	num varchar(4) NOT NULL, /* example: 1073*/
	name varchar(64) NOT NULL /* example: Intro to Java I */
);