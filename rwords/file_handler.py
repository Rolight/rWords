import pickle

from rwords.models import WordBook, WordList, Dict
from rwords.webspider.upgrade_dict import upgrade_Example, upgrade_Synonym
from django.conf import settings

def dict_file_handler(dict_file, wordbook):
    file_path = '/tmp/rwords_dict_%d.dat' % wordbook.id
    with open(file_path, 'wb+') as destination:
        for chunk in dict_file.chunks():
            destination.write(chunk)
    load_dict(file_path, wordbook)


def load_dict(file_path, wordbook, output=True, spider=False):
    dlist = {}
    try:
        data = open(file_path, 'rb')
        dlist = pickle.load(data)
        wordlist = []
        dicts = []
        for word, wdef in dlist.items():
            if not Dict.objects.filter(text=word):
                dicts.append(Dict(text=word))
        Dict.objects.bulk_create(dicts)
        for word, wdef in dlist.items():
            wordlist.append(WordList(
                wordbook=wordbook,
                word=Dict.objects.get(text=word),
                definition=wdef.replace('\n', '<br/>')
            ))
            if output:
                print('找到单词:\n%s\n %s\n' % (word, wdef))
        WordList.objects.bulk_create(wordlist)
        if output:
            print('成功导入%d个单词' % len(dlist))
        if spider or settings.auto_spider:
            upgrade_dict()
    except Exception:
        print(Exception.with_traceback())
        print('导入失败')

def upgrade_dict():
    print('正在更新例句库..')
    upgrade_Example()
    print('正在更新近义词库..')
    upgrade_Synonym()


