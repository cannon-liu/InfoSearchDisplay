# -*- coding = utf-8 -*-
__author__ = 'cannon'
__date__ = '2018/7/16 13:38'

import scrapy
from scrapy.selector import Selector
import requests
import time
import random
import datetime
import MySQLdb


Xici_header={
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    # 'Cookie': 'JSESSIONID=ABAAABAAAFCAAEGBC99154D1A744BD8AD12BA0DEE80F320; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; _ga=GA1.2.1111395267.1516570248; _gid=GA1.2.1409769975.1516570248; user_trace_token=20180122053048-58e2991f-fef2-11e7-b2dc-525400f775ce; PRE_UTM=; LGUID=20180122053048-58e29cd9-fef2-11e7-b2dc-525400f775ce; index_location_city=%E5%85%A8%E5%9B%BD; X_HTTP_TOKEN=7e9c503b9a29e06e6d130f153c562827; _gat=1; LGSID=20180122055709-0762fae6-fef6-11e7-b2e0-525400f775ce; PRE_HOST=github.com; PRE_SITE=https%3A%2F%2Fgithub.com%2Fconghuaicai%2Fscrapy-spider-templetes; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2F4060662.html; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1516569758,1516570249,1516570359,1516571830; _putrc=88264D20130653A0; login=true; unick=%E7%94%B0%E5%B2%A9; gate_login_token=3426bce7c3aa91eec701c73101f84e2c7ca7b33483e39ba5; LGRID=20180122060053-8c9fb52e-fef6-11e7-a59f-5254005c3644; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1516572053; TG-TRACK-CODE=index_navigation; SEARCH_ID=a39c9c98259643d085e917c740303cc7',
    'Host': 'www.xicidaili.com',
    # 'Origin': '',
    'Referer':'http://www.xicidaili.com/',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'Upgrade-Insecure-Requests':'1'

}

class Get_XiciIP(object):
    def __init__(self):
        self.xici_session = requests.Session()
        self.conn = MySQLdb.connect(
            host="127.0.0.1",
            user="root",
            passwd="123456",
            db="informationspider",
            charset="utf8")
        self.cursor = self.conn.cursor()

    def get_ip(self, page=10):

        for num in range(page):
            if num == 0:
                url = 'http://www.xicidaili.com/nn/'
                refer = 'http://www.xicidaili.com/'
            elif num == 1:
                url = 'http://www.xicidaili.com/nn/{0}'.format(num+1)
                refer = 'http://www.xicidaili.com/nn/'
            else:
                url = 'http://www.xicidaili.com/nn/{0}'.format(num+1)
                refer = 'http://www.xicidaili.com/nn/{0}'.format(num)


            Xici_header['Referer'] = refer
            responce = self.xici_session.get(url=url, headers=Xici_header)

            if responce.status_code == 200:
                print('第{0}次OK'.format(num+1))
                responce_text = responce.text
                html = Selector(text=responce.text)

                tr_xpath = '//div[@id="body"]/table[@id="ip_list"]//tr'
                ip_xpath = 'td[2]/text()'
                port_xpath = 'td[3]/text()'
                address_xpath = 'td[4]/a/text()'
                type_xpath = 'td[6]/text()'
                is_valid = 0

                re_selectors = html.xpath(tr_xpath)
                for re_selector in re_selectors:
                    # if re_selector.xpath(ip_xpath)[0] == 'IP地址':
                    #     continue
                    ip = re_selector.xpath(ip_xpath).extract()
                    port = re_selector.xpath(port_xpath).extract()
                    address = re_selector.xpath(address_xpath).extract()
                    type = re_selector.xpath(type_xpath).extract()
                    if len(ip) and len(port) and len(address) and len(type):
                        proxy = type[0].lower() + '://' + ip[0] + ':' + port[0]
                        if self.check_ip(proxy):
                            is_valid = 1
                            self.insert_proxy(proxy, address[0], is_valid)
                        else:
                            continue
                    time.sleep(random.randint(3, 6))

            pass



    def check_ip(self,proxy):
        test_url = 'https://www.baidu.com'
        proxy_dict = {
            "http": proxy,
        }
        res = self.xici_session.get(url=test_url, proxies=proxy_dict)
        if res.status_code == 200:
            is_valid = 1
            return is_valid
        else:
            is_valid = 0
            return is_valid

    def insert_proxy(self,proxy,address,is_valid):

        insert_sql = "insert proxy_ip(proxy, address,is_valid) VALUES ('{0}', '{1}', '{2}')".format(proxy, address, is_valid)
        self.cursor.execute(insert_sql)
        self.conn.commit()

    def delete_proxy(self,proxy):
        delete_sql = """
            delete from proxy_ip where proxy='{0}'
        """.format(proxy)
        self.cursor.execute(delete_sql)
        self.conn.commit()

    def get_random_ip(self,cnt=10):

        if cnt == 0:
            raise Exception("No_proxy_valid!")

        # 从数据库中随机获取一个可用的ip
        random_sql = """
              SELECT proxy,address FROM proxy_ip WHERE is_valid = TRUE 
            ORDER BY RAND()
            LIMIT 1
            """
        temp = self.cursor.execute(random_sql)
        results = self.cursor.fetchall()
        if results == None:
            raise Exception("No_proxy_exist!")

        for res in results:
            proxy = res[0]
            address = res[1]

        if self.check_ip(proxy):
            return proxy
        else:
            self.delete_proxy(proxy)
            cnt = cnt - 1
            return self.get_random_ip(cnt)




if __name__ == '__main__':
    xici = Get_XiciIP()
    test_proxy = 'http://122.114.31.177:808'
    random_proxy = xici.delete_proxy(test_proxy)
    pass


