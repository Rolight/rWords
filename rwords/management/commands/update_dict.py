from django.core.management.base import BaseCommand, CommandError

from rwords.file_handler import upgrade_dict

class Command(BaseCommand):

    help = '使用爬虫更新数据库'

    def handle(self, *args, **options):
        upgrade_dict()
        self.stdout.write(self.style.SUCCESS('更新成功'))

