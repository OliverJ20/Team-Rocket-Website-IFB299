import sqlite3
from random import choice, randrange
from passlib.hash import sha256_crypt

class Database:
    def __init__(self, **kwargs):
        self.filename = kwargs.get('filename')
        self._db = sqlite3.connect(self.filename, check_same_thread=False)
        self._db.row_factory = sqlite3.Row

        #Make Tables
        self._db.execute('create table IF NOT EXISTS parkingPermits (User_ID INTEGER, Vehicle_Type text, Department text, Permit_Duration text, Permit_Start text, Permit_End text, Permit_Number INTEGER PRIMARY KEY NOT NULL, Approved text)')
        self._db.execute('create table IF NOT EXISTS parkingViolations (Citation_Number INTEGER PRIMARY KEY NOT NULL, User_ID INTEGER NOT NULL, Date text, Time text, Description text, Permit_Number INTEGER, Vehicle_License_number text, Vehicle_Type text, FOREIGN KEY(Permit_Number) REFERENCES parkingPermits(Permit_Number))')
        self._db.execute('create table IF NOT EXISTS otherViolations (Citation_Number INTEGER PRIMARY KEY NOT NULL, User_ID INTEGER, Violation_Type text, Description text, Department text, Supervisor text, Date text, Time text, Place_in_campus text)')
        self._db.execute('create table IF NOT EXISTS healthAndSafetyIssues (Issue_Number INTEGER PRIMARY KEY NOT NULL, Date text, Time text, Person_Name text, Department text, Description text, Supervisor text, Place_in_campus text, Resolution_Date text, Resolution_Time text, Resolution_Description text)')
        self._db.execute('create table IF NOT EXISTS finePayments (Fine_Number INTEGER PRIMARY KEY NOT NULL, Citation_Number INTEGER NOT NULL, Citation_Type text, Payment_status text)')
        self._db.execute('create table IF NOT EXISTS paymentDetails (Fine_Number INTEGER NOT NULL, Amount INTEGER, Date text, Card_Name text, Card_Type text, Card_Number text, Expiration_date text, First_Name text, Last_Name text, Billing_Address text, City text, Post_Code text, Phone text)')
        self._db.execute('create table IF NOT EXISTS users (User_ID INTEGER PRIMARY KEY NOT NULL, Name text, Email text, Password text, Department text, Account_Type text)')
        self._db.execute('create table IF NOT EXISTS userNotifications (User_ID INTEGER NOT NULL, Notification_Type text)')
        self._db.execute('create table IF NOT EXISTS rulesDB (Rule_ID INTEGER PRIMARY KEY NOT NULL,Rule_Title text, Rule_Description text)')

    def insertParkingPermit(self, row):
        self._db.execute('insert into parkingPermits (User_ID, Vehicle_Type, Department, Permit_Duration, Permit_Start, Permit_End, Approved) values (?,?,?,?,?,?,?)',(row['User_ID'], row['Vehicle_Type'], row['Department'], row['Permit_Duration'], row['Permit_Start'], row['Permit_End'], row['Approved']))
        self._db.commit()

    def insertRules(self, row):
            self._db.execute('insert into rulesDB (Rule_Title, Rule_Description) values (?,?)',(row['Rule_Title'], row['Rule_Description']))
            self._db.commit()

    def insertParkingViolation(self, row):
        self._db.execute('insert into parkingViolations (User_ID, Date, Time, Description, Permit_Number, Vehicle_License_number, Vehicle_Type) values (?,?,?,?,?,?,?)',(row['User_ID'], row['Date'], row['Time'], row['Description'], row['Permit_Number'], row['Vehicle_License_number'], row['Vehicle_Type']))
        self._db.commit()

    def insertOtherViolation(self, row):
        self._db.execute('insert into otherViolations (User_ID, Violation_Type, Description, Department, Supervisor, Date, Time, Place_in_campus) values (?,?,?,?,?,?,?,?)',(row['User_ID'], row['Violation_Type'], row['Description'], row['Department'], row['Supervisor'], row['Date'], row['Time'], row['Place_in_campus']))
        self._db.commit()

    def insertHealthAndSafetyIssue(self, row):
        self._db.execute('insert into healthAndSafetyIssues (Date, Time, Person_Name, Department, Description, Resolution_Date, Resolution_Time, Resolution_Description, Supervisor, Place_in_campus) values (?,?,?,?,?,?,?,?,?,?)',(row['Date'], row['Time'], row['Person_Name'], row['Department'], row['Description'], row['Resolution_Date'], row['Resolution_Time'], row['Resolution_Description'], row['Supervisor'], row['Place_in_campus']))
        self._db.commit()

    def insertFinePayment(self, row):
        self._db.execute('insert into finePayments (Citation_Number, Citation_Type, Payment_status) values (?,?,?)',(row['Citation_Number'], row['Citation_Type'], row['Payment_status']))
        self._db.commit()

    def insertPaymentDetails(self, row):
        self._db.execute('insert into paymentDetails (Fine_Number, Amount, Date, Card_Name, Card_Type, Card_Number, Expiration_date, First_Name, Last_Name, Billing_Address, City, Post_Code, Phone) values (?,?,?,?,?,?,?,?,?,?,?,?,?)',(row['Fine_Number'], row['Amount'], row['Date'], row['Card_Name'], row['Card_Type'], row['Card_Number'], row['Expiration_date'], row['First_Name'], row['Last_Name'], row['Billing_Address'], row['City'], row['Post_Code'], row['Phone']))
        self._db.commit()

    def insertUser(self, row):
        self._db.execute('insert into users (Name, Email, Password, Department, Account_Type) values (?,?,?,?,?)',(row['Name'], row['Email'], str(sha256_crypt.encrypt(row['Password'])), row['Department'], row['Account_Type']))
        self._db.commit()

    def insertUserNotification(self, row):
        self._db.execute('insert into userNotifications (User_ID, Notification_Type) values (?,?)',(row['User_ID'], row['Notification_Type']))
        self._db.commit()

    def retrieve(self, table, key, val):
        cursor = self._db.execute('select * from {} where {} = ?'.format(table, key), (val,))
        try:
            return dict(cursor.fetchone())
        except:
            return []
    #Use this if expecting multiple results
    def retrieveMulti(self, table, key, val):
        cursor = self._db.execute('select * from {} where {} = ?'.format(table, key), (val,))
        entries = []
        try:
            for row in cursor:
                entries.append(dict(row))
        except:
            pass
        return entries

    def retrieveAll(self, table):
        cursor = self._db.execute('select * from {} '.format(table))
        entries = []
        try:
            for row in cursor:
                entries.append(dict(row))
        except:
            pass
        return entries

    #Get a fine number based on violation type
    def retrieveFine(self, vType, ID):
        cursor = self._db.execute('select * from finePayments where Citation_Type = ? AND Citation_Number = ?', (vType,ID))
        try:
            return dict(cursor.fetchone())
        except:
            return []

    def updateRules(self, key, val, ID):
        self._db.execute('update rulesDB set {} = ? where Rule_ID = ?'.format(key),(val, ID))
        self._db.commit()

    def updateParkingPermit(self, key, val, ID):
        self._db.execute('update parkingPermits set {} = ? where Permit_Number = ?'.format(key),(val, ID))
        self._db.commit()

    def updateParkingViolation(self, key, val, ID):
        self._db.execute('update parkingViolations set {} = ? where Citation_Number = ?'.format(key),(val, ID))
        self._db.commit()

    def updateOtherViolation(self, key, val, ID):
        self._db.execute('update otherViolations set {} = ? where Citation_Number = ?'.format(key),(val, ID))
        self._db.commit()

    def updateHealthAndSafetyIssue(self, key, val, ID):
        self._db.execute('update healthAndSafetyIssues set {} = ? where Issue_Number = ?'.format(key),(val, ID))
        self._db.commit()

    def updateRulesDB (self, key, val, ID):
        self._db.execute('update rulesDB set {} = ? where Rule_ID = ?'.format(key),(val, ID))
        self._db.commit()

    def updateFinePayment(self, key, val, ID):
        self._db.execute('update finePayments set {} = ? where Fine_Number = ?'.format(key),(val, ID))
        self._db.commit()

    def updatePaymentDetails(self, val, ID):
        self._db.execute('update userNotifications set Notification_Type = ? where User_ID = ?',(val, ID))
        self._db.commit()

    def updateUser(self, key, val, ID):
        #Check if password change
        if key == "Password":
            self._db.execute('update users set {} = ? where User_ID = ?'.format(key),(str(sha256_crypt.encrypt(val)), ID))
        else:
            self._db.execute('update users set {} = ? where User_ID = ?'.format(key),(val, ID))
        self._db.commit()

    def updatePaymentDetails(self, key, val, ID):
        self._db.execute('update paymentDetails set {} = ? where Fine_Number = ?'.format(key),(val, ID))
        self._db.commit()

    def delete(self, table, key, val):
        self._db.execute('delete from {} where {} = ?'.format(table, key),(val,))
        self._db.commit()

    """
        Performs a password correctness check for login purposes
        Returns True if correct password
    """
    def passwordCheck(self, email, password):
        storedHash = self.retrieve("users", "Email", email.lower())
        #If user not in database, return false
        if storedHash == []:
            return False
        #sha256_crypt.verify hashes the inputed password and compaires it to the stored hash
        elif sha256_crypt.verify(password, str(storedHash['Password'])):
            return True
        else:
            return False

    def RunSQL(self, sql):
        self._db.execute(sql)
        self._db.commit()

    def close(self):
        self._db.close()
        del self.filename

