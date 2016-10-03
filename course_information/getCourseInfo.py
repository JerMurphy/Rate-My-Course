from bs4 import BeautifulSoup

soup1 = BeautifulSoup(open("Fredericton_2016_Summer_CS_INFO.html"), 'html.parser')
soup2 = BeautifulSoup(open("Fredericton_2016_Fall_CS_INFO.html"), 'html.parser')
soup3 = BeautifulSoup(open("Fredericton_2017_Winter_CS_INFO.html"), 'html.parser')

def getCourseInfo(soup):
	courseInfo = {}
	numberOfCourses = 0

	#get number of courses
	for course in soup.find_all(lambda tag: tag.name == 'td' and tag.get('class') == ['ms-SrvMenuUI']):
		numberOfCourses = numberOfCourses + 1

	#extract information out of course html
	for i in range(1,numberOfCourses+1):
		courseHTML = "SEC_SHORT_TITLE_" + str(i)
		professorHTML = "SEC_FACULTY_INFO_" + str(i)

		rawCourse = soup.find(id=courseHTML).text
		courseID = ""
		courseName = ""
		professor = soup.find(id=professorHTML).text

		#get course ID from string
		index = 0
		starCounter = 0
		while starCounter < 2:
			if rawCourse[index] == "*":
				starCounter += 1
			else:
				courseID += rawCourse[index]
			index += 1

		#get course name from string
		courseName += " ".join(rawCourse.split()[2:len(rawCourse.split())])

		#ignore cscoop and cspep
		if (courseID != "CSCOOP") and (courseID != "CSPEP"):
			print courseID
			print courseName
			print professor


if __name__ == "__main__":
	getCourseInfo(soup1) #Summer 2016
	getCourseInfo(soup2) #Fall 2016
	getCourseInfo(soup3) #Winter 2017