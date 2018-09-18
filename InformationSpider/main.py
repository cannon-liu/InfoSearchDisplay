# -*- coding = utf-8 -*-
__author__ = 'cannon'
__date__ = '2018/7/11 14:51'


from scrapy.cmdline import execute
import sys
import  os

#获得articleSpider的路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", "ft_new"])
# execute(["scrapy", "crawl", "pengpai_new"])
# execute(["scrapy", "crawl", "zaker_new"])
# execute(["scrapy", "crawl", "qq_new"])
# execute(["scrapy", "crawl", "lagou"])
