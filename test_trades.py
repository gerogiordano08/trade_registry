import unittest
from main import main
from unittest.mock import patch, mock_open
class TestTrades(unittest.TestCase):
    @patch('builtins.input', side_effect=['1', 'intc.ba', '19', '2025-06-26', '5400', 'yes', '2025-07-16', '5670'])
    @patch('builtins.print')
    def test_add_trade(self, mock_print, mock_input):
        main()
        # Check if the trade was added correctly
        mock_print.assert_called_with('Trade added with ID: 2')
if __name__ == '__main__':
    unittest.main()
