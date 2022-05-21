import datetime
import time
from threading import Timer , Thread
import re

import random

import os
import base64
import io
import asyncio

import json
import html

from bottle import Bottle,static_file,template,request,BaseRequest
try:
    from pyrogram import Client , filters
    from pyrogram.types import InputMediaPhoto, InputMediaVideo , ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardMarkup,InlineKeyboardButton
    import jdatetime
    from pyrogram.raw.functions.messages import EditMessage
except ModuleNotFoundError:
    import os
    
    os.system("pip install pyrogram")
    os.system("pip3 install -U tgcrypto")
    os.system("pip install tinydb")
    os.system("pip install jdatetime")
    print("\n\n\n\n\n\n\n\n\n\n\nRestart the program")
    quit()

from plugins.errors import *
from plugins import config


from plugins.Modules import B_invite

from plugins.Modules import B_inbox

from plugins.Modules import B_category
from plugins.Modules import B_product
from plugins.Modules import B_photo

from plugins.Modules import B_about

import plugins.Modules.Models.M_error as error

from plugins.Modules.B_admin import *

from plugins.Modules import B_user
from plugins.Modules.Models.M_user import User


from plugins.Modules.E_stats import stat

import plugins.Modules.TG_Filters as customFilters

from plugins import CallBack

botPlugins = dict(root="plugins",exclude=["Modules"])
botClient = Client("ShopBot",api_id=2496,api_hash="8da85b0d5bfe62527e5b244c209159c3")

WebApplication = Bottle()
BaseRequest.MEMFILE_MAX = 1024 * 1024

UserInterface = lambda env,Text="",CallBackValue="" :{
    "Bootstrap":[
        [
            InlineKeyboardButton(
                config.Button_Showitems,
                callback_data=CallBack.Get("UserGetCategories")
            )
        ],
        [
            InlineKeyboardButton(
                config.Button_ContactUs,
                callback_data=CallBack.Get("UserContact")
            ),
            InlineKeyboardButton(
                config.Button_JoinChannel,
                url=config.URL_ChannelLink
            )
        ],
        [
            InlineKeyboardButton(
                config.Button_AboutOurService,
                callback_data=CallBack.Get("UserAbout")
            )
        ]
    ],
    
    "UserAbout":[
        InlineKeyboardButton(
            config.Button_AboutFAQ,
            callback_data=CallBack.Get("UserFAQ")
        ),
        InlineKeyboardButton(
            config.Button_AboutAStory,
            callback_data=CallBack.Get("UserMushroomHistory")
        ),
    ],

    }[env]

UserBackButton = lambda env,CallBackValue="":{
    "MainMenu" : [
        InlineKeyboardButton(
            config.Button_Back,
            callback_data=CallBack.Get("BackToMainMenu")
        )
    ],
    "Categories" : [
        InlineKeyboardButton(
            config.Button_Back,
            callback_data=CallBack.Get("UserGetCategories",1)
        )
    ],
    "Category" : [
        InlineKeyboardButton(
            config.Button_Back,
            callback_data = CallBack.Get("Showitems",CallBackValue)
        )
    ],
    "About" : [
        InlineKeyboardButton(
            config.Button_Back,
            callback_data = CallBack.Get("UserAbout")
        )
    ]
}[env]

AdminUIBackButtons = lambda env,CallBackValue="" : {
    "AdminManage" :
        [
            InlineKeyboardButton(
                config.Button_Back,
                callback_data=CallBack.Get("iiixz5")
            )
        ],
    "UserManage" :
        [
            InlineKeyboardButton(
                config.Button_Back,
                callback_data=CallBack.Get("imperator93")
            )
        ],
}[env]

def getUserUserInterface(client,message,Uid = 0):
    uid = message.from_user.id
    client.send_message(chat_id = Uid or uid,
        text=config.Text_userStart,
        reply_markup = InlineKeyboardMarkup(
            UserInterface("Bootstrap")
        )
    )

