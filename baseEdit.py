from threading import Thread, Lock, Condition
import shelve
import os
import subprocess
from twilio.rest import TwilioRestClient



# account = "jss459@cornell.edu"
# token = "EWHCornell15"
# client = TwilioRestClient(account, token)

ACCOUNT_SID = "ACa5e347084157a766bc1de658a87fd1a2" 
AUTH_TOKEN = "7a1f3723994c80d335f285dea61ac8e9" 
 
client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 


# message = client.messages.create(to="+18328770092", from_="+15512226265", body="Hello there!")

#TODO: make this class thread safe
class Database(object):
    def __init__(self,filename):
        self.lock = Lock()
        self.database = shelve.open(filename, writeback=True) #loads file in dict form

    #saves database dict in filename
    def saveDatabase(self):
    	with self.lock:
            self.database.sync()
    
    #make data structure itself thread-safe
    #writes to database only if not locked
    def write(self, key, value):
        with self.lock:
            self.database[key] = value

    def read(self, key):
        if self.inDatabase(key):
            with self.lock:
                return self.database[key]

    def inDatabase(self, key):
        with self.lock:
            return self.database.has_key(key)

    def clear(self):
        self.database.clear()

    def isEmpty(self):
        return not self.database

    def isNew(self, key):
        return not self.database.has_key(key)


#TODO: make thread safe + addPhoneNum
class DataManager(object):
    def __init__(self,nurseDb_file, patientDb_file):
        self.nurseDb_file = nurseDb_file
        self.patientDb_file = patientDb_file


    def add_nurse(self):
        while True:
            name = raw_input("Enter nurse name (x to cancel): ")
            if name == 'x':
                return

            nurseDb = Database(self.nurseDb_file)

            number = raw_input("Enter nurse " + `name` + "'s phone number: ")

            if name not in nurseDb.database:
                nurseDb.write(name, number)
                print "Nurse added to database."

            print "You've entered " + `name` + " with number " + `number` + "... storing to database..."

            addAnother = raw_input("Add another nurse? (y/n)")
            if addAnother != 'y':
                nurseDb.database.close()
                break

    def add_patient(self):
        while True:
            name = raw_input("Enter patient name (x to cancel): ")
            if name == 'x':
                return

            patientDb = Database(self.patientDb_file)

            location = raw_input("Enter patient " + `name` + "'s location: ")

            condition = raw_input("Enter patient " + `name` + "'s condition (s:stable, i:intermediate, c:critical): ")

            if name not in patientDb.database:
                patientDb.write(name,(location, condition))
                print "patient added to database."

            print "You've entered " + `name` + " with location " + `location` + " and condtion" + condition  + "... storing to database..."

            addAnother = raw_input("Add another patient? (y/n): ")
            if addAnother != 'y':
                patientDb.database.close()
                break




    #def hasNurse(self, name, number):
     #   return self.nurseDb.database.has_key(name) and self.nurseDb[name] == number #no key error because of operator precedence

    #need to complete
    #wait for external input (commandline text), then add to nurseDb
    def run(self):
        while True:
            to_add = raw_input("Add nurse(n) or patient(p): ")
            if to_add.lower() == 'p':
                self.add_patient()

            if to_add.lower() == 'n':
                self.add_nurse()




#========================================================================================================
#    Main
#========================================================================================================

if __name__ == "__main__":
    nurseDb_file = "nurses.db"
    patientDb_file = "patients.db"
    DataManager(nurseDb_file, patientDb_file).run()