#Testing function
if __name__ == "__main__":
    db = Database(filename = "IFB299.db")
    #Drop all tables for testing purposes
    db.RunSQL('drop table parkingPermits')
    db.RunSQL('drop table parkingViolations')
    db.RunSQL('drop table otherViolations')
    db.RunSQL('drop table healthAndSafetyIssues')
    db.RunSQL('drop table finePayments')
    db.RunSQL('drop table paymentDetails')
    db.RunSQL('drop table users')
    db.RunSQL('drop table userNotifications')
    db.RunSQL('drop table rulesDB')

    db = Database(filename = "IFB299.db")

    #Insert Rules
    print("Inserting Rules")
    db.insertRules(dict(Rule_ID = 1, Rule_Title = "Failing to display a valid permit for the area.", Rule_Description = "This infringement is issued to vehicles not displaying a valid permit for the particular area in which they have parked. It may also be issued if the officer can not read the entire permit through the windscreen.It is your responsibility to:\n"
                                                                                                                        "Ensure that the permit is on display while you are parked on campus. Note the offence is failing to display a permit, not failing to hold a permit.\n"
                                                                                                                        "Ensure that the entire permit is easily visible through the windscreen.\n"
                                                                                                                        "Display the permit on the bottom right hand corner (driver's side) of your dash.\n"
                                                                                                                        "Ensure that you are parked in the area permitted by the permit. For instance A permit holders are not permitted to park in SV areas and vice versa.\n"
                                                                                                                        "You should also be aware that a permit which has been copied or amended in any way is not a valid permit and should you be found to be using such a permit you will also lose any parking privileges that you hold.The Green Zone (formerly known as 'Lot 5') parking area at the Creative Industries Precinct covers all parking spaces which you access by driving past the large entrance sign. In general, if the only legitimate way to access the parking area is by passing an entrance sign, the instructions contained on that entrance sign apply.Motorcycle riders at Gardens Point are also advised that parking under S, Z and C Blocks is paid parking only. The only exception to this is the marked motorcycle area next to the exit boom gate at C Block level 1 (this is the area on the Z Block side of the boom gate)"))

    db.insertRules(dict(Rule_ID = 2, Rule_Title = "Parking permits must be displayed in the appropriate locations", Rule_Description="Permits must be displayed on the bottom right hand corner of the windscreen on four wheelers and the front of the vehcile in the case of two wheelers. Permits must be wholly visible at all times.The permit/ticket should not be placed in a position where it will obstruct the drivers view.	The permit/ticket is not to be defaced, altered or reproduced under any circumstances. You must display an original permit issued by the Parking Office on your vehicle, or an original ticket issued from a ticket machine."))

    db.insertRules(dict(Rule_ID = 3, Rule_Title = "Failing to display a valid ticket for the area.", Rule_Description = "this infringement is issued to vehicles parked in the Pay & Display car parks who are not displaying a valid ticket purchased from the machines within the car park. It may also be issued if the officer can not read the entire permit through the windscreen.It is your responsibility to:\n"
                                                                                                                        "ensure that you purchase a ticket to cover the entire time you wish to park. You should also take into account the possibility of delays in returning to your vehicle.\n"
                                                                                                                        "ensure that the ticket is displayed in the vehicle while you are using the car park.\n"
                                                                                                                        "ensure that the entire ticket is easily visible through the windscreen. You should check that the ticket is still visible after closing the door and before leaving the vehicle.\n"
                                                                                                                        "display the ticket on the bottom right hand corner (driver's side) of your dash. You should also remove any old tickets from your dash.\n"
                                                                                                                        "ensure that you are parked within the confines of the Pay & Display area. Pay & Display tickets are not valid if if the vehicle is parked in a permit parking area.\n"
                                                                                                                        "you should also be aware that a ticket which has been copied or amended in any way is not a valid ticket and should you be found to be using such a ticket you will also lose any parking privileges that you hold."))


    db.insertRules(dict(Rule_ID=4, Rule_Title="parking in an area not set aside as a parking area.", Rule_Description="you may only park in designated car parks on any campus, and within the marked bay if these are provided. Atmiya College has to follow certain guidelines when installing parking areas that take into consideration vehicle and pedestrian access, the use of the area, vehicle size and turning requirements.\n"
                                                                                                                      "the following are not a valid excuses for requesting a waiver:\n"
                                                                                                                      "there were no other car parks\n"
                                                                                                                      "I needed to park close to the building to carry equipment\n"
                                                                                                                      "I was not blocking any traffic or causing any obstruction\n"
                                                                                                                      "There were other cars parked there\n"
                                                                                                                      "I was only parked for 5 minutes\n"
                                                                                                                      "My friend/ lecturer/school admin staff (or any one else) said it was OK to park there.</p>"))

    db.insertRules(dict(Rule_ID=5, Rule_Title="Parking longer than permitted time", Rule_Description="Some bays on campus have a time restriction in place and an infringement will be issued when vehicles overstay the permitted length of time. Please note that that you must remove your car from the area, and not simply move car spaces within an area. Time restrictions are placed on car parks to ensure that there is a turnover of vehicles and to cater for staff and students who need access to the campus for a short period of time. In addition to signposted 2P and 4P parking bays, all loading bays on campus are strictly 30 minutes only.\n"
                                                                                                      "The Short Term Car Park at Atmiya is a maximum of 4 hours in any one day. This means that if you must remove your vehicle after a maximum of 4 hours. You are not permitted to purchase additional hours or move your vehicle to another space or return and park later during the day."))


    db.insertRules(dict(Rule_ID=6, Rule_Title="Parking against a yellow kerbside or roadway marking", Rule_Description="Yellow line marking indicates 'No Standing Anytime' and is used in places where it would be hazardous to have a vehicle parked. This could be to accommodate the types of vehicles that use the area, to ensure safe distance from a junction or to ensure the smooth flow of traffic. Some drivers have claimed that they didn't know what yellow line marking means. It is your responsibility as a licensed driver to be aware of the road rules, one of which is the meaning of yellow line marking. Only in exceptional circumstance are infringements waived."))

    db.insertRules(dict(Rule_ID=7, Rule_Title="Parking in a restricted area", Rule_Description="This infringement would apply to a vehicle that is parked in a disabled bay, a loading zone or any parking area that has signposted restrictions on its use. A valid Disability permit is required in any Disabled Parking bay identified by the international symbol or lettering. Having a injury of any sort does not permit non permit holders to use the bay. If you do have an injury that requires you to park on campus you should contact the Parking Office before you are required to attend the campus, preferably at least 48 hours before you need access.\n"
                                                                                                "Only in exceptional circumstances are infringement waived."))

    db.insertRules(dict(Rule_ID=8, Rule_Title="Parking against a No Standing sign", Rule_Description="These signs are placed in areas where it would be hazardous to have a vehicle parked. This could be to accommodate the types of vehicles that use the area, to ensure safe distance from a junction or to ensure the smooth flow of traffic. Some drivers have claimed that they didn't know what yellow line marking means. It is your responsibility as a licensed driver to be aware of the road rules, one of which is the meaning of yellow line marking. Only in exceptional circumstance are infringements waived."))

    db.insertRules(dict(Rule_ID=9, Rule_Title="Parking contrary to the scheme of orderly parking", Rule_Description="These infringements are issued for area on campus which is set aside for parking, but which has no marked parking bays and where the vehicle is either blocking other vehicles from either entering or exiting the car park, or blocking access to a building, walkway etc. An infringement may also be issued if a vehicle is parked across multiple bays in a car park with marked bays.\n"
                                                                                                                     "Obstructing emergency vehicle access or traffic flow.\n"
                                                                                                                     "This infringement will be issued to any vehicle which obstructs traffic flow or emergency vehicle access, including access to fire hydrants, buildings etc. Blocking emergency vehicles or traffic flow could have life-threatening even if its 2am in the morning and there are no other vehicles around."))

    db.insertRules(dict(Rule_ID=10, Rule_Title="Parking in a direction contrary to that permitted", Rule_Description="Vehicles must park in the direction of traffic flow. Vehicles parked contrary to the direction of traffic flow will more than likely have had to drive for some distance on the wrong side of the road or the wrong way in a one-way street. Doing so is extremely dangerous and as such infringements for this offence will not be waived."))

    db.insertRules(dict(Rule_ID=11, Rule_Title="Failing to obey direction of a traffic officer or authorised person", Rule_Description="From time to time it may be necessary for the Parking or Security Officers to give directions to drivers. This will be to ensure the smooth flow of traffic or to respond to an emergency or roadway obstruction. Failure to obey the instructions could escalate the problem. The only acceptable reason for not following the directions given, is if doing so would put you or your vehicle in danger."))

    db.insertRules(dict(Rule_ID=12, Rule_Title="Parking against a No parking sign", Rule_Description="No Parking signs are erected for a reason. Failure to see the sign is not a valid excuse as it is your responsibility as a driver to check for signage."))

    db.insertRules(dict(Rule_ID=13, Rule_Title="Driving in a direction contrary to that permitted.", Rule_Description="This infringement will be issued to vehicles that are either driving on the wrong side of the road or the wrong way in a one-way street. As this offence has the potential to cause an accident, these infringements will not be waived."))

    db.insertRules(dict(Rule_ID=14, Rule_Title="Failing to obey a traffic control device", Rule_Description="Traffic signs and other control devices such as witches hats and boom gates are put in place to ensure the safe flow of vehicles around campus. In the event of construction works or other disruptions to the normal flow of traffic on campus, it may be necessary to utilise officers to direct traffic using temporary “Stop/Go” hand held signs.  In the event that a driver refuses to follow these directions an infringement will be issued. There is no basis for an appeal against this infringement unless at the time of the offence the officer was not paying attention and accidentally directed you to drive towards a cliff or other such abyss, or into a large stationery object like a building or tree."))

    db.insertRules(dict(Rule_ID=15, Rule_Title="Driving in area not constructed as a carriage way or parking area", Rule_Description="This infringement would be issued to drivers who drive over grassed or garden areas.  Driving in such places would cause damage to these areas.  The only situation where this is permitted is when you are directed to do so by a Parking, Traffic or Security Officer."))

    db.insertRules(dict(Rule_ID=16, Rule_Title="Obstructing emergency vehicle access or traffic flow", Rule_Description="This infringement would be issued to drivers who drive over grassed or garden areas.  Driving in such places would cause damage to these areas.  The only situation where this is permitted is when you are directed to do so by a Parking, Traffic or Security Officer."))








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

    #Insert fine payments
    print("Inserting Parking Fine Payments")
    for entry in db.retrieveAll("parkingViolations"):
        db.insertFinePayment(dict(Citation_Number = entry['Citation_Number'], Citation_Type = "Parking", Payment_status = "Pending"))

    print("Inserting Other Fine Payments")
    for entry in db.retrieveAll("otherViolations"):
        db.insertFinePayment(dict(Citation_Number = entry['Citation_Number'], Citation_Type = "Other", Payment_status = "Pending"))

    print("Setup User notifications")
    for entry in db.retrieveAll("parkingViolations"):
        User_ID = db.retrieve("parkingPermits","Permit_Number", entry["Permit_Number"])["User_ID"]
        db.insertUserNotification(dict(User_ID = User_ID, Notification_Type = "New Parking Violation"))

    for entry in db.retrieveAll("otherViolations"):
        db.insertUserNotification(dict(User_ID = entry['User_ID'], Notification_Type = "New Campus Violation"))

    #Insert payment details
    print("Inserting Payment Details for parking")
    entry = db.retrieve("parkingViolations","Citation_Number", 1)
    payment = dict(Fine_Number = "", Amount = 90, Date = "12/10/2016", Card_Name = "", Card_Type = "Visa", Card_Number = "2353 XXXX XXXX 0234", Expiration_date = "06/19", First_Name = "", Last_Name = "",
    Billing_Address = "12 Fake St", City = "Brisbane", Post_Code = "4000", Phone = "0411 111 111")
    #Make card name temporally User_ID of permit, and then actual user's name
    payment['Card_Name'] = db.retrieve("parkingPermits","Permit_Number", entry["Permit_Number"])["User_ID"]
    payment['Card_Name'] = db.retrieve("users","User_ID", payment['Card_Name'])["Name"]
    payment['First_Name'] = str(payment['Card_Name']).split( )[0]
    payment['Last_Name'] = str(payment['Card_Name']).split( )[1]
    fine = db.retrieveFine("Parking",1)
    payment['Fine_Number'] = fine['Fine_Number']
    db.insertPaymentDetails(payment)
    db.updateFinePayment("Payment_status", "Paid", payment['Fine_Number'])
    if fine['Citation_Type'] == "Parking":
        Permit = db.retrieve("parkingViolations","Citation_Number",fine['Citation_Number'])['Permit_Number']
        User_ID = db.retrieve("parkingPermits","Permit_Number", Permit)["User_ID"]
    else:
        User_ID = db.retrieve("otherViolations","Citation_Number",fine['Citation_Number'])['User_ID']

    db.insertUserNotification(dict(User_ID = User_ID, Notification_Type = "Fine Payment Recieved"))

    print("Inserting Payment Details for other")
    entry = db.retrieve("otherViolations","Citation_Number", 3)
    payment = dict(Fine_Number = "", Amount = 50, Date = "12/10/2016", Card_Name = "", Card_Type = "Visa", Card_Number = "2353 XXXX XXXX 0234", Expiration_date = "06/19", First_Name = "", Last_Name = "",
    Billing_Address = "12 Fake St", City = "Brisbane", Post_Code = "4000", Phone = "0411 111 111")
    payment['Card_Name'] = db.retrieve("users","User_ID", entry['User_ID'])["Name"]
    payment['First_Name'] = payment['Card_Name'].split(" ")[0]
    payment['Last_Name'] = payment['Card_Name'].split(" ")[1]
    fine = db.retrieveFine("Other",3)
    payment['Fine_Number'] = fine['Fine_Number']
    db.insertPaymentDetails(payment)
    db.updateFinePayment("Payment_status", "Paid", payment['Fine_Number'])
    if fine['Citation_Type'] == "Parking":
        Permit = db.retrieve("parkingViolations","Citation_Number",fine['Citation_Number'])['Permit_Number']
        User_ID = db.retrieve("parkingPermits","Permit_Number", Permit)["User_ID"]
    else:
        User_ID = db.retrieve("otherViolations","Citation_Number",fine['Citation_Number'])['User_ID']
    db.insertUserNotification(dict(User_ID = User_ID, Notification_Type = "Fine Payment Recieved"))

    print("Done")
