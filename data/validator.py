def validate_tsetmc_data(data):
    """
    بررسی اولیه کامل بودن داده‌های دریافت‌شده از TSETMC.
    """

    required_keys = [
        "closing",
        "orderbook",
        "client_type",
        "history",
    ]

    missing = []

    for key in required_keys:
        if key not in data:
            missing.append(key)
            continue

        if data[key] is None:
            missing.append(key)

    if missing:
        return {
            "status": "NEEDS_REVIEW",
            "ok": False,
            "missing": missing,
        }

    return {
        "status": "OK",
        "ok": True,
        "missing": [],
    }


def validate_instrument_search(data):
    """
    بررسی نتیجه جستجوی نماد در TSETMC.
    """

    if data is None:
        return {
            "status": "NEEDS_REVIEW",
            "ok": False,
        }

    if isinstance(data, dict) and not data:
        return {
            "status": "NEEDS_REVIEW",
            "ok": False,
        }

    return {
        "status": "OK",
        "ok": True,
    }
