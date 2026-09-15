import os
import requests


class TSETMC:
    BASE_URL = "https://cdn.tsetmc.com/api"

    def __init__(self, timeout=None):
        self.timeout = timeout or int(os.getenv("TSETMC_TIMEOUT", "15"))
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": (
                "Mozilla/5.0 (Linux; Android 10) "
                "AppleWebKit/537.36 Chrome/120 Safari/537.36"
            ),
            "Accept": "application/json, text/plain, */*",
            "Referer": "https://www.tsetmc.com/",
        })

    def _get(self, path):
        url = f"{self.BASE_URL}{path}"

        response = self.session.get(
            url,
            timeout=self.timeout
        )

        response.raise_for_status()
        return response.json()

    def search_instrument(self, symbol):
        return self._get(
            f"/Instrument/GetInstrumentSearch/{symbol}"
        )

    def closing_price(self, instrument_id):
        return self._get(
            f"/ClosingPrice/GetClosingPriceInfo/{instrument_id}"
        )

    def order_book(self, instrument_id):
        return self._get(
            f"/BestLimits/{instrument_id}"
        )

    def client_type(self, instrument_id):
        return self._get(
            f"/ClientType/GetClientType/{instrument_id}/1/0"
        )

    def daily_history(self, instrument_id):
        return self._get(
            f"/ClosingPrice/GetClosingPriceDailyList/{instrument_id}/0"
        )

    def get_all(self, instrument_id):
        return {
            "closing": self.closing_price(instrument_id),
            "orderbook": self.order_book(instrument_id),
            "client_type": self.client_type(instrument_id),
            "history": self.daily_history(instrument_id),
        }
