import datetime
import time
from threading import Timer
import re

try:
    from pyrogram import Client , filters
    from pyrogram.types import InputMediaPhoto, InputMediaVideo , ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardMarkup,InlineKeyboardButton
except ModuleNotFoundError:
    import os
    os.system("pip install pyrogram")
    os.system("pip install tinydb")
    print("\n\n\n\n\n\n\n\n\n\n\nRestart the program")
    quit()

from plugins.errors import *
from plugins import config
#from .Modules import B_item as item
from .Modules import B_user as user
from .Modules.Models import M_error as error
from .Modules import B_admin as Admin
from .Modules.Models.M_admin import Admin as iiix
from .Modules.E_stats import stat
from .Modules import TG_Filters as customFilters
from . import CallBack
#backToP3$

AdminUIBackButtons = lambda env,CallBackValue="" : {
    "AdminManage" :
        [
            InlineKeyboardButton(
                config.Button_Back,
                callback_data=CallBack.Get("iiixz5")
            )
        ],
    "AdminManage93":[
        InlineKeyboardButton(
                config.Button_Back,
                callback_data=CallBack.Get("iiixz93")
            )
    ],
    "AdminManage93Select" : [
        InlineKeyboardButton(
                config.Button_Back,
                callback_data=CallBack.Get("iiixz93",CallBackValue)
            )
        ],
    "MainMenu" : [
        InlineKeyboardButton(
                config.Button_Back,
                callback_data=CallBack.Get("backToP")+"3"
            )
        ]
}[env]

AdminUserInterface = lambda env,role,CallBackValue="" : {
    "SupremePanelAdminManagement" : {
        Admin.Roles["Supreme"] : [
            [
                InlineKeyboardButton(
                    config.Button_SupremeAdminAdd,
                    callback_data=CallBack.Get("iiixz3")
                )
            ],
            [
                InlineKeyboardButton(
                    config.Button_SupremeAdminList,
                    callback_data=CallBack.Get("iiixz93")
                )
            ],
        ]
    }[role],
    
    "SupremePanelAdminSelectedManage" : {
        Admin.Roles["Supreme"]:[
            [
                InlineKeyboardButton(
                    config.Button_SupremeAdminDelete,
                    callback_data=CallBack.Get("iiixz9",CallBackValue)
                )
            ],
            [
                InlineKeyboardButton(
                    config.Button_SupremeAdminRole,
                    callback_data=CallBack.Get("iiixzr",CallBackValue + ("0",))
                )
            ]
        ]
    }[role]
}[env]

#Admin management panel
@Client.on_callback_query(filters.regex(r"^"+CallBack.Get("iiixz5") + r"$") & customFilters.AdminPremission(Admin.Roles["Supreme"]),group = CallBack.groupSetter())
def CallBackSupremeAdmin5(client,callback_query):
    Adminuid = callback_query.from_user.id # Admin user id
    mid = callback_query.message.message_id
    Admin.Admins[Admin.Admins.index(Admin.AdminGet(Adminuid))].Status = stat.nothing
    client.edit_message_text(
        chat_id=Adminuid,
        message_id=mid,
        text=config.Text_Supreme5Admin,
        reply_markup = InlineKeyboardMarkup(
            AdminUserInterface("SupremePanelAdminManagement",Admin.Roles["Supreme"]) + [AdminUIBackButtons("MainMenu")])
    )

#Admin add
@Client.on_callback_query(filters.regex(r"^" + CallBack.Get("iiixz3") + r"$") & customFilters.AdminPremission(Admin.Roles["Supreme"]),group = CallBack.groupSetter())
def CallBackSupremeCreateAdmin(client,callback_query):
    Adminuid = callback_query.from_user.id # Admin user id
    mid = callback_query.message.message_id
    currentEnv = Admin.AdminGet(Adminuid)
    currentEnv.Status = stat.AdminAdd
    Admin.AdminSet(currentEnv)
    client.edit_message_text(
        chat_id=Adminuid,
        message_id=mid,
        text=config.Text_AdminAdd,
        reply_markup = InlineKeyboardMarkup([AdminUIBackButtons("AdminManage")])
    )

