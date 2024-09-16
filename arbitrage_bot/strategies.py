from arbitrage_bot.pair_finder import PairFinder
from arbitrage_bot.strategies import TriangularArbitrage
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

        # Initialize strategy and pair finder
        self.arbitrage_strategy = None
        self.pair_finder = None

    async def fetch_symbols_and_pairs(self):
        """
        Fetch available trading pairs dynamically and identify triangular arbitrage opportunities.
        """
        self.logger.info("Fetching available symbols...")
        symbols = await self.exchange.load_markets()
        symbols = list(symbols.keys())  # Extract symbol names

        # Find triangular pairs
        self.pair_finder = PairFinder(symbols)
        triangular_pairs = self.pair_finder.find_triangular_pairs()

        self.logger.info(f"Identified {len(triangular_pairs)} triangular pairs.")
        return triangular_pairs

    async def fetch_real_time_prices(self, triangular_pairs):
        """
        Fetch real-time prices using WebSocket for triangular pairs.
        Automatically reconnects if the connection is lost.
        """
        while True:
            try:
                market_data = {}
                # Fetch price data for all symbols in triangular pairs
                symbols_to_watch = set([pair for triplet in triangular_pairs for pair in triplet])

                for symbol in symbols_to_watch:
                    ticker = await self.exchange.watch_ticker(symbol)
                    market_data[symbol] = ticker['last']
                    self.logger.info(f"Real-time price for {symbol}: {ticker['last']}")

                # Pass data to the arbitrage strategy
                self.arbitrage_strategy.find_arbitrage_opportunities(triangular_pairs, market_data)

                await asyncio.sleep(1)  # Short delay to prevent overload
            except Exception as e:
                self.logger.error(f"Error fetching real-time prices: {e}")
                await asyncio.sleep(5)  # Wait 5 seconds before retrying

    async def run_websocket_tasks(self):
        """
        Run WebSocket tasks concurrently to fetch real-time prices for all triangular pairs.
        """
        triangular_pairs = await self.fetch_symbols_and_pairs()

        # Initialize strategy with triangular pairs
        self.arbitrage_strategy = TriangularArbitrage(self)

        await asyncio.gather(
            self.fetch_real_time_prices(triangular_pairs)
        )


if __name__ == "__main__":
    api_key = "YOUR_BINANCE_API_KEY"
    api_secret = "YOUR_BINANCE_API_SECRET"

    data_fetcher = DataFetcher(api_key, api_secret)

    # Run WebSocket tasks
    loop = asyncio.get_event_loop()
    loop.run_until_complete(data_fetcher.run_websocket_tasks())
