def _num(value):
    try:
        if value is None:
            return None
        return float(value)
    except Exception:
        return None


def _round_price(value):
    if value is None:
        return None

    value = float(value)

    if value >= 10000:
        return round(value / 100) * 100

    if value >= 1000:
        return round(value / 10) * 10

    return round(value)


def build_signal(snapshot, technical, orderbook, money_flow, score):
    """
    ساخت سیگنال نهایی سهم.

    خروجی مورد انتظار app.py:
        score
        decision
        entry_1
        stop

    علاوه بر آن:
        entry_2
        resistance
        support
        risk_reward
        warnings
    """

    snapshot = snapshot or {}
    technical = technical or {}
    orderbook = orderbook or {}
    money_flow = money_flow or {}
    score = score or {}

    # ---------------------------------------------------------
    # قیمت جاری
    # ---------------------------------------------------------

    current = None

    closing = snapshot.get("closing")

    if isinstance(closing, dict):
        for key in [
            "pClosing",
            "price",
            "lastPrice",
            "last",
            "closingPrice",
            "PClosing",
        ]:
            current = _num(closing.get(key))

            if current is not None:
                break

    elif isinstance(closing, (int, float)):
        current = float(closing)

    if current is None:
        current = _num(
            technical.get("last_close")
        )

    # ---------------------------------------------------------
    # حمایت و مقاومت
    # ---------------------------------------------------------

    support = _num(
        technical.get("support_20")
    )

    resistance = _num(
        technical.get("resistance_20")
    )

    if support is None and current is not None:
        support = current * 0.95

    if resistance is None and current is not None:
        resistance = current * 1.05

    # ---------------------------------------------------------
    # میانگین‌ها
    # ---------------------------------------------------------

    sma20 = _num(
        technical.get("sma_20")
    )

    sma50 = _num(
        technical.get("sma_50")
    )

    # ---------------------------------------------------------
    # قدرت خرید
    # ---------------------------------------------------------

    buy_power = _num(
        money_flow.get("buy_power")
    )

    real_flow = _num(
        money_flow.get("real_money_flow")
    )

    # ---------------------------------------------------------
    # امتیاز
    # ---------------------------------------------------------

    total_score = _num(
        score.get("score")
    )

    if total_score is None:
        total_score = 0

    # ---------------------------------------------------------
    # هشدارها
    # ---------------------------------------------------------

    warnings = []

    if orderbook.get("queue") == "SELL_QUEUE":
        warnings.append("فشار فروش در دفتر سفارش")

    if orderbook.get("queue") == "SELL_PRESSURE":
        warnings.append("غلبه عرضه بر تقاضا")

    if real
