from django.test import SimpleTestCase
from django.core.management import call_command

from django.db.utils import OperationalError
from psycopg2 import OperationalError as Psycopg2OpError

from unittest.mock import patch


@patch('core.management.commands.wait_for_db.Command.check')
class CommandsTest(SimpleTestCase):
    """Testin wait for db."""

    def test_db_is_available(self, mock_check):
        """Test if db is available."""
        mock_check.return_value = True

        call_command('wait_for_db')

        mock_check.assert_called_once_with(databases=['default'])

    def test_db_is_not_available(self, mock_check):
        mock_check.side_effect = [Psycopg2OpError] * 2 + [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertTrue(mock_check.call_count, 6)
