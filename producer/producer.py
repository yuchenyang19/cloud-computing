# -*- coding:utf-8 -*-

# 运行在python 3.8.1版本
import json
from kafka import KafkaProducer
import time,datetime
from spider import bilibili_api
from spider.customizedAPI import get_comments
from spider.bilibiliSeries import getTodayDanmaku
from spider.bilibiliSeries import getAllComments
from spider.textDealWith import get_all_statis
from timeUtils import timestamp2date,formatDate,date2timestamp
producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=lambda m: json.dumps(m).encode('ascii'))
while True:
    timestamp = int(time.time())
    with open("/home/cc/Desktop/cloud-computing-dev/producer/timestampRecord.txt", 'r') as f:
        lastTimestamp = int(f.readline())
    #距离上一次执行程序已过两分钟
    if timestamp - lastTimestamp >= 120:
        with open("/home/cc/Desktop/cloud-computing-dev/producer/timestampRecord.txt", 'w') as timestampFile:
            timestampFile.write(str(timestamp))
        comment = getAllComments(timeLimit=lastTimestamp)
        danmaku = getTodayDanmaku(timeLimit=lastTimestamp)
        #Todo set comment and danmaku data format like {'content': str, 'date':%Y-%M-%D}
        for i in range(0, len(comment)):
            ack=producer.send('test', {'comment':comment[i]['content'], 'date': timestamp2date(comment[i]['ctime'])})
            metadata=ack.get()
            print(metadata.topic, metadata.partition)
        for i in range(0, len(danmaku)):
            ack = producer.send('test', {'comment':danmaku[i]['content'], 'date': formatDate(danmaku[i]['send_time'])})
            metadata = ack.get()
            print(metadata.topic, metadata.partition)

    else:
        time.sleep(1)
# #此处for循环替换为爬虫代码
# i=1
# while i<5:
#     comment="此处for循环替换为爬虫代码"
#     date="2010-02-14"
#     dic={'comment':"虎杖悠仁 虎杖蔷薇 野蔷薇Brother brother 挚友",'date':"2012-01-14"}
   
#     ack = producer.send('test', dic)
#     # ack = producer.send('bangumi', 1)
#     metadata=ack.get()
#     print(metadata.topic, metadata.partition)
#     i+=1
producer.close()
