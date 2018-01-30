import csv
import codecs
import os

class Cleardata:
    id = 1
    save_path = '1_29new.csv'
    hash = {}
    hash_length = 3000
    fold = codecs.open('finalfinalfinalfight!!!.csv','r')
    fnew = codecs.open('1_29.csv','r')
    a = 'id	house_id city_id	area_name	area_id	block_id	block_name	community_id	community_name	title_name	price	avg_price	room_num	hall_num	toilet_num	area_num	address	default_photo	floor_total	floor_num	house_age	house_ori	tags	owner	owner_tel	source_type	property_rights	commition_type	lat	lng	isFive_only	fitment_type	equipment	property	status	follow_up_time	outlet	borkers	brokerTel	houseSource_type	owner_type	street	house_number	registration_date	confidentialityRemarks	inputUser	deliveryTime	fangChanNum	garageRemarks	keyNumber	key	structure	garage	traffic_condition	paymentMethod	seeTheApartmentMethod	price_condition	description	is_intermediary	user_id	nick_name	belong	release_time	cityName	modelImg'
    column_name = a.split()
    def __init__(self):                                  #保存不重复的房源到新文件里，并弄好表头
        if not os.path.exists(self.save_path):
            with codecs.open(self.save_path,'a') as f:
                writer = csv.DictWriter(f,self.column_name)
                writer.writeheader()

    def get_hash_address(self):
        fold = self.fold
        hash = self.hash
        lines = csv.DictReader(fold,self.column_name)
        for line in lines:
            try:
                house_id = int(line['house_id'][3:])
                hash_address = house_id % self.hash_length
                while hash.get(hash_address):  # 开放寻址法
                    hash_address += 1
                hash[hash_address] = house_id
            except:
                pass

    def find_same_house(self):
        fnew = self.fnew
        hash = self.hash
        lines = csv.DictReader(fnew,self.column_name)

        for line in lines:
            try:
                house_id = int(line['house_id'][3:])
                hush_address = house_id % self.hash_length
                while hash.get(hush_address) and hash.get(hush_address) != house_id:
                    hush_address += 1
                    hush_address = hush_address % self.hash_length
                if hash.get(hush_address) == None:
                    print("这是新房源!",line['id'])
                    self.save_out(line)
                    continue
                    pass
                #if hash.get(huah_address) == house_id:
                print('重复房源！在新文件里id为', line['id'])

            except Exception as e:
                print(str(e))
                pass

    def save_out(self,line):
        line['id'] = self.id
        items = {}
        for i in line.items():
            items[i[0]] = i[1]
        print(items)

        with codecs.open(self.save_path,'a') as f:
            writer = csv.DictWriter(f,self.column_name)
            writer.writerow(items)
            self.id += 1
            print('以保存第%d套新房'%(self.id -1))
            f.close()













mydata = Cleardata()
mydata.get_hash_address()
mydata.find_same_house()