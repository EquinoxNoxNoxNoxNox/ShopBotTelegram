from tinydb import TinyDB , Query
from .Models.M_inbox import Inbox
import random
import string
import json
import time

def InviteKeyGenerator():
    return ''.join([random.choice(string.ascii_letters) for x in range(6)])


db = TinyDB("datas/inbox.json")
q = Query()


def _update(val):
        def upd(doc):
            if doc["Id"] == val["Id"]:
                for key in doc.keys(): # THERE IS A 'None' VALUE IN BETWEEN SO I COULDN'T USE dict.update() METHOD
                    doc[key] = val[key]
        return upd

#Set an Inbox in db
def SetInbox(param : Inbox) -> Inbox:
    if(param.Id != 0): 
        res = db.update(_update(param.getValues()))
        if(res):
            return param
    try:
        LastRow = db.all()[-1]
        param.Id = LastRow["Id"] + 1
    except IndexError: # IF THERE IS NO LAST ROW
        param.Id = 1
    db.insert(param.getValues())
    return param

def ResetAnswered(_dict):
    _dict["IsAnswered"] = False
    return _dict

#Check user spam
def CheckUserValidity(UserId):
    res = db.search(q.IsAnswered == False and q.UserId==UserId)
    if(len(res) > 5):
        return False
    return True

#Get unanswered messages from Inbox 
def GetUnaswered() -> Inbox:
    res = db.search(q.IsAnswered == False)
    if(len(res) > 500):
        with open(f"datas/bk.inbox{int(time.time())}.json","w") as fp:
            json.dump([ResetAnswered(i) for i in res], fp)
        db.remove(q.IsAnswered == True or q.IsAnswered == False)
    return [SetInbox(Inbox(r["Mid"],r["UserId"],True,r["Date"],r["Id"])) for r in res]