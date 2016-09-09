#!/usr/bin/env python3

# 自动更新数据库
from rwords.models import Dict, Synonym, Example
from rwords.webspider import jukuu, synonymdotcom


def upgrade_Example():
    words = Dict.objects.all()
    spider = jukuu.WebSpider()
    data = []
    for word in words:
        if Example.objects.filter(word=word):
            continue
        # 获得例句
        examples = spider.get_example(word.text)
        if not examples:
            print('没找到例句')
        for example in examples:
            if word.text not in example[0]:
                continue
            data.append(Example(
                word=word,
                text_eng=example[0],
                text_chs=example[1]
            ))
            if len(data) >= 10:
                Example.objects.bulk_create(data)
                data = []
    print('writing to database')
    Example.objects.bulk_create(data)
    print('finished')

def upgrade_Synonym():
    words = Dict.objects.all()
    spider = synonymdotcom.WebSpider()
    data = []
    for word in words:
        if Synonym.objects.filter(word=word):
            continue
        synonyms = spider.get_synonym(word.text)
        for synonym in synonyms:
            if Synonym.objects.filter(word=word, text=synonym):
                continue
            data.append(Synonym(
                word=word,
                text=synonym
            ))
    print('writing to database')
    Synonym.objects.bulk_create(data)
    print('finished')

if __name__ == '__main__':
    upgrade_Example()
    upgrade_Synonym()

