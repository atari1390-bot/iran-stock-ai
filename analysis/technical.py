import numpy as np
import pandas as pd


def _find_column(df, candidates):
    for col in candidates:
        if col in df.columns:
            return col
    return None


def calculate_rsi(series, period=14):
    delta = series.diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.ewm(
        alpha=1 / period,
        min_periods=period,
        adjust=False
    ).mean()

    avg_loss = loss.ewm(
        alpha=1 / period,
        min_periods=period,
        adjust=False
    ).mean()

    rs = avg_gain / avg_loss.replace(0, np.nan)

    return 100 - (100 / (1 + rs))


def calculate_macd(series):
    ema12 = series.ewm(
        span=12,
        adjust=False
    ).mean()

    ema26 = series.ewm(
        span=26,
        adjust=False
    ).mean()

    macd = ema12 - ema26

    signal = macd.ewm(
        span=9,
        adjust=False
    ).mean()

    histogram = macd - signal

    return macd, signal, histogram


def analyze_technical(history):
    """
    تحلیل تکنیکال داده‌های تاریخی TSETMC.

    خروجی:
    - قیمت پایانی
    - RSI
    - MACD
    - میانگین‌های 20/50/100/200
    - حمایت و مقاومت 20 روزه
    - میانگین حجم
    """

    if history is None:
        return {}

    if isinstance(history, dict):
        rows = None

        for key in [
            "closingPriceDaily",
            "closingPriceDailyList",
            "items",
            "data",
            "values",
        ]:
            if key in history and isinstance(history[key], list):
                rows = history[key]
                break

        if rows is None:
            return {}

        df = pd.DataFrame(rows)

    elif isinstance(history, list):
        df = pd.DataFrame(history)

    else:
        return {}

    if df.empty:
        return {}

    close_col = _find_column(
        df,
        [
            "pClosing",
            "price",
            "close",
            "Close",
            "PClosing",
        ]
    )

    volume_col = _find_column(
        df,
        [
            "qTotTran5J",
            "volume",
            "Volume",
            "volumeValue",
        ]
    )

    if close_col is None:
        return {}

    df[close_col] = pd.to_numeric(
        df[close_col],
        errors="coerce"
    )

    df = df.dropna(subset=[close_col]).copy()

    if df.empty:
        return {}

    close = df[close_col]

    result = {}

    result["last_close"] = float(close.iloc[-1])

    # Moving averages
    for period in [20, 50, 100, 200]:
        if len(close) >= period:
            result[f"sma_{period}"] = float(
                close.rolling(period).mean().iloc[-1]
            )
        else:
            result[f"sma_{period}"] = None

    # RSI
    rsi = calculate_rsi(close)

    result["rsi_14"] = (
        float(rsi.iloc[-1])
        if not pd.isna(rsi.iloc[-1])
        else None
    )

    # MACD
    macd, signal, histogram = calculate_macd(close)

    result["macd"] = float(macd.iloc[-1])
    result["macd_signal"] = float(signal.iloc[-1])
    result["macd_histogram"] = float(histogram.iloc[-1])

    # 20-day support/resistance
    lookback = min(20, len(close))

    result["support_20"] = float(
        close.tail(lookback).min()
    )

    result["resistance_20"] = float(
        close.tail(lookback).max()
    )

    # Volume
    if volume_col is not None:
        df[volume_col] = pd.to_numeric(
            df[volume_col],
            errors="coerce"
        )

        volume = df[volume_col].dropna()

        if not volume.empty:
            result["volume_last"] = float(volume.iloc[-1])

            result["volume_avg_20"] = float(
                volume.tail(
                    min(20, len(volume))
                ).mean()
            )

    # وضعیت قیمت نسبت به میانگین‌ها
    current = result["last_close"]

    result["above_sma20"] = (
        result["sma_20"] is not None
        and current > result["sma_20"]
    )

    result["above_sma50"] = (
        result["sma_50"] is not None
        and current > result["sma_50"]
    )

    result["above_sma100"] = (
        result["sma_100"] is not None
        and current > result["sma_100"]
    )

    result["above_sma200"] = (
        result["sma_200"] is not None
        and current > result["sma_200"]
    )

    return result
