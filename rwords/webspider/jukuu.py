#!/usr/bin/env python3

import sys
import urllib.request
import re
import socket
# 从句酷网爬取例句
class WebSpider:
    # 网站地址
    website_url = 'http://www.jukuu.com/search.php?q=%s'

    opener = None
    content = None
    resp = None

    def get_example(self, word):
        self.opener = urllib.request.build_opener()
        self.opener.addheaders = [
            ('User-agent',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36')]
        socket.setdefaulttimeout(15)
        while True:
            try:
                self.resp = self.opener.open(self.website_url % word)
                self.content = self.resp.read().decode()
                break
            except Exception:
                print('连接失败，正在尝试重新连接')

        pattern = re.compile(
            '<tr class=e.*?</td><td>(.*?)</td>.*?<tr class=c>.*?</td><td>(.*?)</td>',
            re.S | re.M
        )
        return pattern.findall(self.content)


if __name__ == '__main__':
    word = input()
    web = WebSpider()
    web.get_example(word)
