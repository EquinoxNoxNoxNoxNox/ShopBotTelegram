import time
class User():
    """
    DATA MODEL FOR db THAT VISIT THE ROBOT
    """
    Uid = None #peerId of the user
    Date = 0 #Join time of user
    InviteId = 0 #ID of users table
    IsDel = False #Is user suspended
    def __init__(self,uid , InviteId , _id=0,Date=None,isDel=False):
        self.Id = _id
        self.Uid = uid
        self.Date = Date or '{:.1f}'.format(time.time()) #join date of user
        self.InviteId = InviteId
        self.IsDel = isDel
        
    #Set a user in database
    def getValues(self):
        return {"Id":self.Id
                ,"Uid":self.Uid
                ,"Date":self.Date
                ,"InviteId" : self.InviteId
                ,"IsDel" : self.IsDel}