#######\#########/########
########\#######/#########
#########\Admin/##########
##########\###/###########
###########\#/############
#OPEN A USER , FUNCTION BOTH USED IN MESSAGE AND CALLBACK
def OpenUser(client,uid,adminUid):
    UserResult = B_user.GetByUid(uid)
    try:
        InviteId = B_invite.GetById(UserResult.InviteId).Title
    except:
        InviteId = UserResult.InviteId
    TextToSend = config.Text_SupremeUserView.format(
        Uid=str(UserResult.Uid),
        _id = str(UserResult.Id),
        InviteId =InviteId ,
        date = str(jdatetime.datetime.fromtimestamp(float(UserResult.Date))).split('.')[0],
        isDel = "🦴مسدود🦴" if UserResult.IsDel else "فعال")
    client.send_message(
            chat_id=adminUid,
            text=TextToSend,
            reply_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton(
                    config.Button_SupremeBanUser,
                    callback_data=CallBack.Get("imperator9",0,UserResult.Id)
                )],[
                InlineKeyboardButton(
                    config.Button_SupremeTalkieUser,
                    callback_data=CallBack.Get("imperatorTalkie",UserResult.Id)
                )
                ]
            ])
        )

#MESSAGE CONFIRM ANNOUNCEMENT
@botClient.on_message(filters.command("oc") & customFilters.AdminPremission(Roles['Supreme']))
def messageAdminAnnouncement(client,message):
    adminUid = message.from_user.id # Admin user id
    try:
        User = botClient.get_users(message.text.split(" ")[1])
    except:
        message.reply("USERNAME INVALID")
        return
    try:
        uid = B_user.GetByUid(User.id).Uid
    except E_NotFound:
        message.reply("این کاربر عضو ربات نیست")
    OpenUser(client,uid,adminUid)
    
#open user
@botClient.on_callback_query(filters.regex(r"^"+CallBack.Get("imperator93")+r"-\d*$")
                            & customFilters.AdminPremission(Roles["Supreme"]),group=CallBack.groupSetter())
def callBackSupremeUserManage(client,callback_query):
    Adminuid = callback_query.from_user.id # Admin user id
    mid = callback_query.message.message_id
    UidOfUser = int(callback_query.data.split("-")[1])
    OpenUser(client, UidOfUser,Adminuid)

#Set admin by username
@botClient.on_message(filters.regex(r"@.*") &
                    customFilters.AdminPremission(Roles["Supreme"],stat.AdminAdd))
def callBackSupremeCreateAdminFromUsername(client,message):
    Adminuid = message.from_user.id # Admin user id
    mid = message.message_id
    try:
        AdminToAdd = botClient.get_users([message.text])[0]
        if(AdminToAdd.is_self):
            client.send_message(chat_id = Adminuid,
                text="FUCKOFF BOOMER👽",
                reply_to_message_id = mid ,
                reply_markup = InlineKeyboardMarkup(
                    [AdminUIBackButtons("AdminManage")]
                )
            )
        try:
            AdminGet(AdminToAdd.id)
            client.send_message(chat_id = Adminuid,
                text="TRY ANOTHER✌️👽\nاین ادمین در سیستم وجود دارد",
                reply_to_message_id = mid ,
                reply_markup = InlineKeyboardMarkup(
                    [AdminUIBackButtons("AdminManage")]
                )
            )
            return
        except error.E_NotFound:
            _setAdmin = AdminSet(Admin(AdminToAdd.id,[Roles["None"]]))
            Admins[AdminIndex(Adminuid)].Status = stat.nothing
            client.send_message(chat_id = Adminuid,
                text="Success✌️👽\nبرای فعال شدن این ادمین ، نقش ایشان را انتخاب کنید",
                reply_to_message_id = mid,
                reply_markup = InlineKeyboardMarkup(
                    [[InlineKeyboardButton(
                        config.Button_SupremeAdminRole,
                        callback_data=CallBack.Get("iiixzr",str(AdminIndex(AdminToAdd.id))))
                    ]]
                )
            )
    except Exception as e:
        client.send_message(chat_id = Adminuid,
            text="آیدی مورد نظر پیدا نشد",
            reply_to_message_id = mid ,
            reply_markup = InlineKeyboardMarkup(
                [AdminUIBackButtons("AdminManage")]
            )
        )
        raise e

