def _num(value, default=0.0):
    try:
        if value is None:
            return default
        return float(value)
    except Exception:
        return default


def score_stock(technical, orderbook, money_flow, validation):
    """
    امتیازدهی سهم از 0 تا 100.

    وزن‌ها:
    - تکنیکال: 40
    - دفتر سفارش: 25
    - جریان پول: 25
    - اعتبار داده: 10
    """

    technical = technical or {}
    orderbook = orderbook or {}
    money_flow = money_flow or {}
    validation = validation or {}

    score = 0.0

    # =========================================================
    # 1. اعتبار داده — حداکثر 10 امتیاز
    # =========================================================

    if validation.get("ok") is True:
        score += 10
    elif validation.get("status") == "NEEDS_REVIEW":
        score += 3

    # =========================================================
    # 2. تکنیکال — حداکثر 40 امتیاز
    # =========================================================

    technical_score = 0

    rsi = _num(technical.get("rsi_14"), None)

    # RSI
    if rsi is not None:
        if 45 <= rsi <= 65:
            technical_score += 10
        elif 35 <= rsi < 45:
            technical_score += 7
        elif 65 < rsi <= 75:
            technical_score += 6
        elif rsi < 30:
            technical_score += 3
        elif rsi > 75:
            technical_score += 2

    # قیمت نسبت به میانگین‌ها
    if technical.get("above_sma20"):
        technical_score += 5

    if technical.get("above_sma50"):
        technical_score += 5

    if technical.get("above_sma100"):
        technical_score += 4

    if technical.get("above_sma200"):
        technical_score += 4

    # MACD
    macd = _num(technical.get("macd"), None)
    signal = _num(technical.get("macd_signal"), None)

    if macd is not None and signal is not None:
        if macd > signal:
            technical_score += 4

    # حجم معاملات
    volume_ratio = _num(
        technical.get("volume_ratio"),
        technical.get("volume_change_ratio", 0)
    )

    if volume_ratio >= 1.5:
        technical_score += 4
    elif volume_ratio >= 1.0:
        technical_score += 2

    # سقف تکنیکال
    technical_score = min(technical_score, 40)

    score += technical_score

    # =========================================================
    # 3. دفتر سفارش — حداکثر 25 امتیاز
    # =========================================================

    orderbook_score = 0

    buy_pressure = _num(
        orderbook.get("buy_pressure"),
        orderbook.get("buy_sell_ratio", 0)
    )

    if buy_pressure > 2:
        orderbook_score += 15
    elif buy_pressure > 1.5:
        orderbook_score += 12
    elif buy_pressure > 1:
        orderbook_score += 8
    elif buy_pressure > 0:
        orderbook_score += 4

    if orderbook.get("buy_queue"):
        orderbook_score += 5

    if orderbook.get("sell_queue"):
        orderbook_score -= 5

    orderbook_score = max(0, min(orderbook_score, 25))

    score += orderbook_score

    # =========================================================
    # 4. جریان پول حقیقی — حداکثر 25 امتیاز
    # =========================================================

    money_score = 0

    real_money_flow = _num(
        money_flow.get("real_money_flow"),
        None
    )

    buy_power = _num(
        money_flow.get("buy_power"),
        None
    )

    if real_money_flow is not None:
        if real_money_flow > 0:
            money_score += 15
        elif real_money_flow < 0:
            money_score += 0

    if buy_power is not None:
        if buy_power >= 2:
            money_score += 10
        elif buy_power >= 1.5:
            money_score += 7
        elif buy_power >= 1:
            money_score += 4

    money_score = max(0, min(money_score, 25))

    score += money_score

    # =========================================================
    # امتیاز نهایی
    # =========================================================

    score = round(max(0, min(score, 100)), 2)

    return {
        "score": score,
        "technical_score": technical_score,
        "orderbook_score": orderbook_score,
        "money_flow_score": money_score,
        "data_score": (
            10 if validation.get("ok") is True
            else 3 if validation.get("status") == "NEEDS_REVIEW"
            else 0
        ),
    }


def calculate_score(technical, orderbook, money_flow, validation):
    return score_stock(
        technical,
        orderbook,
        money_flow,
        validation
    )
