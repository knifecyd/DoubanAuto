# -*- coding: utf-8 -*-
import random
import time
import sys
sys.path.append("../")

from group import comment
from config import doubanurl

from util import doubanutil


if __name__ == "__main__":

    group_id = ""
    group_url = doubanurl.DOUBAN_GROUP + group_id
    #  r = requests.get(group_url, cookies=doubanutil.get_cookies())
    #  group_topics_html = etree.HTML(r.text)
    #  group_topics = group_topics_html.xpath(
    #      "//table[@class='olt']/tr/td[@class='title']/a/@href")
    #  group_topics = group_topics[5:]
    # for topic_url in group_topics:

    topiclist = doubanutil.get_topics()

    for k in topiclist:
        assert isinstance(k, object)
        print "topics : " + k

    count = 20

while count > 0:
    # test_header = doubanutil.get_header()
    # for  i  in test_header:
    #    print  "header[%s] = " % i , test_header[i]  
    for tp in topiclist:
        topic_url = tp
        print "the processing topics url is :[%s]" % tp
        comment_topic_url = topic_url + "/add_comment#last"
        comment_str = "up" + "%d" % random.randint(100, 500)
        #无验证码使用
        # comment_dict = comment.make_comment_dict(topic_url, comment_str)
        #使用tesseract识别验证码
        comment_dict = comment.make_comment_dicts_by_ocr(topic_url, comment_str)
        for k in comment_dict:
            print "comment_dict[%s]=" % k, comment_dict[k]\

        comment.comment_topic(comment_topic_url, comment_dict)
        
        random_sleep = random.randint(10, 50)
        time.sleep(random_sleep)
        count = count - 1

print "the autoComment is finished"
