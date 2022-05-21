class Photo():
    """
    DATA MODEL REPRESENTING A PRODUCT PHOTO
    """
    Id = 0 #Id of photo
    ProductId = 0 # Id of product table
    FileId = 0 # File id recived in telegram
    IsDeleted = False
    def __init__(self,
                 ProductId:int,
                 FileId:str,
                 _id:int=0):
        self.Id = _id
        self.ProductId = ProductId
        self.FileId = FileId
    
    def getValues(self) -> dict:
        return {"Id":self.Id
        ,"FileId" : self.FileId
        ,"ProductId" : self.ProductId
        ,"IsDeleted" : self.IsDeleted}