#Show user list
@botClient.on_callback_query(filters.regex(r"^"+CallBack.Get("Imperator93")+r"-\d-\d*-\d")
                            & customFilters.AdminPremission(Roles["Supreme"]))
def callBackSupremeUserList(client,callback_query):
    Adminuid = callback_query.from_user.id # Admin user id
    mid = callback_query.message.message_id
    target = int(callback_query.data.split("-")[1])
    pageNumber = int(callback_query.data.split("-")[2])
    InviteLinkId = int(callback_query.data.split("-")[3])
    
    if target==0:
        _listUsers = B_user.getAllBanned()
    elif target==1:
        _listUsers = B_user.getAll()
    elif InviteLinkId:
        _listUsers = B_user.getByInviteId(InviteLinkId)
    
    ListUsers = []
    _counter = 0
    try:
        for u in _listUsers[config.ListOffset * pageNumber:]:
            if _counter == config.ListOffset:
                break
            ListUsers.append(u.Uid)
            _counter+=1
    except Exception as e:
        client.edit_message_text(
            chat_id=Adminuid,
            message_id=mid,
            text="هیچ کاربری وجود ندارد",
            reply_markup = InlineKeyboardMarkup([AdminUIBackButtons("UserManage")])
        )
        raise e
        return
    
    ResultList = botClient.get_users(ListUsers)
    ResultText = ""
    ResultButtons = []
    _TempButtonContainer = []
    _counter = 1
    for user in ResultList:
        _TempButtonContainer.append(
            InlineKeyboardButton(
                str(_counter),
                callback_data=CallBack.Get("imperator93",user.id)
            )
        )
        if _counter % 3 == 0:
            ResultButtons.append(_TempButtonContainer)
            _TempButtonContainer = []
        ResultText += ("🤖" if user.is_bot else "🧙")
        ResultText += f"{str(_counter)}.[Profile:{user.first_name}](tg://user?id={str(user.id)})[{str(jdatetime.datetime.fromtimestamp(float(B_user.GetByUid(user.id).Date))).split('.')[0]}]\n"
        _counter += 1
    BackNForthButton = []
    IsLastPage = len(ResultButtons) < config.ListOffset
    
    if pageNumber != 0:
        BackNForthButton.append(
            [InlineKeyboardButton(
                "قبلی",
                callback_data=CallBack.Get(f"imperator93",str(target),str(pageNumber - 1))
            )]
        )
    elif not IsLastPage:
        BackNForthButton.append(
            [InlineKeyboardButton(
                "بعدی",
                callback_data=CallBack.Get(f"imperator93",str(target),str(pageNumber + 1))
            )]
        )
    
    client.edit_message_text(
        chat_id=Adminuid,
        message_id=mid,
        text=ResultText,
        reply_markup = InlineKeyboardMarkup(ResultButtons + BackNForthButton + [AdminUIBackButtons("UserManage")])
    )

def ShowAdminNoneRole(client,message):
    Adminuid = message.from_user.id
    client.send_message(chat_id = Adminuid,
        text="HI, U GOT NO ROLES AS AN ADMIN👽",
        reply_to_message_id = mid
    )

#ADMIN CMD Start
@botClient.on_message(filters.command("start")
                    & customFilters.AdminPremission(0))
