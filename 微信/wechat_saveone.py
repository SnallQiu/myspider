# -- coding: utf-8 --
# author: snall  time: 2018/2/26
from email.mime.text import MIMEText
from email import encoders
from email.header import Header
from email.utils import parseaddr, formataddr
import smtplib
import itchat
itchat.auto_login(hotReload=True)
@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):


    try:
        if msg['RecommendInfo']['RemarkName'] == '赵艳':
            print('有信息发来啦！')
            sendmail(msg['Text'])
    except:
        pass
def sendmail(text):
    smtp_server = 'smtp.163.com'
    msg = MIMEText(text, 'plain', 'utf-8')
    msg['Subject'] = Header('小猪猪来信息啦', 'utf-8').encode()
    server = smtplib.SMTP(smtp_server, 25, timeout=10)
    server.starttls()
    server.set_debuglevel(1)
    server.login('17854212463@163.com', 'qq345817576')
    server.sendmail('17854212463@163.com','17854212463@163.com', msg.as_string())
    server.quit()
itchat.run()


