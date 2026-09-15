def _to_number(value):
    try:
        if value is None:
            return None

        if isinstance(value, (int, float)):
            return float(value)

        return float(str(value).replace(",", ""))

    except Exception:
        return None


def _extract_rows(data):
    """
    استخراج ردیف‌های سفارش از ساختارهای مختلف پاسخ TSETMC.
    """

    if data is None:
        return []

    if isinstance(data, list):
        return data

    if isinstance(data, dict):
        for key in [
            "bestLimits",
            "BestLimits",
            "items",
            "Items",
            "data",
            "Data",
            "result",
            "Result",
        ]:
            value = data.get(key)

            if isinstance(value, list):
                return value

        # اگر خود دیکشنری یک ردیف سفارش باشد
        if any(
            key in data
            for key in [
                "pMeDem",
                "pMeOf",
                "qTitMeDem",
                "qTitMeOf",
            ]
        ):
            return [data]

    return []


def _extract_value(row, keys):
    for key in keys:
        if key in row:
            value = _to_number(row.get(key))

            if value is not None:
                return value

    return None


def orderbook_analysis(orderbook):
    """
    تحلیل دفتر سفارش TSETMC.

    خروجی:
    - بهترین خرید
    - بهترین فروش
    - حجم خرید
    - حجم فروش
    - نسبت قدرت خرید/فروش در دفتر سفارش
    - وضعیت صف
    """

    rows = _extract_rows(orderbook)

    if not rows:
        return {
            "status": "NO_DATA",
            "best_buy": None,
            "best_sell": None,
            "buy_volume": 0,
            "sell_volume": 0,
            "buy_sell_ratio": None,
            "queue": "UNKNOWN",
        }

    buy_levels = []
    sell_levels = []

    for row in rows:

        if not isinstance(row, dict):
            continue

        buy_price = _extract_value(
            row,
            [
                "pMeDem",
                "priceBuy",
                "buyPrice",
                "PriceBuy",
                "buy_price",
            ],
        )

        sell_price = _extract_value(
            row,
            [
                "pMeOf",
                "priceSell",
                "sellPrice",
                "PriceSell",
                "sell_price",
            ],
        )

        buy_qty = _extract_value(
            row,
            [
                "qTitMeDem",
                "buyVolume",
                "volumeBuy",
                "BuyVolume",
                "buy_volume",
            ],
        )

        sell_qty = _extract_value(
            row,
            [
                "qTitMeOf",
                "sellVolume",
                "volumeSell",
                "SellVolume",
                "sell_volume",
            ],
        )

        if buy_price is not None:
            buy_levels.append(
                {
                    "price": buy_price,
                    "volume": buy_qty or 0,
                }
            )

        if sell_price is not None:
            sell_levels.append(
                {
                    "price": sell_price,
                    "volume": sell_qty or 0,
                }
            )

    best_buy = None
    best_sell = None

    if buy_levels:
        best_buy = max(
            level["price"]
            for level in buy_levels
        )

    if sell_levels:
        best_sell = min(
            level["price"]
            for level in sell_levels
        )

    buy_volume = sum(
        level["volume"]
        for level in buy_levels
    )

    sell_volume = sum(
        level["volume"]
        for level in sell_levels
    )

    if sell_volume > 0:
        buy_sell_ratio = buy_volume / sell_volume
    else:
        buy_sell_ratio = None

    queue = "BALANCED"

    if buy_volume > 0 and sell_volume == 0:
        queue = "BUY_QUEUE"

    elif sell_volume > 0 and buy_volume == 0:
        queue = "SELL_QUEUE"

    elif buy_sell_ratio is not None:

        if buy_sell_ratio >= 2:
            queue = "BUY_PRESSURE"

        elif buy_sell_ratio <= 0.5:
            queue = "SELL_PRESSURE"

    return {
        "status": "OK",
        "best_buy": best_buy,
        "best_sell": best_sell,
        "buy_volume": buy_volume,
        "sell_volume": sell_volume,
        "buy_sell_ratio": buy_sell_ratio,
        "queue": queue,
        "buy_levels": buy_levels,
        "sell_levels": sell_levels,
    }


# Compatibility alias
analyze_orderbook = orderbook_analysis
