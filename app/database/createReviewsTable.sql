DROP TABLE IF EXISTS reviews

CREATE TABLE reviews (
	reviewID int NOT NULL AUTO_INCREMENT,
	review varchar(500),
	rating float NOT NULL,
	courseID varchar(10) NOT NULL,
	PRIMARY KEY (reviewID),
	FOREIGN KEY (courseID) REFERENCES courses(courseID)
)
