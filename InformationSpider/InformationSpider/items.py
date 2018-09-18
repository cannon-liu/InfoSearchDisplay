# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst
from InformationSpider.models.es_news import NewsType
import redis

from elasticsearch_dsl.connections import connections
es = connections.create_connection(NewsType._doc_type.using)

redis_client = redis.StrictRedis(host="localhost")


def gen_suggests(index, info_tuple):
    #根据字符串生成搜索建议数组
    #先来先到，已经用过的字符串不使用，通过set()来去重
    used_words = set()
    suggests = []
    for text, weight in info_tuple:
        if text:
            #调用es的analyze接口分析字符串
            words = es.indices.analyze(index=index, analyzer="ik_max_word", params={'filter':["lowercase"]}, body=text)
            anylyzed_words = set([r["token"] for r in words["tokens"] if len(r["token"])>1])
            new_words = anylyzed_words - used_words
            used_words = used_words|new_words
        else:
            new_words = set()

        if new_words:
            suggests.append({"input":list(new_words), "weight":weight})

    return suggests



class InformationspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class NewsItem(scrapy.Item):
    title = scrapy.Field(
        output_processor=TakeFirst()
    )
    url = scrapy.Field(
        output_processor=TakeFirst()
    )
    url_md5 = scrapy.Field(
        output_processor=TakeFirst()
    )
    category = scrapy.Field(
        output_processor=TakeFirst()
    )
    summary = scrapy.Field(
        output_processor=TakeFirst()
    )
    image_urls = scrapy.Field()
    image_path = scrapy.Field()

    from_platform = scrapy.Field(
        output_processor=TakeFirst()
    )
    news_time = scrapy.Field(
        output_processor=TakeFirst()
    )
    crawl_time = scrapy.Field(
        output_processor=TakeFirst()
    )
    news_score = scrapy.Field(
        output_processor=TakeFirst()
    )

    def get_insert_sql(self):
        insert_sql = """
            insert into news(title, url, url_md5,category,summary,image_urls, image_path, from_platform, news_time, crawl_time, news_score)
            VALUES (%s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE news_time=VALUES(news_time),crawl_time=VALUES(crawl_time)
        """
        params = (
            self["title"],
            self["url"],
            self["url_md5"],
            self["category"],
            self["summary"],
            self["image_urls"],
            self["image_path"],
            self["from_platform"],
            self["news_time"],
            self["crawl_time"],
            self["news_score"],
        )
        return insert_sql, params

    def save_to_es(self):
        # 新闻类型
        news = NewsType()
        news.title = self["title"]
        news.url = self["url"]
        news.url_md5 = self["url_md5"]
        news.category = self["category"]
        news.summary = self["summary"]
        news.image_urls = self["image_urls"]
        news.image_path = self["image_path"]
        news.from_platform = self["from_platform"]
        news.news_time = self["news_time"]
        news.crawl_time = self["crawl_time"]
        news.news_score = self["crawl_time"]
        news.suggest = gen_suggests(index=NewsType._doc_type.index, info_tuple=((news.title,10),(news.summary,3)))

        redis_client.incr('news_count')

        news.save()


class JobItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    department = scrapy.Field()
    salary = scrapy.Field()
    city = scrapy.Field()
    work_years = scrapy.Field()
    education = scrapy.Field()
    work_type = scrapy.Field()
    tags = scrapy.Field()
    publish_time = scrapy.Field()
    crawl_time = scrapy.Field()
    platform = scrapy.Field()
    description = scrapy.Field()
    work_requirements = scrapy.Field()
    address = scrapy.Field()
    company_name = scrapy.Field()
    company_profession = scrapy.Field()
    company_level = scrapy.Field()
    staff_nums = scrapy.Field()
    homepage = scrapy.Field()


