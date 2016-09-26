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

		course = soup.find(id=courseHTML).text
		professor = soup.find(id=professorHTML).text

		print course
		print professor

	#TODO
	#parse course and professor and add them to courseInfo dictionary

if __name__ == "__main__":
	getCourseInfo(soup1) #Summer 2016
	getCourseInfo(soup2) #Fall 2016
	getCourseInfo(soup3) #Winter 2017