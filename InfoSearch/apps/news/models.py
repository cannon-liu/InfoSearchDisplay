from django.db import models
from datetime import datetime
from elasticsearch_dsl import DocType,Date,Nested,Boolean,analyzer,InnerObjectWrapper,Completion,Keyword,Text
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl.analysis import CustomAnalyzer as MyCustomAnalyzer

# Create your models here.




#与elasticsearch服务器进行连接，允许多个
connections.create_connection(hosts=["localhost"])

class CustomAnalyzer(MyCustomAnalyzer):
    def get_analysis_definition(self):
        return {}

ik_analyzer = CustomAnalyzer("ik_max_word",filter="['lowercase']")


class NewsType(DocType):
    title = Text(analyzer="ik_max_word")
    suggest = Completion(analyzer=ik_analyzer)
    url = Keyword()
    url_md5 = Keyword()
    category = Text(analyzer="ik_smart")
    summary = Text(analyzer="ik_smart")
    image_urls = Keyword()
    image_path = Keyword()
    from_platform = Keyword()
    news_time = Keyword()
    crawl_time = Date()
    news_score = Keyword()
    class Meta:
        index = "information"
        doc_type = "news"


if __name__ == "__main__":
    NewsType.init()
    pass
