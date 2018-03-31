#!/usr/bin/env python

#import flask
from flask import Flask, flash, request, url_for, render_template, session, redirect, jsonify
from functools import wraps
from lookup import *
from testfunctions import *
from flask_mail import Message, Mail
import datetime as dt


# email server

#MAIL_SERVER = 'smtp.googlemail.com'
#MAIL_PORT = 465
#MAIL_USE_TLS = False
#MAIL_USE_SSL = True
#MAIL_USERNAME = 'ojx2010@gmail.com'
#MAIL_PASSWORD = 'Gmaster333'

# administrator list


#from models import User
import time

import os
# We require 're' module for validating email address with regular expression
import re

#initalize app
app = Flask(__name__)


app.config.update(
    DEBUG = True,
    MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'teamRocket299@gmail.com',
	MAIL_PASSWORD = 'MaristCollege!'
)
mail = Mail(app)


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
    return render_template("index.html", info = getHeaderInfo())

@app.route('/application', methods = ["GET","POST"])
@login_required
def application():
    # Initialize the errors variable to empty string. We will have the error messages
    # in that variable, if any.
    errors = ''

    if request.method == "GET":
        # If the user already has a permit, send them to the update permit page. Else render the page
        if getProfileInfo(session['userEmail'])['Permit'] != []:
            return redirect(url_for('updateApp'))
        else:
            return render_template("application.html", errors = errors, info = getHeaderInfo())
    else:
        # Since gender field is a radio button, it will not be available in the POST
        # data if no choice is selected. If we try to access it in such a scenario, we
        # will get an exception, so we are using the get() method on the 'form' dictionary
        # specify a default value if the key doesn't exist in the dictionary.
        vType = str(request.form['vehicleType'])
        tDuration = str(request.form['duration'])

        print ("Type is " + vType);
        print ("Duration is " + tDuration);
        # Check if all the fields are non-empty and raise an error otherwise
        if emptyField(vType) or emptyField(tDuration) or emptyField(startDate):
            errors = "Please enter all the fields."
            print("Errors detected.", errors)
            print()

        if not errors:
            # If there are no errors, create a dictionary containing all the entered
            # data and pass it to the template to be displayed
            #permit = dict(User_ID = session['userEmail'], Vehicle_Type = str(request.form['vehicleType']), Department=str(request.form['department']), Permit_Duration=str(request.form['duration']), Permit_Start=str(request.form['startDate']), Permit_End=str(request.form['endDate']), Approved=True)
            permit = dict(Vehicle_Type = str(request.form['vehicleType']), Department = convertDepartment(str(request.form['department'])), Permit_Duration = str(request.form['duration']), Permit_Start  =str(request.form['startDate']), Permit_End=str(request.form['endDate']))
            addPermit(permit)

            return redirect(url_for('profile'))
        # Render the form template with the error messages
        return render_template("application.html", errors=errors, info = getHeaderInfo())

        # This is the code that gets executed when the current python file is
        # executed.

@app.route('/updateApp/', methods =["GET", "POST"])
@login_required
def updateApp():
    if request.method == 'POST':
        permit = dict(User_ID = session['userEmail'], Vehicle_Type=str(request.form['options']), Permit_Duration=str(request.form['Doptions']), Permit_End="")
        updatePermit(permit)
        return redirect(url_for('profile'))

    return render_template("updateApp.html", info = getHeaderInfo() , Info = getProfileInfo(session['userEmail']))

@app.route('/rules', methods =["GET", "POST"])
def rules():
	return render_template("rules.html", info = getHeaderInfo())

@app.route('/team')
def team():
	return render_templates("team.html", info = getHeaderInfo())

@app.route('/addRules/', methods =["GET", "POST"])
@admin_required
def addRules():
    rules = dict(Rule_Title="", Rules_Description="")
    if request.method == "POST":
        rules['Rule_Title'] = str(request.form['title'])
        rules['Rule_Description'] = str(request.form['description'])

        errors = ''

        if emptyField(rules['Rule_Title']) or emptyField(rules['Rule_Description']):
            errors = "Please enter all the fields."
        if not numsField(rules['Rule_Title']):
            errors = "Title should not contain numbers."
            print("Errors detected.", errors)
            print(rules)
        if not errors:
            print("No errors.")
            addRule(rules)
            return redirect(url_for('rules'))
        else:
            return render_template("addRules.html", info = getHeaderInfo())
    else:
        return render_template("addRules.html", info = getHeaderInfo())

