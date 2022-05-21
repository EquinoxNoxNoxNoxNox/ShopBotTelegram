from tinydb import TinyDB , Query
from .Models.M_invite import Invite
from .Models.M_error import E_NotFound
import random
import string

def InviteKeyGenerator():
    return ''.join([random.choice(string.ascii_letters) for x in range(6)])


db = TinyDB("datas/invite.json")
q = Query()

def _update(val):
        def upd(doc):
            if doc["Id"] == val["Id"]:
                for key in doc.keys(): # THERE IS A 'None' VALUE IN BETWEEN SO I COULDN'T USE dict.update() METHOD
                    doc[key] = val[key]
        return upd

#Set an Invite in db
def Set(param : Invite) -> Invite:
    Key = InviteKeyGenerator()
    _KeySearch = db.search(q.InviteKey == Key)
    
    if not _KeySearch:
        param.InviteKey = Key
    
    if param.Id != 0:
        res = db.update(_update(param.getValues()))
        if res:
            return param
    
    try:
        LastRow = db.all()[-1]
        param.Id = LastRow["Id"] + 1
    except IndexError: # IF THERE IS NO LAST ROW
        param.Id = 1
    
    db.insert(param.getValues())
    return param

#Get all invite keys
def GetAll() -> list:
    _Invites = db.all()
    return [Invite(r["Title"],r["Id"],r["InviteKey"],r["Date"]) for r in _Invites]

#Get Invite from key 
def GetByKey(InviteKey) -> Invite:
    try:
        res = db.search(q.InviteKey == InviteKey)[0]
    except IndexError:
        raise E_NotFound("Invite key not found")
    return Invite(r["Title"],r["Id"],r["InviteKey"],r["Date"])

#Get Invite from Id
def GetById(InviteId) -> Invite:
    try:
        res = db.search(q.Id == InviteId)[0]
    except IndexError:
        raise E_NotFound("Invite key not found")
    return Invite(r["Title"],r["Id"],r["InviteKey"],r["Date"])