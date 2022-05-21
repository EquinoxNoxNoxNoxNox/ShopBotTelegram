from tinydb import TinyDB , Query
from .Models.M_product import Product
from .Models.M_error import E_NotFound

db = TinyDB("datas/product.json")
q = Query()

def _update(val):
        def upd(doc):
            if doc["Id"] == val["Id"]:
                for key in doc.keys(): # THERE IS A 'None' VALUE IN BETWEEN SO I COULDN'T USE dict.update() METHOD
                    doc[key] = val[key]
        return upd

#Set an Product in db
def Set(param : Product) -> Product:
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

#Get product
def GetById(Id) -> Product:
    try:
        r = db.search(q.Id == int(Id))[0]
        return Product(r["Title"], r["Description"], r["Price"], r["CategoryId"],r["Id"],r["IsDeleted"],r["Date"],r["Views"])
    except IndexError:
        raise E_NotFound(f"product with id {Id} not found")

#Get product
def GetByCategory(CatId) -> list:
    try:
        res = db.search(q.CategoryId == CatId)
        return [Product(r["Title"], r["Description"], r["Price"], r["CategoryId"],r["Id"],r["IsDeleted"],r["Date"],r["Views"]) for r in res if not r["IsDeleted"] and r["CategoryId"]==int(CatId)]
    except IndexError:
        raise E_NotFound(f"product with id {Id} not found")

#Get all products
def GetAll() -> list:
    res = db.all()
    return [Product(r["Title"], r["Description"], r["Price"], r["CategoryId"],r["Id"],r["IsDeleted"],r["Date"],r["Views"]) for r in res]