def AdminCommandStart(client,message):
    Adminuid = message.from_user.id
    currentAdmin = AdminGet(Adminuid)

    LoginRoleKeyboards = { # ALL THE ROLES EXCEPt SUPREME
        Roles["Support"] : [KeyboardButton(config.Keyboard_OperatorSupport)],
        Roles["Supply"] : [KeyboardButton(config.Keyboard_Operatoritem)]
    }

    getUserUserInterface(client, message)
    
    OptionsToAttend = []
    for Role in currentAdmin.Role:
        if Role == Roles["Supreme"]:
            OptionsToAttend=[
                [KeyboardButton(config.Keyboard_Operatoritem)],
                [KeyboardButton(config.Keyboard_OperatorSupreme)],
                [KeyboardButton(config.Keyboard_OperatorSupport)]
            ]
            break
        else:
            OptionsToAttend.append(LoginRoleKeyboards[Role])
    client.send_message(chat_id = Adminuid,
        text=config.Text_AdminStart,
        reply_markup = ReplyKeyboardMarkup(OptionsToAttend+[[KeyboardButton(config.Keyboard_OperatorStart)]])
    )

###########/#\###########
##########/###\##########
#########/#USER\#########
########/#######\########
#######/#########\#######

#user /start
@botClient.on_message(filters.command("start"))
def commandUserStart(client,message) -> None:
    uid=message.from_user.id
    try:
        B_user.GetByUid(uid)
        getUserUserInterface(client, message)
        return
    except E_NotFound:
        try:
            InviteKey = message.command[1]
            CurrentInvite = B_invite.GetByKey(InviteKey)
        except IndexError:
            CurrentInvite = B_invite.Invite("")
            pass
        except E_NotFound:
            return
        B_user.SetUser(User(uid,CurrentInvite.Id))
    getUserUserInterface(client, message)

#callback user backToMainMenu , panel of User
@botClient.on_callback_query(filters.regex(r"^"+CallBack.Get("BackToMainMenu")))
def CallBackUasaearBackMainMenu(client,callback_query):
    getUserUserInterface(client, callback_query.message,callback_query.from_user.id)

#User get categories
@botClient.on_callback_query(filters.regex(r"^"+CallBack.Get("UserGetCategories")))
def callUserBackGetCategories(client, callback_query) -> None:
    uid = callback_query.from_user.id
    mid = callback_query.message.message_id
    try:
        target = int(callback_query.data.split("-")[1])
    except:
        target=None
        
    Categories = B_category.GetAll()
    replyButtons = []
    
    for Category in Categories:
        replyButtons.append(
            [
                InlineKeyboardButton(
                    Category.Title,
                    callback_data=CallBack.Get("Showitems",Category.Id)
                )
            ])
    Buttons=InlineKeyboardMarkup(replyButtons + [UserBackButton("MainMenu")] if len(replyButtons) else [UserBackButton("MainMenu")])
    if(not target):
        client.send_message(
            chat_id=uid,
            text=config.Text_userShowitems,
            reply_markup = Buttons
        )
    else:
        client.edit_message_text(
            chat_id=uid,
            message_id=mid,
            text=config.Text_userShowitems,
            reply_markup = Buttons
        )

#User InlineKeyboard get all produts of a Category
@botClient.on_callback_query(filters.regex(r'^'+CallBack.Get("Showitems") + "-\d*$"))
def callUserGetitems(client, callback_query) -> None:
    uid = callback_query.from_user.id
    mid = callback_query.message.message_id
    CategoryId = callback_query.data.split('-')[1]
    Products = B_product.GetByCategory(int(CategoryId))
    Category = B_category.GetById(int(CategoryId))
    replyButtons=[]
    for product in Products:
        replyButtons.append(
            [
                InlineKeyboardButton(
                    product.Title,
                    callback_data=CallBack.Get("Showitem",str(product.Id))
                )
            ])
    client.edit_message_text(chat_id = uid,
        message_id = mid,
        text=Category.Title,
        reply_markup = InlineKeyboardMarkup(replyButtons + [UserBackButton("Categories")])
    )

