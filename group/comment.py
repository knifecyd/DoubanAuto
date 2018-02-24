# -*- coding: utf-8 -*-
import requests

from util import doubanutil
from util import tools
from verifycode import wordrecognition


def comment_topic(topic_url, comment_dict):
    # 在一个帖子下发表回复

    # doubanutil.get_cookies_as_strings()

    r = requests.post(topic_url, cookies=doubanutil.get_cookies(), data=comment_dict)
    # doubanutil.logger.info("in func comment_topic(), " + str(comment_dict) + "| status_code: " + str(r.status_code)
    #   +  " , the content :  "  +  str(r.text))
    doubanutil.logger.info(
        "in func comment_topic(), " + str(comment_dict) + "| status_code: " + str(r.status_code) + " ")
    return r


def comment_post(url, _header, _data):
    r = requests.post(url, headers=_header, data=_data)
    # doubanutil.logger.info("in func comment_topic(), " + str(_data) +   ",
    # header : " + str(_header) +  "| status_code: " + str(r.status_code)  +  " ")
    doubanutil.logger.info("in comment_topic(), " + str(_data) + "| status_code: " + str(r.status_code) + " ")
    return r


def make_comment_dicts(topic_url, rv_comment):
    # type: (object, object) -> object
    # 组装回帖的参数

    pic_url, pic_id = doubanutil.get_verify_code_pic(topic_url)
    verify_code = ""
    if len(pic_url):
        pic_path = tools.save_pic_to_disk(pic_url)
        verify_code = wordrecognition.get_word_in_pic(pic_path)
    comment_dict = {
        "ck": doubanutil.get_form_ck_from_cookie(),
        "rv_comment": rv_comment,
        "start": 0,
        "captcha-solution": verify_code,
        "captcha-id": pic_id,
        "submit_btn": u"发送"
    }
    return comment_dict


def make_comment_dict(topic_url, rv_comment):

    comment_dict = {
        "ck": doubanutil.get_form_ck_from_cookie(),
        "rv_comment": rv_comment,
        "start": 0,
        "submit_btn": u"发送"
    }
    return comment_dict
