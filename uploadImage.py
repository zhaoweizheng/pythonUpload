# -*- coding: utf-8 -*-
# flake8: noqa
from qiniu import Auth, put_file, etag, urlsafe_base64_encode
import qiniu.config
import sys
import os
import time
import subprocess

#-----------默认配置-----------
# accessKey和secretkey是七牛的秘钥
access_key = '七牛上面找'
secret_key = '七牛上面找'

# 域名
bucket_url = '自己存储空间的外链域名'
# 存储空间
bucket_name = '自己建的存储空间'

img_suffix = ["jpg", "jpeg", "png", "bmp", "gif"]

# 以下路径可以自己设置
# 本地存放图片地址
oldPath = '/Users/zwz/Desktop/md文件/mdImage'
# 修改名字后存放在的新地址
newPath = '/Users/zwz/Desktop/md文件/mdNewImage'

result_file = '/Users/zwz/Desktop/result_file.txt'



dataArr = []
#
def rename(name):
    count = 0
    fileList = os.listdir(oldPath)# 该文件夹下所有的文件（包括文件夹）
    for files in fileList: #遍历所有的文件
        oldDir = os.path.join(oldPath, files) #原来的文件路径
        if os.path.isdir(oldDir): #如果是文件夹就跳过
            continue
        fileName = os.path.splitext(files)[0]  #文件名
        fileType = os.path.splitext(files)[1]  #文件扩展名
        if fileType == '.jpg' or fileType == '':
            fileType = '.png'
        timeString = time.strftime("$%Y-%m-%d$", time.localtime())
        dataName = name + timeString + str(count) + fileType

        newDir = os.path.join(newPath, dataName) # 新的文件路径
        os.rename(oldDir, newDir)
        count += 1
        #链接添加到数组
        dataArr.append(upload_data(dataName,newDir))



#上传文件到七牛, 返回链接地址
def upload_data(newName, localfilePath):
    q = Auth(access_key, secret_key)
    # 上传到七牛后保存的文件名
    key = newName;
    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 3600)
    # 要上传文件的本地路径
    localfile = localfilePath
    ret, info = put_file(token, key, localfile)
    return bucket_url + key


def crateFile(dataList):
    with open(result_file, 'w+') as f:
        for data in dataList:
            # 如果是图片则生成图片的markdown格式引用
            if os.path.splitext(data)[1][1:] in img_suffix:
                f.write('![image]('+data+')'+'\n')

    f.close()


if __name__ == '__main__':

    rename(input('请输入md文章标题:  '))
    crateFile(dataArr)
    os.system('open '+ result_file)



