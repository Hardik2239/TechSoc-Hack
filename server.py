from flask import Flask, redirect, request, make_response, render_template
from model import Booking
import requests
import sys
import json
from datetime import datetime, timedelta

CLIENT_SECRET = '162991cb37e2b660506ebf18d1a7827a58de35b77adfa9e25de3dcce0c19771e'
CLIENT_ID = '3240514769869690.9992035169504409'
API_TOKEN = 'uclapi-8bc330970aaf6b3-c779cef1c45d064-a4b8b5da4798be7-5a457ead2b42f86'
studentName = ""


app = Flask(__name__, template_folder="templates")
app.testing = True

testBookings = [
    Booking("Lucas Marrie", "21342321", "Room 406 - Student Center", "Computer Science", "Maths and Stats study time :D", "43243f", "15/02/21", "8:00", "9:00"),
    Booking("Hadi Khan", "28105803", "Room 20 - Science Library", "Art History", "Baroque study", "34156f", "16/02/21", "12:00", "13:00"),
    Booking("Matt Gomez Cullen", "28425190", "Meeting Room 3 - IOE", "Economics", "Revising for Macroeconomics test", "24456e", "16/02/21", "10:00", "11:00"),
    Booking("Hardik Agrawal", "30421195", "Room 102 - Student Center", "Sociology", "Functionalism coursework", "14436d", "24/02/21", "16:00", "17:00"),
    Booking("Krish", "19435261", "Room 203 - Student Center", "Mechanical Engineering", "Energy loss due to Friction", "14256g", "02/03/21", "7:00", "8:00"),
]

#list of all available seats
spaceids = ['469', '470', '471', '472', '473', '474', '475', '475', '476', '477', '478']
availableSpaces = []

#region Authentication

def checkAuth(token):
    return token is not None
    

@app.route('/authentication')
def authentication():
    token = request.cookies.get('access_token')
    authenticated = checkAuth(token)

    return render_template("index.html", authenticated = authenticated)


@app.route('/authentication/login')
def uclapi_login():
    print("test", )

    url = f"https://uclapi.com/oauth/authorise/?client_id={CLIENT_ID}&state=1"
    # return "<p>Hello, World!</p>"
    return redirect(url)


@app.route('/authentication/logout')
def ucl_logout():
    resp = make_response(redirect('/'))
    resp.delete_cookie('access_token')
    return resp


@app.route('/callback')
def receive_callback():
    # receive parameters
    result = request.args.get('result', '')
    code = request.args.get('code', '')
    state = request.args.get('state', '')
    print(request.args, file=sys.stdout)
    # do something with these parameters
    # e.g. request an auth token from /oauth/token

    params = {
        "client_id": CLIENT_ID,
        "code": code,
        "client_secret": "162991cb37e2b660506ebf18d1a7827a58de35b77adfa9e25de3dcce0c19771e",
        "state": state
    }

    r = requests.get("https://uclapi.com/oauth/token", params=params)
    print(r.json())
    print(r.json(), file=sys.stdout)

    access_token =  r.json()['access_token']

    resp = make_response(redirect('/'))
    resp.set_cookie('access_token', access_token)

    '''
    params2 = {
        "client_secret": CLIENT_SECRET
    }

    r = requests.get("https://uclapi.com/oauth/user/data", params=params2)
    data = r.json()
    studentName = data['full_name']
    '''

    return resp

#endregion


# Main Pages
@app.route('/')
def homepage():
    token = request.cookies.get('access_token')
    authenticated = checkAuth(token)
    if not authenticated:
        return redirect('/authentication')

    return render_template("home.html", authenticated = authenticated)


# Bookings
@app.route('/create', methods = ['GET', 'POST'])
def createBooking():
    token = request.cookies.get('access_token')
    authenticated = checkAuth(token)
    if not authenticated:
        return redirect('/authentication')
    
    if request.method == 'POST':
        form = request.form
        studentName = "Lucas Marrie"
        bookingName = form['bookingName']
        
        date = datetime.strptime(form['date'], '%Y-%m-%d').strftime('%d/%m/%y')
        fromTime = form['fromTime']
        endTime =  (datetime.strptime(fromTime, '%H:%M') + timedelta(hours=1)).strftime('%H:%M')
        location = form['location']
        course = form['course']

        testBookings.append(Booking(studentName, "0", location, course, bookingName, "_", date, fromTime, endTime))



    # params = {
    #         "client_secret" : CLIENT_SECRET,
    #         "access_token" : token
    # }
    # r = requests.get("https://uclapi.com/oauth/user/data", params=params)
    # data = r.json()
    # print(data)



    # params2 = {
    #     "ids": ','.join(spaceids),
    #     "token" : API_TOKEN
    # }

    # r = requests.get("https://uclapi.com/libcal/space/item", params=params2)
    # data = r.json()
    #Seems to be an api bug problem ¯\_(ツ)_/¯
    # print(data)
    # if data["ok"]:
    #     roomName = data['questions'][0]['name']
    #     availableSpaces.append(roomName)
    # else:
    #     print("Error - Error")


    return render_template("create.html" ,authenticated = authenticated)

    


@app.route('/browse', methods = ['GET'])
def browseBooking():
    token = request.cookies.get('access_token')
    authenticated = checkAuth(token)
    if not authenticated:
        return redirect('/authentication')

    return render_template("browse.html", bookings = testBookings, authenticated = authenticated)


app.run()