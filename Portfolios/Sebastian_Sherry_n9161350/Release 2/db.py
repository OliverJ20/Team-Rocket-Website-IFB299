import sqlite3
from random import choice, randrange

class Database:
    def __init__(self, **kwargs):
        self.filename = kwargs.get('filename')
        self._db = sqlite3.connect(self.filename, check_same_thread=False)
        self._db.row_factory = sqlite3.Row

        self._db.execute('create table IF NOT EXISTS finePayments (Fine_Number INTEGER PRIMARY KEY NOT NULL, Citation_Number INTEGER NOT NULL, Citation_Type text, Payment_status text)')
        self._db.execute('create table IF NOT EXISTS paymentDetails (Fine_Number INTEGER NOT NULL, Amount INTEGER, Date text, Card_Name text, Card_Type text, Card_Number text, Expiration_date text, First_Name text, Last_Name text, Billing_Address text, City text, Post_Code text, Phone text)')
        self._db.execute('create table IF NOT EXISTS userNotifications (User_ID INTEGER NOT NULL, Notification_Type text)')

    def insertFinePayment(self, row):
        self._db.execute('insert into finePayments (Citation_Number, Citation_Type, Payment_status) values (?,?,?)',(row['Citation_Number'], row['Citation_Type'], row['Payment_status']))
        self._db.commit()

    def insertPaymentDetails(self, row):
        self._db.execute('insert into paymentDetails (Fine_Number, Amount, Date, Card_Name, Card_Type, Card_Number, Expiration_date, First_Name, Last_Name, Billing_Address, City, Post_Code, Phone) values (?,?,?,?,?,?,?,?,?,?,?,?,?)',(row['Fine_Number'], row['Amount'], row['Date'], row['Card_Name'], row['Card_Type'], row['Card_Number'], row['Expiration_date'], row['First_Name'], row['Last_Name'], row['Billing_Address'], row['City'], row['Post_Code'], row['Phone']))
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

    def updateFinePayment(self, key, val, ID):
        self._db.execute('update finePayments set {} = ? where Fine_Number = ?'.format(key),(val, ID))
        self._db.commit()

    def updatePaymentDetails(self, key, val, ID):
        self._db.execute('update paymentDetails set {} = ? where Fine_Number = ?'.format(key),(val, ID))
        self._db.commit()

    def delete(self, table, key, val):
        self._db.execute('delete from {} where {} = ?'.format(table, key),(val,))
        self._db.commit()

    def RunSQL(self, sql):
        self._db.execute(sql)
        self._db.commit()

    def close(self):
        self._db.close()
        del self.filename

#Testing function
if __name__ == "__main__":
    db = Database(filename = "IFB299.db")

    #Insert fine payments
    print("Inserting Parking Fine Payments")
    for entry in db.retrieveAll("parkingViolations"):
        db.insertFinePayment(dict(Citation_Number = entry['Citation_Number'], Citation_Type = "Parking", Payment_status = "Pending"))

    print("Inserting Other Fine Payments")
    for entry in db.retrieveAll("otherViolations"):
        db.insertFinePayment(dict(Citation_Number = entry['Citation_Number'], Citation_Type = "Other", Payment_status = "Pending"))

    #Insert payment details
    print("Inserting Payment Details for parking")
    entry = db.retrieve("parkingViolations","Citation_Number", 1)
    payment = dict(Fine_Number = "", Amount = 90, Date = "2016/10/12", Card_Name = "", Card_Type = "Visa", Card_Number = "2353 XXXX XXXX 0234", Expiration_date = "06/19", First_Name = "", Last_Name = "",
    Billing_Address = "12 Fake St", City = "Brisbane", Post_Code = "4000", Phone = "0411 111 111")
    #Make card name temporally User_ID of permit, and then actual user's name
    payment['Card_Name'] = db.retrieve("parkingPermits","Permit_Number", entry["Permit_Number"])["User_ID"]
    payment['Card_Name'] = db.retrieve("users","User_ID", payment['Card_Name'])["Name"]
    payment['First_Name'] = str(payment['Card_Name']).split( )[0]
    payment['Last_Name'] = str(payment['Card_Name']).split( )[1]
    payment['Fine_Number'] = db.retrieveFine("Parking",1)['Fine_Number']
    db.insertPaymentDetails(payment)
    db.updateFinePayment("Payment_status", "Paid", payment['Fine_Number'])

    print("Inserting Payment Details for other")
    entry = db.retrieve("otherViolations","Citation_Number", 3)
    payment = dict(Fine_Number = "", Amount = 50, Date = "2016/10/12", Card_Name = "", Card_Type = "Visa", Card_Number = "2353 XXXX XXXX 0234", Expiration_date = "06/19", First_Name = "", Last_Name = "",
    Billing_Address = "12 Fake St", City = "Brisbane", Post_Code = "4000", Phone = "0411 111 111")
    payment['Card_Name'] = db.retrieve("users","User_ID", entry['User_ID'])["Name"]
    payment['First_Name'] = payment['Card_Name'].split(" ")[0]
    payment['Last_Name'] = payment['Card_Name'].split(" ")[1]
    payment['Fine_Number'] = db.retrieveFine("Other",3)['Fine_Number']
    db.insertPaymentDetails(payment)
    db.updateFinePayment("Payment_status", "Paid", payment['Fine_Number'])
    print("Done")
