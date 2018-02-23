# -*- coding: utf-8 -*-
import random
import time
import requests
from lxml import etree

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
    

    count = 10 

while (count > 0): 
    test_header = doubanutil.get_header()
    
    #for  i  in test_header:
    #    print  "header[%s] = " % i , test_header[i]  
    
    topic_url= "https://www.douban.com/group/topic/112873079"
    comment_topic_url = topic_url + "/add_comment#last"
    comment_str = "up" + "%d"%random.randint(100,500)
    #comment_str = "uAp" 
    comment_dict = comment.make_comment_dict(topic_url, comment_str)
    for  i in  comment_dict: 
	print  "comment_dict[%s]=" % i,comment_dict[i]
    comment.comment_topic(comment_topic_url, comment_dict)
    #comment.comment_post(comment_topic_url, test_header, comment_dict)
    
    random_sleep = random.randint(100, 500)
    time.sleep(random_sleep)
    count  = count - 1


print  " the  autoComment is finished "


