# coding: u8


# 监视日志文件，如果出现302那么禁用爬虫一会，再启动

import commands
import os
import time


os.system('killall scrapy')
os.system('scrapy crawl bdmms&')

while 1:
    time.sleep(0.1)

    # 得到日志中302的个数
    cnt_302 = int(commands.getstatusoutput('cat bdmms.log | grep -n "Redirecting (302)" | wc -l')[1])
    # 读取上次302的个数
    last_cnt = int(open('./302count.txt').read().strip())

    if cnt_302 != last_cnt:
        # 将新302个数写到文件
        open('./302count.txt', 'w').write(str(cnt_302))

        # 杀死爬虫
        print 'killing...'
        os.system('killall scrapy')

        # 暂停
        N = 10
        print 'sleeping %s minute...' % N
        time.sleep(60 * N)

        # 启动爬虫
        print 'starting scrapy...'
        # 保险起见，再杀一遍
        os.system('killall scrapy')
        os.system('scrapy crawl bdmms&')
