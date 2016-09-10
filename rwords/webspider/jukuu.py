#!/usr/bin/env python3

import sys
import urllib.request
import re
import socket

import time

# 用来加密单词的js

# 从句酷网爬取例句
class WebSpider:
    # 网站地址
    website_url = 'http://dict.youdao.com/search?q=lj:%s&ljblngcont=0&le=eng'
    opener = None
    content = None
    resp = None

    def get_example(self, word):
        print('finding example of word "%s"...' % word)
        self.opener = urllib.request.build_opener()
        self.opener.addheaders = [
            ('User-agent',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'),
        ]
        socket.setdefaulttimeout(15)
        re_cnt = 0
        self.content = ''
        pattern = re.compile('<span.*?>|</span>|\s\s+', re.S|re.M)
        while re_cnt <= 20:
            try:
                self.resp = self.opener.open(self.website_url % word)
                self.content = self.resp.read().decode()
                self.content = pattern.sub('', self.content)
                pattern = re.compile('<li>.*?<p>(.*?)<a class=\"sp dictvoice.*?<p>(.*?)</p>', re.S|re.M)
                break
            except Exception:
                print('连接失败，正在尝试重新连接')
                re_cnt += 1

        time.sleep(55)
        return pattern.findall(self.content)[:-1]


if __name__ == '__main__':
    word = input()
    web = WebSpider()
    for s in web.get_example(word):
        print(s)

