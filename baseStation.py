from threading import Thread, Lock, Condition
import shelve
import os
import time

#TODO: make this class thread safe
class Database(object):
    def __init__(self,filename):
        self.lock = Lock()
        self.database = shelve.open(filename,writeback=True)

    #saves database dict in filename
    def saveDatabase(self):
        with self.lock:
            self.database.sync()
            self.database.close()
            self.database = shelve.open(filename,writeback=True)

    #need to complete
    def write(self, key, value):
        with self.lock:
            self.database[key] = value


    #need to complete
    def read(self, key):
        with self.lock:
            return self.database[key]


    #need to complete
    def inDatabase(self, key):
        with self.lock:
            self.database.has_key(key)
        


#TODO: make multi-thread safe + write: formatText, isNegStatusChange, saveInfo
class VitalDataHandler(Thread):
    def __init__(self,patientDb,nurseDb,dataInput,handlerId):
        self.patientDb = patientDb
        self.nurseDb = nurseDb
        self.dataInput = dataInput
        self.handlerId = handlerId
        Thread.__init__(self)

    #converts status to int
    def intStatus(self,status):
        return {'stable':1,'intermediate':0,'critical':-1}[status]

    #need to complete
    #Formats and returns the the text that will be sent out
    #inputs: String patientId, String location, String status
    def formatText(self,patientId,location,status):
        return str(patientId) + "|" + str(location) + "|" + str(status)

    #need to complete
    #checks database.db if there is a negative status change in the patient
    #returns false if the patient does not exist in the database
    #possible statuses: "stable","intermediate","critical"
    def isNegStatusChange(self,patientId,location,status):
        key = str(patientId) + "," + str(location)
        prev_status = self.patientDb.read(key)
        
        if ((prev_status == "intermediate" and status == "critical") or (prev_status == "stable" and status == "intermediate")):
            return True

        return False

    #need to complete
    #sends text from pi to nurses
    def sendText(self,msg):
        os.system("echo "+msg)

    #need to complete
    #saves all info in a database.db
    #KEY: patientId+','+location; VAL: status
    def saveInfo(self,patientId,location,status):
        key = str(patientId) + "," + str(location)
        self.patientDb.write(key, status)
        
        
    #need to complete
    #thread's main function
    def run(self):
        while True:
            inputs = self.dataInput.split(",")
            patientId = inputs[0]
            location = inputs[1]
            status = inputs[2]
            key = str(patientId) + "," + str(location)
            if (self.patientDb.inDatabase(key)):
                if (self.isNegStatusChange(patientId,location,status)):
                    self.sendText(self.formatText(patientId,location,status))
            else:
                self.saveInfo(patientId,location,status)
                self.sendText("New: " + self.formatText(patientId,location,status) + ", added to database")


 
        

    
#TODO: make thread safe + addPhoneNum
class NurseHandler(Thread):
    def __init__(self,nurseDb):
        self.nurseDb = nurseDb
        Thread.__init__(self)

    #need to complete
    #adds KEY:name, VAL:num to nurseDb and saves to nurseDb
    def addPhoneNum(self,name,num):
        self.nurseDb.write(name, num)

    #need to complete
    #wait for external input (commandline text), then add to nurseDb
    def run(self):
        name = raw_input("Enter a name: ")
        num = raw_input("Enter a phone number: ")
        print "Storing " + name + " with number: " + num + " to database..."
        self.addPhoneNum(name, num)
#========================================================================================================
#    Main
#========================================================================================================

if __name__ == "__main__":
    patientDb = Database("patients")
    nurseDb = Database("nurses")
    dataInputStream = ["p1,bed1,stable","p2,bed5,critical","p3,bed6,intermediate","p1,bed1,critical","p2,bed5,stable","p3,bed6,intermediate","p1,bed1,critical","p2,bed5,intermediate","p3,bed6,critical"]
    NurseHandler(nurseDb).start()
    #gives 10 seconds to input nurse 'name' and 'num'
    time.sleep(10)
    for ii in range(9):
        vdh = VitalDataHandler(patientDb,nurseDb,dataInputStream[ii],ii).start()
        vdh.join()