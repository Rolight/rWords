#!/usr/bin/env python3

import sys
import urllib.request
import re
import socket
# 从synonym.com爬取近义词
class WebSpider:
    # 网站地址
    website_url = 'http://www.synonym.com/synonyms/%s'

    opener = None
    content = None
    resp = None

    def get_synonym(self, word):
        print('finding synonyms of word "%s"' % word)
        self.opener = urllib.request.build_opener()
        self.opener.addheaders = [
            ('User-agent',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36')]
        socket.setdefaulttimeout(15)
        re_cnt = 0
        self.content = []
        while re_cnt <= 20:
            try:
                self.resp = self.opener.open(self.website_url % word)
                self.content = self.resp.read().decode()
                pattern = re.compile(
                    '<li class="syn">.*?<a href=".*?">(.*?)</a>',
                    re.S | re.M
                )
                print('finished')
                break
            except Exception:
                print('连接失败，正在尝试重新连接')
                re_cnt += 1


        return pattern.findall(self.content)[:5]


if __name__ == '__main__':
    word = input()
    web = WebSpider()
    web.get_example(word)
