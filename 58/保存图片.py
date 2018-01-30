import os
import requests
import csv


def getHtmlpic(url,headers):
    r=requests.get(url,headers=headers)
    r.raise_for_status()
    r.encoding=r.apparent_encoding
    return r.content
def main():
    path = '/Users/zangxiaojie/PycharmProjects/安居客/安居客jpg'
    if not os.path.exists(path):
        os.mkdir(path)
    with open('/Users/zangxiaojie/PycharmProjects/安居客/安居客第三版.csv','r') as f:
        reader = csv.DictReader(f)
        row = 1
        for x in reader:
            #print(x)
            #row = 1
            if x['default_photo']:
                #piclist = []
                piclist = x['default_photo'].split(',')
                id = 1
                #print(piclist)
                for picurl in piclist:
                    try:
                        headers = {
                            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Mobile Safari/537.36'
                        }
                        # id = 1
                        # print(id,row)
                        picture = getHtmlpic(picurl, headers)
                        #print(x)
                        pathpicdir = path + '/' + str(x['\ufeffid']) +'_' +x['house_id']
                        #print(1)
                        pathpic = pathpicdir + '/' + str(id) + '.jpg'
                        if not os.path.exists(pathpicdir):
                            os.mkdir(pathpicdir)
                        if not os.path.exists(pathpic):
                            with open(pathpic, 'wb') as pf:
                                pf.write(picture)
                                pf.close()
                                print('已保存第%d套房第%d张图' % (row, id))
                        id = id + 1
                    #print(picurl)
                    #print(1)

                    except Exception as e:
                        print(str(e))
                    # pass

                row += 1

        f.close()




main()