#User get Products
@botClient.on_callback_query(filters.regex(r'^'+CallBack.Get("Showitem") + r"-\d*$") and customFilters.UserFilter)
def callUserBackGetProducts(client, callback_query) -> None:
    uid = callback_query.from_user.id
    mid = callback_query.message.message_id
    productId = int(callback_query.data.split('-')[1])
    MediasToSend = []
    Product = B_product.GetById(productId)
    ProductImages = B_photo.GetByProductId(productId)
    try:
        AllProducts = B_product.GetByCategory(Product.CategoryId)
        NextPrevButton=[]
        RandomProduct = None
        for _Product in AllProducts:
            if(_Product.Id == Product.Id):
                try:
                    RandomProduct = AllProducts[AllProducts.index(_Product) + 1]
                except IndexError:
                    try:
                        RandomProduct = AllProducts[AllProducts.index(_Product) - 1]
                    except:
                        pass
        if RandomProduct:
            NextPrevButton.append(
                [
                    InlineKeyboardButton(
                        "محصول بعدی",
                        callback_data=CallBack.Get("Showitem",str(RandomProduct.Id))
                    )
                ]   
            )
        
        for Image in ProductImages:
            MediasToSend.append(
                [
                    InputMediaPhoto(
                        media=Image.FileId,
                        caption = "TTT" + str(random.choice(range(100)))
                    )
                ]
            )
        PhotoMessage = client.send_media_group(
            uid,
            [x[0] for x in MediasToSend],
            disable_notification=True,
            protect_content=True
        )
        SentMessage = client.send_message(chat_id = uid,
            text=config.Text_Signature.format(Text=Product.Description),
            reply_to_message_id = PhotoMessage[0].message_id,
            reply_markup = InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton(
                        config.Button_Shop,
                        callback_data=CallBack.Get("ُShopItem")
                    )
                ]]+
                [UserBackButton("Category",str(Product.CategoryId))] + NextPrevButton if NextPrevButton else UserBackButton("Category",str(Product.CategoryId))
            )
        )
        
    except Exception as e:
        raise e

#Purchase product
@botClient.on_callback_query(filters.regex(r'^'+CallBack.Get("ُShopItem")) and customFilters.UserFilter)
def callUserBackShopProduct(client, callback_query) -> None:
    uid = callback_query.from_user.id
    mid = callback_query.message.message_id
    client.edit_message_text(chat_id = uid,
            text=config.Text_Shop,
            message_id = mid,
            reply_markup = InlineKeyboardMarkup(
                [UserBackButton("Categories")]
            )
    )

#User about Us
@botClient.on_callback_query(filters.regex(r'^'+CallBack.Get("UserAbout")))
def callUserAboutUs(client, callback_query) -> None:
    uid = callback_query.from_user.id
    mid = callback_query.message.message_id
    client.edit_message_text(chat_id = uid,
        text=B_about.read(B_about.Address.About),
        message_id = mid,
        reply_markup = InlineKeyboardMarkup(
            [UserInterface("UserAbout")] +
            [UserBackButton("MainMenu")]
        )
    )

#User MUSHROOM HISTORY
@botClient.on_callback_query(filters.regex(r'^'+CallBack.Get("UserMushroomHistory")))
def callUserAboutUs(client, callback_query) -> None:
    uid = callback_query.from_user.id
    mid = callback_query.message.message_id
    client.edit_message_text(chat_id = uid,
        message_id = mid,
        text=B_about.read(B_about.Address.History),
        reply_markup = InlineKeyboardMarkup(
            [UserBackButton("MainMenu")]
        )
    )

#User about mushroom history
@botClient.on_callback_query(filters.regex(r'^'+CallBack.Get("UserMushroomHistory")))
def callUserMushroomHistory(client, callback_query) -> None:
    uid = callback_query.from_user.id
    mid = callback_query.message.message_id
    client.edit_message_text(chat_id = uid,
        message_id = mid,
        text=B_about.read(B_about.Address.History),
        reply_markup = InlineKeyboardMarkup(
            [UserBackButton("About")]
        )
    )

