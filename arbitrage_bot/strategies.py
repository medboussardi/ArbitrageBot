from arbitrage_bot.order_manager import OrderManager


class TriangularArbitrage:
    def __init__(self, data_fetcher, trading_fee=0.001, api_key=None, api_secret=None):
        self.data_fetcher = data_fetcher
        self.trading_fee = trading_fee
        self.order_manager = OrderManager(api_key, api_secret)  # Initialize order manager here

    def calculate_profitability(self, price_a, price_b, price_c):
        # Same profitability logic as before
        starting_amount = 1.0
        intermediate_amount = starting_amount * price_a * (1 - self.trading_fee)
        next_step_amount = intermediate_amount / price_b * (1 - self.trading_fee)
        final_amount = next_step_amount / price_c * (1 - self.trading_fee)
        profit = final_amount - starting_amount
        return profit

    def find_arbitrage_opportunities(self, triangular_pairs, market_data):
        min_profit_margin = 0.0001  # Minimum profit margin to account for slippage, etc.

        for pair_a, pair_b, pair_c in triangular_pairs:
            try:
                price_a = market_data[pair_a]
                price_b = market_data[pair_b]
                price_c = market_data[pair_c]
            except KeyError:
                continue

            # Calculate profitability after fees
            profit = self.calculate_profitability(price_a, price_b, price_c)

            if profit > min_profit_margin:
                print(f"Arbitrage opportunity detected! {pair_a}, {pair_b}, {pair_c} Profit: {profit:.6f}")
                # Execute trades if the profit exceeds the minimum margin
                self.execute_arbitrage_trades(pair_a, pair_b, pair_c)
            else:
                print(f"No profitable arbitrage opportunity for {pair_a}, {pair_b}, {pair_c}")

    def execute_arbitrage_trades(self, pair_a, pair_b, pair_c):
        """
        Execute the three trades in the arbitrage loop, adjusting for available balances.
        """
        try:
            # Fetch current balance for each asset in the triangular pair
            balance = self.data_fetcher.exchange.fetch_balance()

            # Get the relevant assets (e.g., BTC, ETH, USDT)
            base_a, quote_a = pair_a.split('/')  # e.g., BTC/USDT -> base_a=BTC, quote_a=USDT
            base_b, quote_b = pair_b.split('/')  # e.g., ETH/BTC -> base_b=ETH, quote_b=BTC
            base_c, quote_c = pair_c.split('/')  # e.g., ETH/USDT -> base_c=ETH, quote_c=USDT

            # Check available balance for relevant currencies (BTC, ETH, USDT)
            balance_base_a = balance[base_a]['free']
            balance_quote_a = balance[quote_a]['free']
            balance_base_b = balance[base_b]['free'] if base_b in balance else 0  # Optional asset

            # Set the amount to trade based on the lowest available balance
            # For example, we'll trade based on the lowest available balance for safety
            amount_to_trade = min(balance_base_a, balance_quote_a / 2, 0.01)  # Adjust as necessary for safety
            print(f"Amount to trade: {amount_to_trade} {base_a}")

            if amount_to_trade > 0:
                # Execute trades sequentially
                self.order_manager.execute_trade(pair_a, amount_to_trade, 'buy')
                self.order_manager.execute_trade(pair_b, amount_to_trade, 'buy')
                self.order_manager.execute_trade(pair_c, amount_to_trade, 'sell')
                print("Trades executed successfully.")
            else:
                print(f"Insufficient balance to trade: {balance_base_a} {base_a}, {balance_quote_a} {quote_a}")
        except Exception as e:
            print(f"Error executing arbitrage trades: {e}")