@app.route('/updateRules/<id>', methods =["GET", "POST"])
@admin_required
def updateRules(id):
    rules = dict(Rule_ID =id, Rule_Title="", Rule_Description="")
    if request.method == "GET":
        rules = getRule(id)
        return render_template("updateRules.html", info = getHeaderInfo(), rules = rules)

    if request.method == "POST":
        rules['Rule_Title'] = str(request.form['title'])
        print (rules['Rule_Title'])
        rules['Rule_Description'] = str(request.form['description'])
        updateRule(rules)
        msg = Message(
            'Rules have been updated',
            sender='teamRocket299@gmail.com',
            recipients=
            ['oj2008@live.com.au'])
        msg.body = "the health and safety department has updated the rules"
        mail.send(msg)
        return redirect(url_for('rules'))

        if emptyField(rules['Rule_Title']) or emptyField(rules['Rule_Description']):
            errors = "Please enter all the fields."
            return render_template("updateRules.html", errors=errors, loggedIn=getLoggedIn())
        if not errors:
                print("no rule errors")
                addRule(rules)
                return redirect(url_for('rules'))
    else:
	    return render_template("updateRules.html", info = getHeaderInfo())

@app.route('/admin/rules')
def ruleSetup():
    return jsonify(ruleValues=getRules())

@app.route('/admin/rules/delete/<Rule_Id>')
@admin_required
def ruleDelete(Rule_Id):
    return jsonify(ruleValues=deleteRule(Rule_Id))

@app.route('/paymentform/<id>', methods =["GET", "POST"])
def paymentForm(id):
    if request.method == "GET":
        return render_template("paymentform.html", info = getHeaderInfo(), amt = getFineAmount(id))
    else:
        payment = {"Fine_Number" : id}
        payment['Amount'] = getOverDuePayment(id)
        payment['Date'] = now = dt.datetime.now().strftime('%d/%m/%y')
        payment['First_Name'] = str(request.form['first'])
        payment['Last_Name'] = str(request.form['last'])
        payment['Card_Name'] = payment['First_Name'] + payment['Last_Name']
        payment['Card_Type'] = str(request.form['cmbCardType'])
        payment['Card_Number'] = protectCardNum(str(request.form['cardNum']))
        payment['Expiration_date'] = str(request.form['cmbExpMon'])+"/"+str(request.form['cmbExpYr'])
        payment['Billing_Address'] = str(request.form['addr1'])+" "+str(request.form['addr2'])
        payment['City'] = str(request.form['city'])
        payment['Post_Code'] = str(request.form['zip'])
        payment['Phone'] = str(request.form['phone'])

        errors = ''
        if emptyField(payment['First_Name']) or emptyField(payment['Last_Name']) or emptyField(payment['Card_Name']) or emptyField(payment['Card_Type']) or emptyField(payment['Card_Number']) or emptyField(payment['Expiration_date']) or emptyField(payment['Billing_Address']) or emptyField(payment['City']) or emptyField(payment['Post_Code']) or emptyField(payment['Phone']):
            errors = "Please Complete All Details"
            return render_template("paymentform.html", errors = errors, info=getHeaderInfo(), amt=getFineAmount(id))
        else:
            recordPayment(payment)
            msg = Message(
                'Fine payment recieved',
                sender='teamRocket299@gmail.com',
                recipients=
                ['oj2008@live.com.au'])
            msg.body = "Your fine has been successfully paid, thank you very much"
            mail.send(msg)
            return redirect(url_for('profile'))

@app.route('/paymentInfo')
def paymentInfo():
	return render_template("paymentInfo.html", info = getHeaderInfo())

@app.route('/search')
def search():
	return render_template("search.html", info = getHeaderInfo())

@app.route('/notifications/')
def notifications():
	return render_template("notifications.html", info = getHeaderInfo())

