import requests
import re
import json
import pandas as pd
from lxml import etree
import time
import random
class Lagou:
    url = 'https://www.lagou.com/jobs/positionAjax.json?px=default&city=%E5%8C%97%E4%BA%AC&needAddtionalResult=false&isSchoolJob=0'
    headers = {

        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Host': 'www.lagou.com',
        'Origin': 'https://www.lagou.com',
        'Referer': 'https://www.lagou.com/jobs/list_java?city=%E6%B7%B1%E5%9C%B3&cl=false&fromSearch=true&labelWords=&suginput=',
    }
    cookies = {
        'Cookie': 'JSESSIONID=ABAAABAACDBABJB891EEAD7CAF67926046A9E14C1E1DC6D; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1518140780; _ga=GA1.2.2036300807.1518140780; _gi\
                        d=GA1.2.646490167.1518140780; user_trace_token=20180209094620-06bd951b-0d3b-11e8-afb1-5254005c3644; LGSID=20180209094620-06bd9ca0-0d3b-11e8-afb1-5254005c3644; \
                        LGUID=20180209094620-06bd9ff6-0d3b-11e8-afb1-5254005c3644; X_HTTP_TOKEN=26d30c9fd7311d5a5db4e19ae94ab7f8; _putrc=E098ED3C343FD6FA; login=true; unick=%E8%A3%98%E6\
                        %82%AB%E6%88%90; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; gate_login_token=f578851d221e23487f0469af5f34255c2c19a7b0e004e\
                        d69; index_location_city=%E4%B8%8A%E6%B5%B7; TG-TRACK-CODE=search_code; _gat=1; SEARCH_ID=f64da2a4c45d479fb02466a7da101319; LGRID=20180209103130-5640ac7b-0d41-11e8-afb\
                        1-5254005c3644; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1518143491',
    }
    id = 151
    def run(self):
        page = self.get_page()
        for i in range(12,page):
            r = self.gethtml(i)
            self.getinfo(r)
            time.sleep(60)

    def get_page(self):
        return 30


    def gethtml(self,i):

        data = {
            'first':'false',
            'pn':str(i),
            'kd':'python',


        }
        r = ''
        #ip_list = json.loads(requests.get('http://127.0.0.1:8000/?types=0&count=30&country=%E5%9B%BD%E5%86%85').text)
        #ip_list_random = random.choice(ip_list)
        #ip = {'https':'http://'+ip_list_random[0]+':'+str(ip_list_random[1]),'http':'http://'+ip_list_random[0]+':'+str(ip_list_random[1])}
        #print(ip)
        try:
            r =requests.post(self.url,cookies = self.cookies,headers = self.headers,data = data )#,proxies= ip)
        except:
            #ip_list.remove(ip_list_random)
            self.gethtml(i)

        return r
    def getinfo(self,r):
        try:
            print(r.json())
            jobs = r.json()['content']['positionResult']['result']
            for job in jobs:
                companyShortName = job['companyShortName']
                positionId = job['positionId']  # 主页ID
                companyFullName = job['companyFullName']  # 公司全名
                companyLabelList = job['companyLabelList']  # 福利待遇
                companySize = job['companySize']  # 公司规模
                industryField = job['industryField']
                createTime = job['createTime']  # 发布时间
                district = job['district']  # 地区
                education = job['education']  # 学历要求
                financeStage = job['financeStage']  # 上市否
                firstType = job['firstType']  # 类型
                secondType = job['secondType']  # 类型
                formatCreateTime = job['formatCreateTime']  # 发布时间
                publisherId = job['publisherId']  # 发布人ID
                salary = job['salary']  # 薪资
                workYear = job['workYear']  # 工作年限
                positionName = job['positionName']  #
                jobNature = job['jobNature']  # 全职
                positionAdvantage = job['positionAdvantage']  # 工作福利
                positionLables = job['positionLables']  # 工种

                detail_url = 'https://www.lagou.com/jobs/{}.html'.format(positionId)
                response = requests.get(url=detail_url, headers=self.headers, cookies=self.cookies)
                response.encoding = 'utf-8'
                tree = etree.HTML(response.text)
                desc = tree.xpath('//*[@id="job_detail"]/dd[2]/div/p/text()')
                x = ''
                for label in positionLables:
                    x += label + ','
                '''
                print(companyFullName)
                print('%s 拉勾网链接:-> %s' % (companyShortName, detail_url))

                print('职位：%s' % positionName)
                print('职位类型：%s' % firstType)
                print('薪资待遇：%s' % salary)
                print('职位诱惑：%s' % positionAdvantage)
                print('地区：%s' % district)
                print('类型：%s' % jobNature)
                print('工作经验：%s' % workYear)
                print('学历要求：%s' % education)
                print('发布时间：%s' % createTime)
                x = ''
                for label in positionLables:
                    x += label + ','
                print('技能标签：%s' % x)
                print('公司类型：%s' % industryField)
                for des in desc:
                    print(des)
                '''
                data = {'positionName': positionName, 'firstType': firstType, 'salary': salary,
                        'positionAdvantage': positionAdvantage,
                        'district': district, 'jobNature': jobNature, 'workYear': workYear, 'education': education,
                        'createTime': createTime,
                        'labels': x, 'industryField': industryField, 'detail_url': detail_url,'companyName':companyFullName}
                save_ = pd.DataFrame(data, index=[self.id])
                self.save_to_csv(save_)
        except:
            pass
    def save_to_csv(self,save_):
        save_.to_csv('lagou2.csv', header=True if self.id == 1 else False, mode='a')
        self.id += 1
        print('以保存%d条职位信息'%(self.id-1))






lagou = Lagou()
lagou.run()

