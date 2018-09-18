# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse
import datetime
from scrapy.loader import ItemLoader

from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from selenium import webdriver


#self package
from InformationSpider.utils.common import get_score, get_md5, make_str, del_str, tranfer_str,\
    get_re_zaker, reverse_tranfer_str, decode_zaker
from InformationSpider.items import NewsItem

class ZakerNewSpider(scrapy.Spider):
    name = 'zaker_new'
    allowed_domains = ['myzaker.com']
    start_urls = ['http://myzaker.com/']
    from_platform = "Zaker新闻"

    # custom_settings = {
    #     "COOKIES_ENABLED": False,
    #     "DOWNLOAD_DELAY": 20,
    #     'DEFAULT_REQUEST_HEADERS': {
    #         # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    #         'Accept-Encoding': 'gzip, deflate, br',
    #         'Accept-Language': 'zh-CN,zh;q=0.9',
    #         'Connection': 'keep-alive',
    #         # 'Cookie': 'JSESSIONID=ABAAABAAAFCAAEGBC99154D1A744BD8AD12BA0DEE80F320; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; _ga=GA1.2.1111395267.1516570248; _gid=GA1.2.1409769975.1516570248; user_trace_token=20180122053048-58e2991f-fef2-11e7-b2dc-525400f775ce; PRE_UTM=; LGUID=20180122053048-58e29cd9-fef2-11e7-b2dc-525400f775ce; index_location_city=%E5%85%A8%E5%9B%BD; X_HTTP_TOKEN=7e9c503b9a29e06e6d130f153c562827; _gat=1; LGSID=20180122055709-0762fae6-fef6-11e7-b2e0-525400f775ce; PRE_HOST=github.com; PRE_SITE=https%3A%2F%2Fgithub.com%2Fconghuaicai%2Fscrapy-spider-templetes; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2F4060662.html; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1516569758,1516570249,1516570359,1516571830; _putrc=88264D20130653A0; login=true; unick=%E7%94%B0%E5%B2%A9; gate_login_token=3426bce7c3aa91eec701c73101f84e2c7ca7b33483e39ba5; LGRID=20180122060053-8c9fb52e-fef6-11e7-a59f-5254005c3644; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1516572053; TG-TRACK-CODE=index_navigation; SEARCH_ID=a39c9c98259643d085e917c740303cc7',
    #         'Host': 'www.myzaker.com',
    #         # 'Origin': 'https://www.lagou.com',
    #         'Referer': 'http://www.myzaker.com/',
    #         # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    #         # 'X - Requested - With':'XMLHttpRequest',
    #
    #     }
    # }

    def start_requests(self):
        origin_url = 'http://www.myzaker.com/'
        yield Request(url=origin_url, callback=self.parse_category)

    def parse(self, response):
        pass

    def parse_category(self, response):
        print('category')
        category_xpath = '//div[@class="nav_outer flex-10"]/div[@class="nav"]/a[@class="nav_item nav_item_active" or "nav_item "]'
        name_xpath = 'text()'
        url_xpath = '@href'

        # # 检测爬取是否正确
        # with open('zaker_test.html', 'wb') as fp:
        #     fp.write(response.text.encode('utf-8'))
        #     fp.close()

        category_selectors = response.xpath(category_xpath)
        pass_word = ('汽车', '科技', '教育')
        for category_selector in category_selectors:
            name = category_selector.xpath(name_xpath).extract()[0]
            url = category_selector.xpath(url_xpath).extract()[0]
            url = 'http:' + url
            #去掉不需要的栏目
            if name in pass_word:
                continue
            else:
                pass
            yield Request(url=url, callback=self.parse_detail, meta={"category": name}, dont_filter=True)

        name = '杭州'
        url = 'http://www.myzaker.com/channel/10296'
        yield Request(url=url, callback=self.parse_detail, meta={"category": name}, dont_filter=True)

        name = '上海'
        url = 'http://www.myzaker.com/channel/10001'
        yield Request(url=url, callback=self.parse_detail, meta={"category": name}, dont_filter=True)



    def parse_detail(self, response):
        print('detail')
        cnt = 0
        div_xpath = '//div[@id="section"]/div[@class="figure flex-block"]'
        title_xpath = 'div/h2/a/text()'
        url_xpath = 'div/h2/a/@href'
        # summary_xpath = 'p/text()'
        image_url_xpath = 'a/@style'
        news_time_xpath = 'div/div/span[2]/text()'

        re_selectors = response.xpath(div_xpath)
        for re_selector in re_selectors:
            title = re_selector.xpath(title_xpath).extract()
            url = re_selector.xpath(url_xpath).extract()[0]
            url = 'http:' + url
            # url_md5 = get_md5(url)
            summary = 'null'
            #提取图片地址
            temp_urls = re_selector.xpath(image_url_xpath).extract()
            if len(temp_urls) >= 1:
                temp_url = temp_urls[0]
                temp = temp_url.split(":")[1]
                temp=temp.replace("url(", "http:")
                temp = temp.replace(");", "")
                img_urls = temp
            else:
                img_urls = 'http://zkres.myzaker.com/static/zaker_web2/img/logo.png?v=20170726'

            category = response.meta.get("category", "")
            from_platform = self.from_platform
            news_time = re_selector.xpath(news_time_xpath).extract()

            try:
                crawl_time = datetime.datetime.strptime(crawl_time, "%Y/%m/%d").date()
            except Exception as e:
                crawl_time = datetime.datetime.now().date()

            #排除亲爱的会员这几种特殊情况
            if len(title) and len(url) and len(news_time) and len(img_urls):
                pass
            else:
                continue

            #设置一个默认值，防止出错
            if len(news_time) >= 1:
                news_score = get_score(news_time[0])
            else:
                news_score = 1.0

            img_url = make_str('http:', img_urls)
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

            # #测试json，减少数量
            # cnt = cnt + 1
            # if cnt == 2:
            #     break

            yield news_item

        #获取下一页json内容
        next_page_xpath = '//div[@id="content"]/div[@class="main flex-block"]/a[@class="next_page"]/@href'
        next_url = response.xpath(next_page_xpath).extract()[0]
        deal_url = tranfer_str(next_url)
        kv = get_re_zaker(deal_url)
        appid = kv.get("appid")
        date = kv.get("date")
        artilce = kv.get("artcile")
        stamp = kv.get("stamp")
        tab = kv.get("tab")
        version = kv.get("version")

        myversion = '&_version='+version

        head = 'http://www.myzaker.com/news/next_new.php?f=myzaker_com&url='
        no_aticle_url = 'http://iphone.myzaker.com/zaker/blog2news.php?app_id={0}&since_date={1}&nt={2}&_appid=iphone&opage={3}&top_tab_id={4}&_version={5}'
        base_url = 'http://iphone.myzaker.com/zaker/blog2news.php?app_id={0}&since_date={1}&nt={2}&next_aticle_id={3}&_appid=iphone&opage={4}&otimestamp={5}&top_tab_id={6}&_version={7}'
        for page in range(1):
            nt = page + 1
            opage = page + 2
            if artilce == None or stamp==None:
                json_url = head + reverse_tranfer_str(no_aticle_url.format(appid, date, nt, opage, tab, version)) + myversion
            else:
                json_url = head + reverse_tranfer_str(base_url.format(appid, date, nt, artilce, opage, stamp, tab, version)) + myversion
            # json_url = 'http://www.myzaker.com/news/next_new.php?f=myzaker_com&url=http%3A%2F%2Fiphone.myzaker.com%2Fzaker%2Fblog2news.php%3Fapp_id%3D10001%26since_date%3D1531383311%26nt%3D1%26_appid%3Diphone%26top_tab_id%3D12183%26_version%3D6.5&_version=6.5'
            yield Request(url=json_url, callback=self.parse_json, meta={"category": category}, dont_filter=True)
        pass

    def parse_json(self, response):
        print('json')
        cnt = 0
        pretty_content = decode_zaker(response.text)

        # 检测爬取是否正确
        # with open('zaker.html', 'wb') as fp:
        #     fp.write(response.text.encode('utf-8'))
        #     fp.close()
        # # print(response.text.decode('unicode_escape'))

        next_url = pretty_content['data']['next_url']
        next_url = 'http:' + next_url
        num = len(pretty_content['data']['article'])
        for article in pretty_content['data']['article']:
            url = article['href']
            title = article['title']
            news_time = article["marks"][1]
            img_urls = article["img"]
            url = 'http:' + url
            summary = 'null'
            # 提取图片地址
            if len(img_urls) >= 1:
                pass
            else:
                img_urls = 'zkres.myzaker.com/static/zaker_web2/img/logo.png?v=20170726'

            category = response.meta.get("category", "")
            from_platform = self.from_platform

            crawl_time = datetime.datetime.now()
            try:
                crawl_time = datetime.datetime.strptime(crawl_time, "%Y/%m/%d").date()
            except Exception as e:
                crawl_time = datetime.datetime.now().date()
            finally:
                pass

            # 排除亲爱的会员这几种特殊情况
            if len(title) and len(url) and len(news_time) and len(img_urls):
                pass
            else:
                continue

            # 设置一个默认值，防止出错
            if len(news_time) >= 1:
                news_score = get_score(news_time)
            else:
                news_score = 1.0

            img_urls = 'http://'+ img_urls
            news_itemloader = ItemLoader(item=NewsItem(), response=response)
            news_itemloader.add_value("title", title)
            news_itemloader.add_value("image_urls", img_urls)
            news_itemloader.add_value("url", url)
            news_itemloader.add_value("url_md5", get_md5(url))
            news_itemloader.add_value("category", category)
            news_itemloader.add_value("summary", summary)
            news_itemloader.add_value("from_platform", from_platform)
            news_itemloader.add_value("news_time", news_time)
            news_itemloader.add_value("crawl_time", crawl_time)
            news_itemloader.add_value("news_score", news_score)
            news_item = news_itemloader.load_item()

            # # 测试json，减少数量
            # cnt = cnt + 1
            # if cnt == 2:
            #     break

            yield news_item

            pass

        depth = int(response.meta.get("depth", ""))
        if depth <= 3:
            yield Request(url=next_url, callback=self.parse_json, meta={"category": category}, dont_filter=True)

