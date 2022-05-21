try:
    from pyrogram import Client , filters
    from pyrogram.types import InputMediaPhoto, InputMediaVideo , ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardMarkup,InlineKeyboardButton
    import jdatetime
except ModuleNotFoundError:
    import os
    os.system("pip install pyrogram")
    os.system("pip install tinydb")
    os.system("pip install jdatetime")
    print("\n\n\n\n\n\n\n\n\n\n\nRestart the program")
    quit()


from plugins import config
from .Modules import B_user
from .Modules.E_stats import stat
from .Modules import TG_Filters as customFilters
from .Modules.B_admin import Roles
from .Modules import B_admin as Admin
from .Modules.Models.M_error import E_NotFound
from . import CallBack
from .Modules import B_invite
AdminUIBackButtons = lambda env,CallBackValue="" : {
    "UserManage" :
        [
            InlineKeyboardButton(
                config.Button_Back,
                callback_data=CallBack.Get("imperator5")
            )
        ],
    "MainMenu" : 
        [
            InlineKeyboardButton(
                    config.Button_Back,
                    callback_data=CallBack.Get("backToP") + "3"
                )
        ],
    "UserList":#
        [
            InlineKeyboardButton(
                config.Button_Back,
                callback_data=CallBack.Get(f"imperator93",str(1),str(1))
            )
        ],
    "InviteManageMenu" :
        [
            InlineKeyboardButton(
                config.Button_Back,
                callback_data=CallBack.Get("InviteMenu")
            )
        ]

}[env]

AdminUserInterface = lambda env,role,CallBackValue="" : {
    "UserManage" : {
        Roles["Supreme"] : [
            [
                InlineKeyboardButton(
                    config.Button_SupremeUserManagement,
                    callback_data=CallBack.Get("imperator93")
                ),
            ],
            [
                InlineKeyboardButton(
                    config.Button_SupremeAnnouncement,
                    callback_data=CallBack.Get("Announcement")
                )
            ],
            [
                InlineKeyboardButton(
                    config.Button_SupremeAdvertisement,
                    callback_data=CallBack.Get("Advertise")
                )
            ]
        ]
    }[role],

    "UsersList" : {
        Roles["Supreme"] : [
            [
                InlineKeyboardButton(
                    config.Button_SupremeActiveUserList,
                    callback_data=CallBack.Get("Imperator93","1","0","0")
                ),
            ],
            [
                InlineKeyboardButton(
                    config.Button_SupremeBanUserList,
                    callback_data=CallBack.Get("Imperator93","0","0","0")
                )
            ]
        ]
    }[role],
    
    "InviteManageMenu" : {
        Roles["Supreme"] : [
            [
                InlineKeyboardButton(
                    config.Button_InviteAdd,
                    callback_data=CallBack.Get("CreateInviteMenu")
                )
            ],
            [
                InlineKeyboardButton(
                    config.Button_InviteLinkList,
                    callback_data=CallBack.Get("InviteLinkList")
                )
            ],
            [
                InlineKeyboardButton(
                    config.Button_Back,
                    callback_data=CallBack.Get("backToP") + str(3)
                )
            ]
        ]
    }[role]

}[env]

#AdminSupreme User panel bootstrap
@Client.on_callback_query(filters.regex(r"^"+CallBack.Get("imperator5")+r"$")
                            & customFilters.AdminPremission(Admin.Roles["Supreme"]),group=CallBack.groupSetter())
def CallBackSupremeUserManagementPanel(client,callback_query):
    Adminuid = callback_query.from_user.id # Admin user id
    mid = callback_query.message.message_id
    Admin.Admins[Admin.Admins.index(Admin.AdminGet(Adminuid))].Status = stat.nothing
    client.edit_message_text(
        chat_id=Adminuid,
        message_id=mid,
        text=config.Text_Supreme5User,
        reply_markup = InlineKeyboardMarkup(
            AdminUserInterface("UserManage",
                            Admin.Roles["Supreme"]) + [AdminUIBackButtons("MainMenu")]
        )
    )

#User management button. 2way to select to show active and banned user list
@Client.on_callback_query(filters.regex(r"^"+CallBack.Get("imperator93")+r"$")
                            & customFilters.AdminPremission(Admin.Roles["Supreme"]),group=CallBack.groupSetter())
def callBackSupremeUserList2Way(client,callback_query):
    print("COMMAND CAUGHT")
    Adminuid = callback_query.from_user.id # Admin user id
    mid = callback_query.message.message_id
    client.edit_message_text(
        chat_id=Adminuid,
        message_id=mid,
        text=config.Text_SupremeUserListText,
        reply_markup = InlineKeyboardMarkup(AdminUserInterface("UsersList",Roles["Supreme"]) + [AdminUIBackButtons("UserManage")])
    )


