import unittest
import db
from views import *
import re
from testfunctions import *
from datetime import date


#Database Object
data = db.Database(filename = "Test.db")

#Alert Lists

alertmessages=["The central bridge is closed down, expect delays", "P block level 5 is closed due to cleaning","Toilets in D block have been closed for maintence"]
testmessages =[]

#Initial Database
tables = ["parkingPermits", "parkingViolations", "otherViolations", "healthAndSafetyIssues", "finePayments", "paymentDetails", "users"]
parkingPermits = [dict(User_ID = 1 , Vehicle_Type = "Two Wheeler", Department = "Administration", Permit_Duration = "Yearly", Permit_Start = "2015/11/10", Permit_End = "2016/11/10" , Approved = "Approved"),
dict(User_ID = 2 , Vehicle_Type = "Four Wheeler", Department = "General", Permit_Duration = "Monthly", Permit_Start = "2016/08/06", Permit_End = "2016/09/06" , Approved = "Pending"),
dict(User_ID = 3 , Vehicle_Type = "Other Wheeler", Department = "Science and Engineering", Permit_Duration = "Daily", Permit_Start = "2016/02/09", Permit_End = "2016/02/10" , Approved = "Approved")]

parkingViolations = [dict(User_ID = 1,Date = "2016/01/10", Time = "10:00", Description = "Illegally Parked in a handicap zone", Permit_Number = 1, Vehicle_License_number = "WAM-011", Vehicle_Type = "Two Wheeler"),
dict(User_ID = 2, Date = "2016/04/12" , Time = "12:00", Description = "Parked without a permit", Permit_Number = None, Vehicle_License_number = "BAT-089", Vehicle_Type = "Four Wheeler"),
dict(User_ID = 3, Date = "2016/02/11", Time = "14:00", Description = "Expired permit", Permit_Number = 3, Vehicle_License_number = "CHR-078", Vehicle_Type = "Other")]

otherViolations = [dict(User_ID = 1, Violation_Type = "Other", Description = "Public Nudity", Department = "Visitor", Supervisor = "Angelica Cole", Date = "2016/05/20", Time = "15:00", Place_in_campus = "In front of P Block"),
dict(User_ID = 2, Violation_Type = "Smoking", Description = None, Department = "Business", Supervisor = "Ben Parker", Date = "2016/07/30", Time = "17:00", Place_in_campus = "O Block level 2"),
dict(User_ID = 3, Violation_Type = "Other", Description = "Trespassing", Department = "Science and Engineering", Supervisor = "Thomas Wayne", Date = "2016/05/05", Time = "20:10", Place_in_campus = "B Block level 5")]

hasIssues = [dict(Date = "01/02/2016", Time = "10:00", Person_Name = "Barry Allen", Department = "Science and Engineering", Resolution_Date = "2016/02/01" , Resolution_Time = "12:00", Resolution_Description = "Chemical spill was cleaned", Supervisor = "Iris West" , Place_in_campus = "W block level 2"),
dict(Date = "02/03/2016", Time = "14:00", Person_Name = "Diana Prince", Department = "Business", Resolution_Date = None, Resolution_Time = None, Resolution_Description = None, Supervisor = "Steve Trevor", Place_in_campus = "B Block level 3"),
dict(Date = "03/05/2016", Time = "16:00", Person_Name = "Steven Strange", Department = "Arts", Resolution_Date = "2016/05/04", Resolution_Time = "20:00", Resolution_Description = "Missing Student was found", Supervisor = "Kent Nelson", Place_in_campus = "A Block level 3")]

finePayments = [dict(Citation_Number = 1, Citation_Type = "Parking", Payment_status = "Pending"),
dict(Citation_Number = 2, Citation_Type = "Parking", Payment_status = "Pending"),
dict(Citation_Number = 3, Citation_Type = "Parking", Payment_status = "Pending")]