@app.route('/report/<userID>', methods =["GET", "POST"])
@admin_required
def report(userID):
    violation = dict(Violation_Type="",Date="",Time="",Description="",Place_in_campus="",Department="")
    if request.method == "POST":
        citType = int(request.form['cmbMoreFunction'])
        violation['Date'] = str(request.form['date'])
        violation['Time'] = str(request.form['time'])
        violation['Description'] = str(request.form['desc'])
        violation['Place_in_campus'] = str(request.form['location'])
        violation['Department'] = convertDepartment(str(request.form['department']))
        violation['User_ID'] = nameToID(str(request.form['name']))

        errors = ''

        if emptyField(violation['Date']) or emptyField(violation['Time']) or emptyField(violation['Description']) or emptyField(violation['Place_in_campus']) or emptyField(violation['Department']):
            errors = "Please enter all the fields."
            print("errors detected")
            print (violation)
        if not errors:
            print("No errors")
            if citType == 0:
                violation['Violation_Type'] = "Parking"
                violation['Permit_Number'] = str(setHasPermit(request.form['permitNumber']))
                violation['Vehicle_Type'] = str(request.form['VehType'])
                violation['Vehicle_License_number'] = str(request.form['license'])
            elif citType == 1:
                violation['Violation_Type'] = "Smoking"
                violation['Supervisor'] = session['userEmail']
            else:
                violation['Violation_Type'] = "Other"
                violation['Supervisor'] = session['userEmail']
            addViolation(violation)
            return redirect(url_for('admin'))
        else:
            user = [] if userID == "new" else getProfileInfo(userID)
            return render_template("report.html", errors=errors, loggedIn=getLoggedIn(), user = user)
    else:
        user = [] if userID == "new" else getProfileInfo(userID)
        return render_template("report.html", info = getHeaderInfo(), violation=violation, user = user)

@app.route('/health/', methods =["GET", "POST"])
@login_required
def reportHAS():

    issue = dict(Issue_Number="", Date="", Time="", Person_Name="", Department="", Description="", Supervisor="", Place_in_campus="", Resolution_Date="", Resolution_Time="", Resolution_Description="")
    if request.method == "POST":

        issue['Date'] = handleDate(str(request.form['date']))
        issue['Time'] = str(request.form['time'])
        issue['Description'] = str(request.form['description'])

        issue['Place_in_campus'] = str(request.form['location'])
        issue['Department'] = convertDepartment(str(request.form['department']))

        issue['Person_Name'] = str(request.form['fname'])
        issue['Supervisor'] = str(request.form['supervisor'])

        try:
            issue['Resolution_Date'] = setResolved(str(request.form['res_date']))
            issue['Resolution_Time'] = setResolved(str(request.form['res_time']))
            issue['Resolution_Description'] = setResolved(str(request.form['res_description']))
        except:
            issue['Resolution_Date'] = setResolved("")
            issue['Resolution_Time'] = setResolved("")
            issue['Resolution_Description'] = setResolved("")

        errors = ''

        if emptyField(issue['Date']) or emptyField(issue['Time']) or emptyField(issue['Description']) or emptyField(issue['Place_in_campus']) or emptyField(issue['Department']):
            errors = "Please enter all the fields."
            print("errors detected",errors)
            print (issue)
        if not numsField(issue['Person_Name'] or numsField(issue['Supervisor'])):
            errors = "Names should not contain numbers"
        if not emptyField(issue['Date']):
            if datelimitField(issue['Date']):
                errors = "Please enter current or past date"
                print("errors detected",errors)
        if not errors:
            print("No errors")
            addIssue(issue)
            return redirect(url_for('index'))
        else:
            return render_template("addhealth.html", errors=errors, info = getHeaderInfo())
    else:
        return render_template("addhealth.html", errors=[], info = getHeaderInfo())

#Editing violation functions

@app.route('/editParking/<id>', methods=["GET", "POST"])
@admin_required
def editParking(id):
    violation = dict(Violation_Type = "Parking", Citation_Number=id, Date = "", Time = "", Description= "", Permit_Number="", Vehicle_License_number="", Vehicle_Type="")
    if request.method == "GET":
        violation = getParkingViolation(id)

        return render_template("editparking.html", info = getHeaderInfo(), violation=violation)
    elif request.method == "POST":
        violation['Violation_Type'] = "Parking"
        violation['Date'] = str(request.form['date'])
        violation['Time'] = str(request.form['time'])
        violation['Description'] = str(request.form['desc'])
        violation['Permit_Number'] = str(setHasPermit(request.form['permitNumber']))
        violation['Vehicle_Type'] = str(request.form['VehType'])
        violation['Vehicle_License_number'] = str(request.form['license'])
        updateViolation(violation)
        msg = Message(
            'Update parking violation!',
            sender='teamRocket299@gmail.com',
            recipients=
            ['oj2008@live.com.au'])
        msg.body = "Your parking violation has been updated"
        mail.send(msg)
        return redirect(url_for('admin'))


