#!/usr/bin/env python
import sys
from flask import Flask, jsonify, abort, request, make_response, session, Response
from flask_restful import reqparse, Resource, Api
from flask_session import Session
from flask.ext.cors import CORS
import json
import MySQLdb
import ldap
import ssl
import settings # Our server and db settings, stored in settings.py

app = Flask(__name__,static_url_path="")
CORS(app)
# force std to use utf-8
reload(sys)
sys.setdefaultencoding('utf-8')


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
  return make_response(jsonify({'status':'Bad request'}), 400)

@app.errorhandler(404) # decorators to add to 404 response
def not_found(error):
  return make_response(jsonify({'status': 'Resource not found'}), 404)

class Homepage(Resource):
  def get(self):
    return app.send_static_file('index.html')

class SignIn(Resource):
  # POST: Set Session and return Cookie
  # curl -i -H "Content-Type: application/json" -X POST -d '{"username": "jmurray2", "password": "***"}' -c cookie-jar -k https://info3103.cs.unb.ca:39348/signin
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
        response = {'status': 'login successful', 'username': session['username']}
        responseCode = 201
      except ldap.LDAPError, error_message:
        response = {'status': 'access denied'}
        responseCode = 401
      finally:
        l.unbind()

    return make_response(jsonify(response), responseCode)

  # GET: Check Cookie data with Session data
  # curl -i -H "Content-Type: application/json" -X GET -b cookie-jar -k https://info3103.cs.unb.ca:39348/signin
  def get(self):
    success = False
    if 'username' in session:
      response = {'status': 'logged in', 'username': session['username']}
      responseCode = 200
    else:
      response = {'status': 'no session found'}
      responseCode = 404

    return make_response(jsonify(response), responseCode)

  # DELETE: Check Cookie data with Session data
  # curl -i -H "Content-Type: application/json" -X DELETE -b cookie-jar -k https://info3103.cs.unb.ca:39348/signin
  def delete(self):
    if 'username' in session:
      response = {'status': 'successfully logged out'}
      responseCode = 200
      session.clear() #clear current session
    else:
      response = {'status': 'no session found'}
      responseCode = 404

    return make_response(jsonify(response), responseCode)


#returns list of courses in a dictionary list
class AllCourses(Resource):
  # curl -i -H "Content-Type: application/json" -X GET -k https://info3103.cs.unb.ca:39348/courses
  def get(self):
    try:
      cursor = db.cursor(MySQLdb.cursors.DictCursor)
      cursor.callproc('getAllCourses')

      resp = Response( json.dumps(cursor.fetchall()), status=200, mimetype="application/json" )
      return resp
    except Exception, msg:
      print msg
      return make_response(jsonify({'status':'Bad request'}), 400)


#returns list of all courses given a subject
class CourseSubjects(Resource):
  def get(self, courseSubject):
    try:
      cursor = db.cursor(MySQLdb.cursors.DictCursor)
      cursor.callproc('getSpecCourses',[courseSubject])

      resp = Response( json.dumps(cursor.fetchall()), status=200, mimetype="application/json" )
      return resp
    except Exception, msg:
      print msg
      return make_response(jsonify({'status':'Bad request'}), 400)


#returns/posts list of reviews in a dictionary list
class AllReviews(Resource):
  # curl -i -H "Content-Type: application/json" -X GET -k https://info3103.cs.unb.ca:39348/reviews
  def get(self):
    try:
      cursor = db.cursor(MySQLdb.cursors.DictCursor)
      cursor.callproc('getAllReviews')

      resp = Response( json.dumps(cursor.fetchall()), status=200, mimetype="application/json" )
      return resp
    except Exception, msg:
      print msg
      return make_response(jsonify({'status':'Bad request'}), 400)

  # curl -i -H "Content-Type: application/json" -X POST -d '{"review":"i'm the man", "tough_rating": "5", "courseload_rating": "5", "usefulness_rating": "5", "exam_bool": false, "courseId": "MATH1013"}' -b cookie-jar -k https://info3103.cs.unb.ca:39348/reviews
  def post(self):
    if 'username' in session:
      try:
        review = request.json['review']
        tough_rating = request.json['tough_rating']
        courseload_rating = request.json['courseload_rating']
        usefulness_rating = request.json['usefulness_rating']
        exam_bool = request.json['exam_bool']
        courseId = request.json['courseId']
        postedBy = session['username']

        data = [review, tough_rating, courseload_rating, usefulness_rating, exam_bool, courseId, postedBy]

        cursor = db.cursor(MySQLdb.cursors.DictCursor)
        cursor.callproc('postReview', data)
        db.commit()

        response = {'status': 'Successfully posted'}
        responseCode = 200
      except Exception, msg:
        print msg
        response = {'status': 'Bad request'}
        responseCode = 400
    else:
      response = {'status': 'Unauthorized'}
      responseCode = 401

    return make_response(jsonify(response), responseCode)


