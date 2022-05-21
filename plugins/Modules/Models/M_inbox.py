from typing import Union
import time

class Inbox():
    Id = 0 # Id of the record
    Date = 0 # Date of the record
    UserId = 0 # Id of user table
    Mid = 0 # Message id
    IsAnswered = False # Is asnwered tag
    def __init__(self,mid:Union[str,int],userId:int,isAnswered=False,date=0,_id=0):
        self.Id = _id
        self.UserId = userId
        self.Mid = mid
        self.Date = date or time.time()
        self.IsAnswered = isAnswered
    def getValues(self) -> dict:
        return {"Id":self.Id,
                "Mid" : self.Mid,
                "UserId" : self.UserId,
                "Date" : self.Date,
                "IsAnswered" : self.IsAnswered
        }