import jdatetime
URL_ChannelLink = "https://t.me/Magicmushroom_iran"
Project_Title = "SilkRoad"
BotUsername = "@KingShamanbot"
caption = "SilkRoad smartshop!⭐️⭐️⭐️⭐️⭐️🌿🍄\nربات فروشگاه silkroad معتبر ترین در ایران\nچطور میتونم کمکتون کنم؟\n"+BotUsername
ListOffset = 15

SellerUsername = "@silkroadadmin1"

Text_Signature = "{Text}\n\n\nفروشگاه تلگرامی SilkRoad \nکامل ترین و بهترین مرجع فروش پلیت و اسپان مجیک ماشروم\nوید و ال اس دی \nدی ام تی و آمفتامین."+BotUsername #+ "\n@" + URL_ChannelLink.split("/")[-1]

Button_Shop = "سفارش محصول🛒"
Text_userStart = u"Welcome to ["+ Project_Title +"]("+ f'http://t.me/{BotUsername}?start)\n' + caption
Text_userShowitems = u"دسته بندی محصولات\nبرای بازدید از موجودی روی دسته بندی مورد نظر کلیلک کنید"
Button_Back = u"بازگشت🔙"

IconAlien = "https://cdn4.vectorstock.com/i/1000x1000/83/53/alien-hugging-cat-cat-is-my-best-friend-cartoon-vector-34188353.jpg"
PhotoAlien = "https://mpng.subpng.com/20180415/fuw/kisspng-alien-drawing-artist-extraterrestrial-life-alien-5ad349c9179153.9936031615237964250965.jpg"

IconWizard = "https://64.media.tumblr.com/f754115e758b00040d95f34a14b15308/fbc3581c89c3ce9c-54/s500x750/a33d7248d7e298c0b9b3e6ed513b32cf05aa8fb3.png"
PhotoWizard = "https://pbs.twimg.com/media/E05LPyLXsAMt1YC.png"

TextMushroomArt = {"GoldenTeacher":
"```     _.._"+
"\n   .'    `."+
"\n .'        `."+
"\n.____________."+
"\n  `\"\"`  `\"\"'"+
"\n      '  '"+
"\nSILK_  :  :"+
"\nROAD   :  :"+
"\nBOT    ;  ;"+
"\n      .  ."+
"\n     '  ."+
"\n    '  ."+
"\n   .  ."+
"\n   ;  :"+
"\n  .    ."+
"\n '      ' ```"
,
"Panaelus":
"```         ,-."+
"\n       ,'   `."+
"\n     ,'       `."+
"\n   ,'           `."+
"\n ,'               `."+
"\n'___________________`"+
"\n         : :"+
"\n         : :"+
"\nSILK     ` `"+
"\nROAD      \ \\"+
"\nBOT        . ."+
"\n           ; ;"+
"\n          . ."+
"\n         . ."+
"\n         ; :"+
"\n        .   . ```"
,
# "semilanceata"
}
TextARTs={"CatInBox":"""```
\n  ,-.       _,---._ __  / \
\n /  )    .-'       `./ /   \
\n(  (   ,'            `/    /|
\n \  `-"             \'\   / |
\n  `.              ,  \ \ /  |
\n   /`*          ,'-`----Y   |
\n  (            ;        |   '
\n  |  ,-.    ,-'         |  /
\n  |  | (   |        357 | /
\n  )  |  \  `.___________|/
\n  `--'   `--'```""",
  "TwoAliens":"""```
\n       .-"\"""-.        .🎀"\""-.
\n      /        \      /        \\
\n     /_        _\    /_        _\\
\n    // \      / \\  // \      / \\\\
\n    |\__\    /__/|  |\__\    /__/|
\n     \    ||    /    \    ||    /
\n      \        /      \        /
\n       \  __  /        \  __  / 
\n        '.__.'          '.__.'
\n         |  |            |  |
\n357      |  |            |  |```""",
"GeoMetric":
"```            _____"+
"\n           /     \\"+
"\n          /       \\"+
"\n    ,----<         >----."+
"\n   /      \       /      \\"+
"\n  /        \_____/        \\"+
"\n  \        /     \        /"+
"\n   \      /       \      /"+
"\n    >----<         >----<"+
"\n   /      \       /      \\"+
"\n  /        \_____/        \\"+
"\n  \        /     \        /"+
"\n   \      /       \\      /"+
"\n    \\'----<         >----'"+
"\n          \       /"+
"\n           \_____/```"
}

Text_Shop =TextMushroomArt["GoldenTeacher"]+ "\n🧙📜برای ثبت سفارش محصول به آیدی زیر پیام بدید \n با بخش ارتباط با پشتیبانی تماس حاصل فرمایید \n" + SellerUsername 

