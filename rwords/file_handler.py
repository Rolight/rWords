import pickle

from rwords.models import WordBook, WordList, Dict


def dict_file_handler(dict_file, wordbook):
    file_path = '/tmp/rwords_dict_%d.dat' % wordbook.id
    with open(file_path, 'wb+') as destination:
        for chunk in dict_file.chunks():
            destination.write(chunk)
    dlist = {}
    with open(file_path, 'rb') as data:
        dlist = pickle.load(data)
    for word, wdef in dlist.items():
        if not Dict.objects.filter(text=word):
            Dict.objects.create(text=word)
        WordList.objects.create(
            wordbook=wordbook,
            word=Dict.objects.get(text=word),
            definition=wdef.replace('\n', '<br/>')
        )
        print('导入:\n%s\n %s\n成功' % (word, wdef))
    wordbook.word_cnt = len(dlist)

