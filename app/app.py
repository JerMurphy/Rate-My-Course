#!/usr/bin/env python
import MySQLdb
from flask import Flask, render_template
app = Flask(__name__)
db = MySQLdb.connect(host='localhost',user='jmurray2',passwd='Mjm12RmR',db='jmurray2')

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/courses')
def getCourses():
  sql = "call getAllCourses()"

  try:
    cursor = db.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    return "%s"%(str(result[0]))

  except Exception, e:
    print "Shit fucked up"


if __name__ == '__main__':
	app.run(host="0.0.0.0", debug=True)