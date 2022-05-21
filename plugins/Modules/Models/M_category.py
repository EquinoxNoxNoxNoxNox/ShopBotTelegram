class Category():
    """
    DATA MODEL REPRESENTING A PRODUCT CATEGORY
    """
    Id = 0
    Title = ""
    Views = 0
    IsDelted = False
    def __init__(self,
                 title:str, # Title of the Category
                 _id:int=0, # ID of the Category
                 views:int=0, # ID of the Category
                 isDeleted:bool = False #Logical delted of a category
                 )->None:
        self.Id = _id
        self.Title = title
        self.IsDeleted = isDeleted
        self.Views = views
    def getValues(self) -> dict:
        return {"Id":self.Id,
                "Title":self.Title,
                "IsDeleted":self.IsDeleted,
                "Views":self.Views}
