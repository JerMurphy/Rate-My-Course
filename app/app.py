#!/usr/bin/env python
import sys
from flask import Flask, jsonify, abort, request, make_response, session, Response
from flask_restful import reqparse, Resource, Api
from flask_session import Session
import json
import MySQLdb
import ldap
import ssl
import settings # Our server and db settings, stored in settings.py

# force std to use utf-8
reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)
db = MySQLdb.connect(host=settings.MYSQL_HOST,user=settings.MYSQL_USER,passwd=settings.MYSQL_PASSWD,db=settings.MYSQL_DB)
# Set Server-side session config: Save sessions in the local app directory.
app.secret_key = settings.SECRET_KEY
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_COOKIE_NAME'] = 'ratemycourse'
app.config['SESSION_COOKIE_DOMAIN'] = settings.APP_HOST
Session(app)

####################################################################################
# Error handlers
##
@app.errorhandler(400) # decorators to add to 400 response
def not_found(error):
  return make_response(jsonify( { 'status': 'Bad request' } ), 400)

@app.errorhandler(404) # decorators to add to 404 response
def not_found(error):
  return make_response(jsonify( { 'status': 'Resource not found' } ), 404)


class SignIn(Resource):
  # POST: Set Session and return Cookie
  # curl -i -H "Content-Type: application/json" -X POST -d '{"username": "jmurray2", "password": "$Weld839z$"}' -c cookie-jar -k https://info3103.cs.unb.ca:39348/signin
  def post(self):

    if not request.json:
      abort(400) # bad request

    # Parse the json
    parser = reqparse.RequestParser()
    try:
      # Check for required attributes in json document, create a dictionary
      parser.add_argument('username', type=str, required=True)
      parser.add_argument('password', type=str, required=True)
      request_params = parser.parse_args()
    except:
      abort(400) # bad request

    if request_params['username'] in session:
      response = {'status': 'success', 'username': request_params['username']}
      responseCode = 200
    else:
      try:
        l = ldap.open(settings.LDAP_HOST)
        l.start_tls_s()
        l.simple_bind_s("uid="+request_params['username']+
          ", ou=People,ou=fcs,o=unb", request_params['password'])
        # At this point we have sucessfully authenticated. 

        session['username'] = request_params['username']
        response = {'status': 'success', 'username': session['username']}
        responseCode = 201
      except ldap.LDAPError, error_message:
        response = {'status': 'access denied'}
        responseCode = 403
      finally:
        l.unbind()
    
    return make_response(jsonify(response), responseCode)

  # GET: Check Cookie data with Session data
  # curl -i -H "Content-Type: application/json" -X GET -b cookie-jar -k https://info3103.cs.unb.ca:39348/signin
  def get(self):
    success = False
    if 'username' in session:
      response = {'status': 'success', 'username': session['username']}
      responseCode = 200
    else:
      response = {'status': 'no session found'}
      responseCode = 403

    return make_response(jsonify(response), responseCode)
  
  # DELETE: Check Cookie data with Session data
  # curl -i -H "Content-Type: application/json" -X DELETE -b cookie-jar -k https://info3103.cs.unb.ca:39348/signin
  def delete(self):
    if 'username' in session:
      response = {'status': 'success', 'username': session['username']}
      responseCode = 200
      session.clear() #clear current session
    else:
      response = {'status': 'no session found'}
      responseCode = 403

    return make_response(jsonify(response), responseCode)
    

#returns list of courses in a dictionary list
class AllCourses(Resource):
  # curl -i -H "Content-Type: application/json" -X GET -k https://info3103.cs.unb.ca:39348/courses
  def get(self):
    sql = "call getAllCourses()"
    try:
      cursor = db.cursor(MySQLdb.cursors.DictCursor)
      cursor.execute(sql)
      result = Response( json.dumps(cursor.fetchall()), mimetype="application/json" )
      return result
    except Exception, msg:
      print msg

    return make_response(jsonify(response), responseCode)

# returns list of courses in a dictionary list
# curl -i -H "Content-Type: application/json" -X GET -k https://info3103.cs.unb.ca:39348/courses
class AllCourses(Resource):
    def get(self):
      sql = "call getAllCourses()"
      try:
        cursor = db.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(sql)
        result = Response( json.dumps(cursor.fetchall()), mimetype="application/json" )
        return result
      except Exception, msg:
        print msg

