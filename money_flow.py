def _to_number(value):
    try:
        if value is None:
            return None

        if isinstance(value, (int, float)):
            return float(value)

        return float(str(value).replace(",", ""))

    except Exception:
        return None


def _extract_value(data, keys):
    if not isinstance(data, dict):
        return None

    for key in keys:
        if key in data:
            value = _to_number(data[key])

            if value is not None:
                return value

    return None


def money_flow_analysis(client_type):
    if client_type is None:
        return {
            "status": "NO_DATA",
            "real_buy": None,
            "real_sell": None,
            "legal_buy": None,
            "legal_sell": None,
            "real_money_flow": None,
            "buy_power": None,
        }

    data = client_type

    if isinstance(data, dict):
        for key in [
            "clientType",
            "ClientType",
            "data",
            "Data",
            "result",
            "Result",
            "items",
            "Items",
        ]:
            if isinstance(data.get(key), (dict, list)):
                data = data[key]
                break

    if isinstance(data, list):
        if not data:
            return {
                "status": "NO_DATA",
                "real_buy": None,
                "real_sell": None,
                "legal_buy": None,
                "legal_sell": None,
                "real_money_flow": None,
                "buy_power": None,
            }

        data = data[-1]

    if not isinstance(data, dict):
        return {
            "status": "NO_DATA",
            "real_buy": None,
            "real_sell": None,
            "legal_buy": None,
            "legal_sell": None,
            "real_money_flow": None,
            "buy_power": None,
        }

    real_buy = _extract_value(
        data,
        [
            "Buy_I_Volume",
            "buy_I_Volume",
            "buyRealVolume",
            "realBuyVolume",
            "RealBuyVolume",
            "buyVolumeReal",
            "buy_I",
        ],
    )

    real_sell = _extract_value(
        data,
        [
            "Sell_I_Volume",
            "sell_I_Volume",
            "sellRealVolume",
            "realSellVolume",
            "RealSellVolume",
            "sellVolumeReal",
            "sell_I",
        ],
    )

    legal_buy = _extract_value(
        data,
        [
            "Buy_N_Volume",
            "buy_N_Volume",
            "buyLegalVolume",
            "legalBuyVolume",
            "LegalBuyVolume",
            "buyVolumeLegal",
            "buy_N",
        ],
    )

    legal_sell = _extract_value(
        data,
        [
            "Sell_N_Volume",
            "sell_N_Volume",
            "sellLegalVolume",
            "legalSellVolume",
            "LegalSellVolume",
            "sellVolumeLegal",
            "sell_N",
        ],
    )

    real_money_flow = None

    if real_buy is not None and real_sell is not None:
        real_money_flow = real_buy - real_sell

    buy_power = None

    if (
        real_buy is not None
        and real_sell is not None
        and real_sell > 0
    ):
        buy_power = real_buy / real_sell

    return {
        "status": "OK",
        "real_buy": real_buy,
        "real_sell": real_sell,
        "legal_buy": legal_buy,
        "legal_sell": legal_sell,
        "real_money_flow": real_money_flow,
        "buy_power": buy_power,
    }


def analyze_money_flow(client_type):
    return money_flow_analysis(client_type)
