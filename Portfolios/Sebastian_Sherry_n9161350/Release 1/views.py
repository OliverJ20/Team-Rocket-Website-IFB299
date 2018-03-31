#!/usr/bin/env python

#import flask
from flask import Flask, request, url_for, render_template, session, redirect, jsonify
from functools import wraps
from lookup import *#getProfileInfo, loginCheck, register, addViolation, checkAdmin, getHealthIssues

#initalize app
app = Flask(__name__)


#Login decorator to prevent unaurthorized access
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session and session['logged_in'] == True:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrap

#Login decorator for admin
def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session and session['logged_in'] == True and session['admin'] == True:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrap

#main page
@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", loggedIn = getLoggedIn())


@app.route('/editHealth/<id>', methods =["GET", "POST"])
@admin_required
def editReport(id):
    violation = dict(Violation_Type=type,Date="",Time="",Description="",Place_in_campus="",Department="")
    if request.method == "GET":
        violation = getOtherViolation(id)
        return render_template("editparking.html", loggedIn = getLoggedIn(), violation=violation)
    elif request.method == "POST":
        if citType == 1:
            violation['Violation_Type'] = "Smoking"
        else:
            violation['Violation_Type'] = "Other"

        violation['Violation_Type'] = "Parking"
        violation['Date'] = str(request.form['date'])
        violation['Time'] = str(request.form['time'])
        violation['Description'] = str(request.form['desc'])
        violation['Place_in_campus'] = str(request.form['location'])
        violation['Department'] = str(request.form['department'])
        violation['Supervisor'] = session['userEmail']
        violation['User_ID'] = str(request.form['name'])
        addViolation(violation)
        return redirect(url_for('admin'))

@app.route('/editHealth/<id>', methods=["GET", "POST"])
@admin_required
def editHealth(id):
    issue = dict(Date = "", Time = "", Person_Name = "", Department = "", Resolution_Date = "" , Resolution_Time = "", Resolution_Description = "", Supervisor = "" , Place_in_campus = "")
    if request.method == "GET":
        issue = getHealthIssue(id)
        return render_template("edithealth.html", loggedIn = getLoggedIn(), issue=issue)
    elif request.method == "POST":
        violation['Date'] = str(request.form['date'])
        violation['Time'] = str(request.form['time'])
        violation['Person_Name'] = str(request.form['name'])
        violation['Department'] = str(request.form['department'])
        violation['Resolution_Date'] = str(request.form['res_date'])
        violation['Resolution_Time'] = str(request.form['res_time'])
        violation['Resolution_Description'] = str(request.form['res_description'])
        violation['Supervisor'] = session['userEmail']
        violation['Place_in_campus'] = str(request.form['location'])
        addViolation(violation)
        return redirect(url_for('admin'))


@app.route('/editOther/<id>', methods =["GET", "POST"])
@admin_required
def editOther(id):
    violation = dict(Violation_Type=type,Date="",Time="",Description="",Place_in_campus="",Department="")
    if request.method == "GET":
        violation = getOtherViolation(id)
        return render_template("editother.html", loggedIn = getLoggedIn(), violation=violation)
    elif request.method == "POST":
        if citType == 1:
            violation['Violation_Type'] = "Smoking"
        else:
            violation['Violation_Type'] = "Other"

        violation['Violation_Type'] = "Parking"
        violation['Date'] = str(request.form['date'])
        violation['Time'] = str(request.form['time'])
        violation['Description'] = str(request.form['desc'])
        violation['Place_in_campus'] = str(request.form['location'])
        violation['Department'] = str(request.form['department'])
        violation['Supervisor'] = session['userEmail']
        violation['User_ID'] = str(request.form['name'])
        addViolation(violation)
        return redirect(url_for('admin'))

@app.route('/editParking/<id>', methods =["GET", "POST"])
@admin_required
def editParking(id):
    violation = dict(Violation_Type=type,Date="",Time="",Description="",Place_in_campus="",Department="")
    if request.method == "GET":
        violation = getParkingViolation(id)
        violation['Violation_Type'] = "Parking"
        return render_template("editparking.html", loggedIn = getLoggedIn(), violation=violation)
    elif request.method == "POST":
        violation['Violation_Type'] = "Parking"
        violation['Date'] = str(request.form['date'])
        violation['Time'] = str(request.form['time'])
        violation['Description'] = str(request.form['desc'])
        violation['Place_in_campus'] = str(request.form['location'])
        violation['Department'] = str(request.form['department'])
        violation['Permit_Number'] = str(request.form['permitNumber'])
        violation['Vehicle_Type'] = str(request.form['VehType'])
        violation['Vehicle_License_number'] = str(request.form['license'])
        addViolation(violation)
        return redirect(url_for('admin'))

@app.route('/login/', methods =["GET", "POST"])
def login():
    #default username for error checking
    user = ""
    if 'logged_in' in session:
        if session['admin']:
            return redirect(url_for('admin'))
        return redirect(url_for('profile'))
    if request.method == "POST":
        user = str(request.form['email'])
        attempt_pass = str(request.form['password'])
        if loginCheck(user, attempt_pass) == True:
            session['logged_in'] = True
            session['userEmail'] = user
            session['admin'] = checkAdmin(user)
            return redirect(url_for('profile'))
    return render_template("login.html", user = user, loggedIn = getLoggedIn())


@app.route('/out/', methods =["GET", "POST"])
def logout():
    if 'logged_in' in session:
        session.clear()
    return redirect(url_for('logoutPage'))
   # return render_template("index.html")


@app.route('/profile/')
@login_required
def profile():
    if session['admin']:
        return redirect(url_for('admin'))
    else:
	    return render_template("profile.html", Info = getProfileInfo(session['userEmail']), loggedIn = getLoggedIn())

@app.route('/admin/')
@admin_required
def admin():
    return render_template("admin.html", Issues = getHealthIssues(), loggedIn = getLoggedIn())

@app.route('/admin/health/')
@admin_required
def adminHealth():
	return jsonify(issues = getHealthIssues())

@app.route('/admin/parking/')
@admin_required
def adminParking():
	return jsonify(issues = getParkingViolations())

@app.route('/admin/other/')
@admin_required
def adminOther():
	return jsonify(issues = getOtherViolations())


#convert Department to string
def convertDepartment(dep):
    departments = [[9,"Science and Engineering"],[10,"Law"],[11,"Health"],[12,"Creative Industries"],[13,"Business"],
    [14,"Research"],[15,"Admin"]]

    for department in departments:
        if int(dep) == department[0]:
            return department[1]

    return ""

#Logged in function
def getLoggedIn():
    status = dict(loggedIn=False,admin=False)
    if 'logged_in' in session:
        status['loggedIn'] = True
        if session['admin']:
            status['admin'] = True

    return status

if __name__ == "__main__":
    app.secret_key = 'REDACTED FOR ARTIFACT'
    app.run(debug=True)
