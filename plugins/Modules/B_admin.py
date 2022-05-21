from tinydb import TinyDB , Query
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware
from .Models.M_error import E_NotFound
from .Models.M_admin import Admin

Owner = 1575934389#1488078746

db = TinyDB("datas/Operator.json")
q = Query()

class Role():
    Id = 0
    Title = ""
    def __init__(self,i,t):
        self.Id = i
        self.Title = t

Admins = [] # Admin in the system

Roles = { # Roles in the system
    "None" : Role(0,u"بدون نقش"),
    "Supreme" : Role(1,u"مدیریت کل سیستم"),
    "Support" : Role(2,u"مدیریت تماس"),
    "Supply" : Role(3,u"مدیریت محصولات")
}

def _getRoles(ids:str):
    res = []
    _iterRole = []
    if "," in str(ids):
        _iterRole=str(ids).split(",")
    else:
        _iterRole = [ids]
    for rid in _iterRole:
        if rid:
            for role in Roles:
                if(Roles[role].Id == int(rid)):
                    res.append(Roles[role])
    return res

def AdminStartBootstrap()->None:
    """Retrive Admin from json to Admin list"""
    global Admins
    Admins = [Admin(Owner,[Roles["Supreme"]])]
    for _Admin in db:
        Admins.append(Admin(
            _Admin["Uid"],
            _getRoles(_Admin["Role"])
        ))

#Remove an Admin from database
def AdminRemove(param : Admin) -> None:
    db.remove((q.Uid == param.Uid))
    return AdminStartBootstrap()

#Get an Admin from Admin by Uid
def AdminGet(uid : int) -> Admin:
    for _Admin in Admins:
        if(_Admin.Uid == str(uid)):
            return _Admin
    raise E_NotFound()

#Get admin index by Uid
def AdminIndex(uid) -> int:
    _index = 0
    for _admin in Admins:
        if str(_admin.Uid) == str(uid):
            return _index
        _index += 1
    raise E_NotFound("Admin not in list")

def _updateAdmin(val):
    def update(doc):
        if doc["Uid"] == val["Uid"]:
            for key in doc.keys(): # THERE IS A 'None' VALUE IN BETWEEN SO I COULDN'T USE dict.update() METHOD
                doc[key] = val[key]
    return update

#Set or update an Admin
def AdminSet(param : Admin) -> None:
    try:
        AdminGet(param.Uid)
        db.update(_updateAdmin(param.getValues()))
    except E_NotFound:
        db.insert(param.getValues())
    return AdminStartBootstrap()

AdminStartBootstrap()