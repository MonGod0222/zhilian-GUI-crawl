import smtplib
import email.mime.multipart
import email.mime.text
from email.mime.application import MIMEApplication
import datetime
import time
import pandas as pd
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import os
import sys


def send_email(smtp_host, smtp_port, sendAddr, password, recipientAddrs, subject='', content=''):
    '''
    :param smtp_host: 域名
    :param smtp_port: 端口
    :param sendAddr: 发送邮箱
    :param password: 邮箱密码
    :param recipientAddrs: 发送地址
    :param subject: 标题
    :param content: 内容
    :return: 无
    '''
    msg = email.mime.multipart.MIMEMultipart()
    msg['from'] = sendAddr
    msg['to'] = recipientAddrs
    msg['subject'] = subject
    content = content
    txt = email.mime.text.MIMEText(content, 'plain', 'utf-8')
    msg.attach(txt)

    # 添加附件图片
    # part1 = MIMEApplication(open(r'1111.png', 'rb').read())
    # part1.add_header('Content-Disposition', 'attachment', filename="1111.png")  # 发送文件名称
    # msg.attach(part1)

    try:
        smtpSSLClient = smtplib.SMTP_SSL(smtp_host, smtp_port)  # 实例化一个SMTP_SSL对象
        loginRes = smtpSSLClient.login(sendAddr, password)  # 登录smtp服务器
        print(f"登录结果：loginRes = {loginRes}")
        if loginRes and loginRes[0] == 235:
            print(f"登录成功，code = {loginRes[0]}")
            smtpSSLClient.sendmail(sendAddr, recipientAddrs, str(msg))
            print(f"mail has been send successfully. message:{str(msg)}")
            smtpSSLClient.quit()
        else:
            print(f"登陆失败，code = {loginRes[0]}")
    except Exception as e:
        print(f"发送失败，Exception: e={e}")


date = datetime.datetime.now().day

user = sys.argv[1]
password = sys.argv[2]
mail = sys.argv[3]
theme = sys.argv[4]
db = sys.argv[5]

mysql_user=sys.argv[6]
mysql_password=sys.argv[7]

FLAGS=3     #默认取前三条数据

def find_from_mysql():
    import pymysql
    mysql_db = pymysql.connect(host='localhost', user=mysql_user, password=mysql_password,
                              port=3306,db='zhilian')
    cursor = mysql_db.cursor()
    sql='SELECT * FROM {} WHERE keyword="{}"'.format('求职信息',theme)
    re_find = cursor.execute(sql)
    if re_find==0:
        print('没有这个主题')
        return None
    else:
        read_data=''
        results=cursor.fetchall()
        for result in results[:FLAGS]:
            read_data=read_data+str(result)+'\n'
        return read_data

def find_from_mongo():
    import pymongo
    import json

    #连接
    client=pymongo.MongoClient()
    mongo_db=client['zhilian']
    collection=mongo_db['求职信息']
    #查询
    results=collection.find({'keyword':theme})
    if not results:
        return None
    read_data = ''
    for result in results[:FLAGS]:#取前FLAGS个数据
        result['_id'] = 'id'
        jsonstr = json.dumps(result)
        temp = jsonstr.encode('utf-8')
        jsonstr = temp.decode('unicode_escape')
        read_data = read_data+jsonstr+'\n'

    return read_data

if db=='mysql':
    read_data=find_from_mysql()
if db=='mongo':
    read_data=find_from_mongo()


while True:
    timenow = datetime.datetime.now()
    nowm = timenow.minute
    nowh = timenow.hour
    if nowh == 9:
        if nowm == 0:
            subject = theme
            content = read_data  # content改为数据库读取数据内容，稍微排版下
            send_email('smtp.qq.com', 465, sendAddr=user, password=password, recipientAddrs=mail, subject=subject,
                       content=content)

# 9点整发送，改成输入指定时间，sendmail中'邮箱账号', '密码', '收件邮箱'写入tk，subject用爬取的主题写入
# 只要修改while True里面内容