#User about FAQ
@botClient.on_callback_query(filters.regex(r'^'+CallBack.Get("UserFAQ")))
def callUserFAQ(client, callback_query) -> None:
    uid = callback_query.from_user.id
    mid = callback_query.message.message_id
    client.edit_message_text(chat_id = uid,
        text=B_about.read(B_about.Address.FAQ),
        message_id = mid,
        reply_markup = InlineKeyboardMarkup(
            [UserBackButton("About")]
        )
    )

#UserContact
@botClient.on_callback_query(filters.regex(r'^'+CallBack.Get("UserContact")))
def callBackUserContact(client, callback_query) -> None:
    uid = callback_query.from_user.id
    mid = callback_query.message.message_id
    client.send_message(chat_id = uid,
        text=config.Text_UserContact,
        reply_markup = InlineKeyboardMarkup(
            [UserBackButton("MainMenu")]
        )
    )

# ANSWER USER AFTER BOT FAKE TYPINGs OVER
_isConfirmedMessage = True
def sendCallSuccessFunction(uid):
    global _isConfirmedMessage
    if(_isConfirmedMessage):
        botClient.send_chat_action(uid, "cancel")
        botClient.send_message(chat_id = uid,text = "پیام شما ارسال شد✌️👽")
    _isConfirmedMessage = False
    return

#user contact message
@botClient.on_message(customFilters.UserTalk)
def messaegUserContact(client,message) -> None:
    uid=message.from_user.id
    mid = message.message_id
    try:
        _user = B_user.GetByUid(uid)
    except E_NotFound:
        try:
            AdminGet(uid)
            return
        except:
            client.send_message(
                chat_id = uid,
                reply_to_message_id = mid,
                text="USE /start"
            )
            return
    B_inbox.SetInbox(B_inbox.Inbox(mid, _user.Id))
    client.send_chat_action(uid, "typing")
    t = Timer(2.0, sendCallSuccessFunction , [uid])
    t.start()

#POST result object
def PreparePostResult(obj:object,isSuccess : bool = True) -> dict:
    return {
        "isSuccess" : isSuccess,
        "resultObject" : obj,
        "statusMessage" : obj
    }

#web CSS
@WebApplication.route('/css/<f>')
def GetWebStyleSheet(f):
    return static_file(f, root="static/css")

#web JS
@WebApplication.route('/js/<f>')
def GetWebStyleSheet(f):
    return static_file(f, root="static/js")

StaticImages = ["bg.jpg"]

#web IMAGES
@WebApplication.route('/img/<f>')
def GetWebStyleImage(f):
    return static_file(f, root="static/img")

#web FONT
@WebApplication.route('/font/<f>')
def GetWebStyleImage(f):
    return static_file(f, root="static/font")

#web POST photo
@WebApplication.post('/ppu')
def PostWebProductPhotoUpload():
    try:
        _image = base64.b64decode(request.json['Picture'])
        _imageio=io.BytesIO(_image)
        FileId = botClient.send_photo(chat_id=Admins[0].Uid,photo=_imageio).photo.file_id
        return PreparePostResult(FileId)
    except Exception as e:
        raise e
        return PreparePostResult(f"خطایی در ثبت تصویر به وجود آمده است \n {str(e)}",False)

async def DeleteTempPhoto():
    await asyncio.sleep(60)
    for file in os.listdir("static/img"):
        if(file not in StaticImages):
            os.remove("static/img/"+file)

#Get length offset of photos of a product
@WebApplication.post('/gil')
def PostWebProductPhotos():
    try:
        ProductId = int(request.json["ProductId"])
        ProductImages = B_photo.GetByProductId(ProductId)
        resultImages = []
        for image in ProductImages:
            try:
                filePath = botClient.download_media(image.FileId,file_name="static\img\\" + "".join(random.sample(["a","b","v","A","B","V"],3)) + ".jpg")
                photoName = filePath.split("\\")[-1]
                resultImages.append({"Name" : photoName,"Id" : image.Id})
                asyncio.create_task(DeleteTempPhoto)
            except:
                pass
        return PreparePostResult(resultImages)
    except Exception as e:
        raise e
        return PreparePostResult(str(e.args),False)

