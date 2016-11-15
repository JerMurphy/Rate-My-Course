import MySQLdb
#import json

#insert a list[id, subject, num, name] into db
def insert_into_db(course):
  #data entry
  try:
    sql_insert = (
      "INSERT INTO courses (id, subject, num, name) "
      "VALUES(%s,%s,%s,%s)"
    )
    data = (course[0],course[1],course[2],course[3])
    #print json.dumps(course)
    cursor.execute(sql_insert, data)
    db.commit()
  except:
    #pass
    db.rollback()


if __name__ == "__main__":
  #connect to database
  db = MySQLdb.connect(host='localhost',user='jmurray2',passwd='Mjm12RmR',db='jmurray2')
  cursor = db.cursor()

  #open file and save first line
  f = open("courseInfo.txt", "r")
  data = f.read().splitlines()

  #iterate through data (id, subject, courseNum, name)
  data_index = 0
  while (data_index < len(data)):
    #every 4 index's is a new course
    if (data_index % 4) == 0:
      if data_index != 0: #edge case
        insert_into_db(course) #insert list into db
      course = []
    course.append(data[data_index])
    data_index += 1

  f.close() #close reader