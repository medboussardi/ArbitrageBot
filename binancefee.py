import ccxt

# Initialize the Binance exchange object
binance = ccxt.binance({
    'apiKey': '8eyJiap5a0hgNZ0dL9nr2l4xjPmwLS1FohL5ZDnT9Rpy0TfsysMaTexnsiIGTBI3',  # Replace with your actual API key
    'secret': 'VyJthJg1a3PhtDZWtrl6ZofOEcI29S33V1LoHGEXpHR02IRCFErM9R8l4uXT0Sk9',  # Replace with your actual API secret
    'enableRateLimit': True,  # Rate limiting to avoid getting blocked
})

def fetch_trading_fees(symbol='BTC/USDT'):
    """
    Fetches the trading fees (maker and taker) for a specific trading pair on Binance.
    """
    try:
        markets = binance.load_markets()  # Load all markets
        if symbol in markets:
            symbol_info = markets[symbol]
            maker_fee = symbol_info['maker']  # Fee for providing liquidity (limit orders)
            taker_fee = symbol_info['taker']  # Fee for taking liquidity (market orders)

            print(f"Trading Fees for {symbol}:")
            print(f"  Maker fee: {maker_fee * 100}%")
            print(f"  Taker fee: {taker_fee * 100}%")
        else:
            print(f"Symbol {symbol} not found on Binance.")
    except Exception as e:
        print(f"Error fetching trading fees: {e}")

def fetch_withdrawal_fees():
    """
    Fetches withdrawal fees for various cryptocurrencies on Binance.
    """
    try:
        fees = binance.fetch_fees()  # Fetches fees from Binance
        if 'withdraw' in fees:
            withdrawal_fees = fees['withdraw']
            print("Withdrawal fees for different assets on Binance:")
            for currency, fee in withdrawal_fees.items():
                print(f"  {currency}: {fee}")
        else:
            print("Withdrawal fee information is unavailable.")
    except Exception as e:
        print(f"Error fetching withdrawal fees: {e}")

def fetch_binance_trading_fee_structure():
    """
    Fetches detailed trading fee structure using Binance's own API.
    This includes more account-specific details like fee tier, discounts, etc.
    """
    try:
        fee_structure = binance.fetch_trading_fees()
        print("Detailed Binance Trading Fee Structure:")
        for symbol, fees in fee_structure.items():
            maker_fee = fees.get('maker')
            taker_fee = fees.get('taker')
            print(f"  {symbol} -> Maker fee: {maker_fee * 100}%, Taker fee: {taker_fee * 100}%")
    except Exception as e:
        print(f"Error fetching detailed trading fee structure: {e}")

if __name__ == "__main__":
    # Example: Fetch trading fees for a specific trading pair (e.g., BTC/USDT)
    fetch_trading_fees('BTC/USDT')

    # Example: Fetch withdrawal fees for various cryptocurrencies
    fetch_withdrawal_fees()

    # Optional: Fetch a detailed trading fee structure for all symbols
    # fetch_binance_trading_fee_structure()
