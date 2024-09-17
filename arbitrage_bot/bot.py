from .data_fetcher import DataFetcher
import asyncio


class ArbitrageBot:
    def __init__(self, api_key, api_secret):
        self.data_fetcher = DataFetcher(api_key, api_secret)

    def run(self):
        """
        Main function to run the arbitrage bot.
        """
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.data_fetcher.run_websocket_tasks())


if __name__ == "__main__":
    from arbitrage_bot.config import load_config

    # Load configuration
    config = load_config()

    # Initialize the bot with API keys
    bot = ArbitrageBot(api_key=config['binance']['api_key'], api_secret=config['binance']['api_secret'])

    # Run the bot
    bot.run()