def getAdminSignByRole(role : "Admin.Role"):
  return {0:"🦴",1:"😼⭐️" , 2:"🤙",3 :"🍬"}[int(role.Id)]

Text_AdminStart = TextMushroomArt["GoldenTeacher"] + f"\n Welcome to {Project_Title} admin panel.\nبرای ورود به بخش مورد نظر ، از دکمه های پائین استفاده کنید"

Text_AdminStartSupremeManagement = u"\nآمار ربات\nبرای دیدن آمار هر بخش کلیک کنید\n"+"🧙Users🧙 : {MembersCount}\n😼Categories😼 : {CategoryCount}\n🍬Items🍬 : {ItemsCount}\n👽Admins👽:{AdminCount}\n🐣Invites🐣:{InviteCount}"
Text_AdminAdd = TextARTs["GeoMetric"] + u"\ncontact or @username"

Button_Showitems = u"مشاهده محصولات"
Button_ContactUs = u"ارتباط با پشتبیانی"
Button_AboutOurService="درباره ی ما"
Button_JoinChannel = u"ورود به کانال"

Keyboard_Operatoritem = u"p1 💰مدیریت محصولات🍄"
Keyboard_OperatorSupport = u"p2 🤙پیام ها🛸"
Keyboard_OperatorSupreme = u"p3 📊آمار و پنل😼"
Keyboard_OperatorStart = "/start 👁‍🗨بازدید از ربات🧙"

Button_AboutFAQ="سوالات متداول"
Button_AboutAStory = "تاریخچه ماشروم"

Button_SupremeAdmins = u"👽ادمین ها👽"
Button_SupremeUsers = u"🧙کاربر ها🧙"

Text_Supreme5Admin = TextARTs["TwoAliens"] + """\n""" + """بخش مدیریت ادمین ها\n"""
Text_Supreme93AdminList = TextARTs["GeoMetric"] + """\n""" + """👽👽👽👽LIST\nهرکدام دارای نقش مجزا و سطح کاربری گوناگون هستند.\nبرای ورورد به جزئیات و اعمال تغییرات روی آیدی های زیر کلیک کنید"""
Text_Supreme93AdminRetrive = lambda role , uid: f"نقش های [این ادمین](tg://user?id={uid})\n{'و '.join([x.Title + getAdminSignByRole(x) for x in role if x.Id != 0]) or 'بدون نقش'}"
Text_SuccessAdminDelete = "ادمین با موفقیت حذف شد✌️👽🦴"
Text_SuccessAdminAdd = "ادمین با موفقیت اضافه شد✌️👽➕"

Text_Supreme5User = TextMushroomArt["Panaelus"] + "\nUSER List\n" + "بخش مدیریت کاربر ها"
Text_Supreme93AdminList = TextARTs["GeoMetric"] + """\n""" + """ADMIN LIST\n🧙📜هرکدام دارای نقش مجزا و سطح کاربری گوناگون هستند.\nبرای ورورد به جزئیات و اعمال تغییرات روی آیدی های زیر کلیک کنید"""

Button_SupremeAdminList = u"👽لیست ادمین ها👽"
Button_SupremeAdminAdd = u"👽➕افزودن ادمین جدید➕👽"
Button_SupremeAdminDelete = u"👽🦴حذف🦴👽"
Button_SupremeAdminRole = u"👽🎭نقش🎭👽"
Button_Supreme93iixz = u"👽🍬مدیریت🍬👽"

Text_AnnouncementNotif = u"پیامی که میخواهید به تمام کاربر ها فرستاده شود را ارسال کنید ، دقت داشته باشید که این پیام شما را تمام کاربر های فعال ربات دریافت خواهند کرد و غیر قابل حذف و تغییر میباشد"

Button_Confirm = u"تائید"

