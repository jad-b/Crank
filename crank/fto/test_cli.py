from io import StringIO
import unittest
from unittest.mock import patch

from crank.fto.cli import process_input


class TestCLI(unittest.TestCase):

    def test_process_input(self):
        inputs = '\n'.join(('Bench Press', 'y' '2', '100'))
        exp = (
            'Bench Press: ',
            '- Training Max: 100 kgs',
            '- week: 2'
        )

        with patch("sys.stdin", StringIO(inputs)), \
                patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            exp = process_input()

        lines = mock_stdout.getvalue().strip().split('\n')
        # skip comparing datetime for now.
        self.assertEqual(lines[1:], exp)
