# -*- coding: utf-8 -*-
import scrapy
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


class QqNewSpider(scrapy.Spider):
    name = 'qq_new'
    allowed_domains = ['news.qq.com']
    start_urls = ['https://news.qq.com/']

    # custom_settings = {
    #     'COOKIES_ENABLE': False,
    #     'DOWNLOADER_MIDDLEWARES' :{
    #     # 'InformationSpider.middlewares.InformationspiderDownloaderMiddleware': 543,
    #     'InformationSpider.middlewares.RandomUserAgentMiddleware': None,
    #     'InformationSpider.middlewares.JSPMiddleware': 30,
    # }
    # }


    def __init__(self):
        super(QqNewSpider, self).__init__()

        # chromedriver不加载图片
        chrome_opt = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_opt.add_experimental_option("prefs",prefs)
        self.browser = webdriver.Chrome(executable_path='E:\software\python\chromedriver.exe', chrome_options=chrome_opt)
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        self.open_selenium = True
        self.from_platform = 'QQ_News'

    def spider_closed(self, spider):
        self.browser.quit()

    def start_requests(self):
        self.open_selenium = True
        origin_url = 'https://new.qq.com/ch/world/'
        # origin_url = 'https://new.qq.com/omn/20180713/20180713A0GU2H.html'
        yield Request(url=origin_url, callback=self.parse_category)

    def parse(self, response):
        pass

    def parse_category(self, response):
        print('category')
        self.open_selenium = True
        category_xpath = '//div[@class="qq_nav"]//ul[@id="main-list"]/li[@class="item " or "item active"]/a'
        name_xpath = 'text()'
        url_xpath = '@href'

        # html_code = chardet.detect(response.text)
        # print(html_code)
        # 检测爬取是否正确
        # with open('qq_test.html', 'wb') as fp:
        #     fp.write(response.text.encode('utf-8')) #用utf-8打印乱码，用gb2312有字段无法编码
        #     fp.close()

        category_selectors = response.xpath(category_xpath)
        pass_word = ('视频', '北京', '世界杯', '要闻', 'NBA')

        # for category_selector in category_selectors:
        #     name = category_selector.xpath(name_xpath).extract()[0]
        #     url = category_selector.xpath(url_xpath).extract()[0]
        #     url = parse.urljoin(response.url, url)
        #     #去掉不需要的栏目
        #     if name in pass_word:
        #         continue
        #     else:
        #         pass
        #     yield Request(url=url, callback=self.parse_detail, meta={"category": name}, dont_filter=True)

        name = '浙江'
        url = 'https://new.qq.com/d/zj'
        yield Request(url=url, callback=self.parse_detail, meta={"category": name}, dont_filter=True)

    def parse_detail(self, response):
        print('detail')
        self.open_selenium = False
        cnt = 0
        div_xpath = '//div[@class="focus-mod"]//a[@class="focus-item"]'
        title_xpath = 'div[@class="txt"]/h2/text()'
        url_xpath = '@href'
        # summary_xpath = 'p/text()'
        image_url_xpath = 'div[@class="pic"]/img/@src'
        news_time_xpath = 'div[@class="txt"]/div[@class="info"]/span[2]/text()'
        re_selectors = response.xpath(div_xpath)

        for re_selector in re_selectors:
            title = re_selector.xpath(title_xpath).extract()
            url = re_selector.xpath(url_xpath).extract()
            # url_md5 = get_md5(url)
            summary = ''
            # 提取图片地址
            temp_urls = re_selector.xpath(image_url_xpath).extract()
            if len(temp_urls) >= 1:
                img_urls = 'http:'+temp_urls[0]
            else:
                img_urls = 'https://mat1.gtimg.com/pingjs/ext2020/newom/build/static/images/new_logo.png'

            category = response.meta.get("category", "")
            from_platform = self.from_platform
            news_time = re_selector.xpath(news_time_xpath).extract()
            if len(news_time) == 0:
                news_time = '1天前'

            crawl_time = datetime.datetime.now().date()

            # 排除亲爱的会员这几种特殊情况
            if len(title) and len(url) and len(news_time) and len(img_urls):
                pass
            else:
                continue

            # 设置一个默认值，防止出错
            if len(news_time) >= 1:
                news_score = get_score(news_time[0])
            else:
                news_score = 1.0

            news_itemloader = ItemLoader(item=NewsItem(), response=response)
            news_itemloader.add_value("title", title)
            news_itemloader.add_value("image_urls", img_urls)
            news_itemloader.add_value("url", url)
            news_itemloader.add_value("url_md5", get_md5(url[0]))
            news_itemloader.add_value("category", category)
            news_itemloader.add_value("summary", summary)
            news_itemloader.add_value("from_platform", from_platform)
            news_itemloader.add_value("news_time", news_time)
            news_itemloader.add_value("crawl_time", crawl_time)
            news_itemloader.add_value("news_score", news_score)
            news_item = news_itemloader.load_item()

            # 测试json，减少数量
            cnt = cnt + 1
            if cnt == 2:
                break

            yield news_item

        self.open_selenium = True
        yield Request(url=response.url, callback=self.parse_more, meta={"category": category}, dont_filter=True)

        pass


    def parse_more(self,response):
        print('more')
        self.open_selenium = False

        cnt = 0
        div_xpath = '//div[@id="List"]//ul[@class="list"]/li[@class="item cf" or "item-pics cf"]'
        title_pics_xpath = 'h3/a/text()'
        title_xpath = 'div[@class="detail"]/h3/a/text()'
        url_xpath = 'div[@class="detail"]/h3/a/@href'
        url_pic_xpath = 'h3/a/@href'
        # summary_xpath = 'p/text()'
        image_url_xpath = 'div[@class="picture" or "fl picture"]//img[1]/@src'
        news_time_xpath = 'div[@class="detail"]//span[@class="time"]/text()'
        re_selectors = response.xpath(div_xpath)

        for re_selector in re_selectors:
            item_type = re_selector.xpath('@class').extract()[0]
            if item_type == "item cf":
                title = re_selector.xpath(title_xpath).extract()
                url = re_selector.xpath(url_xpath).extract()
            else:
                title = re_selector.xpath(title_pics_xpath).extract()
                url = re_selector.xpath(url_pic_xpath).extract()
            # url_md5 = get_md5(url)
            summary = ''
            # 提取图片地址
            temp_urls = re_selector.xpath(image_url_xpath).extract()
            if len(temp_urls) >= 1:
                img_urls = 'http:' + temp_urls[0]
            else:
                img_urls = 'https://mat1.gtimg.com/pingjs/ext2020/newom/build/static/images/new_logo.png'

            category = response.meta.get("category", "")
            from_platform = self.from_platform
            news_time = re_selector.xpath(news_time_xpath).extract()
            if len(news_time) == 0:
                news_time = '1天前'

            crawl_time = datetime.datetime.now().date()

            # 排除亲爱的会员这几种特殊情况
            if len(title) and len(url) and len(news_time) and len(img_urls):
                pass
            else:
                continue

            # 设置一个默认值，防止出错
            if len(news_time) >= 1:
                news_score = get_score(news_time[0])
            else:
                news_score = 1.0

            news_itemloader = ItemLoader(item=NewsItem(), response=response)
            news_itemloader.add_value("title", title)
            news_itemloader.add_value("image_urls", img_urls)
            news_itemloader.add_value("url", url)
            news_itemloader.add_value("url_md5", get_md5(url[0]))
            news_itemloader.add_value("category", category)
            news_itemloader.add_value("summary", summary)
            news_itemloader.add_value("from_platform", from_platform)
            news_itemloader.add_value("news_time", news_time)
            news_itemloader.add_value("crawl_time", crawl_time)
            news_itemloader.add_value("news_score", news_score)
            news_item = news_itemloader.load_item()

            # 测试json，减少数量
            cnt = cnt + 1
            if cnt == 2:
                break

            yield news_item

        pass