@app.route('/editOther/<id>', methods =["GET", "POST"])
@admin_required
def editOther(id):
    violation = dict(Violation_Type="", Citation_Number=id, Date="",Time="",Description="",Place_in_campus="",Department="")
    if request.method == "GET":
        violation = getOtherViolation(id)
        return render_template("editother.html", info = getHeaderInfo(), violation=violation)
    elif request.method == "POST":
        citType = int(request.form['cmbMoreFunction'])
        if citType == 1:
            violation['Violation_Type'] = "Smoking"
        else:
            violation['Violation_Type'] = "Other"

        violation['Date'] = str(request.form['date'])
        violation['Time'] = str(request.form['time'])
        violation['Description'] = str(request.form['desc'])
        violation['Place_in_campus'] = str(request.form['location'])
        violation['Department'] = convertDepartment(str(request.form['department']))
        violation['Supervisor'] = str(request.form['supervisor'])
        violation['User_ID'] = str(request.form['name'])
        updateViolation(violation)
        msg = Message(
            'Updated other violation!',
            sender='teamRocket299@gmail.com',
            recipients=
            ['oj2008@live.com.au'])
        msg.body = "Your Other violation has been updated"
        mail.send(msg)
        return redirect(url_for('admin'))

@app.route('/editHealth/<id>', methods =["GET", "POST"])
@admin_required
def editHealth(id):
    issue = dict(Issue_Number=id, Date="", Time="", Person_Name="", Department="", Description="", Supervisor="", Place_in_campus="", Resolution_Date="", Resolution_Time="", Resolution_Description="")
    if request.method == "GET":
        issue = getHealthIssue(id)
        return render_template("edithealth.html", info = getHeaderInfo(), issue=issue)
    elif request.method == "POST":
        issue['Date'] = str(request.form['date'])
        issue['Time'] = str(request.form['time'])
        issue['Person_Name'] = str(request.form['name'])
        issue['Description'] = str(request.form['description'])
        issue['Place_in_campus'] = str(request.form['location'])
        issue['Department'] = convertDepartment(str(request.form['department']))
        issue['Supervisor'] = str(request.form['supervisor'])
        issue['Resolution_Date'] = str(request.form['res_date']) if str(request.form['res_date']) != "" else None
        issue['Resolution_Time'] = str(request.form['res_time']) if str(request.form['res_time']) != "" else None
        issue['Resolution_Description'] = str(request.form['res_description']) if str(request.form['res_description']) != "" else None
        updateIssue(issue)
        msg = Message(
            'Updated Health violation!',
            sender='teamRocket299@gmail.com',
            recipients=
            ['oj2008@live.com.au'])
        msg.body = "Your Health violation has been updated"
        mail.send(msg)
        return redirect(url_for('admin'))

@app.route('/visitor')
def visitor():
    visit = dict(Name="", Email="")
    if request.method == "POST":
        visit['Name'] = str(request.form['name']).replace("-","/")
        visit['Email'] = str(request.form['email'])

        if emptyField(visit['Name']) or emptyField(visit['Email']):
            errors = "Please enter all the fields."
            print("errors detected",errors)
        if not numsField(visit['Name']):
            errors = "Names should not contain numbers"
            print("errors detected",errors)
        if not emptyField(visit['Email']):
            if emailField(visit['Email']):
                errors = "Please enter proper email format."
                print("errors detected", errors)
        if not errors:
            print("No errors")
            addIssue(visit)
            return redirect(url_for('index'))
        else:
            return render_template("index.html", info=getHeaderInfo())
    else:
        return render_template("visitor.html", info=getHeaderInfo())

@app.route('/contactus')
def contactus():
	return render_template("contactus.html", info = getHeaderInfo())

@app.route('/login/', methods =["GET", "POST"])
def login():
    #default username for error checking
    user = ""
    if 'logged_in' in session:
        if session['admin']:
            return redirect(url_for('admin'))
        return redirect(url_for('profile'))
    if request.method == "POST":
        user = str(request.form['email']).lower()
        attempt_pass = str(request.form['password'])
        if loginCheck(user, attempt_pass) == True:
            session['logged_in'] = True
            session['userEmail'] = user
            session['admin'] = checkAdmin(user)
            return redirect(url_for('profile'))

    return render_template("login.html", user = user, info = getHeaderInfo())


@app.route('/out/', methods =["GET", "POST"])
def logout():
    if 'logged_in' in session:
        session.clear()
    return redirect(url_for('logoutPage'))
   # return render_template("index.html")

@app.route('/logoutPage')
def logoutPage():
	return render_template("logout.html", info = getHeaderInfo())

@app.route('/profile/')
@login_required
def profile():
    if session['admin']:
        return redirect(url_for('admin'))
    else:
        for alerts in getUserNotifications(session['userEmail']):
            flash(alerts)
        return render_template("profile.html", profile = getProfileInfo(session['userEmail']), info = getHeaderInfo())


