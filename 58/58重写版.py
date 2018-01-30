# -- coding: utf-8 --

import requests
import os
import re
import codecs
import random
import time
import csv
from bs4 import BeautifulSoup
import json
from urllib.request import urlopen, quote
import requests
def getlnglat(address):
    url = 'http://api.map.baidu.com/geocoder/v2/'
    output = 'json'
    ak = 'CFP87YVGgB6bup8BGNoY9IIsSeVI0uNP'
    add = quote(address) #由于本文地址变量为中文，为防止乱码，先用quote进行编码
    uri = url + '?' + 'address=' + add  + '&output=' + output + '&ak=' + ak
    req = urlopen(uri)
    res = req.read().decode()
    temp = json.loads(res)
    lat=temp['result']['location']['lat']
    lng=temp['result']['location']['lng']
    return lat,lng
import urllib

def getHtmlText(url,headers,**proxies):
    #print(url)
    r=requests.get(url,headers=headers,proxies = proxies)
    r.raise_for_status()
    r.encoding=r.apparent_encoding
    return r.text

def getHtmlpic(url,headers):
    r=requests.get(url,headers=headers)
    r.raise_for_status()
    r.encoding=r.apparent_encoding
    return r.content



def gethouseurl(html):
    soup = BeautifulSoup(html,'html.parser')
    list = []
    #print(soup)
    list_info = soup.find_all('div',attrs={'class':'list-info'})#,attrs={'class':'list-info'})
    #print(list_info)
    for div in list_info:
        #print(div)
        #print(div.find('h2').find('a'))
        list.append(div.find('a').get('href'))

    return list
def gettelphone(url,**proxies):
    headers = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    htmltp = getHtmlText(url,headers = headers,proxies = proxies)
    #print(htmltp)
    soup = BeautifulSoup(htmltp,'html.parser')
    tel = soup.find('p',attrs={'class':'phone-num'}).text
    return tel



