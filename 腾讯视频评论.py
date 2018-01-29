# -- coding: utf-8 --
# author: snall  time: 2018/1/8


import requests
import re
def getHtmlText(url):
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',

    }
    r=requests.get(url,headers=headers)
    r.raise_for_status()
    r.encoding=r.apparent_encoding
    return r.text
def getcomment(userid,data):
    with open('国家宝藏腾讯视频评论.txt','a') as f:
        for i in range(len(userid)):
            try:
                # print(i)
                comment = eval('u"' + userid[i][1] + '"')
                nick = eval(
                    'u"' + re.search('"userid":"{}","nick":"(.*?)"'.format(int(userid[i][0])), data).group(1) + '"')
                # nick = re.search('"userid":"{}","nick":"(.*?)"'.format(int(userid[i][0])), data).group(1)
                # print("-------------------分割线-------------------")
                print('%s : %s' % (nick, comment))
                f.writelines('%s : %s\n' % (nick, comment))
                print("-------------------分割线-------------------")

            except:
                pass
    f.close()



def pageinfo(commentid):
    vid = '2344132955'

    url = 'https://video.coral.qq.com/varticle/' + vid +\
          '/comment/v2?callback=jQuery112407056568032817538_1515417350329&orinum=10&oriorder=o&pageflag=1&cursor='\
          +commentid+'&scorecursor=0&orirepnum=2&reporder=o&reppageflag=1&source=9&_=1515417350331HTTP/1.1'
    data = getHtmlText(url)
    userid = re.compile('"userid":"(\d*)","content":"(.*?)"').findall(data)
    lastid = re.compile('"last":"(\d*)"').findall(data)[0]
    #print(data)
    #print(userid)
    getcomment(userid,data)
    return lastid


def main():
    commentid = '6355794464040770578'
    for i in range(int(input('请输入要爬取的评论页面数：'))):
        commentid = pageinfo(commentid)





    pass


main()





'''
https://video.coral.qq.com/
/varticle/2292665416/comment/v2?callback=jQuery112406324952002971012_1515412817600&orinum=10&oriorder=o&pageflag=1&cursor=6346680114453423483&scorecursor=0&orirepnum=2&reporder=o&reppageflag=1&source=9&_=1515412817602%20HTTP/1.1
/varticle/2292665416/comment/v2?callback=jQuery112405689483337122796_1515413724555&orinum=10&oriorder=o&pageflag=1&cursor=6348410629216806385&scorecursor=0&orirepnum=2&reporder=o&reppageflag=1&source=9&_=1515413724559 HTTP/1.1
/varticle/2292665416/comment/v2?callback=jQuery112405689483337122796_1515413724555&orinum=10&oriorder=o&pageflag=1&cursor=6354468489109450047&scorecursor=0&orirepnum=2&reporder=o&reppageflag=1&source=9&_=1515413724560 HTTP/1.1
'''