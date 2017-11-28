# -*- coding: utf8 -*-
"""
多线程crawl video
"""
import time
import csv
import random
import sys
from multiprocessing.dummy import Pool as ThreadPool
from getvideoinfo_v2_1 import BiliVideo


def get_info(mid):
    gu = BiliVideo(mid)
    info = gu.getVideoInfo()
    # gu.getUserInfo()
    # print(mid, gu.info)
    # return gu.info
    #time.sleep(1)
    return info


def go_get(start, end, fileindex):
    """
    start, end: 起始uid
    fileindex：写入文件的index
    """
    NUMS = list(range(start, end))
    pool = ThreadPool(4)
    try:
        results = pool.map(get_info, NUMS)
    except Exception as e:
        print(e)
        time.sleep(100)
        results = pool.map(get_info, NUMS)
    pool.close()
    pool.join()

    with open('vinfo/vinfo_{}.csv'.format(fileindex), 'a', encoding='utf8', newline='') as f:
        for result in results:
            if result:
                csvwriter = csv.writer(f)
                csvwriter.writerow(result)


if __name__ == '__main__':
    #test()
    # 1000一个文件,10个文件
    # try:
    #     size = int(input("请输入每轮抓取的video数量size:(10000默认)"))
    # except:
    #     size = 10000
    # uid_start = int(input("请输入开始uid的size整数倍数(0,1...10...): "))
    # num = int(input("爬取多少轮(size个id一轮): "))
    size, uid_start, num = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    # num = 10  # 每次跑10轮
    # size = 100  # 每个文件10000个(size是step的整数倍)
    for i in range(uid_start, uid_start + num):
        start, end, step = size * i + 1, size * (i + 1) , 100
        # step次请求休息一下
        print('===第{}轮===:(每轮size:{})'.format(i + 1, size))
        for loop in range(start, end, step):
            go_get(loop, loop + step, i + 1)
            # 请求不要过于频繁，不要过于增加服务器的过载哦
            secs = round(random.uniform(10, 15), 2)  # 随机休息时间间隔
            time.sleep(secs)
