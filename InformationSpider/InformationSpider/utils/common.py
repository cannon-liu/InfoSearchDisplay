# -*- coding = utf-8 -*-
__author__ = 'cannon'
__date__ = '2018/7/11 17:22'

import hashlib
import time
import re
import json

def get_score(news_time=""):
    score = 2.0
    if "分钟" in news_time:
        score = score - 0
    elif "小时" in news_time:
        score = score - 0.5
    elif "天" in news_time:
        score = score - 1
    elif "月" in news_time:
        score = score - 1.5
    else:
        score = 0.5

    return score


def get_md5(url):
    # str就是unicode了.Python3中的str对应2中的Unicode
    if isinstance(url, str):
        url = url.encode("utf-8")
    temp = type(url)
    url_md5 = hashlib.md5()
    url_md5.update(url)
    return url_md5.hexdigest()

def make_str(head,list_content):
    if isinstance(list_content, list):
        for index in range(len(list_content)):
            if isinstance(list_content[index], str):
                list_content[index] = head + list_content[index]
        return list_content


def del_str(head,list_content):
    if isinstance(list_content, list):
        for index in range(len(list_content)):
            if isinstance(list_content[index], str):
                list_content[index] = list_content[index].replace(head, '')
        return list_content


def tranfer_str(url):
    origin = ['%3A', '%2F', '%3F', '%3D', '%26']
    tranfer = [':', '/', '?', '=', '&']
    data_url = url
    for i, symbol in enumerate(origin):
        test = symbol
        temp_url = data_url.replace(symbol, tranfer[i])
        data_url = temp_url

    return data_url


def reverse_tranfer_str(url):
    origin = ['%3A', '%2F', '%3F', '%3D', '%26']
    tranfer = [':', '/', '?', '=', '&']
    data_url = url
    for i, symbol in enumerate(tranfer):
        test = symbol
        temp_url = data_url.replace(symbol, origin[i])
        data_url = temp_url

    return data_url


#提取zaker的json appid相关信息
def get_re_zaker(url):
    pattern_appid = 'app_id=(\d+)'
    pattern_date = 'since_date=(\d+)'
    pattern_article = 'next_aticle_id=(\w*)'
    pattern_stamp = 'otimestamp=(\d+)'
    pattern_tab = 'top_tab_id=(\d+)'
    pattern_version ='_version=(\d+\.\d+)'

    try:
        appid = re.search(pattern_appid, url).group(1)
        date = re.search(pattern_date, url).group(1)

        if re.search(pattern_article, url):
            article = re.search(pattern_article, url).group(1)
        else:
            article = None
        if re.search(pattern_stamp, url):
            stamp = re.search(pattern_stamp, url).group(1)
        else:
            stamp= None
        tab = re.search(pattern_tab, url).group(1)
        version = re.search(pattern_version, url).group(1)
    except Exception as e:
        print(e)
        print(url)

    kv = {
        "appid": appid,
        "date": date,
        "artcile": article,
        "stamp": stamp,
        "tab": tab,
        "version": version
    }
    return kv

def decode_zaker(content):

    # with open('zaker.txt', 'r') as fp:
    #     content = fp.read().encode('utf-8')
    #     fp.close()
    res = content
    pretty_content = json.loads(res)
    return pretty_content
    # url = pretty_content['data']['next_url']
    # num = len(pretty_content['data']['article'])
    # for article in pretty_content['data']['article']:
    #     href = article['href']
    #     title = article['title']
    #     news_time = article["marks"][1]
    #     img_url = article["img"]
    #     print(title)
    # print(url)
    # print(num)
    # pass




