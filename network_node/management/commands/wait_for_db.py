import time

from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError


class Command(BaseCommand):
    """Команда для ожидания доступности БД"""

    def handle(self, *args, **options):
        self.stdout.write("Ожидание БД...")
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections["default"]
                db_conn.cursor()
            except OperationalError:
                self.stdout.write("БД недоступна, ожидание 1 сек...")
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("БД доступна!"))
