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
                "AppleWebKit/537.36 "
                "Chrome/120.0 Mobile Safari/537.36"
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

    def snapshot(self, symbol):
        """
        دریافت یک Snapshot کامل از نماد از TSETMC.
        """

        search = self.search_instrument(symbol)

        instrument_id = self._extract_instrument_id(search)

        if not instrument_id:
            raise ValueError(
                f"Instrument not found on TSETMC: {symbol}"
            )

        return {
            "symbol": symbol,
            "instrument_id": instrument_id,
            "closing": self.closing_price(instrument_id),
            "orderbook": self.order_book(instrument_id),
            "client_type": self.client_type(instrument_id),
            "history": self.daily_history(instrument_id),
        }

    @staticmethod
    def _extract_instrument_id(data):
        """
        استخراج شناسه نماد از پاسخ جستجوی TSETMC.
        ساختار پاسخ ممکن است در طول زمان تغییر کند،
        بنابراین چند حالت مختلف بررسی می‌شود.
        """

        if data is None:
            return None

        if isinstance(data, list):
            for item in data:
                result = TSETMC._extract_instrument_id(item)

                if result:
                    return result

        if isinstance(data, dict):

            possible_keys = [
                "insCode",
                "InsCode",
                "instrumentId",
                "InstrumentId",
                "instrumentID",
                "InstrumentID",
                "id",
                "ID",
            ]

            for key in possible_keys:
                value = data.get(key)

                if value:
                    return value

            for key in [
                "instrument",
                "Instrument",
                "data",
                "Data",
                "items",
                "Items",
                "result",
                "Result",
            ]:
                if key in data:
                    result = TSETMC._extract_instrument_id(
                        data[key]
                    )

                    if result:
                        return result

        return None

    def get_all(self, instrument_id):
        return {
            "closing": self.closing_price(instrument_id),
            "orderbook": self.order_book(instrument_id),
            "client_type": self.client_type(instrument_id),
            "history": self.daily_history(instrument_id),
        }
