import ccxt
import time
import logging


class BinanceExchange:
    def __init__(self, api_key=None, api_secret=None):
        self.api_key = api_key
        self.api_secret = api_secret

        # Initialize the Binance exchange connection
        self.exchange = ccxt.binance({
            'apiKey': self.api_key,
            'secret': self.api_secret,
            'enableRateLimit': True  # To prevent hitting rate limits
        })

        # Logger setup
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def retry(self, func, retries=3, delay=5):
        """
        Retry mechanism for handling temporary failures.
        :param func: Function to execute
        :param retries: Number of retries before giving up
        :param delay: Delay in seconds between retries
        """
        for attempt in range(retries):
            try:
                return func()
            except Exception as e:
                self.logger.error(f"Attempt {attempt + 1}/{retries} failed: {e}")
                time.sleep(delay)
        return None

    def fetch_ticker(self, symbol):
        """
        Fetch the latest ticker information for a specific symbol (e.g., BTC/USDT)
        """
        return self.retry(lambda: self.exchange.fetch_ticker(symbol))

    def fetch_order_book(self, symbol, limit=10):
        """
        Fetch the order book for a specific symbol (e.g., BTC/USDT)
        """
        return self.retry(lambda: self.exchange.fetch_order_book(symbol, limit=limit))

    def fetch_symbols(self):
        """
        Fetch all available trading pairs on Binance (e.g., BTC/USDT, ETH/BTC)
        """
        return self.retry(self.exchange.load_markets)

    def fetch_balance(self):
        """
        Fetch the account balance
        """
        return self.retry(self.exchange.fetch_balance)