users =[dict(User_ID = 1, Name = "Alex Parks", Email = "Alex.Parks12@atmiye.edu.au", Password = "Martha", Department = "Sci", Account_Type = "Staff"),
dict(User_ID = 2, Name = "Aaron Luthor", Email = "Aaron.Luthor@atmiye.edu.au", Password = "Wally2", Department = "Sci", Account_Type = "Student"),
dict(User_ID = 3, Name = "George Curious", Email = "George.Curious@atmiye.edu.au", Password = "StupidShinji", Department = "Sci",  Account_Type = "Visitor")]

paymentDetails = dict(Fine_Number = "1", Amount = 90, Date = "2016/10/12", Card_Name = "James", Card_Type = "Visa", Card_Number = "2353 XXXX XXXX 0234", Expiration_date = "06/19", First_Name = "James", Last_Name = "Ultron",
               Billing_Address = "12 Fake St", City = "Brisbane", Post_Code = "4000", Phone = "0411 111 111")

class TestStringMethods(unittest.TestCase):

##TEST NAME FIELD
    def testValidName(self): #Tests name field for input
        self.assertTrue(numsField('John'))

    def testTrimmedName(self): #Tests name field to trim excess space from input
        self.assertTrue(numsField('John  '))

    def testNumberedName(self):  #Tests name field for numerical inputs
        self.assertFalse(numsField('John12'))

    def testPresentName(self): #Tests name field is not empty
        self.assertFalse(emptyField('John'))

    def testMultipleName(self): #Tests first name field for multiple names
        self.assertFalse(lengthField('Johnathan Jerome'))

    def testNameLimit(self):   #Tests name field for input length. 13 Maximum
        self.assertFalse(lengthField('Johnathannnnnnnnnnnnnnnnnnnn'))

##TYPE FIELD
    def testDeptSelect(self): #Tests department field for input
        self.assertFalse(emptyField('Visitor'))

    def testDurationSelect(self): #Tests duration field for input
        self.assertFalse(emptyField('Monthly'))

    def testDurationEnd(self): #Tests duration field for end date
        self.assertFalse(emptyField('12/12/2017'))

##EMAIL FIELD
    def testPresentEmail(self): #Tests email field for present email input
        self.assertFalse(emptyField('testemail@test.test'))

    def testValidEmail(self): #Tests email field to for incorrect email addresses. Format must be xxxxx@xxx.xxx
        self.assertFalse(emailField('testemail@test.test'))


##DETAILS FIELD
    def testAgeSelect(self): #Tests age field for present input
        self.assertFalse(emptyField('12/12/1996'))

    def testPhoneLetter(self): #Tests phone number field for alphabetical input
        self.assertFalse(letterField('three one three'))

    def testPhonePresent(self): #Tests phone field for valid input
        self.assertFalse(emptyField('3138 8822'))

    def testDateYear(self): #Tests date field for input beyond the current date
        self.assertFalse(datelimitField('21/09/2016'))

    def testReverseDateYear(self): #Tests date field for input beyond the current date AND with reverse input
        self.assertFalse(datelimitField('2016/09/21'))

##DEPARTMENT FIELD

    def testDeptPresent(self): #Tests department field for present input
        self.assertFalse(emptyField('Health'))

##PAYMENT FIELDS

    def testAccountNumber(self):  #Tests account number field for numerical input
        self.assertFalse(letterField('n31176'))

    def testAccountLetterEnd(self):  #Tests account number field for inverse alphabetical input
        self.assertTrue(letterField('31176n'))

#DATABASE ACCESS AND CONTROL

##Setup Functions
    def testDatabaseRetrieve(self):  #Tests database access retrieving current permit
        self.assertTrue(retrieveField(2, "Citation_Number", 1))

    def testParkingInsert(self):    #Tests database - parking table, for valid access and insertion
        self.assertFalse(insertField("Parking"))

    def testOtherInsert(self):  #Tests database - other table, for valid access and insertion
        self.assertFalse(insertField("Other"))

    def testHSInsert(self):  #Tests database - health and safety table, for valid access and insertion
        self.assertFalse(insertField("HS"))

    def testVioInsert(self):   #Tests database - violations table, for valid access and insertion
        self.assertFalse(insertField("Vio"))

