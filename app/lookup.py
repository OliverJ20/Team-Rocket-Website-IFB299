#imports
import db
import datetime as dt

"""
Profile Page accessor
Grabs the relivant information for a profile page
id can be an email or User_ID
"""
def getProfileInfo(id):
    data = db.Database(filename = "IFB299.db")
    info = dict(Name = "", Department = "", Permit = [], ParkingVil = [], OtherVil = [])
    #try is as User_ID
    try:
        user = data.retrieve("users", "User_ID", int(id))
    except:
        user = data.retrieve("users", "Email", id)
    info["Name"] = user['Name']
    info["Department"] = user['Department']
    info["Permit"] = data.retrieve("parkingPermits", "User_ID", user['User_ID'])
    #if permit, look for parking Violations
    if info["Permit"] != []:
        info["ParkingVil"] = data.retrieveMulti("parkingViolations", "Permit_Number", info["Permit"]['Permit_Number'])
        for entry in info['ParkingVil']:
            entry['Fine_Number'] = data.retrieveFine("Parking", entry['Citation_Number'])["Fine_Number"]
            #Don't display fine that's been payed
            if getStatus(entry, "Parking") == "Paid": info["ParkingVil"].remove(entry)
    info["OtherVil"] = data.retrieveMulti("otherViolations", "User_ID", user['User_ID'])
    for entry in info['OtherVil']:
        entry['Fine_Number'] = data.retrieveFine("Other", entry['Citation_Number'])["Fine_Number"]
        #Don't display fine that's been payed
        if getStatus(entry, "Other") == "Paid": info["OtherVil"].remove(entry)
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

        #grab all parking Violations performed by this user to get Citation_Number
        res = data.retrieveMulti("parkingViolations","Permit_Number",violation["User_ID"])
        #asign the last entry's Citation_Number, as this would be the same violation
        violation['Citation_Number'] = res[len(res)-1]['Citation_Number']

    else:
        violation['Supervisor'] = data.retrieve("users", "Email", violation['Supervisor'])['Name']
        data.insertOtherViolation(violation)
        #for payment information
        violation['Violation_Type'] == "Other"

        #grab all other Violations performed by this user to get Citation_Number
        res = data.retrieveMulti("otherViolations","User_ID",violation['User_ID'])
        #asign the last entry's Citation_Number, as this would be the same violation
        violation['Citation_Number'] = res[len(res)-1]['Citation_Number']

    #Add notification
    data.insertUserNotification(dict(User_ID = violation['User_ID'], Notification_Type = "New Parking Violation"))
    #Add a new payment entry to track payment
    trackNewPayment(violation)
    data.close()


def addRule(rule):
    data = db.Database(filename="IFB299.db")
    data.insertRules(rule)
       #Add notification
    #data.insertUserNotification(dict(User_ID = User_ID, Notification_Type = "New Parking Violation"))
    for users in data.retrieveAll("users"):
        data.insertUserNotification(dict(User_ID=users['User_ID'], Notification_Type="Rules Added"))

    data.close()

def getHealthIssues():
    data = db.Database(filename="IFB299.db")
    res = data.retrieveAll("healthAndSafetyIssues")
    data.close()
    return res

def getRules():
    data = db.Database(filename="IFB299.db")
    rulesLookup = data.retrieveAll("rulesDB")
    data.close()
    return rulesLookup

def getRule(id):
    data = db.Database(filename="IFB299.db")
    rule = data.retrieve("rulesDB", "Rule_ID", id)
    data.close()
    return rule

def getUrgentHealthIssues():
    issues = getHealthIssues()
    urgent = []
    for issue in issues:
        if issue['Resolution_Date'] == None:
            urgent.append(issue)
    return urgent

def getParkingViolations():
    data = db.Database(filename="IFB299.db")
    res = data.retrieveAll("parkingViolations")
    for entry in res:
        #Set payment status of the violation
        entry['Status'] = getStatus(entry, "Parking")
        if entry['Status'] != "Paid":
            entry['Fine_Number'] = data.retrieveFine("Parking", entry['Citation_Number'])["Fine_Number"]
    data.close()
    return res

def getOtherViolations():
    data = db.Database(filename="IFB299.db")
    res = data.retrieveAll("otherViolations")
    for entry in res:
        entry['Status'] = getStatus(entry, "Other")
        if entry['Status'] != "Paid":
            entry['Fine_Number'] = data.retrieveFine("Other", entry['Citation_Number'])["Fine_Number"]
    data.close()
    return res

