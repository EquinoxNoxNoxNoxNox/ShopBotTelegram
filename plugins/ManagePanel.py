from pyrogram import Client , filters
from pyrogram.types import InputMediaPhoto, InputMediaVideo , ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardMarkup,InlineKeyboardButton
import jdatetime
from . import config
from .Modules import B_invite
from .Modules.Models import M_error
from .Modules.B_admin import *
from .Modules import B_category
from .Modules import B_user
from .Modules.Models.M_user import User
from .Modules.E_stats import stat
from .Modules import TG_Filters as customFilters
from . import CallBack

AdminUserInterface = lambda env,CallBackValue="" :{
    "SupplyManage":[
        [
            InlineKeyboardButton(
                config.Button_SupplyCategory,
                callback_data=CallBack.Get("CategoryManage")
            )
        ],
    ],
    "SupportManage":[
        [
            InlineKeyboardButton(
                config.Button_Inbox,
                callback_data=CallBack.Get("GetInbox","1")
            )
        ],
    ],
    "SupremePanel" :[
        [
            InlineKeyboardButton(
                config.Button_SupremeUsers,
                callback_data=CallBack.Get("imperator5")
            )
        ],
        [
            InlineKeyboardButton(
                config.Button_SupremeAdmins,
                callback_data=CallBack.Get("iiixz5")
            )
        ],
        [
            InlineKeyboardButton(
                config.Button_Invite,
                callback_data=CallBack.Get("InviteMenu")
            )
        ]
    ]
}[env]

#Show p1 panel
def showPanelSupply(client,message,uid=0,isBack=False):
    Adminuid = uid or message.from_user.id # Admin user id
    mid = message.message_id
    currentAdmin = AdminGet(Adminuid)
    currentAdmin.Boot = Roles["Supply"].Id
    TextToSend = config.Text_SupplyPanel
    if isBack:
        client.edit_message_text(
            chat_id=Adminuid,
            message_id=mid,
            text=TextToSend,
            reply_markup =InlineKeyboardMarkup(
                AdminUserInterface("SupplyManage"))
        )
    else:
        client.send_message(
            chat_id = Adminuid,
            text=TextToSend,
            reply_markup = InlineKeyboardMarkup(
                AdminUserInterface("SupplyManage"))
        )
#Show p2 panel
def ShowPanelSupport(client,message,uid=0,isBack=False):
    Adminuid = uid or message.from_user.id # Admin user id
    mid = message.message_id
    currentAdmin = AdminGet(Adminuid)
    currentAdmin.Boot = Roles["Support"].Id
    TextToSend = config.Text_SupportPanel
    if isBack:
        client.edit_message_text(
            chat_id=Adminuid,
            message_id=mid,
            text=TextToSend,
            reply_markup =InlineKeyboardMarkup(
                AdminUserInterface("SupportManage"))
        )
    else:
        client.send_message(
            chat_id = Adminuid,
            text=TextToSend,
            reply_markup = InlineKeyboardMarkup(AdminUserInterface("SupportManage"))
        )
#Show p3 panel
def ShowPanelSupreme(client,message,uid=0,isBack=False):
    Adminuid = uid or message.from_user.id # Admin user id
    mid = message.message_id
    currentAdmin = AdminGet(Adminuid)
    currentAdmin.Boot = Roles["Supreme"].Id
    ItemsCount = len([])
    CategoriesCount = len(B_category.db.search(B_category.q.IsDeleted == False))
    UsersCount = len(B_user.db.all())
    InviteLinkCount = len(B_invite.db.all())
    TextToSend = config.Text_AdminStartSupremeManagement.format(
                    MembersCount = str(UsersCount),
                    CategoryCount = str(CategoriesCount),
                    ItemsCount = str(ItemsCount),
                    AdminCount = str(len(Admins)),
                    InviteCount = str(InviteLinkCount)
                )
    if isBack:
        client.edit_message_text(
            chat_id=Adminuid,
            message_id=mid,
            text=TextToSend,
            reply_markup =InlineKeyboardMarkup(
                AdminUserInterface("SupremePanel"))
        )
    else:
        client.send_message(chat_id = Adminuid,
            text=TextToSend,
            reply_markup = InlineKeyboardMarkup(AdminUserInterface("SupremePanel"))
        )

#callback panel
@Client.on_callback_query(filters.regex(r"^" + CallBack.Get("backToP") + r"\d$")
                      & customFilters.AdminPremission(Roles["Supreme"]),group=CallBack.groupSetter())
def CallBackPanelSupport(client,callback_query):
    if(callback_query.data.endswith("1")):
        showPanelSupply(client,callback_query.message,callback_query.from_user.id,isBack = True)
    if(callback_query.data.endswith("2")):
        ShowPanelSupport(client,callback_query.message,callback_query.from_user.id,isBack = True)
    if(callback_query.data.endswith("3")):
        ShowPanelSupreme(client,callback_query.message,callback_query.from_user.id,isBack = True)

#CMD panels
@Client.on_message(filters.regex(r"^p\d") &
                customFilters.AdminPremission(Roles["Supreme"]),group=CallBack.groupSetter())
def CommandPanelSupreme(client,message):
    {
        "3":ShowPanelSupreme,
        "2":ShowPanelSupport,
        "1":showPanelSupply
    }[message.text[1]](client,message,message.from_user.id)
