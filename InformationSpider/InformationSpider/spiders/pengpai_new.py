# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse
import datetime
from scrapy.loader import ItemLoader


#self package
from InformationSpider.utils.common import get_score, get_md5, make_str, del_str
from InformationSpider.items import NewsItem

class PengpaiNewSpider(scrapy.Spider):
    name = 'pengpai_new'
    allowed_domains = ['thepaper.cn']
    start_urls = ['https://www.thepaper.cn/']
    from_platform = '澎湃'

    custom_settings = {
        "COOKIES_ENABLED": False,
        "DOWNLOAD_DELAY": 20,
        'DEFAULT_REQUEST_HEADERS': {
            # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            # 'Cookie': 'JSESSIONID=ABAAABAAAFCAAEGBC99154D1A744BD8AD12BA0DEE80F320; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; _ga=GA1.2.1111395267.1516570248; _gid=GA1.2.1409769975.1516570248; user_trace_token=20180122053048-58e2991f-fef2-11e7-b2dc-525400f775ce; PRE_UTM=; LGUID=20180122053048-58e29cd9-fef2-11e7-b2dc-525400f775ce; index_location_city=%E5%85%A8%E5%9B%BD; X_HTTP_TOKEN=7e9c503b9a29e06e6d130f153c562827; _gat=1; LGSID=20180122055709-0762fae6-fef6-11e7-b2e0-525400f775ce; PRE_HOST=github.com; PRE_SITE=https%3A%2F%2Fgithub.com%2Fconghuaicai%2Fscrapy-spider-templetes; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2F4060662.html; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1516569758,1516570249,1516570359,1516571830; _putrc=88264D20130653A0; login=true; unick=%E7%94%B0%E5%B2%A9; gate_login_token=3426bce7c3aa91eec701c73101f84e2c7ca7b33483e39ba5; LGRID=20180122060053-8c9fb52e-fef6-11e7-a59f-5254005c3644; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1516572053; TG-TRACK-CODE=index_navigation; SEARCH_ID=a39c9c98259643d085e917c740303cc7',
            # 'Host': 'www.myzaker.com',
            # 'Origin': 'https://www.lagou.com',
            # 'Referer': 'http://www.myzaker.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            # 'X - Requested - With':'XMLHttpRequest',

        }
    }

    def start_requests(self):
        origin_url = 'https://www.thepaper.cn/'
        yield Request(url=origin_url, callback=self.parse_category)

    def parse(self, response):
        pass


    def parse_category(self,response):
        print('category')
        category_xpath = '//div[@class="head_banner"]/div[@class="bn_bt index" or "bn_bt"]'
        name_xpath = 'a/text()'
        url_xpath = 'a/@href'
        node_xpath = 'div[@class="slider"]/ul/li/a/@href'

        category_selectors = response.xpath(category_xpath)
        pass_word = ('视频', '订阅', '问吧', '问政')

        for category_selector in category_selectors:
            name = category_selector.xpath(name_xpath).extract()[0]
            url = category_selector.xpath(url_xpath).extract()[0]
            category_url = parse.urljoin(response.url, url)
            #去掉不需要的栏目
            if name in pass_word:
                continue
            else:
                pass
            if name == '精选':
                node = '25949'

            else:
                node_ids = category_selector.xpath(node_xpath).extract()
                node = ','.join(del_str(head='list_', list_content=node_ids)) + ','
            yield Request(url=category_url, callback=self.parse_detail, meta={"category": name, 'nodeids': node}, dont_filter=True)

    def parse_detail(self, response):
        print("detail")
        div_xpath = '//div[@class="newsbox"]/div[@class="news_li xh-highlight" or "news_li"]'
        title_xpath = 'h2/a/text()'
        url_xpath = 'h2/a/@href'
        summary_xpath = 'p/text()'
        image_url_xpath = 'div[@class="news_tu"]/a/img/@src'
        news_time_xpath = 'div[@class="pdtt_trbs"]/span[1]/text()'

        # topCid1_xpath = '//div[@class="pdtt01"]/div[@class="pdtt_lt"]/a[@class="tiptitleImg"]/@data-id'
        # topCid23_xpath = '//div[@class="newsbox"]/div[@class="news_li xh-highlight" or "news_li"]/div/a/@data-id'
        # # test_xpath = '//div[@id="masonryContent"]/div[@id="cont2257855"]/div[@class="news_tu"]/a[@class="tiptitleImg"]'
        # lasttime_xpath = '//div[@class="newsbox"]/div[@class="news_li" and @id="last1"]/@lasttime'
        # topCid1 = response.xpath(topCid1_xpath).extract()[0]
        # topCid2 = response.xpath(topCid23_xpath).extract()[0]
        # topCid3 = response.xpath(topCid23_xpath).extract()[1]
        # last_time = response.xpath(lasttime_xpath).extract()[0]
        # topCids = []
        # topCids.append(topCid1)
        # topCids.append(topCid2)
        # topCids.append(topCid3)
        # topCid = ','.join(topCids)
        #
        # kv = {"category": name, "nodeids": node, "time": last_time, "topCids": topCid}


        cnt = 0
        re_selectors = response.xpath(div_xpath)
        for re_selector in re_selectors:
            title = re_selector.xpath(title_xpath).extract()
            url = re_selector.xpath(url_xpath).extract()
            # url_md5 = get_md5(url)
            temp_summary = re_selector.xpath(summary_xpath).extract()
            if len(temp_summary)>=1:
                summary = temp_summary
            else:
                summary = ''
            img_urls = re_selector.xpath(image_url_xpath).extract()
            category = response.meta.get("category", "")
            from_platform = self.from_platform
            news_time = re_selector.xpath(news_time_xpath).extract()
            try:
                crawl_time = datetime.datetime.strptime(crawl_time, "%Y/%m/%d").date()
            except Exception as e:
                crawl_time = datetime.datetime.now().date()

            # 检测爬取是否正确
            with open('pengpai_test.html', 'wb') as fp:
                fp.write(response.text.encode('utf-8'))
                fp.close()

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

            base_url = 'https://www.thepaper.cn/'
            img_url = make_str('http:', img_urls)
            news_itemloader = ItemLoader(item=NewsItem(), response=response)
            news_itemloader.add_value("title", title)
            news_itemloader.add_value("image_urls", img_url)
            news_itemloader.add_value("url", parse.urljoin(base_url, url[0]))
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




        node = response.meta.get("nodeids","")
        index_add = 2
        if node != "":
            for i in range(2):
                page = i+2
                if category == '精选':
                    json_url = 'https://www.thepaper.cn/load_chosen.jsp?nodeids={0}&pageidx={1}'.format(node, page)
                else:
                    json_url = 'https://www.thepaper.cn/load_index.jsp?nodeids={0}&pageidx={1}'.format(node, page)
                yield Request(url=json_url, callback=self.parse_json, meta={"category": category}, dont_filter=True)


    def parse_json(self, response):
        print("json")
        div_xpath = '//div[@class="news_li xh-highlight" or "news_li"]'
        title_xpath = 'h2/a/text()'
        url_xpath = 'h2/a/@href'
        summary_xpath = 'p/text()'
        image_url_xpath = 'div[@class="news_tu"]/a/img/@src'
        news_time_xpath = 'div[@class="pdtt_trbs"]/span[1]/text()'

        cnt = 0
        re_selectors = response.xpath(div_xpath)
        for re_selector in re_selectors:
            title = re_selector.xpath(title_xpath).extract()
            url = re_selector.xpath(url_xpath).extract()
            # url_md5 = get_md5(url)
            summary = re_selector.xpath(summary_xpath).extract()
            img_urls = re_selector.xpath(image_url_xpath).extract()
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
            base_url = 'https://www.thepaper.cn/'
            img_url = make_str('http:', img_urls)
            news_itemloader = ItemLoader(item=NewsItem(), response=response)
            news_itemloader.add_value("title", title)
            news_itemloader.add_value("image_urls", img_url)
            news_itemloader.add_value("url", parse.urljoin(base_url, url[0]))
            news_itemloader.add_value("url_md5", get_md5(url[0]))
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















