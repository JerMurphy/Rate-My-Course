DROP TABLE IF EXISTS courses

CREATE TABLE courses (
	courseID varchar(4) NOT NULL, /* example: 1013 */
	subject varchar(5) NOT NULL, /* example: CS */
	course varchar(10) NOT NULL, /* example: CS1013 */ 
	name varchar(32) NOT NULL, /* example: Intro to Java I */
	professor varchar(500) NOT NULL, /* example: Natalie Webber, we should try and make this a list somehow */
	PRIMARY KEY (courseID)
);
