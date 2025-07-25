import ccxt
import pandas as pd
import ta

exchange = ccxt.binance()

def get_symbols():
    markets = exchange.load_markets()
    return [s for s in markets if s.endswith("/USDT") and markets[s]['info']['quoteAsset'] == 'USDT' and float(markets[s]['info'].get('lastPrice', 0)) < 1]

def fetch_ohlcv(symbol, timeframe='15m', limit=100):
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['ema_fast'] = ta.trend.ema_indicator(df['close'], window=9)
        df['ema_slow'] = ta.trend.ema_indicator(df['close'], window=21)
        df['rsi'] = ta.momentum.rsi(df['close'], window=14)
        return df
    except Exception:
        return None

def analyze(df):
    if df is None or len(df) < 21:
        return None

    last = df.iloc[-1]
    prev = df.iloc[-2]

    if last['ema_fast'] > last['ema_slow'] and prev['ema_fast'] <= prev['ema_slow'] and last['rsi'] < 70:
        return 'LONG 📈'
    elif last['ema_fast'] < last['ema_slow'] and prev['ema_fast'] >= prev['ema_slow'] and last['rsi'] > 30:
        return 'SHORT 📉'
    else:
        return None

def get_signals():
    signals = []
    for symbol in get_symbols():
        df = fetch_ohlcv(symbol)
        if df is None:
            continue
        signal = analyze(df)
        if signal:
            signals.append(f"{symbol}: {signal}")
    return signals