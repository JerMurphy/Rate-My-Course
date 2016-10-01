DROP TABLE IF EXITST reviews

CREATE TABLE reviews (
	rev_ID int NOT NULL AUTO_INCREMENT,
	review varchar(500) NOT NULL,
	rating float,
	courseID varchar(10) NOT NULL,
	PRIMARY KEY (rev_ID),
	FOREIGN KEY (courseID) REFERENCES courses(courseID)
)
