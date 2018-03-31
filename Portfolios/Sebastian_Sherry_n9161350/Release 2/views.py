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
        recordPayment(payment)
        return redirect(url_for('profile'))


@app.route('/notifications/')
def notifications():
	return render_template("notifications.html", info = getHeaderInfo())

@app.route('/health/', methods =["GET", "POST"])
@admin_required
def reportHAS():
    issue = dict(Issue_Number="", Date="", Time="", Person_Name="", Department="", Description="", Supervisor="", Place_in_campus="", Resolution_Date="", Resolution_Time="", Resolution_Description="")
    if request.method == "POST":
        issue['Date'] = str(request.form['date'])
        issue['Time'] = str(request.form['time'])
        issue['Description'] = str(request.form['description'])
        issue['Place_in_campus'] = str(request.form['location'])
        issue['Department'] = convertDepartment(str(request.form['department']))
        issue['Person_Name'] = str(request.form['name'])
        issue['Supervisor'] = str(request.form['supervisor'])
        issue['Resolution_Date'] = setResolved(str(request.form['res_date']))
        issue['Resolution_Time'] = setResolved(str(request.form['res_time']))
        issue['Resolution_Description'] = setResolved(str(request.form['res_description']))

        errors = ''

        if emptyField(issue['Date']) or emptyField(issue['Time']) or emptyField(issue['Description']) or emptyField(issue['Place_in_campus']) or emptyField(issue['Department']):
            errors = "Please enter all the fields."
            print("errors detected")
            print (issue)
        if not errors:
            print("No errors")
            addIssue(issue)
            return redirect(url_for('index'))
        else:
            return render_template("addHealth.html", errors=errors, info = getHeaderInfo())
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
        violation['Permit_Number'] = str(request.form['permitNumber'])
        violation['Vehicle_Type'] = str(request.form['VehType'])
        violation['Vehicle_License_number'] = str(request.form['license'])
        updateViolation(violation)
        return redirect(url_for('admin'))


@app.route('/editOther/<id>', methods =["GET", "POST"])
@admin_required
def editOther(id):
    violation = dict(Violation_Type="", Citation_Number=id, Date="",Time="",Description="",Place_in_campus="",Department="")
    if request.method == "GET":
        violation = getOtherViolation(id)
        print(violation)
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
        return redirect(url_for('admin'))

@app.route('/admin/users/')
@admin_required
def adminUsers():
	return jsonify(users = getAllUsers())


#convert Department to string
def convertDepartment(dep):
    departments = [[9,"Science and Engineering"],[10,"Law"],[11,"Health"],[12,"Creative Industries"],[13,"Business"],
    [14,"Research"],[15,"Admin"]]

    for department in departments:
        if int(dep) == department[0]:
            return department[1]

    return ""

#Takes the input form the resolution fields and sets it to the appropriate value if empty
def setResolved(inpt):
    if inpt == "":
        return None
    else:
        return inpt

#Replaces middle 8 digits of a credit card number with X's
def protectCardNum(number):
    number = number.strip(" ")
    return number[:3]+" XXXX XXXX "+number[12:]

#get header info
def getHeaderInfo():
    loggedIn = getLoggedIn()
    info = dict(loggedIn=False, admin=False, issues=[])
    info['loggedIn'] = loggedIn['loggedIn']
    info['admin'] = loggedIn['admin']
    info['issues'] = getUrgentHealthIssues()
    info['numIssues'] = len(info['issues'])
    return info
