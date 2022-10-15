#importing needed things, used the same method as homework 2
import flask
from flask import Flask
from flask import jsonify
from flask import request




#stuff to connect to mysql database, same as homework 2
import mysql.connector
from mysql.connector import Error


conn = None
try:
    conn = mysql.connector.connect(host='cis3368fall.cjgzy39nyp3b.us-east-1.rds.amazonaws.com',
                                       database='cis3368fall',
                                       user='RaziAshraf',
                                       password='Razizain77')
    if conn.is_connected():
            print('Connected to MySQL database')

except Error as e:
    print(e)

#passing in dictionary as true so we can get our get Apis in a nice dictionary form, same as homework 2
cursor = conn.cursor(dictionary=True)


app = flask.Flask(__name__)#Setting up application name
app.config['DEBUG'] = True #allow to show errors in browser


mylist = [] #creating an empty list for the post api 

@app.route('/api/airports/get' , methods=['GET'])#api to get all airports, got help from https://webdamn.com/create-restful-api-using-python-mysql/
def get_airports():
    try:
        cursor.execute("SELECT id, airportcode, airportname, country FROM airports")   
        airportRows = cursor.fetchall()
        response = jsonify(airportRows)
        return response
    except Exception as e:
        print(e)


@app.route('/api/planes/get' , methods=['GET'])#api to get all planes
def get_planes():
    try:
        cursor.execute("SELECT id, make, model, year, capacity FROM planes")   
        planeRows = cursor.fetchall()
        response = jsonify(planeRows)
        return response
    except Exception as e:
        print(e)


@app.route('/api/flights/get' , methods=['GET'])#api to get all flights
def get_flights():
    try:
        cursor.execute("SELECT id, planeid, airportfromid, airporttoid, date FROM flights")   
        flightRows = cursor.fetchall()
        response = jsonify(flightRows)
        return response
    except Exception as e:
        print(e)












































app.run()