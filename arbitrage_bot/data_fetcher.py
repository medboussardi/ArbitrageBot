import ccxt.pro as ccxtpro
import asyncio
import logging


class DataFetcher:
    def __init__(self, api_key=None, api_secret=None):
        self.exchange = ccxtpro.binance({
            'apiKey': api_key,
            'secret': api_secret,
            'enableRateLimit': True,
        })

        # Logger setup
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    async def fetch_real_time_prices(self, symbols):
        """
        Fetch real-time prices using WebSocket for multiple symbols.
        Automatically reconnects if the connection is lost.
        """
        while True:
            try:
                market_data = {}
                for symbol in symbols:
                    ticker = await self.exchange.watch_ticker(symbol)
                    market_data[symbol] = ticker['last']
                    self.logger.info(f"Real-time price for {symbol}: {ticker['last']}")
                return market_data
            except Exception as e:
                self.logger.error(f"Error fetching real-time prices: {e}")
                await asyncio.sleep(5)  # Wait 5 seconds before retrying

    async def fetch_real_time_order_books(self, symbols, limit=10):
        """
        Fetch real-time order book using WebSocket for multiple symbols.
        Automatically reconnects if the connection is lost.
        """
        while True:
            try:
                order_books = {}
                for symbol in symbols:
                    order_book = await self.exchange.watch_order_book(symbol, limit)
                    order_books[symbol] = order_book
                    self.logger.info(f"Real-time order book for {symbol}: {order_book}")
                return order_books
            except Exception as e:
                self.logger.error(f"Error fetching real-time order books: {e}")
                await asyncio.sleep(5)  # Wait 5 seconds before retrying

    async def fetch_account_balance(self):
        """
        Fetch real-time account balance using WebSocket.
        Automatically reconnects if the connection is lost.
        """
        while True:
            try:
                balance = await self.exchange.watch_balance()
                self.logger.info(f"Real-time account balance: {balance}")
                return balance
            except Exception as e:
                self.logger.error(f"Error fetching real-time balance: {e}")
                await asyncio.sleep(5)  # Wait 5 seconds before retrying

    async def run_websocket_tasks(self, symbols):
        """
        Run WebSocket tasks concurrently to fetch real-time prices and order books.
        """
        await asyncio.gather(
            self.fetch_real_time_prices(symbols),
            self.fetch_real_time_order_books(symbols)
        )


if __name__ == "__main__":
    api_key = "8eyJiap5a0hgNZ0dL9nr2l4xjPmwLS1FohL5ZDnT9Rpy0TfsysMaTexnsiIGTBI3"
    api_secret = "VyJthJg1a3PhtDZWtrl6ZofOEcI29S33V1LoHGEXpHR02IRCFErM9R8l4uXT0Sk9"

    data_fetcher = DataFetcher(api_key, api_secret)
    symbols = ['BTC/USDT', 'ETH/USDT', 'ETH/BTC']

    # Run WebSocket tasks concurrently
    loop = asyncio.get_event_loop()
    loop.run_until_complete(data_fetcher.run_websocket_tasks(symbols))
