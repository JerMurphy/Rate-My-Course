#!/usr/bin/env python
import sys
from flask import Flask, jsonify, abort, request, make_response, session, Response
from flask_restful import reqparse, Resource, Api
from flask_session import Session
import json
import ldap
import settings # Our server and db settings, stored in settings.py
import MySQLdb

# force std to use utf-8
reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)
db = MySQLdb.connect(host=settings.MYSQL_HOST,user=settings.MYSQL_USER,passwd=settings.MYSQL_PASSWD,db=settings.MYSQL_DB)
# Set Server-side session config: Save sessions in the local app directory.
#app.secret_key = settings.SECRET_KEY
#app.config['SESSION_TYPE'] = 'filesystem'
#app.config['SESSION_COOKIE_NAME'] = 'peanutButterAndJam'
#app.config['SESSION_COOKIE_DOMAIN'] = settings.APP_HOST
#Session(app)

####################################################################################
#
# Error handlers
#
@app.errorhandler(400) # decorators to add to 400 response
def not_found(error):
  return make_response(jsonify( { 'status': 'Bad request' } ), 400)

@app.errorhandler(404) # decorators to add to 404 response
def not_found(error):
  return make_response(jsonify( { 'status': 'Resource not found' } ), 404)


####################################################################################
#
# Routing: GET and POST using Flask-Session
#
# Demonstration only!
#
class SignIn(Resource):
  #
  # Login, start a session and get session cookie
  #
  # Example curl command: 
  # curl -i -H "Content-Type: application/json" -X POST -d '{"username": "Casper", "password": "c\*ap"}'
  #   -c cookie-jar http://info3103.cs.unb.ca:61340/signin
  #
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
      response = {'status': 'success'}
      responseCode = 200
    else:
      try:
        l = ldap.open(settings.LDAP_HOST)
        l.start_tls_s()
        l.simple_bind_s("uid="+request_params['username']+
          ", ou=People,ou=fcs,o=unb", request_params['password'])
        # At this point we have sucessfully authenticated. 

        session['username'] = request_params['username']
        response = {'status': 'success' }
        responseCode = 201
      except ldap.LDAPError, error_message:
        response = {'status': 'Access denied'}
        responseCode = 403
      finally:
        l.unbind()
    
    return make_response(jsonify(response), responseCode)

  # GET: Check for a login
  #
  # Example curl command: 
  # curl -i -H "Content-Type: application/json" -X GET -b cookie-jar 
  # http://info3103.cs.unb.ca:61340/signin
  def get(self):
    success = False
    if 'username' in session:
      response = {'status': 'success'}
      responseCode = 200
    else:
      response = {'status': 'fail'}
      responseCode = 403
      
    return make_response(jsonify(response), responseCode)
  
  # DELETE: Logout: remove session
  #
  # Example curl command: 
  # curl -i -H "Content-Type: application/json" -X DELETE -b cookie-jar 
  # http://info3103.cs.unb.ca:61340/signin

  #
  # Here's your chance to shine!
  # ...later

#returns list of courses in a dictionary list
class GetAllCourses(Resource):
  def get(self):
    sql = "call getAllCourses()"
    try:
      cursor = db.cursor(MySQLdb.cursors.DictCursor)
      cursor.execute(sql)
      result = Response( json.dumps(cursor.fetchall()), mimetype="application/json" )
      return result
    except Exception, msg:
      print msg

#returns list of reviews in a dictionary list
class GetAllReviews(Resource):
  def get(self):
    sql = "call getAllReviews()"
    try:
      cursor = db.cursor(MySQLdb.cursors.DictCursor)
      cursor.execute(sql)
      result = Response( json.dumps(cursor.fetchall()), mimetype="application/json" )
      return result
    except Exception, msg:
      print msg


#Add url endpoints to api
api = Api(app)
api.add_resource(SignIn, '/signin')
api.add_resource(GetCourses, '/courses')
api.add_resource(GetReviews, '/reviews')

if __name__ == "__main__":
    app.run(host=settings.APP_HOST, port=settings.APP_PORT, debug=settings.APP_DEBUG)
