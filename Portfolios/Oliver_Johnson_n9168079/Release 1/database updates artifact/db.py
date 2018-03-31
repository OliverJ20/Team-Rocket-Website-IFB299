import sqlite3
from random import choice, randrange
from passlib.hash import sha256_crypt

class Database:



    #Insert Users
    print("Inserting Users")
    db.insertUser(dict(User_ID = 1, Name = "Alex Parks", Email = "alex.parks@atmiya.edu.au", Password = "Martha", Department = "Science and Engineering", Account_Type = "Staff"))
    db.insertUser(dict(User_ID = 2, Name = "Aaron Luthor", Email = "aaron.luthor@atmiya.edu.au", Password = "Wally2", Department = "Law", Account_Type = "Student"))
    db.insertUser(dict(User_ID = 3, Name = "George Curious", Email = "george.curious@atmiya.edu.au", Password = "StupidShinji", Department = "Health", Account_Type = "Visitor"))
    db.insertUser(dict(User_ID = 4, Name="admin", Email="admin@atmiya.edu.au", Password="admin", Department = "Admin", Account_Type="Admin"))
    db.insertUser(dict(User_ID = 5, Name="Bob McDude", Email="bob.mcdude@atmiya.edu.au", Password="bruh", Department = "Creative Industries", Account_Type="Student"))
    db.insertUser(dict(User_ID = 6, Name="Oliver Johnson", Email="oj2008@live.com.au", Password="Marist", Department = "Business", Account_Type="Student"))
    db.insertUser(dict(User_ID = 7, Name="Eliot Wilson ", Email="eliot.wilson#atmiya.edu.au", Password="badnet", Department = "Science and Engineering", Account_Type="Student"))
    db.insertUser(dict(User_ID = 8, Name="Dom Phips", Email="dom.phips@atmiya.edu.au", Password="shenzi", Department = "Research", Account_Type="Staff"))
    db.insertUser(dict(User_ID = 9, Name="Tim Beck", Email="tim.beck@atmiya.edu.au", Password="wow", Department = "Science and Engineering", Account_Type="Visitor"))
    db.insertUser(dict(User_ID = 10, Name="William Minazzoo", Email="william.minazzo@atmiya.edu.au", Password="superheroes", Department = "Law", Account_Type="Student"))
    db.insertUser(dict(User_ID = 11, Name="Mark Hogg", Email="mark.hogg@atmiya.edu.au", Password="science", Department = "Health", Account_Type="Staff"))
    db.insertUser(dict(User_ID = 12, Name="J-Mari Zeman", Email="j-mari.zeman@atmiya.edu.au", Password="czech", Department = "Creative Industries", Account_Type="Student"))
    db.insertUser(dict(User_ID = 13, Name="Kaelan Reece", Email="kaelan.reece@atmiya.edu.au", Password="popcorn", Department = "Business", Account_Type="Student"))
    db.insertUser(dict(User_ID = 14, Name="Sam Kendall", Email="sam.kendall@atmiya.edu.au", Password="dnd", Department = "Science and Engineering", Account_Type="Student"))
    db.insertUser(dict(User_ID = 15, Name="Seb Sherry", Email="seb.sherry@atmiya.edu.au", Password="codegod", Department = "Law", Account_Type="Student"))
    db.insertUser(dict(User_ID = 16, Name="Gabe Goldheart", Email="gabe.goldheart@atmiya.edu.au", Password="backstabber", Department = "Health", Account_Type="Student"))
    db.insertUser(dict(User_ID = 17, Name="Luke Skywalker", Email="luke.skywalker@atmiya.edu.au", Password="theforce", Department = "Creative Industries", Account_Type="Staff"))
    db.insertUser(dict(User_ID = 18, Name="John Smith", Email="john.smith@atmiya.edu.au", Password="password", Department = "Business", Account_Type="Student"))
    db.insertUser(dict(User_ID = 19, Name="James Jacob", Email="james.jacob@atmiya.edu.au", Password="halo", Department = "Science and Engineering", Account_Type="Student"))
    db.insertUser(dict(User_ID = 20, Name="Jesse Cox", Email="jesse.cox@atmiya.edu.au", Password="youtube", Department = "Creative Industries", Account_Type="Visitor"))

    #Insert Parking Permits
    print("Inserting Parking Permits")
    db.insertParkingPermit(dict(User_ID = 1 , Vehicle_Type = "Two Wheeler", Department = "Admin", Permit_Duration = "Yearly", Permit_Start = "10/11/2015", Permit_End = "10/11/2016" , Approved = "Approved"))
    db.insertParkingPermit(dict(User_ID  = 2 , Vehicle_Type = "Four Wheeler", Department = "Business", Permit_Duration = "Monthly", Permit_Start = "06/08/2016", Permit_End = "06/09/2016" , Approved = "Pending"))
    db.insertParkingPermit(dict(User_ID  = 3 , Vehicle_Type = "Other Wheeler", Department = "Science and Engineering", Permit_Duration = "Daily", Permit_Start = "09/02/2016", Permit_End = "10/02/2016" , Approved = "Approved"))
    db.insertParkingPermit(dict(User_ID = 6 , Vehicle_Type="Sick Wheeler", Department ="Science and Engineering", Permit_Duration="Monthly", Permit_Start="09/02/2016", Permit_End="09/03/2016", Approved="Approved"))
    db.insertParkingPermit(dict(User_ID = 8, Vehicle_Type="Four Wheeler", Department ="Business", Permit_Duration="Monthly", Permit_Start="09/02/2016", Permit_End="09/03/2016", Approved="Approved"))
    db.insertParkingPermit(dict(User_ID = 10, Vehicle_Type="Four Wheeler", Department="Creative Industry", Permit_Duration="Monthly", Permit_Start="09/02/2016", Permit_End="09/03/2016", Approved="Approved"))
    db.insertParkingPermit(dict(User_ID = 11, Vehicle_Type="Four Wheeler", Department="Creative Industry", Permit_Duration="Monthly",Permit_Start="09/02/2016", Permit_End="09/03/2016", Approved="Approved"))
    db.insertParkingPermit(dict(User_ID = 12, Vehicle_Type="Four Wheeler", Department="Business", Permit_Duration="Monthly",Permit_Start="09/02/2016", Permit_End="09/03/2016", Approved="Approved"))
    db.insertParkingPermit(dict(User_ID = 14, Vehicle_Type="Four Wheeler", Department="Law", Permit_Duration="Monthly",Permit_Start="09/02/2016", Permit_End="09/03/2016", Approved="Approved"))
    db.insertParkingPermit(dict(User_ID = 16, Vehicle_Type="Four Wheeler", Department="Law", Permit_Duration="Monthly",Permit_Start="09/02/2016", Permit_End="09/03/2016", Approved="Approved"))
    db.insertParkingPermit(dict(User_ID = 18, Vehicle_Type="Four Wheeler", Department="Law", Permit_Duration="Monthly",Permit_Start="09/02/2016", Permit_End="09/03/2016", Approved="Approved"))
    db.insertParkingPermit(dict(User_ID = 19, Vehicle_Type="Four Wheeler", Department="Creative Industry", Permit_Duration="Monthly",Permit_Start="09/02/2016", Permit_End="09/03/2016", Approved="Approved"))

    #Insert Parking Violations
    print("Inserting Parking Violations")
    db.insertParkingViolation(dict(Date="10/01/2016", Time = "10:00", Description = "Illegally Parked in a handicap zone", Permit_Number = 1, User_ID = 1, Vehicle_License_number = "WAM-011", Vehicle_Type = "Two Wheeler"))
    db.insertParkingViolation(dict(Date="12/10/2016" , Time = "12:00", Description = "Parked without a permit", Permit_Number = 2, User_ID = 2, Vehicle_License_number = "BAT-089", Vehicle_Type = "Four Wheeler"))
    db.insertParkingViolation(dict(Date="11/07/2016", Time = "14:00", Description = "Expired permit", Permit_Number = 3, User_ID = 3, Vehicle_License_number = "CHR-078", Vehicle_Type = "Other"))
    db.insertParkingViolation(dict(Date="12/10/2016", Time="12:00", Description="Car does not meet legal standards", Permit_Number = 4, User_ID = 6, Vehicle_License_number="SIX-999", Vehicle_Type="Four Wheeler"))
    db.insertParkingViolation(dict(Date="12/10/2016", Time="12:00", Description="Illegally parked", Permit_Number = 5, User_ID = 8, Vehicle_License_number="SUY-935", Vehicle_Type="Four Wheeler"))
    db.insertParkingViolation(dict(Date="12/10/2016", Time="12:00", Description="No permit found on vehicle", Permit_Number = 6, User_ID = 10, Vehicle_License_number="BIT-329", Vehicle_Type="Four Wheeler"))
    db.insertParkingViolation(dict(Date="12/10/2016", Time="12:00", Description="Wrong Vehicle Permit Type", Permit_Number = 7, User_ID = 11, Vehicle_License_number="BOB- 769", Vehicle_Type="Four Wheeler"))
    db.insertParkingViolation(dict(Date="12/10/2016", Time="12:00", Description="double parked", Permit_Number = 8, User_ID = 12, Vehicle_License_number="LUV-404", Vehicle_Type="Four Wheeler"))
    db.insertParkingViolation(dict(Date="12/10/2016", Time="12:00", Description="Expired permit", Permit_Number = 9, User_ID = 14, Vehicle_License_number="OPK-735", Vehicle_Type="Four Wheeler"))

    #Insert other Violations
    print("Inserting Other Violations")
    db.insertOtherViolation(dict(User_ID = 1, Violation_Type = "Other", Description = "Public Nuisance", Department = "Creative Industries", Supervisor = "Angelica Cole", Date = "10/10/2016", Time = "15:00", Place_in_campus = "In front of P Block"))
    db.insertOtherViolation(dict(User_ID = 2, Violation_Type = "Smoking", Description = "", Department = "Business", Supervisor = "Ben Parker", Date = "30/07/2016", Time = "17:00", Place_in_campus = "O Block level 2"))
    db.insertOtherViolation(dict(User_ID = 3, Violation_Type = "Other", Description = "Trespassing in staff only area", Department = "Science and Engineering", Supervisor = "Thomas Wayne", Date = "05/05/2016", Time = "20:10", Place_in_campus = "B Block level 5"))
    db.insertOtherViolation(dict(User_ID = 6, Violation_Type = "Other", Description = "Caused damage to campus vending machines", Department = "Science and Engineering", Supervisor = "Thomas Wayne", Date = "05/05/2016", Time = "20:10", Place_in_campus = "Literally everywhere"))
    db.insertOtherViolation(dict(User_ID = 7, Violation_Type="Other", Description="broke window", Department="Science and Engineering", Supervisor="Thomas Wayne", Date="05/05/2016", Time="20:10", Place_in_campus="B Block level 5"))
    db.insertOtherViolation(dict(User_ID = 15, Violation_Type="Other", Description="littered", Department="Science and Engineering", Supervisor="Thomas Wayne", Date="05/05/2016", Time="20:10", Place_in_campus="B Block level 5"))
    db.insertOtherViolation(dict(User_ID = 12, Violation_Type="Other", Description="loitering", Department="Science and Engineering", Supervisor="Thomas Wayne", Date="05/05/2016", Time="20:10", Place_in_campus="B Block level 5"))
    db.insertOtherViolation(dict(User_ID = 13, Violation_Type="Other", Description="selling unauthorised merchanidse on campus", Department="Science and Engineering", Supervisor="Thomas Wayne", Date="05/05/2016", Time="20:10", Place_in_campus="B Block level 5"))
    db.insertOtherViolation(dict(User_ID = 9, Violation_Type="Other", Description="Trespassing", Department="Business", Supervisor="Thomas Wayne", Date="05/05/2016", Time="20:10", Place_in_campus="B Block level 5"))
    db.insertOtherViolation(dict(User_ID = 16, Violation_Type="Other", Description="Public Nuisance", Department="Law", Supervisor="Thomas Wayne", Date="05/05/2016", Time="20:10", Place_in_campus="B Block level 5"))
    db.insertOtherViolation(dict(User_ID = 8, Violation_Type="Other", Description="Ignored fire safety instructors during building evacuation", Department="Creative Industrys",Supervisor="Thomas Wayne", Date="05/05/2016", Time="20:10", Place_in_campus="B Block level 5"))
    db.insertOtherViolation(dict(User_ID = 11, Violation_Type="Other", Description="littering on campus", Department="Creative Industrys", Supervisor="Thomas Wayne", Date="05/05/2016", Time="20:10", Place_in_campus="B Block level 5"))
    db.insertOtherViolation(dict(User_ID=19, Violation_Type="Other", Description="breaking campus materials", Department="Law",Supervisor="Thomas Wayne", Date="05/05/2016", Time="20:10", Place_in_campus="P Block"))

    # Insert Health and Safety Issues
    print("Inserting Health and Safety Issues")
    db.insertHealthAndSafetyIssue(dict(Date="01/02/2016", Time="10:00", Person_Name="Barry Allen", Description="Updated parking terms and conditions", Department="Science and Engineering", Resolution_Date="01/02/2016",  Resolution_Time="12:00", Resolution_Description="Chemical spill was cleaned", Supervisor="Iris West", Place_in_campus="W block level 2"))
    db.insertHealthAndSafetyIssue(dict(Date="02/03/2016", Time="14:00", Person_Name="Diana Prince", Description="Loose roofing tile in hall way",  Department="Business", Resolution_Date=None, Resolution_Time=None, Resolution_Description=None, Supervisor="Steve Trevor", Place_in_campus="B Block level 3"))
    db.insertHealthAndSafetyIssue(dict(Date="03/05/2016", Time="16:00", Person_Name="Steven Strange", Description="Toilets in D block are closed",Department="Creative Industries", Resolution_Date="04/05/2016", Resolution_Time="20:00",  Resolution_Description="Fires were extinguished. Troublesome gear removed", Supervisor="Kent Nelson", Place_in_campus="D Block level 1"))
    db.insertHealthAndSafetyIssue(dict(Date="02/03/2016", Time="14:00", Person_Name="Jay ZedMan",  Description="Issues with shuttle bus to KG, expect delays", Department="Business", Resolution_Date=None, Resolution_Time=None,       Resolution_Description=None, Supervisor="Steve Trevor",  Place_in_campus="B Block level 3"))
    db.insertHealthAndSafetyIssue(dict(Date="02/03/2016", Time="14:00", Person_Name="Kylo Ren", Description="Power will be disrupted to L-block Research labs", Department="Law",   Resolution_Date=None, Resolution_Time=None, Resolution_Description=None,   Supervisor="Steve Trevor", Place_in_campus="B Block level 3"))
    db.insertHealthAndSafetyIssue(dict(Date="02/03/2016", Time="14:00", Person_Name="Gary Chuck",   Description="Computers in F block are temporally down",Department="Creative Industrys", Resolution_Date=None, Resolution_Time=None,   Resolution_Description=None, Supervisor="Steve Trevor",   Place_in_campus="B Block level 3"))
    db.insertHealthAndSafetyIssue(dict(Date="02/03/2016", Time="14:00", Person_Name="Henry Jenkins", Description="fire safety inspection in D block",       Department="Science and Engineering", Resolution_Date=None, Resolution_Time=None,   Resolution_Description=None, Supervisor="Steve Trevor",    Place_in_campus="B Block level 3"))