Button_SupremeBanUser = u"🧙🦴بن کردن کاربر🦴🧙"
Button_SupremeTalkieUser = u"🧙🔊صحبت با کاربر🔊🧙"
Button_SupremeUserManagement = "🧙🧙مدیریت کاربران🧙🧙"
Button_SupremeActiveUserList = u"🧙❤️لیست کاربر های فعال❤️🧙"
Button_SupremeBanUserList = u"🧙🦴لیست کاربر های مسدود🦴🧙"
Button_SupremeAnnouncement = u"🔊ارسال اطلاعیه🔊"
Button_SupremeAdvertisement = u"⭐️تبلیغات⭐️"
Text_SupremeUserListText = u"🧙📜در این بخش میتوانید لیست کاربر های ربات را ببینید و بر روی دسترسی آنها تغییراتی اعمال کنید \n توجه داشته باشید که این لیست با توجه به تاریخ عضویت دسته بندی شده است. از جدید به قدیم\nSHORTCUT : /oc @[Username]"
Text_SupremeUserBanText = u"🧙📜کاربر مسدود دیگر نمیتواند هیچ استفاده از ربات داشته باشد\n آیا از مسدود کردن کاربر مطمئن هستید؟"
Text_SupremeUserBanConfirmText = u"کاربر با موفقیت مسدود شد🧙🦴"
Text_SupremeUserView = u"[🧙مشخصات کاربر](tg://user?id={Uid})\nوضعیت 💓: {isDel}\nتاریخ عضویت 🗓: {date}\nمعرفی شده توسط 🐣: {InviteId}\nآیدی 🆔: {_id}"
Text_SupportPanel = "به پنل پشتیبانی مشتریان خوش آمدید🤙🛸"
Button_Inbox = u"📬صندوق پیام های دریافتی📫"
Text_AdminNewMessage = "#TALKIE\n{date}\nFrom : [This guy](tg://user?id={uid})\nUser Id:то{userId}то\n🖖🖖🖖برای پاسخ به کاربر ، روی این مسیج reply کنید🖖🖖🖖"

Text_AdminNoMessage = u"چیزی در صندوق وجود ندارد ، چند دقیقه دیگه دکمه تلاش مجدد رو بزن 📫🦴"
Text_AdminTalkieConnect = "#TALKIE🤙[This guy](tg://user?id={uid})\nUser Id:то{userId}то\nروی این پیام reply کنید تا پیام شما دست کاربر برسد"
Text_FileInvalid = u"این مدل فایل فرستاده نمیشود ، چون حاجیم اینجوری درستم کرده🦴"
#Button_Supreme3iixz = u""

Link_invite = lambda x:f"`http://t.me/{BotUsername}?start={x}`"

Text_InviteMenu = u"لینک عضویت یا پورتال ورودی ربات \n قابلیتی است که با استفاده از آن میتوانید تعداد ورودی های ربات را زیر نظر داشته باشید\nدر صورت کار نکردن دکمه ها ، از دستور زیر استفاده کنید : \n /CreateInvite برای ساخت لینک \n /Invites دیدن لینک های موجود"
Text_InviteAdd = u"لطفا عنوان لینک رو بفرستید\nمثال : AVACADO GP\nFirst Portal\nYOUSIFAMIR LUXURY"
Text_InviteConfirm = "آیا از ثبت این عنوان مطمئن هستید؟"
Text_InviteSuccess = "با موفقیت ثبت شد\n`http://t.me/"+BotUsername+"?start={Key}`"

Text_Invites = lambda ListInv:"".join([ "[" + str(jdatetime.datetime.fromtimestamp(x.Date)).split('.')[0] + "]\nMEMBERS:🧙" + str(y) +"🧙" + "\nTitle:" +  x.Title + "\nLink:" + Link_invite(x.InviteKey) for x,y in ListInv])

Button_Invite = "🐣لینک عضویت🐣"
Button_InviteAdd = "اضافه کردن لینک عضویت+🐣"
Button_InviteLinkList = "مدیریت لینک ها👉🐣"
Text_InviteLinkExpire = "لینک عضویت شما از بین رفته است"
Text_InviteLinkInvalid = "لینک عضویت شما فاقد اعتبار میباشد"
Text_InviteLinkNeed = "برای ورود به ربات نیاز به لینک عضویت دارید"

Text_SupplyPanel = "🍄🍬Supply management\nبخش مدیریت و دسته بندی محصولات\n.\n.\n."
Text_SupplyCategory ="دسته بندی های فعال با 🔆 نمایش داده میشود"#🌚
Text_SupplyCategoryAddSuccess = "🍄دسته بندی با موفقیت اضافه شد"
Text_SupplyCategoryAdd = "عنوان دسته بندی را وارد کنید"
Button_SupplyCategory = "مدیریت دسته بندی ها🍬"
Button_SupplyAddCategory = "اضافه کردن+🍬"
Button_SupplyRemoveCategory = "حذف"

Button_CategoryDelete = "حذف دسته بندی"
Text_CategoryDelete = "در این بخش میتوانید دسته بندی ها را فعال و غیر فعال کنید\nبا کلیک کردن روی کلمه مورد نظر"
Text_CategoryDeleteSuccess = "با موفقیت انجام شد"

Text_UserContact = "#INBOX🧙🤙\nپیام خود را روی این مسیج reply کنید"