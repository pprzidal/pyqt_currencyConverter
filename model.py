import os

from dotenv import load_dotenv


class CurrencyConverterCrawler:
    _URL = "http://api.exchangeratesapi.io/v1/latest"
    # _API_KEY = "36517c0199f77a3eb3f068ef0fe58e8c"  # TODO change

    def __init__(self):
        self.rates = None
        self.base = None
        load_dotenv()
        self._API_KEY = os.getenv("API_KEY")

    def crawl(self, renew=False):
        import os, json, datetime
        today = datetime.datetime.today().strftime('%Y-%m-%d')
        if (not os.path.isfile(f"./exchangerates_{today}")) or renew:
            import requests
            ans = requests.get(self._URL, params={"access_key": self._API_KEY}).text # TODO catch err
            with open(f"exchangerates_{today}", "w+") as file:
                file.write(ans)
        jsondict = json.load(open(f"./exchangerates_{today}"))
        self.rates = jsondict["rates"]
        self.base = jsondict["base"]

    def convert(self, amount: float, base: str, desired: list):
        a = []
        for d in desired:
            try:
                a.append({"amount": self.rates[d] / self.rates[base] * amount, "currency": d, "rate": self.rates[d] / self.rates[base]})
            except KeyError:
                raise Exception(f'Keine Currency die {d} heißt. Wahrscheinlich ein schreibfehler in Zielwährung')
        return a


if __name__ == "__main__":
    ccc = CurrencyConverterCrawler()
    ccc.crawl()
    print(ccc.convert(42.64442, "AED", ["EUR", "AFN", "ALL"]))
    # [42.64442, 1047.77026, 1213.19335]
    # [10.0, 1047.77026, 1213.19335]
