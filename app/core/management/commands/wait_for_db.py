from django.core.management import BaseCommand
from django.db.utils import OperationalError
from psycopg2 import OperationalError as Psycopg2OpError


class Command(BaseCommand):
    def handle(self, *args, **options):
        is_ready = False
        self.stdout.write("Checking availability of database ...")

        while not is_ready:
            try:
                self.check(databases=['default'])
                is_ready = True
                self.stdout.write(self.style.SUCCESS('Database is ready now ...'))
            except (Psycopg2OpError, OperationalError):
                self.stdout.write(self.style.ERROR("Database is still unavailable ..."))
