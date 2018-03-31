import sqlite3

from passlib.hash import sha256_crypt

class Database:
    def __init__(self, **kwargs):
        self.filename = kwargs.get('filename')
        self._db = sqlite3.connect(self.filename, check_same_thread=False)
        self._db.row_factory = sqlite3.Row

        #Make Tables
        self._db.execute('create table IF NOT EXISTS parkingPermits (User_ID INTEGER, Vehicle_Type text, Department text, Permit_Duration text, Permit_Start text, Permit_End text, Permit_Number INTEGER PRIMARY KEY NOT NULL, Approved text)')
        self._db.execute('create table IF NOT EXISTS parkingViolations (Citation_Number INTEGER PRIMARY KEY NOT NULL, Date text, Time text, Description text, Permit_Number INTEGER, Vehicle_License_number text, Vehicle_Type text, FOREIGN KEY(Permit_Number) REFERENCES parkingPermits(Permit_Number))')
        self._db.execute('create table IF NOT EXISTS otherViolations (Citation_Number INTEGER PRIMARY KEY NOT NULL, User_ID INTEGER, Violation_Type text, Description text, Department text, Supervisor text, Date text, Time text, Place_in_campus text)')
        self._db.execute('create table IF NOT EXISTS healthAndSafetyIssues (Issue_Number INTEGER PRIMARY KEY NOT NULL, Date text, Time text, Person_Name text, Department text, Resolution_Date text, Resolution_Time text, Resolution_Description text, Supervisor text, Place_in_campus text)')
        self._db.execute('create table IF NOT EXISTS finePayments (Citation_Number INTEGER PRIMARY KEY NOT NULL, Payment_status text, FOREIGN KEY(Citation_Number) REFERENCES parkingViolations(Citation_Number), FOREIGN KEY(Citation_Number) REFERENCES otherViolations(Citation_Number))')
        self._db.execute('create table IF NOT EXISTS users (User_ID INTEGER PRIMARY KEY NOT NULL, Name text, Email text, Password text, Account_Type text)')

    def insertParkingPermit(self, row):
        self._db.execute('insert into parkingPermits (User_ID, Vehicle_Type, Department, Permit_Duration, Permit_Start, Permit_End, Approved) values (?,?,?,?,?,?,?)',(row['User_ID'], row['Vehicle_Type'], row['Department'], row['Permit_Duration'], row['Permit_Start'], row['Permit_End'], row['Approved']))
        self._db.commit()

    def insertParkingViolation(self, row):
        self._db.execute('insert into parkingViolations (Date, Time, Description, Permit_Number, Vehicle_License_number, Vehicle_Type) values (?,?,?,?,?,?)',(row['Date'], row['Time'], row['Description'], row['Permit_Number'], row['Vehicle_License_number'], row['Vehicle_Type']))
        self._db.commit()

    def insertOtherViolation(self, row):
        self._db.execute('insert into otherViolations (User_ID, Violation_Type, Description, Department, Supervisor, Date, Time, Place_in_campus) values (?,?,?,?,?,?,?,?)',(row['User_ID'], row['Violation_Type'], row['Description'], row['Department'], row['Supervisor'], row['Date'], row['Time'], row['Place_in_campus']))
        self._db.commit()

    def insertHealthAndSafetyIssue(self, row):
        self._db.execute('insert into healthAndSafetyIssues (Date, Time, Person_Name, Department, Resolution_Date, Resolution_Time, Resolution_Description, Supervisor, Place_in_campus) values (?,?,?,?,?,?,?,?,?)',(row['Date'], row['Time'], row['Person_Name'], row['Department'], row['Resolution_Date'], row['Resolution_Time'], row['Resolution_Description'], row['Supervisor'], row['Place_in_campus']))
        self._db.commit()

    def insertFinePayment(self, row):
        self._db.execute('insert into finePayments (Citation_Number, Payment_status) values (?,?)',(row['Citation_Number'], row['Payment_status']))
        self._db.commit()

    def insertUser(self, row):
        self._db.execute('insert into users (Name, Email, Password, Account_Type) values (?,?,?,?)',(row['Name'], row['Email'], str(sha256_crypt.encrypt(row['Password'])), row['Account_Type']))
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

    def updateFinePayment(self, key, val, ID):
        self._db.execute('update finePayments set {} = ? where Citation_Number = ?'.format(key),(val, ID))
        self._db.commit()

    def updateUser(self, key, val, ID):
        #Check if password change
        if key == "Password":
            self._db.execute('update users set {} = ? where User_ID = ?'.format(key),(str(sha256_crypt.encrypt(val)), ID))
        else:
            self._db.execute('update users set {} = ? where User_ID = ?'.format(key),(val, ID))
        self._db.commit()

    def delete(self, table, key, val):
        self._db.execute('delete from {} where {} = ?'.format(table, key),(val,))
        self._db.commit()

    """
        Performs a password correctness check for login purposes
        Returns True if correct password
    """
    def passwordCheck(self, email, password):
        storedHash = self.retrieve("users", "Email", email)
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
    db.RunSQL('drop table users')

    db = Database(filename = "IFB299.db")
    #Insert Parking Permits
    print("Inserting Parking Permits")
    db.insertParkingPermit(dict(User_ID = 1 , Vehicle_Type = "Two Wheeler", Department = "Admin", Permit_Duration = "Yearly", Permit_Start = "10/11/2015", Permit_End = "10/11/2016" , Approved = "Approved"))
    db.insertParkingPermit(dict(User_ID  = 2 , Vehicle_Type = "Four Wheeler", Department = "Business", Permit_Duration = "Monthly", Permit_Start = "06/08/2016", Permit_End = "06/09/2016" , Approved = "Pending"))
    db.insertParkingPermit(dict(User_ID  = 3 , Vehicle_Type = "Other Wheeler", Department = "Science and Engineering", Permit_Duration = "Daily", Permit_Start = "09/02/2016", Permit_End = "10/02/2016" , Approved = "Approved"))

    #Insert Parking Violations
    print("Inserting Parking Violations")
    db.insertParkingViolation(dict(Date = "2016/01/10", Time = "10:00", Description = "Illegally Parked in a handicap zone", Permit_Number = 1, Vehicle_License_number = "WAM-011", Vehicle_Type = "Two Wheeler"))
    db.insertParkingViolation(dict(Date = "2016/04/12" , Time = "12:00", Description = "Parked without a permit", Permit_Number = None, Vehicle_License_number = "BAT-089", Vehicle_Type = "Four Wheeler"))
    db.insertParkingViolation(dict(Date = "2016/02/11", Time = "14:00", Description = "Expired permit", Permit_Number = 3, Vehicle_License_number = "CHR-078", Vehicle_Type = "Other"))

    #Insert other Violations
    print("Inserting other Violations")
    db.insertOtherViolation(dict(User_ID = 1, Violation_Type = "Other", Description = "Public Nudity", Department = "Visitor", Supervisor = "Angelica Cole", Date = "2016/05/20", Time = "15:00", Place_in_campus = "In front of P Block"))
    db.insertOtherViolation(dict(User_ID = 2, Violation_Type = "Smoking", Description = None, Department = "Business", Supervisor = "Ben Parker", Date = "2016/07/30", Time = "17:00", Place_in_campus = "O Block level 2"))
    db.insertOtherViolation(dict(User_ID = 3, Violation_Type = "Other", Description = "Trespassing", Department = "Science and Engineering", Supervisor = "Thomas Wayne", Date = "2016/05/05", Time = "20:10", Place_in_campus = "B Block level 5"))

    #Insert Health and Safety Issues
    print("Inserting Health and Safety Issues")
    db.insertHealthAndSafetyIssue(dict(Date = "01/02/2016", Time = "10:00", Person_Name = "Barry Allen", Department = "Science and Engineering", Resolution_Date = "2016/02/01" , Resolution_Time = "12:00", Resolution_Description = "Chemical spill was cleaned", Supervisor = "Iris West" , Place_in_campus = "W block level 2"))
    db.insertHealthAndSafetyIssue(dict(Date = "02/03/2016", Time = "14:00", Person_Name = "Diana Prince", Department = "Business", Resolution_Date = None, Resolution_Time = None, Resolution_Description = None, Supervisor = "Steve Trevor", Place_in_campus = "B Block level 3"))
    db.insertHealthAndSafetyIssue(dict(Date = "03/05/2016", Time = "16:00", Person_Name = "Steven Strange", Department = "Arts", Resolution_Date = "2016/05/04", Resolution_Time = "20:00", Resolution_Description = "Missing Student was found", Supervisor = "Kent Nelson", Place_in_campus = "A Block level 3"))

    #Insert fine payments
    print("Inserting Fine Payments")
    db.insertFinePayment(dict(Citation_Number = 1, Payment_status = "Paid"))
    db.insertFinePayment(dict(Citation_Number = 2, Payment_status = "Further Processing"))
    db.insertFinePayment(dict(Citation_Number = 3, Payment_status = "Pending"))

    #Insert fine payments
    print("Inserting Users")
    db.insertUser(dict(User_ID = 1, Name = "Alex Parks", Email = "Alex.Parks12@atmiya.edu.au", Password = "Martha", Account_Type = "Staff"))
    db.insertUser(dict(User_ID = 2, Name = "Aaron Luthor", Email = "Aaron.Luthor@atmiya.edu.au", Password = "Wally2", Account_Type = "Student"))
    db.insertUser(dict(User_ID = 3, Name = "George Curious", Email = "George.Curious@atmiya.edu.au", Password = "StupidShinji", Account_Type = "Visitor"))
    db.insertUser(dict(User_ID= 4, Name="admin", Email="admin@atmiya.edu.au", Password="admin", Account_Type="Admin"))
    db.insertUser(dict(User_ID= 5, Name="Bob McDude", Email="Bob.McDude@atmiya.edu.au", Password="bruh", Account_Type="Student"))

    print("Done")
