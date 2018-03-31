import db

#Inital Data
tables = ["parkingPermits", "parkingViolations", "otherViolations", "healthAndSafetyIssues", "finePayments", "users"]

parkingPermits = [dict(User_ID = 1 , Vehicle_Type = "Two Wheeler", Department = "Administration", Permit_Duration = "Yearly", Permit_Start = "2015/11/10", Permit_End = "2016/11/10" , Approved = "Approved"),
dict(User_ID = 2 , Vehicle_Type = "Four Wheeler", Department = "General", Permit_Duration = "Monthly", Permit_Start = "2016/08/06", Permit_End = "2016/09/06" , Approved = "Pending"),
dict(User_ID = 3 , Vehicle_Type = "Other Wheeler", Department = "Science and Engineering", Permit_Duration = "Daily", Permit_Start = "2016/02/09", Permit_End = "2016/02/10" , Approved = "Approved")]

parkingViolations = [dict(Date = "2016/01/10", Time = "10:00", Description = "Illegally Parked in a handicap zone", Permit_Number = 1, Vehicle_License_number = "WAM-011", Vehicle_Type = "Two Wheeler"),
dict(Date = "2016/04/12" , Time = "12:00", Description = "Parked without a permit", Permit_Number = None, Vehicle_License_number = "BAT-089", Vehicle_Type = "Four Wheeler"),
dict(Date = "2016/02/11", Time = "14:00", Description = "Expired permit", Permit_Number = 3, Vehicle_License_number = "CHR-078", Vehicle_Type = "Other")]

otherViolations = [dict(User_ID = 1, Violation_Type = "Other", Description = "Public Nudity", Department = "Visitor", Supervisor = "Angelica Cole", Date = "2016/05/20", Time = "15:00", Place_in_campus = "In front of P Block"),
dict(User_ID = 2, Violation_Type = "Smoking", Description = None, Department = "Business", Supervisor = "Ben Parker", Date = "2016/07/30", Time = "17:00", Place_in_campus = "O Block level 2"),
dict(User_ID = 3, Violation_Type = "Other", Description = "Trespassing", Department = "Science and Engineering", Supervisor = "Thomas Wayne", Date = "2016/05/05", Time = "20:10", Place_in_campus = "B Block level 5")]

hasIssues = [dict(Date = "01/02/2016", Time = "10:00", Person_Name = "Barry Allen", Department = "Science and Engineering", Resolution_Date = "2016/02/01" , Resolution_Time = "12:00", Resolution_Description = "Chemical spill was cleaned", Supervisor = "Iris West" , Place_in_campus = "W block level 2"),
dict(Date = "02/03/2016", Time = "14:00", Person_Name = "Diana Prince", Department = "Business", Resolution_Date = None, Resolution_Time = None, Resolution_Description = None, Supervisor = "Steve Trevor", Place_in_campus = "B Block level 3"),
dict(Date = "03/05/2016", Time = "16:00", Person_Name = "Steven Strange", Department = "Arts", Resolution_Date = "2016/05/04", Resolution_Time = "20:00", Resolution_Description = "Missing Student was found", Supervisor = "Kent Nelson", Place_in_campus = "A Block level 3")]

finePayments = [dict(Citation_Number = 1, Payment_status = "Paid"),
dict(Citation_Number = 2, Payment_status = "Further Processing"),
dict(Citation_Number = 3, Payment_status = "Pending")]

users =[dict(User_ID = 1, Name = "Alex Parks", Email = "Alex.Parks12@atmiye.edu.au", Password = "Martha", Account_Type = "Staff"),
dict(User_ID = 2, Name = "Aaron Luthor", Email = "Aaron.Luthor@atmiye.edu.au", Password = "Wally2", Account_Type = "Student"),
dict(User_ID = 3, Name = "George Curious", Email = "George.Curious@atmiye.edu.au", Password = "StupidShinji", Account_Type = "Visitor")]

def printTable(db, table):
    for entry in db.retrieveAll(table):
        print(entry)

def resetDatabase():
    d = db.Database(filename = "Test.db")
    d.RunSQL('drop table parkingPermits')
    d.RunSQL('drop table parkingViolations')
    d.RunSQL('drop table otherViolations')
    d.RunSQL('drop table healthAndSafetyIssues')
    d.RunSQL('drop table finePayments')
    d.RunSQL('drop table users')
    d.close()

