# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst

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


