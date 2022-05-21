import re
import random
import jdatetime
from pyrogram import Client , filters
from pyrogram.types import InputMediaPhoto, InputMediaVideo , ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardMarkup,InlineKeyboardButton
import plugins.Modules.TG_Filters as customFilters
from .Modules import B_admin as Admin
from .Modules import B_user as User
from .Modules import B_inbox
from .Modules import E_stats
from . import CallBack
from . import config

#MESSAGE CONFIRM PREMISSION
@Client.on_message(customFilters.AdminTalk(Admin.Roles['Support']))
def messageAdminInboxReply(client,message):
    adminUid = message.from_user.id # Admin user id
    userPeerId = message.reply_to_message.message_id
    client.send_message(
        chat_id=message.chat.id,
        text="آیا از ارسال این پیام مطمئن هستید؟",
        reply_to_message_id=message.message_id,
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton(text="ارسال",
                                  callback_data=CallBack.Get("ConfirmMessageAdmin","1"))],
            [InlineKeyboardButton(text="لغو",
                                  callback_data=CallBack.Get("ConfirmMessageAdmin","0"))]
        ])
    )

#CONFIRM CALLBACK
@Client.on_callback_query(filters.regex(r'^'+CallBack.Get("ConfirmMessageAdmin")+r'-\d$')
                            & customFilters.AdminPremission(Admin.Roles['Support']),group=CallBack.groupSetter())
def call_BackMessageConfirm(client, callback_query):
    adminUid = callback_query.from_user.id # Admin user id
    mid = callback_query.message.message_id
    target = int(callback_query.data.split("-")[1])
    MessageToSend = callback_query.message.reply_to_message
    MessageToGetIdFrom = client.get_messages(adminUid,[MessageToSend.message_id])
    UserToSendId = re.findall(r'то(\d*)то', MessageToGetIdFrom[0].reply_to_message.text)[0]
    if not target:
        client.edit_message_text(chat_id = adminUid, message_id = mid, text = "ارسال نشد",reply_markup =[])
        return
    try:
        _tempUser = User.GetById(int(UserToSendId))
        UserToSendId = _tempUser.Uid
        if(MessageToSend.media):
            client.copy_message(chat_id = UserToSendId , from_chat_id = adminUid , message_id = MessageToSend.message_id, caption  = "admin🤙👽:\n" + str(MessageToSend.text or MessageToSend.caption))
        else:
            client.send_message(
                chat_id=UserToSendId,
                text="admin🤙👽:\n" + (MessageToSend.text or MessageToSend.caption),
                reply_markup = InlineKeyboardMarkup([
                    [InlineKeyboardButton(text="پاسخ",
                                        callback_data=CallBack.Get("UserContact"))]
                ]) if len(MessageToSend.text or MessageToSend.caption) > 15 else None
            )
        
        client.edit_message_text(chat_id = adminUid, message_id = mid, text = "ارسال شد",reply_markup =[])
    except Exception as e:
        raise e

#INBOX SHOW
@Client.on_callback_query(filters.regex(r'^'+CallBack.Get("GetInbox")+r'-\d$')
                            & customFilters.AdminPremission(Admin.Roles['Support']),group=CallBack.groupSetter())
def callBackMessageConfirm(client, callback_query):
    adminUid = callback_query.from_user.id # Admin user id
    mid = callback_query.message.message_id
    InboxResult = B_inbox.GetUnaswered()
    target = int(callback_query.data.split("-")[1])
    if len(InboxResult):
        MessageSorts = {}
        for InboxMessage in InboxResult:
            if InboxMessage.UserId not in MessageSorts.keys():
                MessageSorts[InboxMessage.UserId] = []
            MessageSorts[InboxMessage.UserId].append(InboxMessage)
        for kInboxMessage in MessageSorts:
            _user = User.GetById(kInboxMessage)
            client.send_message(
                chat_id = adminUid,
                text=config.Text_AdminNewMessage.format(
                        date = str(jdatetime.datetime.fromtimestamp(float(_user.Date))).split('.')[0],
                        uid = _user.Uid,
                        userId = kInboxMessage
                    ))
            for vInboxMessage in MessageSorts[kInboxMessage]:
                client.copy_message(
                    chat_id=adminUid,
                    from_chat_id=_user.Uid,
                    message_id=vInboxMessage.Mid
                )
    else:
        if(target):
            client.send_message(
                chat_id = adminUid,
                text=config.Text_AdminNoMessage,
                reply_markup = InlineKeyboardMarkup([
                    [InlineKeyboardButton(text="تلاش مجدد",
                                          callback_data=CallBack.Get("GetInbox","0"))]]
                )
            )
        else:
            client.edit_message_text(
                chat_id=adminUid,
                message_id=mid,
                text=config.Text_AdminNoMessage + str(random.choice(range(50))),
                reply_markup = InlineKeyboardMarkup(
                    [[InlineKeyboardButton(text="تلاش مجدد",
                                          callback_data=CallBack.Get("GetInbox","0"))]]
                )
            )
