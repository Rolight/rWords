#!/usr/bin/env python3

# 自动更新数据库
from rwords.models import Dict, Synonym, Example
from rwords.webspider import jukuu, synonymdotcom


def upgrade_Example():
    words = Dict.objects.all()
    spider = jukuu.WebSpider()
    for word in words:
        if Example.objects.filter(word=word):
            continue
        # 获得例句
        examples = spider.get_example(word.text)
        for example in examples:
            Example.object.create(
                word=word,
                text_eng=example[0],
                text_chs=example[1]
            )

def upgrade_Synonym():
    words = Dict.objects.all()
    spider = synonymdotcom.WebSpider()
    for word in words:
        if Synonym.objects.filter(word=word):
            continue
        synonyms = spider.get_synonym(word.text)
        for synonym in synonyms:
            if Synonym.objects.filter(
                    word=word,
                    text=synonym[0]
            ):
                continue
            Synonym.objects.create(
                word=word,
                text=synonym[0]
            )

if __name__ == '__main__':
    upgrade_Example()
    upgrade_Synonym()