def getinformation(houseurlhtml,phonenumber,id,save_path):
    soup = BeautifulSoup(houseurlhtml,'html.parser')
    #print(soup)
    #print(soup)
    '''得到标题'''
    try:
        title = soup.find('title').text.split('-',1)[0]#[0].split('】')[1]#.strip()
    except:
        title = soup.find('title').text
    '''得到区块#市北'''
    meta = soup.find('meta',attrs= {'name':'description'})
    #block_area = meta.get('content').strip().split('-')[1].strip()
    block_area = '其他'
    try:#将不能用'——'分割的地区分割出来
        block_area = meta.get('content').strip().split('-')[1].strip()

        if block_area.split(',')[1]:
            #print(block_area)
            block_area = block_area.split(',')[0].strip()


    except:
        #print(block_area)
        pass
    '''得到block-name #市北家乐福'''
    li = soup.find('li',attrs = {'class':'address-info'})
    try:
        block_name = li.text.split('-')[-1].strip()
        #print(block_name)
    except Exception as e:#这里要改 没有block—name的要默认一个东西
        block_name = '其他'
        #print(str(e))
        pass

    '''得到comminuty_name #海湾花园'''
    dist_title = soup.find('h2',attrs = {'class':'dist-title'})
    comminuty_name = '其他'
    try:
        comminuty_name = dist_title.text.split('：')[-1].strip()
        #print(comminuty_name)
        try:
            comminuty_name = comminuty_name.split(' ')[0]
            #print(comminuty_name)
        except:
            #print(comminuty_name)
            pass
    except:
        pass










    '''得到核心卖点'''
    try:
        maidian = soup.find('section',attrs = {'class':'desc-section'}).find('p').text.strip()
    except:
        pass


    '''得到售价户型面积'''
    try:
        area = 100.0
        price = 100
        soupsize = soup.find('div', attrs={'class': 'size-bar'})
        #print(soup)
        #print(soupsize)
        sizeinfo = soupsize.find_all('p', attrs={'class': 'item-value'})
        price, house_type, area = sizeinfo
        price, house_type, area = price.text, house_type.text, area.text
        price = int(re.search(r'\d+',price).group(0))
        area = float('%.2f'%(float(re.search(r'\d+', area).group(0))))
        while price>1000:
            price /=10

    except Exception as e:
        #print(str(e))
        pass

    #print(price,house_type,area)
    '''得到几室几厅几卫信息返回一个列表'''
    try:
        room_num = int(re.findall(r'\d',house_type)[0])
        hall_num = int(re.findall(r'\d',house_type)[1])
        toilet_num = int(re.findall(r'\d',house_type)[2])

    except:
        room_num = 1
        hall_num = 1
        toilet_num = 1
        pass#这里输入如果爬不到信息的默认值


    '''得到单价，发布'''
    floor = []
    try:
        detail_table = soup.find('table', attrs={'class': 'detail-table'})
        detail_value = detail_table.find_all('span', attrs={'class': 'detail-value'})
        unit_price, times, *floor = detail_value
        unit_price, times = unit_price.text, times.text
        unit_price = int(re.search(r'\d+', unit_price).group(0))
    except:
        pass

    '''得到总楼层'''
    try:
        if floor[0]:
            floor_total = floor[0].text.split('/')[-1]
            flt = re.search(r'\d+', floor_total).group(0)
            flt = int(flt)


        else:
            flt = 10

    except:
        pass
        #flt = 10#如果没有得到总楼层，返回默认值10
        #fln = 5#如果没有得到总楼层，返回默认值当前楼层5
    '''得到房屋所在楼层'''
    try:
        if floor[0]:
            floor_num = floor[0].text.split('/')[0]
            n1 = 0
            fln = 5
            filterff = filter(str.isdigit, floor_num)
            if filterff:
                for fti in filterff:  # 这里floor_total返回的是str
                    n1 = n1 + 1
                    if n1 == 1:
                        fln = fti
                    if n1 == 2:
                        fln = fln + fti
            if floor_num == '底层':
                fln = int(flt) * 0.1
            if floor_num == '中层':
                fln = int(flt) * 0.5
            if floor_num == '高层':
                fln = int(flt) * 0.8
            fln = int(fln)
        else:
            fln = 5


    except Exception as e:
        pass
        #print(str(e))
        #fln = 5  # 如果没有得到总楼层，返回默认值当前楼层5
    '''得到house_ori,house_age,fitment_type'''
    house_ori = '南'
    fitment_type = '简单装修'
    houseSource_type = '多层住宅'
    try:
        soupdetail_value = soup.find('table',attrs = {'class':'detail-table'})
        for xx in soupdetail_value.find_all('td'):

            if re.match(r'^.{2}',xx.text).group(0) == '装修':
                fitment_type = xx.find('span',attrs = {'class':'detail-value'}).text

            if re.match(r'^.{2}',xx.text).group(0) == '类型':
                #print('11111')
                houseSource_type = xx.find('span',attrs = {'class':'detail-value'}).text





    except:
        pass


    house_age = None
    if floor[1:]:
        try:
            house_ori = floor[1].text
        except:
            pass
        try:
            house_age = re.search(r'\d{4}',floor[4].text[:-1]).group(0)#得到类似2007
        except:
            pass
    '''得到联系人姓名和联系方式'''
    #print(soup)
    try:
        owener = soup.find('h2',attrs = {'class':'agent-title'}).text
    except:
        owener = '青岛'
    #联系方式在另一个函数给出并已经带进来了




    '''得到图片的地址'''
    souppic = soup.find_all('div',attrs= {'class':'swiper-slide'})
    picurllist = []
    for i in souppic:#得到每套房的图片url保存成列表
        picurllist.append(i.find('div')['bg-src'])
    picurls = ','.join(picurllist)
    block_id = '00'
    '''获得house_id'''
    if block_area =='市北':
        block_id = '02'
    if block_area =='市南':
        block_id = '01'
    if block_area =='四方':
        block_id = '03'
    if block_area =='崂山':
        block_id = '04'
    if block_area =='李沧':
        block_id = '05'
    if block_area =='城阳':
        block_id = '06'
    if block_area =='黄岛':
        block_id = '07'
    if block_area =='即墨':
        block_id = '08'
    if block_area =='胶南':
        block_id = '09'
    if block_area =='胶州':
        block_id = '10'
    day_time = time.strftime('%m%d',time.localtime(time.time()))[1:]
    if round(area)>=100&round(area)<1000:
        house_id = day_time + block_id + str(round(area))
    if round(area)<100:
        house_id = day_time + block_id + '0' + str(round(area))


    #print(house_id)
    '''得到经纬度'''
    detailaddress = '青岛市'+block_name
    lat,lng = getlnglat(detailaddress)








    #print(souppic)

    #print(soup)

    '''
    #print(soup)
    print(block_area)
    print(block_name)
    print(comminuty_name)
    print(title)
    print(price)
    print(unit_price)
    print(room_num,hall_num,toilet_num)
    print(area)
    print(picurls)
    print(flt, fln)
    print(house_ori, fitment_type, house_age)
    print(owener)
    print(phonenumber)
    print(maidian)
    print(houseSource_type)



    print('###############################')
    '''

    '''输出到csv文件'''
    a = 'id	house_id city_id	area_name	area_id	block_id	block_name	community_id	community_name	title_name	price	avg_price	room_num	hall_num	toilet_num	area_num	address	default_photo	floor_total	floor_num	house_age	house_ori	tags	owner	owner_tel	source_type	property_rights	commition_type	lat	lng	isFive_only	fitment_type	equipment	property	status	follow_up_time	outlet	borkers	brokerTel	houseSource_type	owner_type	street	house_number	registration_date	confidentialityRemarks	inputUser	deliveryTime	fangChanNum	garageRemarks	keyNumber	key	structure	garage	traffic_condition	paymentMethod	seeTheApartmentMethod	price_condition	description	is_intermediary	user_id	nick_name	belong	release_time	cityName	modelImg'
    column_name = a.split()
    try:
        with codecs.open(save_path, 'a', 'utf_8_sig') as csvfile:
            writer = csv.DictWriter(csvfile, column_name)
            #print(writer)
            writer.writerow(
                {'id': id, 'area_name': block_area, 'block_name': block_name, 'community_name': comminuty_name,
                 'title_name': title, 'price': price, 'avg_price': unit_price, 'room_num': room_num,
                 'hall_num': hall_num, 'toilet_num': toilet_num, 'area_num': area, 'default_photo': picurls,
                 'floor_total': flt, 'floor_num': fln, 'house_age': house_age, 'house_ori': house_ori,
                 'fitment_type': fitment_type, 'owner': owener, 'owner_tel': phonenumber, 'description': maidian , 'property_rights':'个人产权',
                 'property':'公盘' , 'status':'正常' , 'owner_type':'A类客户' , 'houseSource_type':houseSource_type,
                 'paymentMethod':'可按揭' , 'seeTheApartmentMethod':'随时', 'price_condition':'一口价', 'is_intermediary':'NO' , 'outlet':'总店' , 'cityName':'青岛', 'city_id':'1',
                 'house_id':int(house_id) , 'area_id':str(int(block_id)) , 'lat':lat , 'lng':lng
                 })

            csvfile.close()
        return 1
    except Exception as ee:
        pass
        #print(str(ee))


