import glob
from os.path import splitext
from PIL import Image
import os


def get_allfiles(path):
    paths = glob.glob(path)
    return paths

def converttype(file,type):
    for jpg in file:
        #print(jpg)
        im = Image.open(jpg)
        png = splitext(jpg)[0] + '.' + type
        im.save(png)
        os.remove(jpg)
        print('已转化%s'%png)




def main():
    path = '58图片jpg副本 2 - 副本 2/*'      #根文件下
    files = get_allfiles(path)                                        #得到根文件下所有文件夹
    type = 'png'
    #print(files)
    for file in files:
        try:
            file = file + '/' + '*.jpg'

            pics = get_allfiles(file)                                 #得到每个文件夹下所有图片
            #print(pics)

            converttype(pics, type)                                   #转化
        except:
            pass

main()