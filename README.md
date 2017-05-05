# pythonUpload
利用python批量上传图片到七牛
### 先说说原因

经常用markdown写笔记, 但是每次遇到添加图片的时候就很苦恼, 以前是在csdn上写笔记, 每次都要先一张一张的把图片上传到CSDN, 然后生成链接, 很是麻烦. 所以调研一下, 用七牛的免费空间做图床.(免费为七牛打广告了)

1. 首先 注册七牛->新建存储空间(操作略省)
![image](http://opetx8797.bkt.clouddn.com/python$2017-05-05$5.png)
2. 定需求, 
> a.  在md文件下新建两个文件夹mdOldImage用于存放每次笔记的图, 上传后清空, mdNewImage用于存放所有的笔记用图.
>
> b.  每次截图修改文件名
>
> c.  批量上传图片到七牛
>
> d.  同时生产md 格式的image引用格式, 保存于txt文件并打开

3. 具体代码如下

```
python3.5
    
pip install qiniu
或
easy_install qiniu
```

```
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
access_key = '七牛账号下查找'
secret_key = '七牛账号下查找'
# 存储空间
bucket_name = 'noteimages'
# 域名
bucket_url = '存储空间的外链域名'

# 格式
img_suffix = ["jpg", "jpeg", "png", "bmp", "gif"]
# 本地存放图片地址
oldPath = '/Users/zwz/Desktop/md文件/mdImage'
# 修改名字后存放在的新地址
newPath = '/Users/zwz/Desktop/md文件/mdNewImage'
# 生成结果文档
result_file = '/Users/zwz/Desktop/result_file.txt'


# 存放链接数组
dataArr = []

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
        #生成新的文件名字
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
    
    #生成链接
    rename(input('请输入md文章标题:  '))
    #写入文件
    crateFile(dataArr)
    #打开文件
    os.system('open '+ result_file)

```
---
![image](http://opetx8797.bkt.clouddn.com/gif$2017-05-05$0.gif)
- 参考 [七牛PythonAPI](https://developer.qiniu.com/kodo/sdk/1242/python)


- [GitHub代码](https://github.com/zhaoweizheng/pythonUpload)