def main():
    url = 'http://qd.58.com/ershoufang/0/'
    #proxies = {'http':'http://183.136.218.253:80'}
    save_path = '1_29.csv'
    headers = {
        'cookie':'id58=c5/nn1cyrfxaSXWdDM0hAg==; city=qd; 58home=qd; commontopbar_myfeet_tooltip=end; als=0; wmda_uuid=c105496b9799caa8ba7f2237ee1476d4; wmda_new_uuid=1; wmda_visited_projects=%3B2385390625025; UM_distinctid=1602555ec271f0-0c9c7d3cef277e-3062750a-100200-1602555ec28ac2; commontopbar_ipcity=qd%7C%E9%9D%92%E5%B2%9B%7C0; sessionid=e8d6036c-d279-4e92-975a-b7caeb64cc71; cookieuid=0ffb82b2-58c3-40fe-984a-656d3cc81d7a; ishome=true; m58comvp=t07v115.159.229.13; hasLaunchPage=%7Cindex%7C; launchFlag=1; cityexit=true; from=""; device=m; qz_gdt=; 58cooper="userid=52010993422607&username=xyvf2tr53&cooperkey=7fb9308fc1bdde4d95bce900c2245543"; www58com="AutoLogin=false&UserID=52010993422607&UserName=xyvf2tr53&CityID=0&Email=&AllMsgTotal=0&CommentReadTotal=0&CommentUnReadTotal=0&MsgReadTotal=0&MsgUnReadTotal=0&RequireFriendReadTotal=0&RequireFriendUnReadTotal=0&SystemReadTotal=0&SystemUnReadTotal=0&UserCredit=0&UserScore=0&PurviewID=&IsAgency=false&Agencys=null&SiteKey=6132DEA395E09C43A8BDF20109DD2DAF3DC98380B37DE7A9E&Phone=&WltUrl=&UserLoginVer=1FC200CCC2CA2C7E903947073BC7E29EC&LT=1512617543074"; ppStore_fingerprint=E2F6CD5E2BE794A5CAAC7435D77234E2B53FE9260AA74603%EF%BC%BF1512617543157; 58tj_uuid=2367da5c-d2dd-4e06-a880-2e56f126c728; new_session=0; new_uv=7; utm_source=; spm=; init_refer=http%253A%252F%252Fm.58.com%252Ferschoufang%252F0%252Fpn69%252F%253Freform%253Dpcfront; commontopbar_new_city_info=122%7C%E9%9D%92%E5%B2%9B%7Cqd; PPU="UID=52010993422607&UN=xyvf2tr53&TT=6f48ada2de075b43b78a2ef6f7ef05ed&PBODY=Ui0AUTmOflOMq2jgJ1B5NT_mTq90K9Zfgvylh0R-XNU-2nQplRddiWbIkkGw6apVys-iIPjylBtgmpuaSo02gjg-pKE6LBj6GVJXq7KcdV3V6IJd-yFrrbGIgasewZqcueVfm-gufAcdsONVeuHLe1p6KPus28gVAx2A-tCT3RA&VER=1"; xxzl_deviceid=zzOLpsRI0WOU1GOsRU39bTzPzk53D%2BFo7DfK1tJrTfwTAsXu76QVVAw%2BrqbfVEwv; xxzl_smartid=c1e319df4ed9e9df5f0eefc2fdbf1deb',
        'Referer': 'http://webim.58.com/index?p=rb',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'

    }
    id = 1670
    flag = 0
    a = 'id	house_id city_id	area_name	area_id	block_id	block_name	community_id	community_name	title_name	price	avg_price	room_num	hall_num	toilet_num	area_num	address	default_photo	floor_total	floor_num	house_age	house_ori	tags	owner	owner_tel	source_type	property_rights	commition_type	lat	lng	isFive_only	fitment_type	equipment	property	status	follow_up_time	outlet	borkers	brokerTel	houseSource_type	owner_type	street	house_number	registration_date	confidentialityRemarks	inputUser	deliveryTime	fangChanNum	garageRemarks	keyNumber	key	structure	garage	traffic_condition	paymentMethod	seeTheApartmentMethod	price_condition	description	is_intermediary	user_id	nick_name	belong	release_time	cityName	modelImg'
    column_name = a.split()
    if not os.path.exists(save_path):
        with codecs.open(save_path, 'a', 'utf_8_sig') as csvfile:

            writer = csv.DictWriter(csvfile, column_name)
            writer.writeheader()


    for x in range(1,70):#二手房个人房源一共有70页
        if x:

            url_page = url + 'pn' + str(x)

            page_html = getHtmlText(url_page, headers)
            houseurllist = gethouseurl(page_html)  # 写函数得到每页下每一套房的url列表
            print(houseurllist)
            for houseurl in houseurllist:

                try:
                    phonenum = gettelphone(houseurl,)

                    houseurlhtml = getHtmlText(houseurl, headers={
                        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Mobile Safari/537.36'},
                                               )
                    flag = getinformation(houseurlhtml, phonenum, id,save_path)
                    if flag ==1:
                        id += 1
                        print('以保存房子id = %d' % (id - 1))


                except Exception as e:
                    print(str(e))
                    pass
                    # print(str(e))
            sleeptime = random.randint(2, 10)
            print(time.ctime())
            time.sleep(sleeptime)
            print(time.ctime())
            if x % 3 == 0:
                time.sleep(random.randint(400, 600))

        #print(houseurllist)




main()