# returns list of reviews in a dictionary list
# curl -i -H "Content-Type: application/json" -X GET -k https://info3103.cs.unb.ca:39348/reviews
class AllReviews(Resource):
  def get(self):
    sql = "call getAllReviews()"
    try:
      cursor = db.cursor(MySQLdb.cursors.DictCursor)
      cursor.execute(sql)
      result = Response( json.dumps(cursor.fetchall()), mimetype="application/json" )
      return result
    except Exception, msg:
      return msg

  # curl -i -H "Content-Type: application/json" -X POST -d '{"review":"this course sucks", "tough_rating": "5", "courseload_rating": "5", "usefulness_rating": "1", "exam_bool": true, "courseId": "STAT4293", "postedBy": "jmurray2"}' -b cookie-jar -k https://info3103.cs.unb.ca:39348/reviews
  def post(self):
    if 'username' in session:
      try:
        review = request.json['review']
        tough_rating = request.json['tough_rating']
        courseload_rating = request.json['courseload_rating']
        usefulness_rating = request.json['usefulness_rating']
        exam_bool = request.json['exam_bool']
        courseId = request.json['courseId']
        postedBy = request.json['postedBy']

        sql_insert = "call postReview(%s,%s,%s,%s,%s,%s,%s)"
        
        data = (review, tough_rating, courseload_rating, usefulness_rating, exam_bool, courseId, postedBy)
        cursor = db.cursor()
        cursor.execute(sql_insert, data)
        db.commit()
        #return?
      except Exception, msg:
        return msg
    else:
      response = {'status': 'unauthorized'}
      responseCode = 401
      return make_response(jsonify(response), responseCode)

class SpecificReviews(Resource):
  def get(self):
    try:
      courseID = request.json['courseID']
      sql = "call getSpecReviews(%s)"
      data = (courseID)
      cursor = db.cursor(MySQLdb.cursors.DictCursor)
      cursor.execute(sql,data)
      result = Response( json.dumps(cursor.fetchall()), mimetype="application/json" )
      return result
    except Exception, msg:
      return msg

class ManipulateReviews(Resource):
  def delete(self):
 
    try:
      reviewID = request.json['id']
      sql = "DELETE from reviews WHERE id = %s"
      data = (reviewID)
      cursor = db.cursor(MySQLdb.cursors.DictCursor)
      cursor.execute(sql,data)
      result = Response( json.dumps(cursor.fetchall()), mimetype="application/json" )
      return result
    except Exception, msg:
      return msg

  #Works now, have to input all data when updating even if its the same
  def put(self):
    if 'username' in session:
      try:
        postedBy = request.json['postedBy']
        if 'username' == postedBy:
          reviewID = request.json['id']
          review = request.json['review']
          tough_rating = request.json['tough_rating']
          courseload_rating = request.json['courseload_rating']
          usefulness_rating = request.json['usefulness_rating']
          exam_bool = request.json['exam_bool']
          courseId = request.json['courseId']

          sql_insert = "call updateReview(%s,%s,%s,%s,%s,%s,%s)"
          data = (review,tough_rating,courseload_rating,usefulness_rating,exam_bool,courseId,reviewID)
          cursor = db.cursor(MySQLdb.cursors.DictCursor)
          cursor.execute(sql_insert,data)
          result = cursor.fetchall()
          return result
        else: 
          response = {'status': 'unauthorized'}
          responseCode = 401
      except Exception, msg:
        return msg
    else:
      response = {'status': 'unauthorized'}
      responseCode = 401
    
    return make_response(jsonify(response), responseCode)

      
class SpecificCourseSubjects(Resource):
  def get(self):
    try:
      subject = request.json['subject']
      sql = "SELECT * FROM courses WHERE subject = %s"
      data = (subject)
      cursor = db.cursor(MySQLdb.cursors.DictCursor)
      cursor.execute(sql,data)
      result = Response( json.dumps(cursor.fetchall()), mimetype="application/json" )
      return result
    except Exception, msg:
      return msg
  

# add url endpoints to api
api = Api(app)
api.add_resource(SignIn, '/signin')
api.add_resource(AllCourses, '/courses')
api.add_resource(AllReviews, '/reviews')
api.add_resource(SpecificReviews, '/reviews/courseID')
api.add_resource(SpecificCourseSubjects, '/courses/subject')
api.add_resource(ManipulateReviews, '/reviews/reviewID')


if __name__ == "__main__":
  context = ('cert.pem', 'key.pem')
  app.run(host=settings.APP_HOST, port=settings.APP_PORT, ssl_context=context, debug=settings.APP_DEBUG)
