import Lock

patientDb = _loadDict()

#Formats the the text that will be sent out
#returns a string, but arrays are usually passed this way anyways
def formatText(patientId,location,status):
    return ("URGENT: " + status " " + PatientID + " at " + location)

#checks database.txt if there is a negative status change in the patient
#returns false if database.txt does not exist or the patient does not exist in the file
#statuses availble: stable = 1, intermediate = 0, critical = -1

def isNegStatusChange(patientId,location,status):
    global patientDb
    if patientDb.has_key(patientId+location):
        if(dict[patientDB] < status):
            return True
    else:
        patientDb[patientId+location]=status
        _saveDict(patientDb)
        return False


#saves all info in a dictionary that is preserved in file
#KEY: patientId+location; VAL: status
#File name: database.dict
def saveInfo(patientId,location,status):
    patientDb[patientId+location]=status
    _saveDict(patientDb)



#========================================================================================================
#    Helper functions
#========================================================================================================

#saves current dictionary in database.dict
def _saveDict(d):
    with open("database.dict","wb") as f:
        json.dump(d,f)

#returns dictionary saved in database.dict
def _loadDict():
    with open("database.dict","rb") as f:
        return json.load(f)

#========================================================================================================
#    Main
#========================================================================================================

if __name__ == "__main__":
    pass
