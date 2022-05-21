from typing import Union
import time

class Invite():
    Id = 0 # Id of the record
    Date = 0 # Date of the records
    Title = "" # Title of invitation
    InviteKey = "" # Random invite key
    def __init__(self,Title:str,_id=0,InviteKey = "",date=0):
        self.Id = _id
        self.Date = date or time.time()
        self.Title = Title
        self.InviteKey = InviteKey
    
    def getValues(self) -> dict:
        return {"Id":self.Id,
                "Date" : self.Date,
                "Title" : self.Title,
                "InviteKey" : self.InviteKey
                }