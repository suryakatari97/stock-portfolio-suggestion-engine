import json
import UserDetails
from flask import Flask, request, Response
import StockSuggestions
from flask_cors import CORS, cross_origin
import re


application = Flask(__name__)
CORS(application)
application.config['CORS_HEADERS'] = 'Content-Type'

# This backend service serves following purpose
# Serve front-end
# Sign up and Login functionality
# Allocate money in stocks

@application.route('/suggestStocks', methods=['POST'])
@cross_origin(origin='*')
def stocks_suggestions():
    req = request.json
    amount = req['amount']
    strategyList = req['strategyList']

    status = 200
    error = ""

    if amount < 5000:
        error = "Please provide an amount greater than $5000"
        status = 500
    
    if len(strategyList) == 0:
        error = "Select at-least one strategy"
        status = 500

    if len(strategyList) > 2:
        status = 500
        error = "Please select no more than two strategies"

    if status is not 500:
        allocations = StockSuggestions.suggest_stocks(amount, strategyList)
        return json.dumps(allocations), 200
    else:
         return json.dumps({"error": error}), status


@application.route('/signup', methods=['POST'])
@cross_origin(origin='*')
def user_signup():
    req = request.json
    firstName = req['firstName']
    lastName = req['lastName']
    email = req['email']
    password = req['password']

    status = 200
    error = ""

    if not firstName:
        error = "Please Provide First Name"
        status = 500

    if not lastName:
        error = "Please Provide Last Name"
        status = 500
    
    if not email or email is None:
        error = "Please Provide Email"
        status = 500

    if not valid_email(email):
        error = "Email is not valid"
        status = 500
    
    if password is None:
        error = "Please provide password"
        status = 500

    if status is not 500:
        token = UserDetails.user_signup(email, password, firstName, lastName)

    if token is None:
        error = "Please provide another email"
        status = 500

    if status is 200:
        resp = Response(json.dumps({'code': 200}))
        resp.set_cookie('token', token)
        return resp
    else:
        return json.dumps({"error": error}), status

def valid_email(email):
    EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")
    return EMAIL_REGEX.match(email)

@application.route('/login', methods=['POST'])
@cross_origin(origin='*')
def user_login():
    req = request.json
    email = req['email']
    password = req['password']
    status = 200
    error = ""

    if email is None:
        error = "Please provide email"
        status = 500

    if password is None:
        error = "Please provide Password"
        status = 500

    if status is not 500:
        token = UserDetails.user_login(email, password)

    if token is None:
        status = 500
        error = "Invalid Credentials"

    if status is 200:
        response = Response(json.dumps({'code': 200}))
        response.set_cookie('token', token)
        return response
    else:
        return json.dumps({"error": error}), status


@application.route('/validateSession', methods=['GET'])
@cross_origin(origin='*')
def check_session():

    token = request.cookies.get('token')
    error = ""
    status = 200

    if token is None:
        error = "Invalid Login"
        status = 500
    
    if status is not 500:
        user = UserDetails.check_login(token)

    if user is None:
        error = "Invalid Login"
        status = 500

    name = user.get('firstName') + " " + user.get('lastName')
    if status is 200:
        response = Response(json.dumps({'code': 200, 'name': name}))
        return response
    else:
        return json.dumps({"error": error}), status


@application.route('/logout', methods=['GET'])
@cross_origin(origin='*')
def user_logout():

    token = request.cookies.get('token')

    if token is None:
        return json.dumps({"code": 200}), 200

    UserDetails.user_logout(token)

    response = Response(json.dumps({'code': 200}))
    return response

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=80)
