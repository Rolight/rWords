from django.test import TestCase
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

# Create your tests here.
from rwords.models import Dict, Example, Synonym
from rwords.models import WordBook, WordList, UserProperty
from rwords.models import Note, LearnState

# 词库模型测试
class DictModelTest(TestCase):
    # 测试默认值
    def test_default_text(self):
        dt = Dict.objects.create(text='apple')
        self.assertEqual(dt.example_set.count(), 0)
        self.assertEqual(dt.synonym_set.count(), 0)
        dt.example_set.create(text='eat apple')
        dt.synonym_set.create(text='leppa')
        self.assertEqual(dt.example_set.first().text, 'eat apple')
        self.assertEqual(dt.synonym_set.first().text, 'leppa')

    # 测试唯一性
    def test_duplicate_text_are_invalid(self):
        dt = Dict.objects.create(text='apple')
        with self.assertRaises(IntegrityError):
            dt1 = Dict(text='apple')
            dt1.save()

    # 测试不能创建空值
    def test_cannot_save_empty_dict(self):
        dt = Dict(text='')
        with self.assertRaises(ValidationError):
            dt.full_clean()
            dt.save()

    def test_cannot_save_empty_example(self):
        dt = Dict.objects.create(text='apple')
        with self.assertRaises(ValidationError):
            example = Example(text='', word=dt)
            example.full_clean()
            example.save()

    def test_cannot_save_empty_synonym(self):
        dt = Dict.objects.create(text='apple')
        with self.assertRaises(ValidationError):
            synonmy = Synonym(text='', word=dt)
            synonmy.full_clean()
            synonmy.save()

    # 测试级联删除
    def test_on_delete_cascade(self):
        dt = Dict.objects.create(text='apple')
        synonmy = Synonym(text='lala', word=dt)
        example = Example(text='lala', word=dt)
        synonmy.save()
        example.save()
        self.assertEqual(Synonym.objects.count(), 1)
        self.assertEqual(Example.objects.count(), 1)
        dt.delete()
        self.assertEqual(Synonym.objects.count(), 0)
        self.assertEqual(Example.objects.count(), 0)


# 单词本模型测试
class WorkBookModelTest(TestCase):
    # 测试是否能够正确创建
    def test_create(self):
        user = User.objects.create_user(username='user', password='password')
        wbook = WordBook.objects.create(author=user, name='my wordbook')

    # 测试多对多关系
    def test_many_to_many_relationship(self):
        user = User.objects.create_user(username='user', password='password')
        wbook = WordBook.objects.create(author=user, name='my wordbook')
        wbook1 = WordBook.objects.create(author=user, name='my another wordbook')
        w1 = Dict.objects.create(text='w1')
        w2 = Dict.objects.create(text='w2')
        wordlist1 = WordList(word=w1, wordbook=wbook, definition='ww')
        wordlist2 = WordList(word=w1, wordbook=wbook1, definition='ww1')
        wordlist3 = WordList(word=w2, wordbook=wbook, definition='ww2')
        wordlist4 = WordList(word=w2, wordbook=wbook1, definition='w3')
        wordlist1.save()
        wordlist2.save()
        wordlist3.save()
        wordlist4.save()
        self.assertEqual(wbook.words.count(), 2)
        self.assertEqual(wbook1.words.count(), 2)
        self.assertIn(w1, wbook.words.all())
        self.assertIn(w1, wbook1.words.all())
        self.assertEqual(WordList.objects.count(), 4)
        wbook.delete()
        self.assertEqual(WordList.objects.count(), 2)
        user.delete()
        self.assertEqual(WordList.objects.count(), 0)
        self.assertEqual(WordBook.objects.count(), 0)

# 笔记以及学习记录模型测试
class NoteAndLearnStateTest(TestCase):
    create_cnt = 1
    # 自动创建测试需要的环境
    def create_environment(self):
        self.user = User.objects.create_user(username='user%d' % self.create_cnt, password='password')
        self.word1 = Dict.objects.create(text='apple')
        self.word2 = Dict.objects.create(text='banana')
        self.wordbook1 = WordBook.objects.create(author=self.user, name='book1')
        self.wordbook2 = WordBook.objects.create(author=self.user, name='book2')
        self.wordlist1 = WordList.objects.create(wordbook=self.wordbook1, word=self.word1)
        self.wordlist2 = WordList.objects.create(wordbook=self.wordbook1, word=self.word2)
        self.wordlist3 = WordList.objects.create(wordbook=self.wordbook2, word=self.word1)
        self.wordlist4 = WordList.objects.create(wordbook=self.wordbook2, word=self.word2)
        self.create_cnt += 1

    # 检查是否能够正确创建笔记
    def test_create_note(self):
        self.create_environment()
        Note.objects.create(user=self.user, word=self.wordlist1, content='My Note')
        Note.objects.create(user=self.user, word=self.wordlist2, content='My Note1')
        Note.objects.create(user=self.user, word=self.wordlist3, content='My Note2')
        Note.objects.create(user=self.user, word=self.wordlist4, content='My Note3')
        self.assertEqual(self.user.notes.count(), 4)
        self.user.delete()
        self.assertEqual(Note.objects.count(), 0)

    # 检查创建学习记录时的初始值
    def test_learn_state_default_val(self):
        self.create_environment()
        lstate = LearnState.objects.create(user=self.user, word=self.wordlist1)
        self.assertEqual(lstate.familiar_level, 0)
        self.assertEqual(lstate.too_simple, False)
        self.assertEqual(lstate.learned, False)

    # 检查是否能重复创建学习记录
    def test_can_create_duplicate_learn_state(self):
        self.create_environment()
        lstate = LearnState.objects.create(user=self.user, word=self.wordlist1)
        with self.assertRaises(IntegrityError):
            lstate1 = LearnState.objects.create(user=self.user, word=self.wordlist1)


