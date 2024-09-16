class TriangularArbitrage:
    def __init__(self, data_fetcher, trading_fee=0.001):
        self.data_fetcher = data_fetcher  # Instance of DataFetcher
        self.trading_fee = trading_fee  # Trading fee (default: 0.1%)

    def calculate_profitability(self, price_a, price_b, price_c):
        """
        Calculate if there's a profitable arbitrage opportunity.
        :param price_a: Price of pair 1 (e.g., BTC/USDT)
        :param price_b: Price of pair 2 (e.g., ETH/BTC)
        :param price_c: Price of pair 3 (e.g., ETH/USDT)
        :return: Profit percentage (if any)
        """
        starting_amount = 1.0

        # Step 1: Convert base to quote via pair 1
        intermediate_amount = starting_amount * price_a * (1 - self.trading_fee)

        # Step 2: Convert quote to another asset via pair 2
        next_step_amount = intermediate_amount / price_b * (1 - self.trading_fee)

        # Step 3: Convert back to the original base via pair 3
        final_amount = next_step_amount / price_c * (1 - self.trading_fee)

        # Profit is the difference between starting and final amounts
        profit = final_amount - starting_amount
        return profit

    def find_arbitrage_opportunities(self, triangular_pairs, market_data):
        """
        Find if there is a triangular arbitrage opportunity based on market data.
        :param triangular_pairs: List of triangular pairs identified by PairFinder.
        :param market_data: Dictionary with real-time prices for the trading pairs
        """
        for pair_a, pair_b, pair_c in triangular_pairs:
            # Fetch real-time prices for the pairs
            try:
                price_a = market_data[pair_a]
                price_b = market_data[pair_b]
                price_c = market_data[pair_c]
            except KeyError:
                continue  # Skip if data for any pair is missing

            # Calculate if there's a profitable arbitrage opportunity
            profit = self.calculate_profitability(price_a, price_b, price_c)

            if profit > 0:
                print(f"Arbitrage opportunity detected! {pair_a}, {pair_b}, {pair_c} Profit: {profit:.6f}")
            else:
                print(f"No arbitrage opportunity for {pair_a}, {pair_b}, {pair_c}")
