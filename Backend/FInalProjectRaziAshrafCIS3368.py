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


#the username and password for our login
authorized_user = [
{
        'username': 'myusername',
        'password': 'mypassword',
        'role': 'default',

}
]

#login api, used the example from class 6
@app.route('/api/usernamepw', methods=['GET'])
def usernamepw_example():
    username = request.headers['username'] 
    pw = request.headers['password']
    for au in authorized_user: 
        if au['username'] == username and au['password'] == pw: 
            return jsonify('You are authorized.')
        else:
            return 'SECURITY ERROR' 





#get api section



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


#post api section


@app.route('/api/planes/post', methods=['POST'])  #creating a post api for planes from the information shared in class, similar to homework 2 and exam 1
def create_plane():
    mylist = []
    request_data = request.get_json()
    newmake = request_data['make']
    newmodel = request_data['model']
    newyear = request_data['year']
    newcapacity= request_data['capacity']
    planes = [newmake, newmodel, newyear, newcapacity]
    mylist.append(planes)
    for plane in mylist:
        sql = "INSERT INTO planes (make, model, year, capacity) VALUES (%s, %s, %s, %s)" 
        val = (planes[0], planes[1], planes[2], planes[3])
        cursor.execute(sql,val)
        conn.commit()
    mylist.clear()
    return ("Plane add request successful")




@app.route('/api/airports/post', methods=['POST'])  #creating a post api for airports from the information shared in class, similar to homework 2 and exam 1
def create_airport():
    mylist = []
    request_data = request.get_json()
    newcode = request_data['airportcode']
    newname = request_data['airportname']
    newcountry = request_data['country']
    airports = [newcode, newname, newcountry]
    mylist.append(airports)
    for airport in mylist:
        sql = "INSERT INTO airports (airportcode, airportname, country) VALUES (%s, %s, %s)" 
        val = (airports[0], airports[1], airports[2])
        cursor.execute(sql,val)
        conn.commit()
    mylist.clear()
    return ("Airport add request successful")


@app.route('/api/flights/post', methods=['POST'])  #creating a post api for flights from the information shared in class, similar to homework 2 and exam 1
def create_flight():
    mylist = []
    request_data = request.get_json()
    newplaneid = request_data['planeid']
    newairportfromid = request_data['airportfromid']
    newairporttoid = request_data['airporttoid']
    newdate = request_data['date']
    flights = [newplaneid, newairportfromid, newairporttoid, newdate]
    mylist.append(flights)
    for airport in mylist:
        sql = "INSERT INTO flights (planeid, airportfromid, airporttoid, date) VALUES (%s, %s, %s, %s)" 
        val = (flights[0], flights[1], flights[2], flights[3])
        cursor.execute(sql,val)
        conn.commit()
    mylist.clear()
    return ("Flight add request successful")




#delete api section

#Delete api, got help from https://webdamn.com/create-restful-api-using-python-mysql/
@app.route('/api/planes/delete', methods=['DELETE'])
def delete_plane():
    request_data = request.get_json()
    newid = request_data['id']
    cursor.execute("SELECT id, make, model, year, capacity FROM planes")
    planeRows = cursor.fetchall()
    for planeRow in planeRows:
        if planeRow['id'] == newid:
            sql = "DELETE FROM planes WHERE id = %s"
            val = [newid]
            cursor.execute(sql, val)
            conn.commit()
            return ("Plane deleted successfully!")



@app.route('/api/airports/delete', methods=['DELETE'])
def delete_airport():
    request_data = request.get_json()
    newid = request_data['id']
    cursor.execute("SELECT id, airportcode, airportname, country FROM airports")
    airportRows = cursor.fetchall()
    for airportRow in airportRows:
        if airportRow['id'] == newid:
            sql = "DELETE FROM airports WHERE id = %s"
            val = [newid]
            cursor.execute(sql, val)
            conn.commit()
            return ("Airport deleted successfully!")


@app.route('/api/flights/delete', methods=['DELETE'])
def delete_flight():
    request_data = request.get_json()
    newid = request_data['id']
    cursor.execute("SELECT id, planeid, airportfromid, airporttoid, date FROM flights")
    flightRows = cursor.fetchall()
    for flightRow in flightRows:
        if flightRow['id'] == newid:
            sql = "DELETE FROM flights WHERE id = %s"
            val = [newid]
            cursor.execute(sql, val)
            conn.commit()
            return ("Flight deleted successfully!")




#put api section

@app.route('/api/planes/put', methods=['PUT'])  #creating a put api from the information shared in class
def update_plane():
    if 'id' in request.args:
        newid = int(request.args['id'])
    else:
        return ('ERROR: No ID provided!')
    request_data = request.get_json()
    newmake = request_data['make']
    newmodel = request_data['model']
    newyear = request_data['year']
    newcapacity = request_data['capacity']

    plane = [newid, newmake, newmodel, newyear, newcapacity]
    jsonify(plane)
    cursor.execute("SELECT id, make, model, year, capacity FROM planes")
    planeRows = cursor.fetchall()
    for planeRow in planeRows:
        if planeRow['id'] == newid:
            sql = "UPDATE planes SET make=%s, model=%s, year=%s, capacity=%s WHERE id= %s"
            val = (plane[1], plane[2], plane[3], plane[4], newid)
            cursor.execute(sql,val)
            conn.commit()
            return ("Plane update successful")

@app.route('/api/airports/put', methods=['PUT'])  
def update_airport():
    if 'id' in request.args:
        newid = int(request.args['id'])
    else:
        return ('ERROR: No ID provided!')
    request_data = request.get_json()
    newcode = request_data['airportcode']
    newname = request_data['airportname']
    newcountry = request_data['country']
    airport = [newid, newcode, newname, newcountry]
    jsonify(airport)
    cursor.execute("SELECT id, airportcode, airportname, country FROM airports")
    airportRows = cursor.fetchall()
    for airportRow in airportRows:
        if airportRow['id'] == newid:
            sql = "UPDATE airports SET airportcode=%s, airportname=%s, country=%s WHERE id= %s"
            val = (airport[1], airport[2], airport[3], newid)
            cursor.execute(sql,val)
            conn.commit()
            return ("Airport update successful")
























app.run()
