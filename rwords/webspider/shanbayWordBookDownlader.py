#!/usr/bin/env python3
from http import cookiejar

import sys
import urllib.request
import re
import pickle
import socket

class WebSpider:
    # 登录地址
    login_url = "https://www.shanbay.com/accounts/login/"
    # 单词书id
    wordbook_id = 2
    # 单词表地址
    wordlist_url = []
    # 保存地址
    save_path = 'dict.dat'

    word_dict = {}
    cj = cookiejar.CookieJar()

    opener = None

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def login_shanbay(self):
        self.cj = cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cj))
        self.opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36')]
        resp = self.opener.open(self.login_url)
        csrftokenvalue = ''
        for c in self.cj:
            print(c.name, '===', c.value)
            if c.name == 'csrftoken':
                csrftokenvalue = c.value

        post_data = {
            'username': self.username,
            'password': self.password,
            'csrfmiddlewaretoken': csrftokenvalue
        }

        print(post_data)
        post_data = urllib.parse.urlencode(post_data)
        post_data = post_data.encode('utf-8')
        resplogin = self.opener.open(self.login_url, data=post_data)
        for c in self.cj:
            print(c.name, '===', c.value)

    def get_all_wordlist(self):
        res_word_book = self.opener.open('https://www.shanbay.com/wordbook/%d/' % self.wordbook_id)
        data = res_word_book.read().decode()
        pat = re.compile(
            "<td class=\"wordbook-wordlist-name\">.*?<a href=\"(/wordlist/\d+/\d+/)\".*?<span>.*?(\d+)",
            re.S | re.M
        )
        for d in pat.findall(data):
            url = 'https://www.shanbay.com' + d[0]
            page = int(d[1]) // 20
            if int(d[1]) % 20:
                page += 1
            self.wordlist_url.append((url, page))

    def run(self):
        self.login_shanbay()
        self.get_all_wordlist()

        print(self.wordlist_url)

        socket.setdefaulttimeout(15)
        for list_url in self.wordlist_url:
            wordlist_url = list_url[0]
            page_num = list_url[1]
            print('now crawling %s, which have %d pages\n' % (wordlist_url, page_num))
            for i in range(1, page_num + 1):
                nowurl = wordlist_url + '?page=%d' % i
                while True:
                    try:
                        print('opening page %s' % nowurl)
                        res = self.opener.open(nowurl)
                        data = res.read().decode()
                        break
                    except Exception:
                        print('time out.\nnow trying again')
                words = self.get_words_list(data)
                for word in words:
                    self.word_dict[word[0]] = word[1]
                    print('add word:\n %s\n%s\n' % (word[0], word[1]))

        # 保存到文件
        with open(self.save_path, 'wb') as f:
            pickle.dump(self.word_dict, f)
            print('save finished, %d words.' % len(self.word_dict))

    def get_words_list(self, content):
        pat = re.compile(
            "<td class=\"span2\">.*?<strong>(.*?)</strong>.*?<td class=\"span10\">(.*?)</td>",
            re.S | re.M
        )
        return pat.findall(content)


if __name__ == '__main__':
    if len(sys.argv) < 5:
        print('arguments error!')
    username = sys.argv[1]
    password = sys.argv[2]
    spider = WebSpider(username, password)
    spider.wordbook_id = int(sys.argv[3])
    spider.save_path = sys.argv[4]
    spider.run()

