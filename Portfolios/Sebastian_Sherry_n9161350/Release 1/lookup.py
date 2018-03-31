#imports
import db

"""
Profile Page accessor
Grabs the relivant information for a profile page
"""
def getProfileInfo(email):
    data = db.Database(filename = "IFB299.db")
    info = dict(Name = "", Permit = [], ParkingVil = [], OtherVil = [])
    user = data.retrieve("users", "Email", email)
    info["Name"] = user['Name']
    info["Permit"] = data.retrieve("parkingPermits", "User_ID", user['User_ID'])
    #if permit, look for parking Violations
    if info["Permit"] != []:
        info["ParkingVil"] = data.retrieveMulti("parkingViolations", "Permit_Number", info["Permit"]['Permit_Number'])
    info["OtherVil"] = data.retrieveMulti("otherViolations", "User_ID", user['User_ID'])
    data.close()
    return info

"""Connects with Database for login checks"""
def loginCheck(email,password):
    data = db.Database(filename = "IFB299.db")
    res = data.passwordCheck(email, password)
    data.close()
    return res

def register(user):
    data = db.Database(filename="IFB299.db")
    data.insertUser(user)
    data.close()

def checkAdmin(email):
    data = db.Database(filename = "IFB299.db")
    res = data.retrieve("users", "Email", email)
    data.close()
    if res['Account_Type'] == "Admin":
        return True
    else: return False

def addViolation(violation):
    data = db.Database(filename="IFB299.db")
    if violation['Violation_Type'] == "Parking":
        data.insertParkingViolation(violation)
    else:
        violation['Supervisor'] = data.retrieve("users", "Email", violation['Supervisor'])['Name']
        data.insertOtherViolation(violation)
    data.close()

def getHealthIssues():
    data = db.Database(filename="IFB299.db")
    res = data.retrieveAll("healthAndSafetyIssues")
    data.close()
    return res

def getParkingViolations():
    data = db.Database(filename="IFB299.db")
    res = data.retrieveAll("parkingViolations")
    data.close()
    return res

def getOtherViolations():
    data = db.Database(filename="IFB299.db")
    res = data.retrieveAll("otherViolations")
    data.close()
    return res

def getHealthIssue(id):
    data = db.Database(filename="IFB299.db")
    res = data.retrieve("healthAndSafetyIssues", "Issue_Number", id)
    res['User_ID'] = data.retrieve("users", "User_ID", res['User_ID'])['Name']
    data.close()
    return res

def getParkingViolation(id):
    data = db.Database(filename="IFB299.db")
    res = data.retrieve("parkingViolations", "Citation_Number", id)
    res['User_ID'] = data.retrieve("parkingPermits", "Permit_Number", res['Permit_Number'])['User_ID']
    res['User_ID'] = data.retrieve("users", "User_ID", int(res['User_ID']))['Name']
    data.close()
    return res

def getOtherViolation(id):
    data = db.Database(filename="IFB299.db")
    res = dict(data.retrieve("otherViolations", "Citation_Number", id))
    res['User_ID'] = data.retrieve("users", "User_ID", res['User_ID'])['Name']
    print(res['Place_in_campus'],res['Description'],res['Department'])
    data.close()
    return res

def addIssue(issue):
    data = db.Database(filename="IFB299.db")
    data.insertHealthAndSafetyIssue(issue)
    data.close()

def updateIssue(issue):
    data = db.Database(filename="IFB299.db")
    oldIssue = data.retrieve("healthAndSafetyIssues", "Issue_Number", issue['Issue_Number'])
    for key in issue:
        if issue[key] != oldIssue[key]:
            res = data.updateHealthAndSafetyIssue(key, issue[key], issue['Issue_Number'])
    data.close()

def updatePermit(permit):
    data = db.Database(filename="IFB299.db")
    permit['User_ID'] = data.retrieve("users", "Email", permit['User_ID'])['User_ID']
    oldPermit = data.retrieve("parkingPermits", "User_ID", permit['User_ID'])
    permit['Permit_End'] = changeEndDate(oldPermit['Permit_Start'], permit['Permit_Duration'])

    for key in permit:
        res = data.updateParkingPermit(key, permit[key], oldPermit['Permit_Number'])

    data.close()

def changeEndDate(date, duration):
    dateSplit = date.split("/")
    if duration == "Yearly":
        dateSplit[2] = int(dateSplit[2])+1
    else:
        dateSplit[1] = int(dateSplit[1])+1

    #fix illegal date
    dateSplit = checkLegalDate(dateSplit)
    return padDate(dateSplit[0])+"/"+padDate(dateSplit[1])+"/"+str(dateSplit[2])

def padDate(num):
    if int(num) < 10:
        return "0"+str(num)
    else:
        return str(num)

#Checks if a date is illegal and fixes it if necessary
def checkLegalDate(date):
    # list of all months which don't have 31 days
    months = [[2,28],[4,30],[6,30],[9,30],[11,30]]
    for month in months:
        #If months match and the day greater than the amount of days in the month
        if month[0] == int(date[1]) and month[1] < int(date[0]):
            #Set date to first of the next month
            date[0] = 1
            date[1]+= 1
            break

    return date
