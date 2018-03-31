from db import *
import views
import re
from forms import *
from datetime import date, datetime

##Test functions for use in test cases.

##WEBFROM VALIDITY AND INPUT CHECK FUNCTION

##TEST NAME FIELD
def emptyField(field):
    field.strip()
    if not field:
        return True
    else:
        return False

def lengthField(field):
    field.strip()
    if not re.match("^[a-zA-Z]{0,13}$", field):
        return False
    else:
        return True

def numsField(field):
    if field == False or field == True:
        return True
    else:
        field.strip()
        if re.match('.*[0-9]+', field):
            return False
        else:
            return True

##TYPE FIELD
def letterField(field):
    field.strip()
    if re.match('[a-zA-Z]+', field):
        return False
    else:
        return True

def agelimitField(field):
    if field < 17:
        return False
    else:
        return True

##EMAIL FIELD
def emailField(field):
    field.strip()
    if not re.match("^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$", field):
        return False
    elif not field :
        return True
    else:
        return False

##DETAILS FIELD
def dateSwap(range): #This function serves the purpose of "flipping" date values in the datelimitField function
    if range[0] > range[1]:
        temp = range[0]
        range[0]=range[2]
        range[2]=temp
        return range
    else:
        return range

def datelimitField(field):
    fieldlist = field.split('/')
    if fieldlist[0] > fieldlist[1]:
        dateSwap(fieldlist)
        fieldlist[2] = int(fieldlist[2])
        fieldlist[0] = int(fieldlist[0])
        if fieldlist[2] < date.today().year or fieldlist[0] < date.today().year:
            return False
        else:
            return True
    else:
        dateTest = datetime.strptime(field,'%d/%m/%Y')
        if dateTest.date() <= date.today():
            return False
        else:
            return True

##DATABASE ACCESS AND CONTROL FUNCTIONS

def retrieveField(field, key, val):
    if data.retrieve(tables[field], key, val) == data.retrieve(tables[field], key, val):
        return True
    else:
        return False

def insertField(type):
    change = False
    if type == "Parking":
        data.insertParkingPermit(dict(User_ID=1000, Vehicle_Type="Two Wheeler", Department="Admin", Permit_Duration="Yearly",Permit_Start="10/11/2015", Permit_End="10/11/2016", Approved="Approved"))
        change = True
        data.delete(tables[0], "User_ID", 1000)
    elif type == "Other":
        data.insertOtherViolation(dict(User_ID=1000, Violation_Type="Other", Description="Public Nudity", Department="Visitor",Supervisor="Angelica Cole", Date="2016/05/20", Time="15:00", Place_in_campus="In front of P Block"))
        change = True
        data.delete(tables[2], "User_ID", 1000)
    elif type == "HS":
        data.insertHealthAndSafetyIssue(dict(Date="01/02/2016", Time="10:00", Person_Name="Test", Department="Science and Engineering", Description="Yes", Resolution_Date="2016/02/01", Resolution_Time="12:00",Resolution_Description="Chemical spill was cleaned", Supervisor="Iris West",Place_in_campus="W block level 2"))
        change = True
        data.delete(tables[3], "Person_Name", "Test")
    elif type == "Vio":
        data.insertParkingViolation(dict(User_ID=1000, Date="2016/01/10", Time="10:00", Description="Illegally Parked in a handicap zone", Permit_Number=1000,Vehicle_License_number="WAM-011", Vehicle_Type="Two Wheeler"))
        change = True
        data.delete(tables[1], "Permit_Number", 1000)
    if change:
        return False
    else:
        return True

def passwordField(email, password):
    if (email, password) == data.passwordCheck(email, password):
        return False
    else:
        return True

def deleteField():
    data.insertParkingPermit(dict(User_ID = 1000 , Vehicle_Type = "Two Wheeler", Department = "Admin", Permit_Duration = "Yearly", Permit_Start = "10/11/2015", Permit_End = "10/11/2016" , Approved = "Approved"))
    if  data.retrieve(tables[0], "User_ID", 1000):
        data.delete(tables[0], "User_ID", 1000)
        return True
    else:
        return False

def paymentField(status):
    if data.retrieve(tables[4],"Payment_status", status):
        return True
    else:
        return False

def noteAd(notification):
    listlength = len(alertmessages)
    alertmessages.append(notification)
    if listlength < len(alertmessages):
        return True
    else:
        return False

def noteRemove():
    listlength = len(alertmessages)
    alertmessages.pop()
    if listlength > len(alertmessages):
        return True
    elif listlength <= len(alertmessages):
        return False

def existingCheck(newtype, id):
    if newtype == "OverduePayment":
        return True
    if newtype == "PaymentTest":
        if getFine(1000):
            return True
        else:
            return False

def cardNumCheck(cardnumber):
    testcard = views.protectCardNum(str(cardnumber))
    if re.match(".*X", testcard):
        return True
    else:
        return False

def checkLogin(ID):
    if(ID == 1):
        status = dict(loggedIn=False,admin=False)
    if(ID == 2):
        status = dict(loggedIn=True,admin=True)
    if status:
        return False
    else:
        return True

def userInsert():
    data.insertUser(dict(Name = "Test",Email = "Test",Password = "Test", Department = "Test", Account_Type = "Test"))
    if data.retrieve("Users", "Email", "Test"):
        return True
    else:
        return False

def userDelete(Test):
    if data.retrieve("Users", "Email", Test):
        data.delete("Users", "Name", Test)
        if data.retrieve("Users", "Email", Test):
            return False
        else:
            return True
    else:
        return False

def paymentCheck(action, other):
    if action == "Insert":
        data.insertFinePayment(dict(Citation_Number = other, Citation_Type = "Test", Payment_status = "Testing"))
        if data.retrieve("finePayments", "Citation_Number", other):
            return True
        else:
            return False
    elif action == "Details":
        data.insertPaymentDetails(dict(Fine_Number = other, Amount = 90, Date = "2016/10/12", Card_Name = "Test", Card_Type = "Test", Card_Number = "1111 XXXX XXXX 1111", Expiration_date = "06/19", First_Name = "Test", Last_Name = "Test",
               Billing_Address = "12 Test St", City = "Brisbane", Post_Code = "4000", Phone = "0411 111 111"))
        if data.retrieve("paymentDetails", "Fine_Number", other):
            return True
        else:
            return False
    elif action == "Check":
        if data.retrieve("paymentDetails", "Fine_Number", other):
            return True
        else:
            return False
    elif action == "Amount":
        if data.retrieve("paymentDetails", "Fine_Number", other):
            amount = ("paymentDetails", "Amount")
            if amount:
                return True
        else:
            return False
    elif action == "Remove":
        if data.retrieve("finePayments", "Citation_Number", other):
            data.delete("finePayments", "Citation_Number", other)
            if data.retrieve("finePayments", "Citation_Number", other):
                return False
            else:
                return True
        else:
                return False
    elif action == "Update":
        if data.retrieve("paymentDetails", "Fine_Number", other):
            return True
        else:
            return False
    elif action == "RemoveD":
        if data.retrieve("paymentDetails", "Fine_Number", other):
            data.delete("paymentDetails", "Fine_Number", other)
            if data.retrieve("paymentDetails", "Fine_Number", other):
                return False
            else:
                return True
        else:
                return False
    else:
        return False
