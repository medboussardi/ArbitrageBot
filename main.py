import ccxt.pro as ccxtpro
import asyncio

async def main():
    exchange = ccxtpro.binance({
        'enableRateLimit': True,
    })

    while True:
        try:
            # Listen to the WebSocket stream for real-time BTC/USDT ticker
            ticker = await exchange.watch_ticker('BTC/USDT')
            print(f"BTC/USDT Price: {ticker['last']}")
        except Exception as e:
            print(f"Error: {e}")
            break

asyncio.run(main())
