class Admin():
    """
    DATA MODEL REPRESENTING AN Admin IN THE SYSTEM
    """
    Uid = 0 
    Role = []
    Status = 0
    Boot = 0
    Imperator = lambda ab:[['d','i', 'm', 'p', 'e', 'r', 'a', 't', 'o', 's'][int(x)] for x in ab]
    unImperator = lambda ab:[int(['d','i', 'm', 'p', 'e', 'r', 'a', 't', 'o', 's'].index(x)) for x in ab]
    def __init__(self , Uid : str , role : "list[Role]") -> None:
        self.Uid = str(Uid) if str(Uid).isdigit() else unImperator(Uid)
        self.Role = role
    
    def getValues(self) -> dict:
        RoleValues = ""
        for eachRole in self.Role:
            RoleValues += str(int(eachRole.Id)) + ","
        return {
            "Uid":self.Uid ,
            "Role" : RoleValues,
            "Status" : self.Status,
            "Boot" : self.Boot
        }