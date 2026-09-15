def _num(value, default=0.0):
    try:
        if value is None:
            return default
        return float(value)
    except Exception:
        return default


def score_stock(technical, orderbook, money_flow, validation):
    """
    امتیازدهی اولیه سهم از 0 تا 100.

    وزن‌ها:
    - تکنیکال: 40
    - دفتر سفارش: 25
    - جریان پول: 25
    - اعتبار داده: 10

    این امتیاز فعلاً «سیستم تصمیم‌گیری اولیه» است.
    بعداً می‌توانیم با بک‌تست و داده واقعی TSETMC آن را بهینه کنیم.
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
        technical_score += 
