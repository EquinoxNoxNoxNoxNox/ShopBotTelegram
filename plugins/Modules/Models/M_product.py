import time
class Product():
    """DATA MODEL REPRESENTING A product"""
    Id = 0 # ID
    Title = "" # Title of the product
    Description="" # Description details of the product
    Price = ""  # Price of the product
    CategoryId = 0 #Category table Id
    Views = 0 #View count of product by users
    IsDeleted = False # Is product deleted
    Date = 0 # Record date
    def __init__(self,
                title:"str Title of the item",
                description:"str Desription of the item",
                price:"str Price of the item",
                CategoryId:"int Id of Category Datbase",
                _id:"int ID of the item"= 0,
                isDeleted : "bool Is product deleted" = False,
                Date : "Record date" = 0,
                views : "int View count of the item" = 0
            )->None:
        self.Id = _id
        self.Title = title
        self.Description = description
        self.Price = price
        self.CategoryId = CategoryId
        self.IsDeleted = isDeleted
        self.Date = Date or '{:.1f}'.format(time.time())
        self.Views = views
    
    def getValues(self) -> dict:
        return {"Id":self.Id 
        ,"Title" : self.Title
        ,"Description":self.Description
        ,"Price":self.Price
        ,"CategoryId":self.CategoryId
        ,"IsDeleted" : self.IsDeleted
        ,"Views":self.Views
        ,"Date" : self.Date}
