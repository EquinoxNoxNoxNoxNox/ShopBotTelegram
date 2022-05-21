class e_interface(Exception):
    messageText = ""
    def __init__(self,message="") -> None:
        self.messageText = message


class E_AccessRestricted(e_interface):
    messageText = "Premission restricted"

class E_DuplicatedRecord(e_interface):
    messageText = "Duplicated record"
    def __init__(self, entityName="") -> None:
        super().__init__("'" +entityName + "'-Duplicated record")
class E_NotFound(e_interface):
    def __init__(self, entityName="") -> None:
        super().__init__("'" +entityName + "'-Not found")