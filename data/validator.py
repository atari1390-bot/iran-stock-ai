def validate_snapshot(snapshot):
    """
    Validate the complete TSETMC snapshot.
    """

    if snapshot is None:
        return {
            "status": "NEEDS_REVIEW",
            "ok": False,
            "missing": ["snapshot"],
        }

    required_keys = [
        "closing",
        "orderbook",
        "client_type",
        "history",
    ]

    missing = []

    for key in required_keys:
        if key not in snapshot:
            missing.append(key)
        elif snapshot[key] is None:
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


def validate_tsetmc_data(data):
    """
    Backward-compatible validation function.
    """

    return validate_snapshot(data)


def validate_instrument_search(data):
    """
    Validate instrument search response.
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
