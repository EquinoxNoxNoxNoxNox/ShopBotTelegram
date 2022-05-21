from .Models.M_about import Address,About
import os

Types={
    Address.About : About(Address.About),
    Address.FAQ : About(Address.FAQ),
    Address.History : About(Address.History)
}
for address in Types:
    with open(os.getcwd()+Types[address].Type,"r+",encoding="utf-8") as file:
        _text = ''
        for line in file.readlines():
            _text +=line
        if(_text):
            Types[address].Text=_text
        else:
            Types[address].Text = "\n🍄مجیک ماشروم ایران_ Magic Mushroom iran🍄\n@Magicmushroom_iran"

def Write(text:str,_type:Address):
    if(Types[_type].Text):
        Types[_type].Text = text
    with open(os.getcwd()+Types[_type].Type,"w+",encoding="utf-8") as file:
        file.write(text)

def read(_type:Address):
    if(Types[_type].Text):
        return Types[_type].Text
    res=""
    with open(os.getcwd()+Types[_type].Type,"r",encoding="utf-8") as file:
        for i in file.readlines():
            res+=i
    if(res):
        Types[_type].Text = res
        return res
    
    