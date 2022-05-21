from tinydb import TinyDB , Query
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware
from .Models.M_error import E_NotFound,E_DuplicatedRecord
from .Models.M_category import Category

db = TinyDB("datas/Categories.json")
q = Query()

def _update(val):
        def upd(doc):
            if doc["Id"] == val["Id"]:
                for key in doc.keys(): # THERE IS A 'None' VALUE IN BETWEEN SO I COULDN'T USE dict.update() METHOD
                    doc[key] = val[key]
        return upd
def Set(param:Category) -> Category:
    try:
        _=db.search(q.Title == param.Title)
        if(not len(_)):
            raise E_NotFound()
        db.update(_update(param.getValues()))
    except E_NotFound:
        try:
            LastRow = db.all()[-1]
            param.Id = LastRow["Id"] + 1
        except IndexError: # IF THERE IS NO LAST ROW
            param.Id = 1
        
        db.insert(param.getValues())
    return param


#Get category by Id
def GetById(Id) -> Category:
    r = db.search(q.Id == int(Id))[0]
    return Category(r["Title"],r["Id"],r["Views"],r["IsDeleted"])
#Get all categories
def GetAll(isAll=False) -> list:
    _res = db.all()
    if(isAll):
        return [Category(r["Title"],r["Id"],r["Views"],r["IsDeleted"]) for r in _res]
    else:
        return [Category(r["Title"],r["Id"],r["Views"],r["IsDeleted"]) for r in _res if not r["IsDeleted"]]