ContactFilter = filters.create(lambda _,__,m : bool(m.contact))
#Set admin by contact
@Client.on_message(customFilters.AdminPremission(Admin.Roles["Supreme"],stat.AdminAdd) & ContactFilter)
def callBackSupremeCreateAdminFromContact(client,message):
    Adminuid = message.from_user.id # Admin user id
    mid = message.message_id
    targetUid = message.contact.user_id
    try:
        Admin.AdminGet(targetUid)
        client.send_message(chat_id = Adminuid,
            text="TRY ANOTHER✌️👽\nاین ادمین در سیستم وجود دارد",
            reply_to_message_id = mid ,
            reply_markup = InlineKeyboardMarkup(
                [AdminUIBackButtons("AdminManage")]
            )
        )
        return
    except error.E_NotFound:
        _setAdmin = Admin.AdminSet(Admin.Admin(targetUid,[Admin.Roles["None"]]))
        Admin.Admins[Admin.AdminIndex(Adminuid)].Status = stat.nothing
        client.send_message(chat_id = Adminuid,
            text="Success✌️👽\nبرای فعال شدن این ادمین ، نقش ایشان را انتخاب کنید",
            reply_to_message_id = mid,
            reply_markup = InlineKeyboardMarkup(
                [[InlineKeyboardButton(
                    config.Button_SupremeAdminRole,
                    callback_data=CallBack.Get("iiixzr",str(Admin.AdminIndex(targetUid)),"0"))
                ]]
            )
        )

#List of admins
@Client.on_callback_query(filters.regex(CallBack.Get("iiixz93")+ r"$") & customFilters.AdminPremission(Admin.Roles["Supreme"]),group = CallBack.groupSetter())
def callBackSupremeAdminManage(client,callback_query):
    Adminuid = callback_query.from_user.id # Admin user id
    mid = callback_query.message.message_id
    CurrentAdmin = Admin.AdminGet(Adminuid)
    OptionButtons = []
    ButtonToAdd = []
    RolesCount = {}
    for role in Admin.Roles:
        RolesCount[Admin.Roles[role].Id] = 0
    _counter = 0
    for _admin in Admin.Admins:
        if(_admin == CurrentAdmin):
            continue
        for role in _admin.Role:
            RolesCount[role.Id] += 1
        _counter += 1
        ButtonToAdd.append(
            InlineKeyboardButton(
                    (config.getAdminSignByRole(Admin.Roles["Supreme"]) if Admin.Roles["Supreme"] in _admin.Role else "") + _admin.Uid,
                    callback_data=CallBack.Get("iiixz93",str(Admin.Admins.index(_admin)))
                )
        )
        if _counter % 3:
            OptionButtons.append(ButtonToAdd)
            ButtonToAdd = []
    
    client.edit_message_text(
        chat_id=Adminuid,
        message_id=mid,
        text=config.Text_Supreme93AdminList,
        reply_markup = InlineKeyboardMarkup(OptionButtons + [AdminUIBackButtons("AdminManage")]) #if len(OptionButtons) else InlineKeyboardMarkup([AdminUIBackButtons("AdminManage")])
    )

#Open an admin
@Client.on_callback_query(filters.regex(CallBack.Get("iiixz93") + r"-\d*$") & customFilters.AdminPremission(Admin.Roles["Supreme"]),group = CallBack.groupSetter())
def callBackSupremeAdminManageSelect(client,callback_query):
    Adminuid = callback_query.from_user.id # Admin user id
    mid = callback_query.message.message_id
    targetIndex = callback_query.data.split("-")[1]
    AdminResult = Admin.Admins[int(targetIndex)]
    client.edit_message_text(
        chat_id=Adminuid,
        message_id=mid,
        text=config.Text_Supreme93AdminRetrive(AdminResult.Role,AdminResult.Uid),
        reply_markup = InlineKeyboardMarkup(
            AdminUserInterface("SupremePanelAdminSelectedManage",
                                Admin.Roles["Supreme"],int(targetIndex),AdminResult.Role) + [AdminUIBackButtons("AdminManage93")])
    )