#Ban user confirm message
@Client.on_callback_query(filters.regex(r"^"+CallBack.Get("imperator9")+r"-\d-\d*$")
                            & customFilters.AdminPremission(Admin.Roles["Supreme"]),group=CallBack.groupSetter())
def callBackSupremeUserBan(client,callback_query):
    Adminuid = callback_query.from_user.id # Admin user id
    mid = callback_query.message.message_id
    target = int(callback_query.data.split("-")[1])
    UserToBanId = int(callback_query.data.split("-")[2])
    
    if int(target) == 0:
        print("TARGET GONNA Q")
        client.edit_message_text(
            chat_id=Adminuid,
            message_id=mid,
            text=config.Text_SupremeUserBanText,
            reply_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton(
                    config.Button_Confirm,
                    callback_data=CallBack.Get("imperator9",1,str(UserToBanId))
                )],
                [InlineKeyboardButton(
                    "بازگشت",
                    callback_data=CallBack.Get("imperator93",UserToBanId)
                )]
            ]
        ))
        return
    else:
        print("TARGET GONNA BAN")
        UserToFind = B_user.GetByUid(Adminuid)
        UserToFind.IsDel = True
        B_user.SetUser(UserToFind)
        client.edit_message_text(
            chat_id=Adminuid,
            message_id=mid,
            text=config.Text_SupremeUserBanConfirmText,
            reply_markup = InlineKeyboardMarkup([AdminUIBackButtons("UsersList")])
        )
        return

#Talkie with a user
@Client.on_callback_query(filters.regex(r"^"+CallBack.Get("imperatorTalkie")+r"-\d*$")
                            & customFilters.AdminPremission(Admin.Roles["Supreme"]),group=CallBack.groupSetter())
def callBackSupremeUserTalkie(client,callback_query):
    Adminuid = callback_query.from_user.id # Admin user id
    mid = callback_query.message.message_id
    IdUserToTalk = int(callback_query.data.split("-")[1])
    _user = B_user.GetById(IdUserToTalk)
    client.send_message(
        chat_id=Adminuid,
        text=config.Text_AdminTalkieConnect.format(uid=_user.Uid,userId=_user.Id)
    )

#Announcement button
@Client.on_callback_query(filters.regex(r'^'+CallBack.Get("Announcement")+r'$')
                            & customFilters.AdminPremission(Admin.Roles['Supreme']),group=CallBack.groupSetter())
def callBackAnnouncementToAll(client, callback_query):
    adminUid = callback_query.from_user.id # Admin user id
    mid = callback_query.message.message_id
    Admin.Admins[Admin.AdminIndex(adminUid)].Status = stat.AdminAnnouncement
    client.send_message(
        chat_id=adminUid,
        text=config.Text_AnnouncementNotif,
        reply_markup = InlineKeyboardMarkup(
            [AdminUIBackButtons("UserManage")]
        )
    )

#MESSAGE CONFIRM ANNOUNCEMENT
@Client.on_message(customFilters.AdminPremission(Admin.Roles['Supreme'],stat.AdminAnnouncement))
def messageAdminAnnouncement(client,message):
    adminUid = message.from_user.id # Admin user id
    client.send_message(
        chat_id=adminUid,
        text="آیا از ارسال این پیام مطمئن هستید؟",
        reply_to_message_id=message.message_id,
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton(text="ارسال",
                                  callback_data=CallBack.Get("ConfirmMessageAnnouncement","1"))]+AdminUIBackButtons("UserList")
        ])
    )    

#CONFIRM CALLBACK
@Client.on_callback_query(filters.regex(r'^'+CallBack.Get("ConfirmMessageAnnouncement")+r'-\d$')
                            & customFilters.AdminPremission(Admin.Roles['Supreme']),group=CallBack.groupSetter())
async def callBackAnnouncementConfirm(client, callback_query):
    adminUid = callback_query.from_user.id # Admin user id
    mid = callback_query.message.message_id
    target = int(callback_query.data.split("-")[1])
    MessageToSend = callback_query.message.reply_to_message
    try:
        UserToSendIds = [x.Uid for x in B_user.getAll()]
    except TypeError:
        await client.edit_message_text(chat_id = adminUid, message_id = mid, text = "هیچ کاربری وجود ندارد",reply_markup =InlineKeyboardMarkup([AdminUIBackButtons("UserManage")]))
        return
    if not target:
        await client.edit_message_text(chat_id = adminUid, message_id = mid, text = "لغو شد",reply_markup = InlineKeyboardMarkup([AdminUIBackButtons("UserManage")]))
        return
    try:
        await client.edit_message_text(chat_id = adminUid, message_id = mid, text = "لطفا صبر کنید و از ربات استفاده نکنید",reply_markup = InlineKeyboardMarkup([AdminUIBackButtons("UserManage")]))
        for UserToSendId in UserToSendIds:
            await client.copy_message(chat_id = UserToSendId , from_chat_id = adminUid , message_id = MessageToSend.message_id, caption  = (MessageToSend.text or MessageToSend.caption) + config.caption)
        await client.edit_message_text(chat_id = adminUid, message_id = mid, text = "انجام شد",reply_markup =None)
    except Exception as e:
        raise e

