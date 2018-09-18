# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request
from urllib import parse
import datetime
from scrapy.loader import ItemLoader
import chardet
import random
import time

from selenium import webdriver
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher


#self package
from InformationSpider.utils.common import get_score, get_md5, make_str, del_str, tranfer_str,\
    get_re_zaker,reverse_tranfer_str,decode_zaker
from InformationSpider.utils.setting import QQ_header
from InformationSpider.items import NewsItem



class LagouSpider(CrawlSpider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']

    def __init__(self):
        super(LagouSpider, self).__init__()
        # chromedriver不加载图片
        chrome_opt = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_opt.add_experimental_option("prefs",prefs)
        self.browser = webdriver.Chrome(executable_path='E:\software\python\chromedriver.exe', chrome_options=chrome_opt)
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        self.open_selenium = True
        self.from_platform = 'lagou'

    def spider_closed(self, spider):
        self.browser.quit()


    # 以免登录，添加的自定义设置，优先级高于settings.py中的项目
    custom_settings = {
        "COOKIES_ENABLED": False,
        "DOWNLOAD_DELAY": 60,
    }

    #起始页选择
    # 'https://www.lagou.com/'，

    start_urls = [
    # 'https://www.lagou.com/'
    # 'https://www.lagou.com/jobs/list_python'
    'https://www.lagou.com/jobs/list_Python?px=new&city=%E6%9D%AD%E5%B7%9E#order/'
    # 'https://www.lagou.com/jobs/list_%E7%88%AC%E8%99%AB?px=new&city=%E6%9D%AD%E5%B7%9E#order',
    # 'https://www.lagou.com/jobs/list_%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90?px=new&city=%E6%9D%AD%E5%B7%9E#order',
    # 'https://www.lagou.com/jobs/list_%E6%95%B0%E6%8D%AE%E6%8C%96%E6%8E%98?px=new&city=%E6%9D%AD%E5%B7%9E#order'
    ]
    #分别是搜索python，爬虫，数据分析，数据挖掘的职位

    rules = (
        Rule(
             LinkExtractor(allow='/jobs/\d+.html'), callback='parse_job', follow=True),
    )

    #
    # def start_requests(self):
    #     self.open_selenium = True
    #     # origin_url = 'https://www.lagou.com/'
    #     origin_url = 'https://www.lagou.com/jobs/list_Python?px=new&city=%E6%9D%AD%E5%B7%9E#order/'
    #     yield Request(url=origin_url, callback=self.parse_job)



    def parse_job(self, response):
        print("parse item")
        temp = response.text
        pass