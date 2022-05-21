from tinydb import TinyDB , Query
from .Models.M_error import E_NotFound
from .Models.M_user import User
db=TinyDB("datas/users.json")
q = Query()

#Get user from database by UID
def GetByUid(uid:str)->User:
    try:
        res = db.search(q.Uid == uid)[0]
        if(res["IsDel"]):
            raise IndexError()
        return User(uid = res["Uid"],InviteId = res["InviteId"] ,_id=res["Id"],Date=res["Date"])
    except IndexError:
        raise E_NotFound(f"user with uid {str(uid)} not found in db")

#Get user from database by ID
def GetById(_id:int)->User:
    try:
        res = db.search(q.Id == _id)[0]
        return User(uid = res["Uid"],InviteId = res["InviteId"] ,_id=res["Id"],Date=res["Date"])
    except IndexError:
        raise E_NotFound(f"user with id {str(uid)} not found in db")

#Get all users sorted by join date
def getAll() -> list:
    r = [User(uid = res["Uid"],InviteId = res["InviteId"] ,_id=res["Id"],Date=res["Date"]) for res in sorted(db.search(q.IsDel==False) , key = lambda k: k['Date'])]
    r.reverse()
    return r

#Get users by wings
def getByInviteId(Id) -> list:
    _res = db.search(q.InviteId == Id)
    if len(_res):
        return [User(uid = res["Uid"],InviteId = res["InviteId"] ,_id=res["Id"],Date=res["Date"]) for res in _res]
    else:
        raise E_NotFound()
#Get all users that are baned/Deleted
def getAllBanned()->list:
    return [User(uid = res["Uid"],InviteId = res["InviteId"] ,_id=res["Id"],Date=res["Date"]) for res in sorted(db.search(q.IsDel==True) , key = lambda k: k['Date'])].reverse()

def _update(val):
        def upd(doc):
            if doc["Id"] == val["Id"]:
                for key in doc.keys(): # THERE IS A 'None' VALUE IN BETWEEN SO I COULDN'T USE dict.update() METHOD
                    doc[key] = val[key]
        return upd

#Set or update an User
def SetUser(param : User) -> None:
    try:
        GetByUid(param.Uid)
        db.update(_update(param.getValues()))
    except E_NotFound:
        try:
            LastRow = db.all()[-1]
            param.Id = LastRow["Id"] + 1
        except IndexError: # IF THERE IS NO LAST ROW
            param.Id = 1
        db.insert(param.getValues())
    return param
