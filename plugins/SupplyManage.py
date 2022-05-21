import re
from pyrogram import Client , filters
from pyrogram.types import InputMediaPhoto, InputMediaVideo , ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardMarkup,InlineKeyboardButton
from pyrogram.handlers import CallbackQueryHandler
import plugins.Modules.TG_Filters as customFilters
from .Modules import B_admin as Admin
from .Modules import B_category
from .Modules.Models.M_category import Category
from .Modules.E_stats import stat
from . import CallBack
from . import config


AdminUIBackButtons = lambda env,CallBackValue="" : {
    "MainSupplyMenu" : [
        InlineKeyboardButton(
            config.Button_Back,
            callback_data=CallBack.Get("backToP") + "1"
        )
    ],
    "CategoryManagement":[
        InlineKeyboardButton(
            config.Button_Back,
            callback_data=CallBack.Get("CategoryManage")
        )
    ],
    "DeleteCategory":[
        InlineKeyboardButton(
            config.Button_Back,
            callback_data=CallBack.Get("DeleteCategory")
        )
    ]
}[env]

AdminUserInterface = lambda env,role,CallBackValue="" : {
    "CategoryManagement" : {
        Admin.Roles["Supreme"] : [
            [
                InlineKeyboardButton(
                    config.Button_SupplyAddCategory,
                    callback_data=CallBack.Get("CategoryAdd")
                )
            ],
            [
                InlineKeyboardButton(
                    config.Button_CategoryDelete,
                    callback_data=CallBack.Get("DeleteCategory")
                )
            ],
        ]
    }[role]
}[env]

#Category management
@Client.on_callback_query(filters.regex(CallBack.Get("CategoryManage")) & customFilters.AdminPremission(Admin.Roles["Supreme"]),group = CallBack.groupSetter())
def message_AdminProductCategories(client,callback_query):
    adminUid = callback_query.from_user.id # Admin user id
    mid = callback_query.message.message_id
    Categories = B_category.GetAll(True)
    Text_ToSend = ""
    Admin.Admins[Admin.AdminIndex(adminUid)].Status = stat.nothing
    for category in Categories:
        Text_ToSend += f"{'🔴 ' if category.IsDeleted else '✅ '}{category.Id}.{category.Title}\n🔆🌀🔆🌀🔆🌀🔆\n"
    client.edit_message_text(
        chat_id = adminUid,
        text = Text_ToSend or "NO CATEGORIES",
        message_id = mid,
        reply_markup = InlineKeyboardMarkup(AdminUserInterface("CategoryManagement",Admin.Roles["Supreme"]) + [AdminUIBackButtons("MainSupplyMenu")])
    )

#CATEGORY TITLE MESSAGE
@Client.on_message(customFilters.AdminPremission(Admin.Roles["Supreme"],stat.CategoryAdd))
def messageAdminProductCategoryTitle(client,message):
    adminUid = message.from_user.id # Admin user id
    mid = message.message_id
    client.send_message(
        chat_id = adminUid,
        text = "آیا از ثبت کردن این عنوان مطمئن هستید؟",
        reply_to_message_id = mid,
        reply_markup = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "ثبت",
                        callback_data=CallBack.Get("SumbitCategory","1")
                    )
                ],
                [
                    InlineKeyboardButton(
                        "لغو",
                        callback_data=CallBack.Get("SumbitCategory","0")
                    )
                ]
            ])
    )

#Submit button on title message
@Client.on_callback_query(filters.regex(CallBack.Get("SumbitCategory") + "-\d") & customFilters.AdminPremission(Admin.Roles["Supreme"]),group = CallBack.groupSetter())
def messageAdminCategorySubmit(client,callback_query):
    adminUid = callback_query.from_user.id # Admin user id
    mid = callback_query.message.message_id
    Admin.Admins[Admin.AdminIndex(adminUid)].Status = stat.nothing
    target = int(callback_query.data.split("-")[1])
    if target:
        B_category.Set(Category(callback_query.message.reply_to_message.text))
        client.edit_message_text(
            chat_id = adminUid,
            message_id = mid,
            text = config.Text_SupplyCategoryAddSuccess,
            reply_markup = InlineKeyboardMarkup([AdminUIBackButtons("CategoryManagement")])
        )
    else:
        client.edit_message_text(
            chat_id = adminUid,
            message_id = mid,
            text = 'لغو شد',
            reply_markup = InlineKeyboardMarkup([AdminUIBackButtons("CategoryManagement")])
        )
#ADD CATEGORY CALLBACK
@Client.on_callback_query(filters.regex(CallBack.Get("CategoryAdd")) & customFilters.AdminPremission(Admin.Roles["Supreme"]),group = CallBack.groupSetter())
def callBackAdminProductCategoryAdd(client,callback_query): 
    adminUid = callback_query.from_user.id # Admin user id
    mid = callback_query.message.message_id
    Admin.Admins[Admin.AdminIndex(adminUid)].Status = stat.CategoryAdd
    client.edit_message_text(
        chat_id = adminUid,
        message_id = mid,
        text = config.Text_SupplyCategoryAdd,
        reply_markup = InlineKeyboardMarkup([AdminUIBackButtons("CategoryManagement")])
    )

#DELETE CATEGORY CALLBACK
@Client.on_callback_query(filters.regex(CallBack.Get("DeleteCategory")) &
    customFilters.AdminPremission(Admin.Roles["Supreme"]),group = CallBack.groupSetter())
def callBackAdminProductCategoryAdd(client,callback_query):
    adminUid = callback_query.from_user.id # Admin user id
    mid = callback_query.message.message_id
    Buttons = []
    for cat in B_category.GetAll(isAll=True):
        Buttons.append([
            InlineKeyboardButton(
                cat.Title,
                callback_data=CallBack.Get("DeleteACategory",cat.Id)
            )
        ])
    client.edit_message_text(
        chat_id = adminUid,
        message_id = mid,
        text = config.Text_CategoryDelete,
        reply_markup = InlineKeyboardMarkup(Buttons + [AdminUIBackButtons("CategoryManagement")])
    )

#Delete a category
@Client.on_callback_query(filters.regex(r"^" + CallBack.Get("DeleteACategory") + "-\d*$") &
    customFilters.AdminPremission(Admin.Roles["Supreme"]),group = CallBack.groupSetter())
def messageDeleteCategory(client,callback_query):
    adminUid = callback_query.from_user.id # Admin user id
    mid = callback_query.message.message_id
    IdToDelete = int(callback_query.data.split("-")[1])
    Category = B_category.GetById(IdToDelete)
    Category.IsDeleted = True if not Category.IsDeleted else False
    B_category.Set(Category)
    client.edit_message_text(
        chat_id = adminUid,
        message_id = mid,
        text = config.Text_CategoryDeleteSuccess,
        reply_markup = InlineKeyboardMarkup([AdminUIBackButtons("CategoryManagement")])
    )