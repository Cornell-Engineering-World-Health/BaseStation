from threading import Thread, Lock, Condition
import shelve

#TODO: make this class multi-thread safe
class Database(object):
    def __init__(self,filename):
        self.lock = Lock()
        self.database = shelve.open(filename,writeback=True) #loads file representing dictionary

    #saves database dict in filename
    def saveDatabase(self):
        with self.lock:
	      self.database.sync()

    def write(self, key, value):
	with self.lock:	
	      self.database[key] = value

    def read(self, key):
	with self.lock:
	      return self.database[key]

    def inDatabase(self,key):
	with self.lock:	
		return key in self.database	



#TODO: make multi-thread safe + write: formatText, isNegStatusChange, saveInfo
class VitalDataHandler(Thread):
    def __init__(self,patientDb,nurseDb,dataInput,handlerId):
        self.patientDb = patientDb
        self.nurseDb = nurseDb
        self.dataInput = dataInput
        self.handlerId = handlerId

    #converts status to int
    def intStatus(self,status):
        return {'stable':1,'intermediate':0,'critical':-1}[status]

    #Formats and returns the the text that will be sent out
    #inputs: String patientId, String location, String status
    def formatText(self,patientId,location,status):
	return "Patient "+patient+";Location "+location+";Status "+status        
	

    #checks database.db if there is a negative status change in the patient
    #returns false if the patient does not exist in the database
    #possible statuses: "stable","intermediate","critical"
    def isNegStatusChange(self,patientId,location,status):
        return intStatus(self.patientDb.Database.read(`patientId`+','+`location`))>intStatus(status)
`	

    #sends text from pi to nurses
 import os   
 def sendText(self,msg):
	os.system('echo '+`msg`)        
	

    #saves all info in a database.db
    #KEY: patientId+location; VAL: status
    def saveInfo(self,patientId,location,status):
        self.patientDb.Database.write(`patientId+','+`location`,`patientId`+','+`status`)
	

    #thread's main function
    def run(self):
        data=self.dataInput.split(',')
	patientId, location, status = data[0], data[1], data[2]
	if isNegStatusChange(patientId,location,status)
		sendText(formatText(patientId,location,status)
	saveInfo(patientId,location,status)
	

#TODO: make thread safe + addPhoneNum
class NurseHandler(Thread):
    def __init__(self,nurseDb):
        self.nurseDb = nurseDb
	self.lock = Lock()
import os
    #adds KEY:name, VAL:num to nurseDb and saves to nurseDb
    def addPhoneNum(self,name,num) :        
	with self.lock;
		self.nurseDb.Database.write(`name`,`name` + ',' + `num`)	
		#os.system("echo Nurse "+`name`+"added to database, with phone number"+`num`)

    #wait for external input (commandline text), then add to nurseDb
    def run(self):
	name = raw_input("Nurse name: ")
	number = raw_input("Enter your phone number: ")
	print "Name: " + `name`
	print "Number: " + `number`
	#os.system("echo Nurse "+`name`+"added to database, with phone number"+`num`)       
	self.addPhoneNum(name,number)

#========================================================================================================
#    Main
#========================================================================================================

if __name__ == "__main__":
    patientDb = Database("patients.db")
    nurseDb = Database("nurses.db")
    dataInputStream = ["p1,bed1,stable","p2,bed5,critical","p3,bed6,intermediate","p1,bed1,critical","p2,bed5,stable","p3,bed6,intermediate","p1,bed1,critical","p2,bed5,intermediate","p3,bed6,critical"]
    NurseHandler(nurseDb).start()
    for ii in range(9):
        vital = VitalDataHandler(patientDb,nurseDb,dataInputStream[ii],ii).start()
	vital.join()