#web POST remove product image
@WebApplication.post('/gr')
def PostWebRemoveProductPhoto():
    try:
        PhotoId = int(request.json["PhotoId"])
        B_photo.remove(PhotoId)
        return PreparePostResult(True)
    except Exception as e:
        raise e
        return PreparePostResult(str(e.args),False)

#web POST add product
@WebApplication.post('/ap')
def PostWebAddProduct():
    try:
        setProduct = B_product.Set(B_product.Product(request.json['Title'],
                request.json['Description'],
                request.json['Price'],
                int(request.json['CategoryId']),
                int(request.json['Id'])))
        for photo in request.json['Photos']:
            B_photo.Set(B_photo.Photo(setProduct.Id, photo["FileId"]))
        return PreparePostResult(True)
    except Exception as e:
        raise e
        return PreparePostResult(f"خطایی در ثبت محصول به وجود آمده است \n {str(e)}",False)

#Add/edit product
@WebApplication.route('/add/<Id>')
def WebAddProduct(Id=0):
    try:
        Product = B_product.GetById(Id)
    except E_NotFound:
        Product = B_product.Product("", "", "", "")
    ViewModel = {
        "Product" : json.dumps(Product.getValues()),
        "Categories" : json.dumps([x.getValues() for x in B_category.GetAll() if not x.IsDeleted]),
        "ProductId" : Product.Id
    }
    return template("AddProduct",**ViewModel)

#List of products
@WebApplication.route('/pro')
def WebGetProducts():
    Products = B_product.GetAll()
    for Product in Products:
        Product.Date = str(jdatetime.datetime.fromtimestamp(float(Product.Date))).split('.')[0]
        Product.CategoryId = B_category.GetById(Product.Id).Title
        print(Product.Date)
    ViewModel = {
        "Products" : json.dumps([x.getValues() for x in Products])
    }
    return template("Product",**ViewModel)

#DELETE PRODUCT
@WebApplication.post('/pr')
def POSTWebDeleteProduct():
    try:
        Id = int(request.json["Id"])
        _product=B_product.GetById(Id)
        _product.IsDeleted = True
        B_product.Set(_product)
        return PreparePostResult(True)
    except Exception as e:
        raise e
        return PreparePostResult(f"خطایی در ثبت  متن به وجود آمده است \n {str(e)}",False)
#Change robot about
@WebApplication.post('/setabo')
def POSTWebAboutSet():
    try:
        Text = request.json["Text"]
        Type = B_about.Address.About if request.json["Target"] == "about" else B_about.Address.FAQ if request.json["Target"] == "FAQ" else B_about.Address.History
        B_about.Write(Text, Type)
    except Exception as e:
        raise e
        return PreparePostResult(f"خطایی در ثبت  متن به وجود آمده است \n {str(e)}",False)

#Change robot about
@WebApplication.route('/abo')
def WebAboutSetting():
    ViewModel = {
        "FAQText" : B_about.read(B_about.Address().FAQ),
        "AboutText" : B_about.read(B_about.Address().About),
        "HistoryText" : B_about.read(B_about.Address().History)
    }
    return template("about",**ViewModel)

@WebApplication.route('/')
def AddHome():
    return template("Home")

print("Client connected")
if __name__ == "__main__":
    #botClient.start()
    #me = botClient.get_me()
    print(config.TextMushroomArt["GoldenTeacher"].replace('`', ''))
    #WebApplication.run(host='localhost', port=80,reloader=True)
    Thread(target=WebApplication.run, daemon=True).start()
    botClient.run()
    #photo = botClient.send_photo(chat_id = "1575934389",photo=r'C:\Users\Hasan\Desktop\E05LPyLXsAMt1YC.png')
