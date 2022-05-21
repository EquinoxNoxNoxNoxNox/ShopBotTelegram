from tinydb import TinyDB , Query
from .Models.M_photo import Photo
from .Models.M_error import E_NotFound

db = TinyDB("datas/photo.json")
q = Query()

def _update(val):
        def upd(doc):
            if doc["Id"] == val["Id"]:
                for key in doc.keys(): # THERE IS A 'None' VALUE IN BETWEEN SO I COULDN'T USE dict.update() METHOD
                    doc[key] = val[key]
        return upd

#Set an Photo in db
def Set(param : Photo) -> Photo:
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

#Get Photo by Product id
def GetByProductId(productId:int) -> list:
    try:
        _r = db.search(q.ProductId == productId)
        return [Photo(res["ProductId"], res["FileId"],res["Id"]) for res in _r if not res["IsDeleted"]]
    except IndexError:
        raise E_NotFound(f"Photo not found with productId of {productId}")

#remove Photo by id
def remove(Id:int) -> bool:
    try:
        res = db.search(q.Id == Id)[0]
        _Photo = Photo(res["ProductId"],res["FileId"],res["Id"])
        _Photo.IsDeleted=True
        Set(_Photo)
        return True
    except IndexError:
        raise E_NotFound(f"Photo not found with Id of {productId}")