#Main
if __name__ == "__main__":
    #Reset Database
    print("Reseting database")
    resetDatabase()

    #Make connection to Database
    print("Connecting to Database")
    db = db.Database(filename = "Test.db")

    #============================================================#
    #Insertion
    #============================================================#
    print("Inserting into tables")
    #Insert Parking Permits
    print("\nInserting Parking Permits")
    for entry in parkingPermits:
        db.insertParkingPermit(entry)
    printTable(db, tables[0])

    #Insert Parking Violations
    print("\nInserting Parking Violations")
    for entry in parkingViolations:
        db.insertParkingViolation(entry)
    printTable(db, tables[1])

    #Insert other Violations
    print("\nInserting other Violations")
    for entry in otherViolations:
        db.insertOtherViolation(entry)
    printTable(db, tables[2])

    #Insert Health and Safety Issues
    print("\nInserting Health and Safety Issues")
    for entry in hasIssues:
        db.insertHealthAndSafetyIssue(entry)
    printTable(db, tables[3])

    #Insert fine payments
    print("\nInserting Fine Payments")
    for entry in finePayments:
        db.insertFinePayment(entry)
    printTable(db, tables[4])

    #Insert Users
    print("\nInserting Users")
    for entry in users:
        db.insertUser(entry)
    printTable(db, tables[5])

    #============================================================#
    #Update
    #============================================================#
    print("\nUpdating Tables")

    #Updating Parking Permits ID = 2
    print("\nParking Permits")
    print("Updating Approved")
    print("Before:", db.retrieve(tables[0], "Permit_Number", 2))
    db.updateParkingPermit("Approved", "Approved", 2)
    print("After:", db.retrieve(tables[0], "Permit_Number", 2))

    #Updating Parking Violations ID = 3
    print("\nParking Violations")
    print("Updating Vehicle_Type")
    print("Before:", db.retrieve(tables[1], "Citation_Number", 3))
    db.updateParkingViolation("Vehicle_Type", "Two Wheeler", 3)
    print("After:", db.retrieve(tables[1], "Citation_Number", 3))

    #Updating other Violations ID = 1
    print("\nOther Violations")
    print("Updating Violation_Type")
    print("Before:", db.retrieve(tables[2], "Citation_Number", 1))
    db.updateOtherViolation("Violation_Type", "Smoking", 1)
    print("After:", db.retrieve(tables[2], "Citation_Number", 1))

    #Updating Health and Safety Issues ID = 2
    print("\nHealth and Safety Issues")
    print("Updating Resolution_Date")
    print("Before:", db.retrieve(tables[3], "Issue_Number", 2))
    db.updateHealthAndSafetyIssue("Resolution_Date", "2016/07/13", 2)
    print("After:", db.retrieve(tables[3], "Issue_Number", 2))

    #Updating fine payments ID = 3
    print("\nFine Payments")
    print("Updating Payment_status")
    print("Before:", db.retrieve(tables[4], "Citation_Number", 3))
    db.updateFinePayment("Payment_status", "Paid", 3)
    print("After:", db.retrieve(tables[4], "Citation_Number", 3))

    #Updating Users ID = 1
    print("\nUsers")
    print("Updating Password")
    print("Before:", db.retrieve(tables[5], "User_ID", 1))
    db.updateUser("Password", "ThisIsAPassword", 1)
    print("After:", db.retrieve(tables[5], "User_ID", 1))

    #============================================================#
    #Delete
    #============================================================#
    print("\nDelete from Tables")
    entry = dict(User_ID = 3, Violation_Type = "Smoking", Description = "Smoking in smoke free zone", Department = "Visitor", Supervisor = "Angelica Cole", Date = "2016/08/31", Time = "11:00", Place_in_campus = "In front of P Block")
    db.insertOtherViolation(entry)
    print("Before")
    printTable(db, tables[2])
    db.delete(tables[2], "User_ID", 3)
    print("After")
    printTable(db, tables[2])

    #============================================================#
    #Password checking
    #============================================================#
    print("\nPassword checking")
    print("Correct Password")
    print("User_ID: 2 Password: Wally2")
    print("Result:", db.passwordCheck("Aaron.Luthor@atmiye.edu.au","Wally2"))
    print("\nIncorrect Password")
    print("User_ID: 2 Password: badPassword")
    print("Result:", db.passwordCheck("Aaron.Luthor@atmiye.edu.au","badPassword"))

    print("\nDone Testing")