def getFine(id):
    """Makes dictionary for fine reminder emails"""
    data = db.Database(filename="IFB299.db")
    fine = data.retrieve("finePayments","Fine_Number",id)
    if fine['Citation_Type'] == "Parking":
        violation = getParkingViolation(id)
    else:
        violation = getOtherViolation(id)
        fine['Location'] = violation['Place_in_campus']

    fine['Name'] = violation['User_ID']
    fine['Description'] = violation['Description']
    fine['Date'] = dt.datetime.strptime(violation['Date'],'%d/%m/%Y').strftime('%d/%m/%Y')
    fine['Time'] = violation['Time']
    fine['Amount'] = getFineAmount(id)
    return fine
    data.close()

def getOverDuePayment(id):
    """Returns the amount of money to add for an overdue fine"""
    data = db.Database(filename="IFB299.db")
    fine = data.retrieve("finePayments","Fine_Number",id)
    issueDate = ""
    if fine['Citation_Type'] == "Parking":
        issueDate = dt.datetime.strptime(data.retrieve("parkingViolations","Citation_Number",fine['Citation_Number'])['Date'],'%d/%m/%Y')
    else:
        issueDate = dt.datetime.strptime(data.retrieve("otherViolations","Citation_Number",fine['Citation_Number'])['Date'],'%d/%m/%Y')

    overdue = dt.datetime.now().date() - issueDate.date()
    data.close()
    #add $5 for every week overdue
    return 5 * int(overdue.days / 7)

def getFineAmount(id):
    """Calculates cost of fine"""
    data = db.Database(filename="IFB299.db")
    fine = data.retrieve("finePayments","Fine_Number",id)
    if fine['Citation_Type'] == "Parking":
        amt = 90 + getOverDuePayment(id)
    else:
        amt = 50 + getOverDuePayment(id)
    data.close()
    return amt

def getAllUsers():
    data = db.Database(filename="IFB299.db")
    res = data.retrieveAll("users")
    data.close()
    return res

def getHealthIssue(id):
    data = db.Database(filename="IFB299.db")
    res = data.retrieve("healthAndSafetyIssues", "Issue_Number", id)
    #res['User_ID'] = data.retrieve("users", "User_ID", res['User_ID'])['Name']
    data.close()
    return res

def getParkingViolation(id):
    data = db.Database(filename="IFB299.db")
    res = data.retrieve("parkingViolations", "Citation_Number", id)
    data.close()
    return res

def getOtherViolation(id):
    data = db.Database(filename="IFB299.db")
    res = dict(data.retrieve("otherViolations", "Citation_Number", id))
    res['User_ID'] = data.retrieve("users", "User_ID", res['User_ID'])['Name']
    data.close()
    return res

def addIssue(issue):
    data = db.Database(filename="IFB299.db")
    data.insertHealthAndSafetyIssue(issue)
    data.close()

def addPermit(permit):
    data = db.Database(filename="IFB299.db")
    permit['User_ID'] = data.retrieve("users", "Email", permit['User_ID'])['User_ID']
    data.insertParkingPermit(permit)
    data.close()

def updateIssue(issue):
    data = db.Database(filename="IFB299.db")
    oldIssue = data.retrieve("healthAndSafetyIssues", "Issue_Number", issue['Issue_Number'])
    for key in issue:
        if issue[key] != oldIssue[key]:
            res = data.updateHealthAndSafetyIssue(key, issue[key], issue['Issue_Number'])
    data.close()

def updateRule(rules):
    data = db.Database(filename="IFB299.db")


    oldRules = data.retrieve("rulesDB", "Rule_ID", rules['Rule_ID'])
    for key in rules:
        if rules[key] != oldRules[key]:

            res = data.updateRulesDB(key, rules[key], rules['Rule_ID'])


    for users in data.retrieveAll("users"):
        {


            data.insertUserNotification(dict(User_ID=users['User_ID'], Notification_Type="Rules Changed"))
        }
    data.close()

def updateViolation(violation):
    data = db.Database(filename="IFB299.db")
    if violation['Violation_Type'] == "Parking":
        oldViolation = data.retrieve("parkingViolations", "Citation_Number", violation['Citation_Number'])
        for key in violation:
            if key != "Violation_Type": data.updateParkingViolation(key, violation[key], violation['Citation_Number'])
    else:
        oldViolation = data.retrieve("otherViolations", "Citation_Number", violation['Citation_Number'])
        for key in violation:
            if key != "Violation_Type": data.updateOtherViolation(key, violation[key], violation['Citation_Number'])
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

