from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.http import HttpResponse, HttpRequest

from rwords.views.home import home_page
from rwords.models import LearnState, LearnTask, WordBook, UserProperty
from rwords.file_handler import load_dict
from datetime import datetime, timedelta


class TestLearningTask(TestCase):


    def create_user(self, username):
        user = User.objects.create_user(username=username, password='password')
        userp = UserProperty.objects.create(user=user)
        return user, userp

    # 加载测试用的单词书，包含一百个单词
    def load_wordbook(self):
        user, userp = self.create_user('user')
        wordbook1 = WordBook.objects.create(
            name='test1', image='a.jpg', author=user
        )
        load_dict('../dict/test.dat', wordbook1, output=False)
        wordbook2 = WordBook.objects.create(
            name='test2', image='a.jpg', author=user
        )
        load_dict('../dict/test.dat', wordbook2, output=False)
        return wordbook1, wordbook2

    # 测试用户每天想学的单词数量远大于单词书的单词数量的情况
    def test_generate_task_more_than_wordbook_count(self):
        w1, w2 = self.load_wordbook()
        # 创建用户
        user, userp = self.create_user('learner')
        # 这个用户想学500个单词，可是单词书里面只有100个
        userp.amount = 500
        userp.learning_wordbook = w1
        userp.save()
        self.assertEqual(userp.learning_wordbook.wordlist_set.all().count(), 100)
        # 用户还是不改变注意，开始了学习
        tasks = LearnTask.get_user_tasks(user)
        # 用户发现自己今天的学习任务还是100个单词
        self.assertEqual(tasks.count(), 100)

    # 测试用户获取学习任务的是否不会得到不是今天的内容
    def test_generate_task_not_exists_yesterday_task(self):
        w1, w2 = self.load_wordbook()
        user, userp = self.create_user('learner')
        userp.amount = 10
        userp.learning_wordbook = w1
        userp.save()
        # 用户在2016年9月8日学习10个单词
        today = datetime.now().date()
        tasks = LearnTask.get_user_tasks(user, today=today)
        self.assertEqual(tasks.count(), 10)
        print(userp.get_diary(today))
        # 时间过得飞快，转眼间来到了9月9日
        # 用户觉得自己昨天学的太少，增加了单词数量
        userp.amount = 15
        userp.save()
        today1 = today + timedelta(days=1)
        # 用户发现自己的任务表里面昨天的单词已经不见了
        # 今天的任务是全新布置的15个单词
        tasks = LearnTask.get_user_tasks(user, today=today1)
        print(userp.get_diary(today))
        #print(userp.get_diary(today1))
        self.assertEqual(tasks.count(), 15)
        self.assertEqual(tasks.filter(build_date=today).count(), 0)
        self.assertEqual(tasks.filter(build_date=today1).count(), 15)

    # 测试认识
    def test_known(self):
        w1, w2 = self.load_wordbook()
        user, userp = self.create_user('learner')
        userp.amount = 1
        userp.learning_wordbook = w1
        userp.save()
        tasks = LearnTask.get_user_tasks(user)
        self.assertEqual(tasks.count(), 1)
        task = tasks[0]
        task.known()
        self.assertTrue(task.remember)
        self.assertFalse(task.finished)
        self.assertEqual(task.get_learn_state().familiar_level, 0)
        task.known()
        self.assertTrue(task.remember)
        self.assertTrue(task.finished)
        self.assertEqual(task.get_learn_state().familiar_level, 1)

    # 测试不认识
    def test_unknow(self):
        w1, w2 = self.load_wordbook()
        user, userp = self.create_user('learner')
        userp.amount = 1
        userp.learning_wordbook = w1
        userp.save()
        tasks = LearnTask.get_user_tasks(user)
        task = tasks[0]
        task.known()
        self.assertTrue(task.remember)
        self.assertFalse(task.finished)
        self.assertEqual(task.get_learn_state().familiar_level, 0)
        task.unknown()
        self.assertFalse(task.remember)
        self.assertFalse(task.finished)
        self.assertEqual(task.get_learn_state().familiar_level, 0)

    # 测试太简单
    def test_too_simple(self):
        w1, w2 = self.load_wordbook()
        user, userp = self.create_user('learner')
        userp.amount = 1
        userp.learning_wordbook = w1
        userp.save()
        tasks = LearnTask.get_user_tasks(user)
        task = tasks[0]
        task.too_simple()
        self.assertTrue(task.remember)
        self.assertTrue(task.finished)
        state = task.get_learn_state()
        self.assertTrue(state.too_simple)

    # 测试任务完成信息
    def test_task_finished_state(self):
        w1, w2 = self.load_wordbook()
        user, userp = self.create_user('learner')
        userp.amount = 2
        userp.learning_wordbook = w1
        userp.save()
        tasks = LearnTask.get_user_tasks(user)
        self.assertEqual(tasks.count(), 2)
        task = tasks[0]
        task.known()
        task.known()
        tasks = LearnTask.get_user_tasks(user)
        self.assertEqual(tasks.count(), 1)
        task = tasks[0]
        task.known()
        task.known()
        tasks = LearnTask.get_user_tasks(user)
        self.assertEqual(tasks.count(), 0)



