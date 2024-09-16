class PairFinder:
    def __init__(self, symbols):
        """
        Initialize with all available symbols from the exchange.
        :param symbols: List of symbols from Binance (e.g., ['BTC/USDT', 'ETH/USDT', 'ETH/BTC']).
        """
        self.symbols = symbols

    def find_triangular_pairs(self):
        """
        Identify valid triangular arbitrage pairs based on available symbols.
        Returns a list of triangular arbitrage opportunities, each as a tuple of three pairs.
        Example output: [('BTC/USDT', 'ETH/BTC', 'ETH/USDT')]
        """
        triangular_pairs = []
        for base in self._get_unique_bases():
            base_pairs = [symbol for symbol in self.symbols if base in symbol]
            for pair_a in base_pairs:
                # Find other symbols that share a quote currency with pair_a
                quote_a = pair_a.replace(base, '').replace('/', '')
                for pair_b in base_pairs:
                    if pair_b != pair_a and quote_a in pair_b:
                        # Now find the pair that connects the quotes of pair_a and pair_b
                        quote_b = pair_b.replace(base, '').replace('/', '')
                        pair_c = f"{quote_b}/{quote_a}"
                        if pair_c in self.symbols or pair_c[::-1] in self.symbols:
                            triangular_pairs.append((pair_a, pair_b, pair_c))
        return triangular_pairs

    def _get_unique_bases(self):
        """
        Extract all unique base currencies from the symbols.
        """
        bases = set()
        for symbol in self.symbols:
            base, _ = symbol.split('/')
            bases.add(base)
        return bases
