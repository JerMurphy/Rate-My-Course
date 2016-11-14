import MySQLdb

#connect to database
db = MySQLdb.connect(host='localhost',user='jmurray2',passwd='Mjm12RmR',db='jmurray2')
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
    sql_insert = (
      "INSERT INTO courses (id, name, prof) "
      "VALUES(%s,%s,%s)"
    )
    data = (course[0],course[1],course[2])
    cursor.execute(sql_insert, data)
    db.commit()
  except:
    db.rollback()

f.close() #close reader