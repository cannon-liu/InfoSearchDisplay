# -*- coding: utf-8 -*-
import scrapy
import scrapy
from scrapy.http import Request
from urllib import parse
import datetime
from scrapy.loader import ItemLoader
import chardet
import random
import time
from scrapy.selector import Selector

#self package
from InformationSpider.utils.common import get_score, get_md5, make_str
from InformationSpider.items import NewsItem


class FtNewSpider(scrapy.Spider):
    name = 'ft_new'
    allowed_domains = ['ftchinese.com/', 'ft.com/', 'i.ftimg.net/']
    start_urls = ['http://www.ftchinese.com/']
    from_platform = 'FT中文网'

    def start_requests(self):
        origin_url = 'http://www.ftchinese.com'
        yield Request(url=origin_url, callback=self.parse_category)

    def parse(self, response):
        pass

#抓取目录和分类表路径
    def parse_category(self, response):
        # category_xpath = '//ol[@class="o-nav__meganav"]/li[@class="nav-section"]'
        category_url_xpath = '//ol/li[@class="nav-section "]/a/@href'
        category_name_xpath = '//ol/li[@class="nav-section "]/a/text()'

        hrefs = response.xpath(category_url_xpath).extract()
        names = response.xpath(category_name_xpath).extract()

        cnt = len(names)
        pass_word = ('首页', '管理', '视频',  '每日英语')
        index = 0
        for name in names:
            if name not in pass_word:
                href = hrefs[index]
                category_url = parse.urljoin(response.url, href)
                yield Request(url=category_url, callback=self.parse_detail, meta={"category": name}, dont_filter=True)
            index = index+1

    def parse_detail(self, response):
        print("detail")
        # html = Selector(response)
        cnt = 0
        div_xpath = '//div/div[@class="item-inner"]'
        title_xpath = 'h2//a/text()'
        url_xpath = 'h2//a/@href'
        summary_xpath = 'div[@class="item-lead"]/text()'
        image_url_xpath = 'a[@class="image"]/figure/@data-url'
        news_time_xpath = 'div[@class="item-time"]/text()'

        re_selectors = response.xpath(div_xpath)
        for re_selector in re_selectors:
            title = re_selector.xpath(title_xpath).extract()
            url = re_selector.xpath(url_xpath).extract()
            # url_md5 = get_md5(url)
            summary = re_selector.xpath(summary_xpath).extract()
            img_url = re_selector.xpath(image_url_xpath).extract()
            category = response.meta.get("category", "")
            from_platform = self.from_platform
            news_time = re_selector.xpath(news_time_xpath).extract()
            try:
                crawl_time = datetime.datetime.strptime(crawl_time, "%Y/%m/%d").date()
            except Exception as e:
                crawl_time = datetime.datetime.now().date()

            #检测爬取是否正确
            # with open('test.html','wb') as fp:
            #     fp.write(response.text.encode('utf-8'))
            #     fp.close()

            #排除亲爱的会员这几种特殊情况
            if len(title) and len(url) and len(news_time) and len(img_url):
                pass
            else:
                continue

            #设置一个默认值，防止出错
            if len(news_time) >= 1:
                news_score = get_score(news_time[0])
            else:
                news_score = 1.0

            # news_item = NewsItem()
            # news_item['title'] = title
            # news_item['image_urls'] = img_url
            # news_item['url'] = url
            # news_item['url_md5'] = get_md5(url)
            # news_item['category'] = category
            # news_item['summary'] = summary
            # news_item['from_platform'] = from_platform
            # news_item['news_time'] = news_time
            # news_item['crawl_time'] = crawl_time
            # news_item['news_score'] = news_score
            test_img = 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p2519070834.webp'


            news_itemloader = ItemLoader(item=NewsItem(), response=response)
            news_itemloader.add_value("title", title)
            news_itemloader.add_value("image_urls", img_url)
            # news_itemloader.add_value("image_path", '/images/full')   #测试scrapyd的时候，指定图片路径
            news_itemloader.add_value("url", parse.urljoin(response.url, url[0]))
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
            if cnt == 3:
                break

            yield news_item

        pass







