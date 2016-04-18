import unittest
from io import StringIO
from unittest.mock import patch

from crank.fto.cli import process_input


class TestCLI(unittest.TestCase):

    def test_process_input(self):
        inputs = ('Bench Press', 'y', '2', '100')
        exp = [
            'Bench press:  40 x 5, 50 x 5, 60 x 3, 70 x 3, 80 x 3, 90 x 8',
            '- Training max: 100 kgs',
            '- week: 2'
        ]

        # Mock input's return values and capture stdout
        with patch("crank.fto.cli.input", side_effect=inputs), \
                patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            process_input()

        raw = mock_stdout.getvalue()
        obs = raw.strip().split('\n')
        # skip comparing datetime for now.
        self.assertEqual(obs[1:], exp, raw)