#Checks the inputed date and formats it to dd/mm/yyyy format. If fails, makes null to fail form validation
def handleDate(date):
    #replace - with /
    date = date.replace("-","/")
    #try dd/mm/yyyy format
    try:
        date = dt.datetime.strptime(date,'%d/%m/%Y')
    #if fails, try reverse
    except:
        try:
            date = dt.datetime.strptime(entry['Date'],'%Y/%m/%d')
        except:
            #return empty string to trigger form checking
            return ''
    #if either succed, return string of the formatted dateSplit
    return date.strftime('%d/%m/%Y')

#Name to User_ID functions
def nameToID(name):
    data = db.Database(filename="IFB299.db")
    ID = data.retrieve("users", "Name", name)['User_ID']
    data.close()
    return ID

#Fine payment Processing
def trackNewPayment(violation):
    """Add a new payment status for a violation"""
    data = db.Database(filename="IFB299.db")
    payment = dict(Citation_Number = violation["Citation_Number"], Citation_Type = violation["Violation_Type"], Payment_status = "Pending")
    data.insertFinePayment(payment)
    data.close()

def recordPayment(payment):
    """Records a payment of a violation"""
    data = db.Database(filename="IFB299.db")
    data.insertPaymentDetails(payment)
    data.updateFinePayment("Payment_status", "Paid", payment['Fine_Number'])
    #Add notification
    fine = data.retrieve("finePayments","Fine_Number",payment['Fine_Number'])
    if fine['Citation_Type'] == "Parking":
        User_ID = data.retrieve("parkingViolations","Citation_Number",fine['Citation_Number'])['User_ID']
    else:
        User_ID = data.retrieve("otherViolations","Citation_Number",fine['Citation_Number'])['User_ID']
    data.insertUserNotification(dict(User_ID = User_ID, Notification_Type = "Fine Payment Recieved"))
    data.close()

def getViolationType(id):
    """Get Violation_Type from Fine_Number"""
    data = db.Database(filename="IFB299.db")
    vType = data.retrieve("finePayments", "Fine_Number", id)['Citation_Type']
    data.close()
    return vType

def getStatus(entry, vType):
    """gets the payment status for a violation"""
    data = db.Database(filename="IFB299.db")
    fine = data.retrieveFine(vType, entry['Citation_Number'])
    if fine['Payment_status'] == "Pending":
        date = dt.datetime.strptime(entry['Date'],'%d/%m/%Y')
        overdue = dt.datetime.now().date() - date.date()
        if overdue.days >= 7:
            return "Overdue"
        else:
            return "Pending"
    else:
        return "Paid"

def getUserNotifications(email):
    data = db.Database(filename = "IFB299.db")
    User_ID = data.retrieve("users", "Email", email)['User_ID']
    #Create overdue fine notifications
    makeOverdueFineNotifications(User_ID)
    res = data.retrieveMulti("userNotifications","User_ID",User_ID)
    notifications = []
    for alert in res:
        if alert['Notification_Type'] == "New Parking Violation":
            notifications.append("You have a new parking fine.")
        elif alert['Notification_Type'] == "New Campus Violation":
            notifications.append("You have a new campus fine.")
        elif alert['Notification_Type'] == "Fine Payment Recieved":
            notifications.append("Your fine payment has been recieved")
        elif alert['Notification_Type'] == "Parking Fine Overdue":
            notifications.append("You have an overdue Parking fine.")
        elif alert['Notification_Type'] == "Rules Changed":
            notifications.append("Rules have been updated.")
        elif alert['Notification_Type'] == "Rules Added":
            notifications.append("Rules have been added.")
        elif alert['Notification_Type'] == "Campus Fine Overdue":
            notifications.append("You have an overdue campus fine.")

    #Remove notifications
    data.delete("userNotifications","User_ID",User_ID)
    data.close()
    return notifications

def deleteRule(Rule_ID):
    data = db.Database(filename = "IFB299.db")
    #Create overdue fine notifications

    data.delete("rulesDB","Rule_ID",Rule_ID)
    data.close()

def makeOverdueFineNotifications(id):
    data = db.Database(filename = "IFB299.db")
    #get parking violations
    res = data.retrieveMulti("parkingViolations","User_ID",id)
    #Check parking Violations for overdue fines
    for fine in res:
        if getStatus(fine, "Parking") == "Overdue": data.insertUserNotification(dict(User_ID = id, Notification_Type = "Parking Fine Overdue"))

    #get other violations
    res = data.retrieveMulti("otherViolations","User_ID",id)
    #Check parking Violations for overdue fines
    for fine in res:
        if getStatus(fine, "Other") == "Overdue": data.insertUserNotification(dict(User_ID = id, Notification_Type = "Campus Fine Overdue"))
