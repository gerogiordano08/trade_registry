import unittest
from unittest.mock import patch, MagicMock
from methods import get_price

class TestGetPrice(unittest.TestCase):
    @patch('methods.yf.Ticker')
    def test_get_price_returns_close_value(self, mock_ticker):
        mock_history = MagicMock()
        mock_history.empty = False
        mock_history.__getitem__.return_value = MagicMock()
        mock_history.__getitem__.return_value.iloc.__getitem__.return_value = 150.0
        mock_ticker.return_value.history.return_value = mock_history

        price = get_price('2023-01-01', 'AAPL')
        self.assertEqual(price, 150.0)

    @patch('methods.yf.Ticker')
    def test_get_price_returns_none_if_data_empty(self, mock_ticker):
        mock_history = MagicMock()
        mock_history.empty = True
        mock_ticker.return_value.history.return_value = mock_history

        price = get_price('2023-01-01', 'AAPL')
        self.assertIsNone(price)

if __name__ == '__main__':
    unittest.main()