#returns list of reviews given a courseID
class SpecificReviews(Resource):
  # curl -i -H "Content-Type: application/json" -X GET -k https://info3103.cs.unb.ca:39348/reviews/CS1073
  def get(self, courseID):
    try:
      cursor = db.cursor(MySQLdb.cursors.DictCursor)
      cursor.callproc('getSpecReviews',[courseID])

      resp = Response( json.dumps(cursor.fetchall()), status=200, mimetype="application/json" )
      return resp
    except Exception, msg:
      print msg
      return make_response(jsonify({'status':'Bad request'}), 400)


#edit/delete review owned by yourself
class ManipulateReviews(Resource):
  #curl -i -H "Content-Type: application/json" -X DELETE -b cookie-jar -k https://info3103.cs.unb.ca:39348/reviews/1
  def delete(self, reviewID):
      if 'username' in session:
        try:
          cursor = db.cursor(MySQLdb.cursors.DictCursor)
          cursor.callproc('deleteReview', [reviewID])
          db.commit()

          resp = Response( json.dumps(cursor.fetchall()), status=200, mimetype="application/json" )
          return resp
        except Exception, msg:
          print msg
          return make_response(jsonify({'status':'Bad request'}), 400)
      else:
        return make_response(jsonify({'status':'Unauthorized'}), 401)

  #curl -i -H "Content-Type: application/json" -X PUT -d '{"review":"i love this course!", "tough_rating": "5", "courseload_rating": "5", "usefulness_rating": "1", "exam_bool": true, "courseId": "CS1073", "postedBy": "jmurray2"}' -b cookie-jar -k https://info3103.cs.unb.ca:39348/reviews/1
  def put(self, reviewID):
    if 'username' in session:
      try:
        postedBy = request.json['postedBy']
        if session['username'] == postedBy:
          review = request.json['review']
          tough_rating = request.json['tough_rating']
          courseload_rating = request.json['courseload_rating']
          usefulness_rating = request.json['usefulness_rating']
          exam_bool = request.json['exam_bool']
          courseId = request.json['courseId']

          data = [review,tough_rating,courseload_rating,usefulness_rating,exam_bool,courseId,reviewID]

          cursor = db.cursor(MySQLdb.cursors.DictCursor)
          cursor.callproc('updateReview', data)
          db.commit()

          resp = Response( json.dumps(cursor.fetchall()), status=200, mimetype="application/json" )
          return resp
        else:
          return make_response(jsonify({'status':'Unauthorized'}), 401)
      except Exception, msg:
        print msg
        return make_response(jsonify({'status':'Bad request'}), 400)
    else:
      return make_response(jsonify({'status':'Unauthorized'}), 401)


# add url endpoints to api
api = Api(app)
api.add_resource(Homepage, '/')
api.add_resource(SignIn, '/signin')
api.add_resource(AllCourses, '/courses')
api.add_resource(CourseSubjects, '/courses/<string:courseSubject>')
api.add_resource(AllReviews, '/reviews')
api.add_resource(SpecificReviews, '/reviews/<string:courseID>')
api.add_resource(ManipulateReviews, '/reviews/<int:reviewID>')

if __name__ == "__main__":
  context = ('cert.pem', 'key.pem')
  app.run(host=settings.APP_HOST, port=settings.APP_PORT, ssl_context=context, debug=settings.APP_DEBUG)
