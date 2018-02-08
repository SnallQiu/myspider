# -- coding: utf-8 --

import itchat
from tuling import getresponse
'''
itchat.login()
friends = itchat.get_friends(update=True)
#print(friends)
male = female = other = 0
for i in friends[1:]:
    sex = i["Sex"]
    if sex==1:
        male += 1
    if sex ==2:
        female += 1
    else:
        other += 1
total = len(friends[1:])
print("男性好友比例：%.2f%%"%(float(male)/total*100))
print("女性好友比例：%.2f%%"%(float(female)/total*100))
'''
@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    print("snall的分身："+getresponse(msg['Text'])['text'])
    return "snall的分身："+getresponse(msg['Text'])['text']
itchat.login()
itchat.run()
