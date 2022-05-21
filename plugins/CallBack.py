import random
import string

try:
    from pyrogram import Client , filters
    from pyrogram.types import InputMediaPhoto, InputMediaVideo , ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardMarkup,InlineKeyboardButton
except ModuleNotFoundError:
    import os
    os.system("pip install pyrogram")
    os.system("pip install tinydb")
    print("\n\n\n\n\n\n\n\n\n\n\nRestart the program")
    quit()

def _rcb():
    return ''.join([random.choice(string.ascii_letters) for x in range(3)])
_cbdb = dict()

#Get portal inline tag with parameter
def Get(keyName,*param):
    param = [str(x) for x in param]
    try:
        return _cbdb[keyName] + ("-" + "-".join(param) if param else "")
    except KeyError:
        _cbdb[keyName] = _rcb()
        return _cbdb[keyName] + ("-" + "-".join(param) if param else "")
GroupId=-1
def groupSetter(_=GroupId):
    global GroupId
    _+=1
    GroupId=1 if not _ else _
    return GroupId
