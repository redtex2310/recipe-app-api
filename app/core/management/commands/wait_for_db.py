"""
 Django command to wait for the DB to be available.
"""

# Use to make psycopg2 sleep
import time

# Error Python throws when DB is not ready
from django.db.utils import OperationalError
# Error thrown by psycopg2 when DB is not ready
from psycopg2 import OperationalError as Psycopg2Error

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to wait for DB"""

    def handle(self, *args, **options):
        """Entrypoint for command"""
        # Logs to the screen
        self.stdout.write('Waiting for database...')
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except(Psycopg2Error, OperationalError):
                self.stdout.write('Database unavailable, waiting 1 s...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available'))
