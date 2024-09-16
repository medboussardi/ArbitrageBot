from arbitrage_bot.exchange import BinanceExchange
import logging


class OrderManager:
    def __init__(self, api_key, api_secret):
        self.exchange = BinanceExchange(api_key, api_secret)
        self.logger = logging.getLogger(__name__)

    def execute_trade(self, symbol, amount, side='buy', price=None):
        """
        Execute a trade on Binance.
        :param symbol: Trading pair (e.g., 'BTC/USDT')
        :param amount: Amount to trade
        :param side: 'buy' or 'sell'
        :param price: Limit price (optional, for limit orders)
        """
        try:
            if price:
                # Place limit order
                order = self.exchange.create_limit_order(symbol, side, amount, price)
            else:
                # Place market order
                order = self.exchange.create_market_order(symbol, side, amount)

            self.logger.info(f"Executed {side} order for {amount} {symbol} at {price}")
            return order
        except Exception as e:
            self.logger.error(f"Failed to execute {side} order for {symbol}: {e}")
            return None
