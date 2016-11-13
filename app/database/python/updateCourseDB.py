import MySQLdb

#connect to database
db = MySQLdb.connect(host='info3103.cs.unb.ca',user='jmurray2',passwd='Mjm12RmR',db='courses')
cursor = db.cursor()

#open file and save first line
f = open("courseInfo.txt", "r")
line = f.readline()

#while lines in the file exist
while line:
  course = []

  #iterate through data (0:id, 1: name, 2:prof)
  for i in range(0,3):
    course.append(line)
    line = f.readline() #f++

  #data entry
  try:
    cursor.execute("INSERT INTO courses(\"id\") VALUES(%s)",(course[0]))
    cursor.execute("INSERT INTO courses(\"name\") VALUES(%s)",(course[1]))
    cursor.execute("INSERT INTO courses(\"professor\") VALUES(%s)",(course[2]))
    db.commit()
  except:
    conn.rollback()

f.close() #close reader