#Remove admin
@Client.on_callback_query(filters.regex(r"^" + CallBack.Get("iiixz9") + r"-\d*$") & customFilters.AdminPremission(Admin.Roles["Supreme"]),group = CallBack.groupSetter())
def callBackSupremeAdminManageDelete(client,callback_query):
    Adminuid = callback_query.from_user.id # Admin user id
    mid = callback_query.message.message_id
    targetIndex = callback_query.data.split("-")[1]
    AdminResult = Admin.Admins[int(targetIndex)]
    Admin.AdminRemove(AdminResult)
    client.edit_message_text(
        chat_id=Adminuid,
        message_id=mid,
        text=config.Text_SuccessAdminDelete,
        reply_markup = InlineKeyboardMarkup(
            [AdminUIBackButtons("AdminManage")])
    )

def _getRoleOptions(AdminResult,targetIndex):
    RoleOptions = []
    for RoleKey in Admin.Roles:
        if Admin.Roles[RoleKey] not in AdminResult.Role:
            ButtonText = config.getAdminSignByRole(Admin.Roles[RoleKey]) + Admin.Roles[RoleKey].Title
            RoleOptions.append(
                [InlineKeyboardButton(
                    ButtonText,
                    callback_data=CallBack.Get("iiixzr",str(targetIndex),str(Admin.Roles[RoleKey].Id))
                )]
            )
    if Admin.Roles["Supreme"] in AdminResult.Role:
        ButtonText = config.getAdminSignByRole(Admin.Roles["None"]) + Admin.Roles["None"].Title
        RoleOptions = [[InlineKeyboardButton(
            ButtonText,
            callback_data=CallBack.Get("iiixzr",str(targetIndex),str(Admin.Roles['None'].Id))
        )]]
    RoleOptions.append(
        AdminUIBackButtons("AdminManage93Select",str(targetIndex))
    )
    return RoleOptions

#set role
@Client.on_callback_query(filters.regex(r"^"+CallBack.Get("iiixzr")+r"-\d*-\d*") & customFilters.AdminPremission(Admin.Roles["Supreme"]),group = CallBack.groupSetter())
def callBackSupremeAdminSetRole(client,callback_query,mid=0):
    Adminuid = callback_query.from_user.id # Admin user id
    mid = mid or callback_query.message.message_id
    targetIndex = callback_query.data.split("-")[1]
    try:
        targetRoleId = int(callback_query.data.split("-")[2])
    except IndexError:
        targetRoleId = 0
    AdminResult = Admin.Admins[int(targetIndex)]

    if targetRoleId == Admin.Roles["Supreme"].Id:
        AdminResult.Role = [Admin.Roles["Supreme"]]

    elif targetRoleId == Admin.Roles["None"].Id:
        AdminResult.Role = [Admin.Roles["None"]]

    else:
        for roleKey in Admin.Roles:
            if Admin.Roles[roleKey].Id == targetRoleId:
                AdminResult.Role.append(Admin.Roles[roleKey])
    
    Admin.AdminSet(AdminResult)
    RoleOptions = _getRoleOptions(AdminResult,targetIndex)
    client.edit_message_text(
        chat_id=Adminuid,
        message_id=mid,
        text=config.Text_Supreme93AdminRetrive(AdminResult.Role,AdminResult.Uid),
        reply_markup = InlineKeyboardMarkup(RoleOptions)
    )
#set role
@Client.on_callback_query(filters.regex(CallBack.Get("iiixzr")+r"-\d") & customFilters.AdminPremission(Admin.Roles["Supreme"]),group = CallBack.groupSetter())
def _callBackSupremeAdminSetRole(client,callback_query):
    callBackSupremeAdminSetRole(client,callback_query,callback_query.message.message_id)