@app.route('/admin/')
@admin_required
def admin():
    for alerts in getUserNotifications(session['userEmail']):
        flash(alerts)
    return render_template("admin.html", Issues = getHealthIssues(), info = getHeaderInfo())

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

@app.route('/admin/users/')
@admin_required
def adminUsers():
	return jsonify(users = getAllUsers())

@app.route('/overduePayment/<fine>')
@admin_required
def adminOverdue(fine):
    msg = Message(
        'You have an Overdue Fine Payment',
        sender='teamRocket299@gmail.com',
        recipients=['oj2008@live.com.au'])

    msg.body = getFineEmailDetails(fine,True)
    mail.send(msg)

    return jsonify(status = "TRUE")



@app.route('/visitorNotification/')
def visitorEmail():
    msg = Message(
        'Atmiya: We have recieved your details!',
        sender='teamRocket299@gmail.com',
        recipients=
        ['oj2008@live.com.au'])
    msg.body = "Thank you for submitting a vistor form. We will be contacting you soon."
    mail.send(msg)

    return jsonify(status="TRUE")


@app.route('/remindPayment/<fine>')
@admin_required
def adminRemind(fine):
    msg = Message(
        'You have an Fine Payment due soon',
        sender='teamRocket299@gmail.com',
        recipients=['oj2008@live.com.au'])

    msg.body = getFineEmailDetails(fine,False)
    mail.send(msg)

    return jsonify(status = "TRUE")


@app.route('/out/')
def out():
    return render_template("out.html", info = getHeaderInfo())

@app.route('/faq')
def faq():
	return render_template("faq.html", info = getHeaderInfo())

@app.route('/about')
def about():
	return render_template("about.html", info = getHeaderInfo())

#convert Department to string
def convertDepartment(dep):
    departments = [[9,"Science and Engineering"],[10,"Law"],[11,"Health"],[12,"Creative Industries"],[13,"Business"],
    [14,"Research"],[15,"Admin"]]

    for department in departments:
        if int(dep) == department[0]:
            return department[1]

    return ""

#Takes the input for the resolution fields and sets it to the appropriate value if empty
def setResolved(inpt):
    if inpt == "":
        return None
    else:
        return inpt

#Takes the input for permit number sets it to the appropriate value if empty
def setHasPermit(inpt):
    #if not integer or is below zero
    try:
        if int(inpt) < 0:
            return None
        else: return inpt
    #Not an integer
    except:
        return None

#Replaces middle 8 digits of a credit card number with X's
def protectCardNum(number):
    number = number.strip(" ")
    return number[:3]+" XXXX XXXX "+number[12:]

def getFineEmailDetails(id, overdue):
    fine = getFine(id)
    msg = "Dear "+str(fine['Name'])+",\n\n"
    if overdue:
        msg = msg + "It has come to our attention that you have overdue payment on a fine issued to you on "+str(fine['Date'])+". We suggest you pay this fine asap to avoid further repercussions."
    else:
        msg = msg + "This is a reminder that you have a payment due on a fine issued to you on "+str(fine['Date'])+". We suggest you pay this fine asap to avoid further repercussions."
    msg = msg + "\n\nPlease find the details of the fine below:\n\n"
    msg = msg+"Date: "+str(fine['Date'])+"\nTime: "+str(fine['Time'])
    if fine['Citation_Type'] == "Other":
        msg = msg + "\nLocation: "+str(fine['Location'])

    msg = msg + "\nDescription: "+str(fine['Description'])+"\nAmount Due: $"+str(fine['Amount'])
    msg = msg + "\n\nTo pay your fine, visit the following website: http://ec2-54-206-46-45.ap-southeast-2.compute.amazonaws.com"
    msg = msg + "\n\nRegards,\nAtmiya Campus Health and Parking Department"
    return msg

#get header info
def getHeaderInfo():
    loggedIn = getLoggedIn()
    info = dict(loggedIn=False, admin=False, issues=[])
    info['loggedIn'] = loggedIn['loggedIn']
    info['admin'] = loggedIn['admin']
    info['issues'] = getUrgentHealthIssues()
    info['numIssues'] = len(info['issues'])
    return info

#Logged in function
def getLoggedIn():
    status = dict(loggedIn=False,admin=False)
    if 'logged_in' in session:
        status['loggedIn'] = True
        if session['admin']:
            status['admin'] = True

    return status

if __name__ == "__main__":
    app.secret_key = 'najhbajbsjanslda'
    app.run(debug=True)