#Advertise button
@Client.on_callback_query(filters.regex(r'^'+CallBack.Get("Advertise")+r'$')
                            & customFilters.AdminPremission(Admin.Roles['Supreme']),group=CallBack.groupSetter())
def callBackAdminAdvertiseToAll(client, callback_query):
    adminUid = callback_query.from_user.id # Admin user id
    mid = callback_query.message.message_id
    client.send_message(chat_id = adminUid , text = "تبلیفات برای این ربات هنوز ساخته نشده است")

#ADD Invite link 
@Client.on_callback_query(filters.regex(r'^'+CallBack.Get("CreateInviteMenu")+r'$') & customFilters.AdminPremission(Admin.Roles['Supreme']),group=CallBack.groupSetter())
def callBackAdm_in_InviteLink(client, callback_query):
    adminUid = callback_query.from_user.id # Admin user id
    mid = callback_query.message.message_id
    Admin.Admins[Admin.AdminIndex(adminUid)].Status = stat.InviteAdd
    client.edit_message_text(
        chat_id = adminUid,
        message_id = mid,
        text = config.Text_InviteAdd,
        reply_markup = InlineKeyboardMarkup([AdminUIBackButtons("InviteManageMenu")])
    )

@Client.on_callback_query(filters.regex(r'^'+CallBack.Get("InviteLinkList")+r'$') & customFilters.AdminPremission(Admin.Roles['Supreme']),group=CallBack.groupSetter())
def messageAdmin__InviteLink(client, callback_query):
    adminUid = callback_query.from_user.id # Admin user id
    mid = callback_query.message.message_id
    InviteLinks = B_invite.GetAll()
    ResultInvite = []
    for invite in InviteLinks: 
        try:
            Count = len(B_user.getByInviteId(invite.Id))
        except E_NotFound:
            Count = 0
        ResultInvite.append([invite,Count])
    if(ResultInvite):
        Text_ToSend = config.Text_Invites(ResultInvite)
    else:
        Text_ToSend = "لینک در سیستم ثبت نشده است"
    client.edit_message_text(
        chat_id = adminUid,
        message_id = mid,
        text = Text_ToSend,
        reply_markup = InlineKeyboardMarkup([AdminUIBackButtons("InviteManageMenu")])
    )
#MESSAGE Invite link 
@Client.on_message(customFilters.AdminPremission(Admin.Roles['Supreme'],stat.InviteAdd)
                ,group=CallBack.groupSetter())
def messageAdminInviteLink(client, message):
    adminUid = message.from_user.id # Admin user id
    mid = message.message_id
    ResInvite = B_invite.Set(B_invite.Invite(message.text))
    Admin.Admins[Admin.AdminIndex(adminUid)].Status = stat.nothing
    client.send_message(
        chat_id = adminUid,
        text=config.Text_InviteSuccess.format(Key=ResInvite.InviteKey),
        reply_markup =[]
    )
    #client.send_message(
    #    chat_id = adminUid,
    #    reply_to_message_id = mid ,
    #    text = config.Text_InviteConfirm,
    #    reply_markup = InlineKeyboardMarkup([
    #        [InlineKeyboardButton(text="تأید",callback_data=CallBack.Get("ConfirmInviteTitle","1"))],
    #        [InlineKeyboardButton(text="لغو",callback_data=CallBack.Get("ConfirmInviteTitle","0"))]
    #    ])
    #)

#Invite link button
@Client.on_callback_query(filters.regex(r'^'+CallBack.Get("InviteMenu")+r'$') & customFilters.AdminPremission(Admin.Roles['Supreme']),group=CallBack.groupSetter())
def callBackAdminInviteLink(client, callback_query):
    adminUid = callback_query.from_user.id # Admin user id
    mid = callback_query.message.message_id
    client.edit_message_text(
        chat_id = adminUid,
        message_id=mid,
        text = config.Text_InviteMenu,
        reply_markup = InlineKeyboardMarkup(AdminUserInterface("InviteManageMenu",Admin.Roles["Supreme"]))
    )