##Checking and Recieving

    def testPasswordCheck(self):  #Tests database - password access for consistent passwords with email addresses
        self.assertTrue(passwordField("Aaron.Luthor@atmiye.edu.au","Wally2"))

    def testInvalidPassword(self): #Tests password input for validity against email in database
        self.assertTrue(passwordField("Aaron.Luthor@atmiye.edu.au","Test"))

    def testUpdateViolation(self):  #Tests database - violations table for access and redability of updates
        self.assertFalse(insertField("Vio"))

    def testPaidPayment(self): #Tests database - payments table for accepted payments
        self.assertFalse(paymentField("Paid"))

    def testPendingPayment(self):  #Tests database - payments table for pending payments
        self.assertFalse(paymentField("Pending"))

    def testInvalidPaidPayment(self):   #Tests database - payments table for invalid payments
        self.assertFalse(paymentField("Invalid"))

##Teardown Functions

    def testDatabaseDelete(self):  #Tests database teardown - tests for deletion of all previously inserted elements.
        self.assertTrue(deleteField())

##Notifications
    def testNotificationAddition(self):  #Tests notifications table for access and ability to add new notifications
        self.assertTrue(noteAd("Test"))

    def testNotificationRemoval(self):  #Tests notifications table for valid removal. N.B. This makes the tests list empty.
        self.assertTrue(noteRemove())

    def testEmptyList(self):  #Tests notifications table for invalid removal if list is empty
        self.assertTrue(noteRemove())

##Account Creation and Payment Inputs

    def testUserInsert(self):  #Tests database - user table for valid insertion of test user
        self.assertTrue(userInsert())

    def testPaymentInsert(self):  #Tests database - payments table for payment insertion relating to particular permit numbers
        self.assertTrue(paymentCheck("Insert", 255))

    def testDetailsInsert(self):  #Tests database - payments table for details insertion relating to particular permit numbers
        self.assertTrue(paymentCheck("Details", 255))

    def testUpdatePayment(self):  #Tests database - payments table for ability to update payment details relating to particular permit numbers
        self.assertFalse(paymentCheck("Update", 255))

    def testCheckPaymentExist(self):  #Tests database - payments table for current outstanding payments relating to particular permit numbers
        self.assertFalse(paymentCheck("Check", 255))

    def testCheckPaymentAmount(self):  #Tests database - payments table for assigned numerical value of outstanding payments relating to particular permit numbers
        self.assertFalse(paymentCheck("Amount", 255))

    def testPaymentInvalidClaim(self): #Tests database - payments table for invalid access claims
        self.assertFalse(paymentCheck("InvalidFunction", "Test"))

    def testRemovePayment(self): #Tests database - payments table for valid removal of payments relating to particular permit numbers
        self.assertTrue(paymentCheck("Remove", 255))

    def testNonExistRemovePayment(self):  #Tests database - payments table for invalid removal of non-requried payments relating to particular permit numbers
        self.assertFalse(paymentCheck("Remove", 255))

    def testRemoveDetails(self):   #Tests database - payments table for valid removal of payments details relating to particular permit numbers
        self.assertFalse(paymentCheck("RemoveD", 255))

    def testNonExistRemoveDetails(self):  #Tests database - payments table for invalid removal of non-existent details relating to particular permit numbers
        self.assertTrue(paymentCheck("RemoveD", 255))

    def testCardProtection(self):   #Tests card protection function for valid card masking
        self.assertTrue(cardNumCheck(1111111111111111))

    def testFalseCardProtection(self):  #Tests card protection function for invalid cards
        self.assertTrue(cardNumCheck(11111111111))

    def testLoggedIn(self):  #Tests login function for websites
        self.assertFalse(checkLogin(1))

    def testLoggedOut(self):  #Tests logout function for websites
        self.assertFalse(checkLogin(2))

    def testUserRemove(self):  #Tests database - user table for valid removal of account details. N.B This removes thest user from the database.
        self.assertTrue(userDelete("Test"))

    def testNonExistUserRemove(self):#Tests database - user table for invalid removal of non existent account details
        self.assertFalse(userDelete("NonExist"))

if __name__ == '__main__':
    unittest.main()

