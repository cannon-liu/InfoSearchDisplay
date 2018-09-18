# -*- coding = utf-8 -*-
__author__ = 'cannon'
__date__ = '2018/7/15 10:46'

import scrapy
from scrapy.selector import Selector
import redis

redis_client = redis.StrictRedis(host="localhost")

def parse_test():


    print('more')
    with open('qq_news.html', 'r') as fp:
        html = fp.read()
        fp.close()

    cnt = 0
    response = Selector(text=html)
    div_xpath = '//div[@id="List"]//ul[@class="list"]/li[@class="item cf" or "item-pics cf"]'
    title_pics_xpath = 'h3/a/text()'
    title_xpath = 'div[@class="detail"]/h3/a/text()'
    url_xpath = 'h3/a/@href or div[@class="detail"]/h3/a/@href'
    # summary_xpath = 'p/text()'
    image_url_xpath = 'div[@class="picture" or "fl picture"]//img[1]/@src'
    news_time_xpath = 'div[@class="detail"]//span[@class="time"]/text()'
    re_selectors = response.xpath(div_xpath)

    for re_selector in re_selectors:
        item_type = re_selector.xpath('@class').extract()[0]
        if item_type == "item cf":
            title = re_selector.xpath(title_xpath).extract()
        else:
            title_xpath = re_selector.xpath(title_pics_xpath).extract()
        url = re_selector.xpath(url_xpath).extract()
        # url_md5 = get_md5(url)
        summary = ''
        # 提取图片地址
        temp_urls = re_selector.xpath(image_url_xpath).extract()
        if len(temp_urls) >= 1:
            img_urls = 'http:' + temp_urls[0]
        else:
            img_urls = 'https://mat1.gtimg.com/pingjs/ext2020/newom/build/static/images/new_logo.png'

        # category = response.meta.get("category", "")
        # from_platform = self.from_platform
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



if __name__ == '__main__':

    print('##############')
    redis_client.incr('news_count')