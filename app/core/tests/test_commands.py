"""
Test custom Django management commands.
"""
# To mock DB behavior
# Check if DB is returning a response
from unittest.mock import patch
# Provides possible error for conneccting before DB is ready
from psycopg2 import OperationalError as Psycopg2Error
# Helper function provided by Django to simulate
# command we're testing
from django.core.management import call_command
# Another error that may be thrown depending on where
# we are on the connecting stage
from django.db.utils import OperationalError
# To create unit test. Does not need to create any DB setup
from django.test import SimpleTestCase
# For mocking DB. The Command.check is provided in the BaseCommand
# class which the Command class inherits from in the wait_for_db.py file.
# It allows to check the status of the DB


@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test Commands."""
    # param (patched_check):
    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database is ready"""
        patched_check.return_value = True
        # Will execute the wait_for_db code
        call_command('wait_for_db')
        # Check if the command was actually called from the check object
        patched_check.assert_called_once_with(databases=['default'])
    # Python defines arg order from the inside out
    # Overrides the sleep function to not pause the unit test

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for DB when getting OperationalError."""
        # Mocking to raise an exception. Side_effect allows to pass
        # items depending on type.
        # First 2 times we call mock method we raise the psycopg2error
        # Next 3 times we raise operational error
        # Number of exceptions are arbiraty can be called as much as we want.
        # 5 expceptions closely replicate real world scenario
        # 6th time this is called it'll return true
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]
        call_command('wait_for_db')
        # The call count should match the number of calls
        # from the above code. If less than 6 then we're not calling
        # exceptions porperly, if more than 6 then we called it more
        # times than intended
        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