if __name__ == '__main__':
    now = time.time()*1000
    print(int(now))
    print(1531353641327)
    #
    # node =['list_123', 'list_456', 'list_789']
    # new=del_str('list_',node)
    # print(new)
    # url = 'http%3A%2F%2Fiphone.myzaker.com%2Fzaker%2Fblog2news.php%3Fapp_id%3D4%26since_date%3D1531291784%26nt%3D2%26next_aticle_id%3D5b462bb79490cbb83d000000%26_appid%3Diphone%26opage%3D3%26otimestamp%3D276%26top_tab_id%3D12183%26_version%3D6.5&_version=6.5'
    # temp = tranfer_str(url)

    # origin = 'http://iphone.myzaker.com/zaker/blog2news.php?app_id=4&since_date=1531291784&nt=2&next_aticle_id=5b462bb79490cbb83d000000&_appid=iphone&opage=3&otimestamp=276&top_tab_id=12183&_version=6.5&_version=6.5'
    # no_article = 'http://www.myzaker.com/news/home_new.php?f=myzaker_com&url=http://iphone.myzaker.com/zaker/blog2news.php?app_id=10296&since_date=1531350000&nt=1&_appid=iphone&top_tab_id=12183&_version=6.5&_version=6.5'
    # get_re_zaker(no_article)
    # test = reverse_tranfer_str(no_article)
    content = '{"data":{"article":[{"href":"\/\/www.myzaker.com\/article\/5b46f43e77ac645a7c63eda7\/","title":" \u9ec4\u6d66\u6c5f\u4e0a\u6700\u5927\u201c\u9f99\u8239\u201d\u5347\u7ea7\u540e\u56de\u5f52\uff01\u80fd\u5bb9\u7eb3\u5343\u540d\u6e38\u5ba2\uff0c650 \u4eba\u540c\u65f6\u7528\u9910 ","typeMark":"","marks":["\u4e0a\u89c2\u65b0\u95fb","21\u5c0f\u65f6\u524d"],"img":"\/\/zkres1.myzaker.com\/201807\/5b46f43f7f52e9e43c000186_320.jpg","comment_counts":0},{"href":"\/\/www.myzaker.com\/article\/5b46f4109490cb743d000024\/","title":" \u5f15\u53d1\u5a74\u513f\u4e0d\u9002\uff0c\u6d77\u5173\u603b\u7f72\uff1a\u8c28\u614e\u6d77\u6dd8\u7231\u4ed6\u7f8e\u5a74\u513f\u4e73\u7c89 ","typeMark":"","marks":["\u5c01\u9762\u65b0\u95fb","21\u5c0f\u65f6\u524d","2 \u8bc4\u8bba"],"img":"\/\/zkres3.myzaker.com\/201807\/aHR0cDovL3prcmVzLm15emFrZXIuY29tL2ltZ191cGxvYWQvY21zL2FydGljbGVfaW1nLzEwMTY5L3VwXzEwMTY5XzE1MzEzNjcwNjY5NDc4LmpwZw==_1242.jpg","comment_counts":0},{"href":"\/\/www.myzaker.com\/article\/5b46f4039490cbc33d00001d\/","title":" \u671f\u5f85\uff01\u592e\u884c 9 \u6708 3 \u65e5\u5c06\u53d1\u884c\u4e2d\u56fd\u9ad8\u94c1 10 \u5143\u7eaa\u5ff5\u5e01\uff01","typeMark":"","marks":["\u4e2d\u56fd\u4eba\u6c11\u94f6\u884c","21\u5c0f\u65f6\u524d","14 \u8bc4\u8bba"],"img":"\/\/zkres3.myzaker.com\/201807\/aHR0cDovL3prcmVzLm15emFrZXIuY29tL2ltZ191cGxvYWQvY21zL2FydGljbGVfaW1nLzEwMTY5L3VwXzEwMTY5XzE1MzEzNjc1MDY4NDYyLmpwZw==_1242.jpg","comment_counts":0},{"href":"\/\/www.myzaker.com\/article\/5b46f3ef9490cbd03d00001f\/","title":" \u5728\u8fd9\u5bb6\u706b\u9505\u5e97\uff0c\u6211\u7adf\u7136\u628a\u4e00\u9505\u6c64\u5e95\u90fd\u559d\u5149\u4e86\uff01","typeMark":"","marks":["\u7f51\u6613\u4e0a\u6d77\u7f8e\u98df","21\u5c0f\u65f6\u524d","1 \u8bc4\u8bba"],"img":"\/\/zkres1.myzaker.com\/201807\/5b46f3f5a07aec1b21023c47_320.jpg","comment_counts":0},{"href":"\/\/www.myzaker.com\/article\/5b46f58577ac645c3453c682\/","title":" \u590f\u65e5\u8d4f\u8377\u597d\u53bb\u5904 \u5bfb\u7740\u8377\u82b1\u5230\u677e\u6c5f\u65b0\u6d5c ","typeMark":"","marks":["\u4e1c\u65b9\u7f51","21\u5c0f\u65f6\u524d"],"img":"\/\/zkres1.myzaker.com\/201807\/5b46f4ed77ac645b995fa222_320.jpg","comment_counts":0},{"href":"\/\/www.myzaker.com\/article\/5b46f1d69490cb7e0d000010\/","title":" \u7eff\u8272\uff0c\u65e0\u516c\u5bb3\uff0c\u6709\u673a\uff0c\u975e\u8f6c\u57fa\u56e0\uff0c\u5343\u4e07\u522b\u518d\u5206\u4e0d\u6e05\u695a\u4e86 ","typeMark":"","marks":["\u7f51\u6613\u4e0a\u6d77\u7f8e\u98df","21\u5c0f\u65f6\u524d","2 \u8bc4\u8bba"],"img":"\/\/zkres1.myzaker.com\/201807\/5b46f1d8a07aec1b21023ba0_320.jpg","comment_counts":0},{"href":"\/\/www.myzaker.com\/article\/5b46d8e777ac64451e67fb15\/","title":" \u201c\u5973\u53cb\u201d\u501f\u5bbf\u540e\u987a\u8d70\u540d\u724c\u5305\u3001\u9ad8\u6863\u8868 \u53ea\u4e3a\u4e70 iPhone","typeMark":"","marks":["\u4e1c\u65b9\u7f51","21\u5c0f\u65f6\u524d","2 \u8bc4\u8bba"],"img":"\/\/zkres1.myzaker.com\/201807\/5b46d83e77ac64455b786cbc_320.jpg","comment_counts":0},{"href":"\/\/www.myzaker.com\/article\/5b46eb759490cb913d00001e\/","title":" \u7279\u65af\u62c9\u843d\u6237\u4e0a\u6d77\uff0c\u9a97\u8865\u7684\u8f66\u4f01\u5f00\u59cb\u98a4\u6296\u5427\uff01","typeMark":"","marks":["\u51b0\u5ddd\u601d\u4eab\u5e93","22\u5c0f\u65f6\u524d","9 \u8bc4\u8bba"],"img":"\/\/zkres1.myzaker.com\/201807\/5b46e09a7f52e98c04000029_320.jpg","comment_counts":0},{"href":"\/\/www.myzaker.com\/article\/5b46d37177ac6441032f3602\/","title":" \u5973\u5b50\u5e26\u7740\u5047\u51b0\u6bd2\u4e0e\u95fa\u871c\u4ea4\u6613\u88ab\u6293 \u6cd5\u9662\u4ee5\u8d29\u5356\u6bd2\u54c1\u7f6a\u5224\u5211 ","typeMark":"","marks":["\u770b\u770b\u65b0\u95fbKnews","22\u5c0f\u65f6\u524d","3 \u8bc4\u8bba"],"img":"\/\/zkres2.myzaker.com\/201807\/5b46d37077ac6441032f35fe_320.jpg","comment_counts":0},{"href":"\/\/www.myzaker.com\/article\/5b46dbff77ac6448a01fbce4\/","title":"391 \u5904\u5386\u53f2\u5efa\u7b51\u5c06\u53ef\u626b\u4e8c\u7ef4\u7801\u201c\u9605\u8bfb\u201d ","typeMark":"","marks":["\u65b0\u95fb\u6668\u62a5","23\u5c0f\u65f6\u524d"],"img":"","comment_counts":0},{"href":"\/\/www.myzaker.com\/article\/5b46d8e577ac64451e67fb12\/","title":" \u4e2d\u56fd\u56fd\u9645\u9752\u5c11\u5e74\u4fdd\u9f84\u7403\u516c\u5f00\u8d5b\u5728\u6caa\u4e3e\u884c ","typeMark":"","marks":["\u4e1c\u65b9\u7f51","23\u5c0f\u65f6\u524d","3 \u8bc4\u8bba"],"img":"\/\/zkres2.myzaker.com\/201807\/5b46d83d77ac64455b786cb5_320.jpg","comment_counts":0},{"href":"\/\/www.myzaker.com\/article\/5b46cd079490cba43d000030\/","title":" \u6700\u9ad8\u68c0\uff1a\u91d1\u878d\u72af\u7f6a\u4ecd\u5904\u591a\u53d1\u72b6\u6001 \u7591\u96be\u590d\u6742\u7a0b\u5ea6\u660e\u663e\u52a0\u5927 ","typeMark":"","marks":["\u4e2d\u65b0\u7f51","\u6628\u5929"],"img":"\/\/zkres1.myzaker.com\/201807\/5b46c9dc77ac643b27521d62_320.jpg","comment_counts":0},{"href":"\/\/www.myzaker.com\/article\/5b46c1dd9490cb8e3d000010\/","title":" \u4e0a\u6d77\u51fa\u65b0\u653f\uff0c\u7279\u65af\u62c9\u7b2c\u4e00\u4e2a\u201c\u62a5\u5230\u201d ","typeMark":"","marks":["\u653f\u77e5\u5c40","\u6628\u5929","3 \u8bc4\u8bba"],"img":"\/\/zkres1.myzaker.com\/201807\/5b46bc017f52e99c7900000a_320.jpg","comment_counts":0},{"href":"\/\/www.myzaker.com\/article\/5b46bde37f52e96704000000\/","title":" \u5feb\u8baf\uff01\u201c\u4e0a\u6d77\u6269\u5927\u5f00\u653e 100 \u6761\u201d\u653f\u7b56\u8981\u70b9\u516c\u5e03\uff01","typeMark":"","marks":["\u5927\u7533\u7f51","\u6628\u5929"],"img":"","comment_counts":0},{"href":"\/\/www.myzaker.com\/article\/5b46b84f9490cb8d3d000007\/","title":" \u5e95\u697c\u4f4f\u6237\u4e0d\u9501\u7a97 \u5609\u5b9a\u4e00\u76d7\u7a83\u56e2\u4f19\u4f5c\u6848 8 \u8d77\u7a83\u5f97 8 \u4e07\u5143 ","typeMark":"","marks":["\u4e1c\u65b9\u7f51","\u6628\u5929","1 \u8bc4\u8bba"],"img":"","comment_counts":0},{"href":"\/\/www.myzaker.com\/article\/5b46b7bc9490cba23d000001\/","title":" \u4e0a\u6d77\u5e02\u5e02\u7ba1\u5e72\u90e8\u63d0\u4efb\u524d\u516c\u793a\uff01\u8fd9\u4e24\u540d\u5e72\u90e8\u62df\u63d0\u4efb ","typeMark":"","marks":["\u4e0a\u6d77\u53d1\u5e03","\u6628\u5929","1 \u8bc4\u8bba"],"img":"\/\/zkres2.myzaker.com\/201807\/5b46b7bfa07aec1b21020cf9_320.jpg","comment_counts":0},{"href":"\/\/www.myzaker.com\/article\/5b46b79a9490cbab3d00000c\/","title":" \u8f66\u7a97\u5939\u4f4f\u7537\u5b69\u5de6\u624b\u81c2 \u6d88\u9632\u5b98\u5175 1 \u79d2\u89e3\u6551\u6210\u529f ","typeMark":"","marks":["\u65b0\u6c11\u665a\u62a5","\u6628\u5929"],"img":"\/\/zkres1.myzaker.com\/201807\/5b46b79ca07aec1b21020ccc_320.jpg","comment_counts":0},{"href":"\/\/www.myzaker.com\/article\/5b46b7289490cbae3d000009\/","title":" \u957f\u5b81\u5bb6\u534f\u201c\u4fdd\u59c6\u9ed1\u540d\u5355\u201d\u8bd5\u70b9 1 \u5e74\u53eb\u505c ","typeMark":"","marks":["\u89e3\u653e\u7f51","\u6628\u5929","6 \u8bc4\u8bba"],"img":"\/\/zkres1.myzaker.com\/201807\/5b46b729a07aec1b21020cbe_320.jpg","comment_counts":0},{"href":"\/\/www.myzaker.com\/article\/5b46b7789490cba53d00000b\/","title":" \u591a\u4f4d\u5e02\u6c11\u53cd\u6620\u901a\u8fc7\u6469\u62dc App \u9000\u6b3e\u201c\u5957\u8def\u6df1\u201d ","typeMark":"","marks":["\u4e1c\u65b9\u7f51","\u6628\u5929","8 \u8bc4\u8bba"],"img":"","comment_counts":0},{"href":"\/\/www.myzaker.com\/article\/5b46b6e19490cb8e3d00000a\/","title":" \u5927\u98ce\u5439\u8d77\u65bd\u5de5\u56f4\u680f \u7838\u4f24\u8fc7\u5f80\u884c\u4eba ","typeMark":"","marks":["\u5ba3\u514b\u7085","\u6628\u5929"],"img":"\/\/zkres1.myzaker.com\/201807\/5b46b6e3a07aec1b21020cb3_320.jpg","comment_counts":0},{"href":"\/\/www.myzaker.com\/article\/5b46b6b69490cb8c3d000010\/","title":" \u53f0\u98ce\u201c\u739b\u8389\u4e9a\u201d\u505c\u6b62\u7f16\u53f7\uff0c\u4e0a\u6d77\u660e\u8d77 4 \u5929\u6301\u7eed\u9ad8\u6e29\uff01","typeMark":"","marks":["\u4e0a\u6d77\u53d1\u5e03","\u6628\u5929","2 \u8bc4\u8bba"],"img":"\/\/zkres1.myzaker.com\/201807\/5b46b6b6a07aec1b21020ca4_320.jpg","comment_counts":0},{"href":"\/\/www.myzaker.com\/article\/5b46b6539490cba83d000006\/","title":" \u6d77\u5de1 01 \u548c\u4e1c\u6d77\u6551 101 \u52a9\u529b\u7b2c\u5341\u56db\u4e2a\u201c\u4e2d\u56fd\u822a\u6d77\u65e5\u201d ","typeMark":"","marks":["\u770b\u770b\u65b0\u95fb","\u6628\u5929"],"img":"\/\/zkres2.myzaker.com\/201807\/5b46124777ac647cf73eb7d4_320.jpg","comment_counts":0},{"href":"\/\/www.myzaker.com\/article\/5b46b6129490cb7b3d000011\/","title":" \u82a6\u6f6e\u6e2f\u6d77\u9c9c\u4e00\u6761\u8857\u53d1\u751f\u706b\u707e \u591a\u5bb6\u6d77\u9c9c\u5e97\u88ab\u6b83\u53ca ","typeMark":"","marks":["\u770b\u770b\u65b0\u95fb","\u6628\u5929","6 \u8bc4\u8bba"],"img":"\/\/zkres1.myzaker.com\/201807\/5b46b03e77ac6424f0637896_320.jpg","comment_counts":0},{"href":"\/\/www.myzaker.com\/article\/5b46b5949490cb7d3d000006\/","title":" \u6bcd\u5b50\u56e4\u79ef\u8fc7\u671f\u8d27\u6572\u8bc8\u8d85\u5e02 \u5148\u6df7\u8fdb\u8d27\u67b6\u518d\u53cd\u54ac\u4e00\u53e3 ","typeMark":"","marks":["\u770b\u770b\u65b0\u95fb","\u6628\u5929","1 \u8bc4\u8bba"],"img":"\/\/zkres2.myzaker.com\/201807\/5b460cd577ac6478514babc3_320.jpg","comment_counts":0},{"href":"\/\/www.myzaker.com\/article\/5b46b54a9490cbc63d000008\/","title":" \u4e0a\u6d77\u56fd\u9645\u6444\u5f71\u5668\u6750\u548c\u6570\u7801\u5f71\u50cf\u5c55\u89c8\u4f1a\u5f00\u5e55 ","typeMark":"","marks":["\u770b\u770b\u65b0\u95fb","\u6628\u5929"],"img":"\/\/zkres1.myzaker.com\/201807\/5b4608ed77ac64757556e8b5_320.jpg","comment_counts":0},{"href":"\/\/www.myzaker.com\/article\/5b46b51d9490cbb83d00000e\/","title":" \u827a\u672f\u5bb6\u5de5\u4f5c\u5ba4\u5165\u9a7b \u5b9d\u5c71\u6253\u9020\u516c\u5171\u6587\u5316\u670d\u52a1\u65b0\u6a21\u5f0f ","typeMark":"","marks":["\u770b\u770b\u65b0\u95fb","\u6628\u5929"],"img":"\/\/zkres1.myzaker.com\/201807\/5b46033177ac646fff315358_320.jpg","comment_counts":0},{"href":"\/\/www.myzaker.com\/article\/5b46b4fb9490cb9f3d000001\/","title":" \u7279\u65af\u62c9\u8d85\u7ea7\u5de5\u5382\u4e3a\u4f55\u9009\u5740\u5728\u8fd9\u91cc\uff1f","typeMark":"","marks":["\u770b\u770b\u65b0\u95fb","\u6628\u5929","2 \u8bc4\u8bba"],"img":"\/\/zkres2.myzaker.com\/201807\/5b45f5f077ac6455a55ff9d2_320.jpg","comment_counts":0},{"href":"\/\/www.myzaker.com\/article\/5b46b49d9490cbb13d000004\/","title":" \u534a\u5e74\u6d88\u9664 2 \u4e07\u591a\u5bb6\u65e0\u8bc1\u9910\u996e \u4e3a\u4f55\u4e3b\u52a8\u964d\u8f6c\u6b63\u95e8\u69db\uff1f","typeMark":"","marks":["\u770b\u770b\u65b0\u95fb","\u6628\u5929"],"img":"\/\/zkres2.myzaker.com\/201807\/5b45f5f177ac6455a55ff9d5_320.jpg","comment_counts":0},{"href":"\/\/www.myzaker.com\/article\/5b46b42c9490cb813d000009\/","title":" \u201c\u6c34 + \u58a8\u201d\u4eca\u5728\u4e0a\u6d77\u5b9d\u5c71\u56fd\u9645\u6c11\u95f4\u827a\u672f\u535a\u89c8\u9986\u5f00\u5e55 ","typeMark":"","marks":["\u770b\u770b\u65b0\u95fb","\u6628\u5929"],"img":"\/\/zkres2.myzaker.com\/201807\/5b45d21d77ac64751946fe12_320.jpg","comment_counts":0},{"href":"\/\/www.myzaker.com\/article\/5b46a90b9490cbc03d000006\/","title":" \u7279\u65af\u62c9\u4e0a\u6d77\u5de5\u5382\u6709\u671b 2 \u5e74\u5efa\u6210 \u5e74\u4ea7\u53ef\u8fbe 50 \u4e07\u8f86 ","typeMark":"","marks":["\u73af\u7403\u7f51","\u6628\u5929","2 \u8bc4\u8bba"],"img":"\/\/zkres1.myzaker.com\/201807\/5b46a80477ac641c276a9d12_320.jpg","comment_counts":0},{"href":"\/\/www.myzaker.com\/article\/5b46a8639490cb8e3d000004\/","title":" \u8fd9\u4e2a\u65f6\u95f4\u70b9\uff0c\u7279\u65af\u62c9\u6765\u4e86 ","typeMark":"","marks":["\u592e\u89c6\u65b0\u95fb","\u6628\u5929","16 \u8bc4\u8bba"],"img":"\/\/zkres1.myzaker.com\/201807\/5b46a570a07aec1b2101fefd_320.jpg","comment_counts":0},{"href":"\/\/www.myzaker.com\/article\/5b462de29490cb773d000000\/","title":" \u65e0\u9521\u9ad8\u6821\u88ab\u6307\u817e\u5bbf\u820d\u7ed9\u7559\u5b66\u751f \u5b66\u751f\u79f0\u201c\u4e0d\u95f9\u624d\u6709\u9b3c\u201d ","typeMark":"","marks":["\u6bcf\u65e5\u4eba\u7269","\u6628\u5929","135 \u8bc4\u8bba"],"img":"\/\/zkres3.myzaker.com\/201807\/aHR0cDovL3prcmVzLm15emFrZXIuY29tL2ltZ191cGxvYWQvZWRpdG9yL2ltZ191cGxvYWQvMjAxODA3MTIvdXBfMTUzMTMyNTc5N180MzUwOV9XNjQwSDM2MFMzNTc3MC5qcGc=_1242.jpg","comment_counts":0},{"href":"\/\/www.myzaker.com\/article\/5b45cdaa77ac6470840289e5\/","title":" \u6084\u65e0\u58f0\u606f\u201c\u6446\u8131\u201d\u67b6\u7a7a\u7ebf \u6b66\u5eb7\u8def\u5c06\u7115\u65b0\u989c \uff1f","typeMark":"","marks":["\u4e1c\u65b9\u7f51","\u6628\u5929","1 \u8bc4\u8bba"],"img":"\/\/zkres2.myzaker.com\/201807\/5b45cd6077ac64700b70ed83_320.jpg","comment_counts":0},{"href":"\/\/www.myzaker.com\/article\/5b45c9e09490cb391800001e\/","title":" \u5f90\u6c47\u4e00\u5973\u5b50\u8fdd\u505c\u6015\u88ab\u7f5a \u62c6\u5378\u724c\u7167\u88ab\u6263 12 \u5206 ","typeMark":"","marks":["\u65b0\u6c11\u665a\u62a5","\u6628\u5929","8 \u8bc4\u8bba"],"img":"","comment_counts":0},{"href":"\/\/www.myzaker.com\/article\/5b45c8a89490cb5f18000018\/","title":" \u9b54\u90fd\u8212\u8299\u857e\u5730\u56fe\uff0c\u7a0d\u7eb5\u5373\u901d\u7684\u7231\u5c31\u662f\u5b83\uff01","typeMark":"","marks":["Shanghai WOW","\u6628\u5929"],"img":"\/\/zkres1.myzaker.com\/201807\/5b45c8b0a07aec1b21019e87_320.jpg","comment_counts":0}],"next_url":"\/\/www.myzaker.com\/news\/next_new.php?f=myzaker_com&url=http%3A%2F%2Fiphone.myzaker.com%2Fzaker%2Fblog2news.php%3Fapp_id%3D10001%26since_date%3D1531300029%26nt%3D2%26_appid%3Diphone%26top_tab_id%3D12183%26_version%3D6.5&_version=6.5"},"stat":1}'
    pretty_content = decode_zaker(content)
    pass

