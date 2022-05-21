from pyrogram import filters
from . import B_admin as Admin
from .Models import M_error as errors
from .E_stats import stat as Stats
from . import B_inbox
from . import B_user

class AdminFilter(filters.user):
    """
    A CALLBACK FILTER FOR checking Admin
    """
    Role = 0 #Role of the premission filter
    Status = 0 #Status that filter require
    currentAdmin = None#Admin
    def __init__(self):
        super().__init__(users = [x.Uid for x in Admin.Admins])

    async def __call__(self, _, message: "Message") -> bool:
        try:
            self.currentAdmin = Admin.AdminGet(message.from_user.id)
        except errors.E_NotFound:
            return False
        return True

class AdminPremission(AdminFilter):
    """
    A CALLBACK FILTER FOR checking Admin ROLES
    """
    def __init__(self,role : Admin.Role = 0 ,status : "stat" = 0) -> None:
        super().__init__()
        self.Role = role
        self.Status = int(status)
    
    async def __call__(self, _, message: "Message") -> bool:
        if(not await super().__call__(_, message)):
            return False
        try:
            message=message.message
        except AttributeError:
            message=message
        return (message.from_user
                and (True if not self.Role
                        else True if Admin.Roles["Supreme"] in self.currentAdmin.Role else self.Role in self.currentAdmin.Role)
                and True if not self.Status else self.Status == self.currentAdmin.Status)

class AdminTalk(AdminPremission):
    """
    A CALLBACK FILTER FOR RECIEVING ADMIN MESSAGES THUS WITH #INBOX IN THE BEGINNING
    """
    def __init__(self,role : Admin.Role = 0 ,status : "stat" = 0) -> None:
        super().__init__()
        self.Role = role
        self.Status = int(status)
    
    async def __call__(self, _, message: "Message") -> bool:
        if(not await super().__call__(_, message)):
            return False
        try:
            message=message.message
        except AttributeError:
            message=message
        try:
            if(message.text):
                if(message.text[0] == "/"):
                    return False
        except TypeError:
            pass
        if message.reply_to_message:
            if message.reply_to_message.text.startswith("#INBOX") or message.reply_to_message.text.startswith("#TALKIE"):
                return True
        return False

class UserFilter(AdminFilter):
    UserToValidate = None
    def __init__(self):
        super()
    async def __call__(self, _, message: "Message") -> bool:
        if(await super().__call__(_, message)):
            return False
        try:
            self.UserToValidate = B_user.GetByUid(message.from_user.id)
            return True
        except errors.E_NotFound:
            return False

class UserTalk(AdminFilter):
    """
    A CALLBACK FILTER FOR RECIEVING USER MESSAGES THUS WITH #INBOX IN THE BEGINNING
    """
    async def __call__(self, _, message: "Message") -> bool:
        if(not await super().__call__(_, message)):
            return False
        try:
            message=message.message
        except AttributeError:
            message=message
        if(message.text[0] == "/"):
            return False
        if message.incoming:
            return B_inbox.CheckUserValidity(a.Uid)
        return False