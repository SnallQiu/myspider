import requests
from lxml import etree
import time
from threading import Thread

class Doubai():
    url = ['https://movie.douban.com/top250?start='+str(x)for x in range(0,250,25)]
    title = []
    tasks = []

    def get_html(self,url):
        return requests.get(url)

    def main(self,url):
        selector = etree.HTML(self.get_html(url).content)
        titles = selector.xpath('//*[@id="content"]/.//span[@class="title"][1]')
        for title in titles:
            self.title.append(title.text)
    def thread(self):
        for i in self.url:
            task = Thread(target=self.main,args=(i,))
            self.tasks.append(task)
            task.start()

        for task in self.tasks:
            task.join()
        for i,title in enumerate(self.title,1):
            print(i,title)
doubai = Doubai()
start = time.time()
doubai.thread()
end = time.time()
print('耗时：',str(end-start))