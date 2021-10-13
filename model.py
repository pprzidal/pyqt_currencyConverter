

class CurrencyConverterCrawler:
    _URL = "http://api.exchangeratesapi.io/v1/latest"
    _API_KEY = "36517c0199f77a3eb3f068ef0fe58e8c"  # TODO change

    def __init__(self):
        self.rates = None
        self.base = None

    def crawl(self, renew=False):
        import os, json
        from datetime import datetime
        today = datetime.today().strftime('%Y-%m-%d')
        if (not os.path.isfile(f"./exchangerates_{today}")) or renew:
            import requests
            ans = requests.get(self._URL, params={"access_key": self._API_KEY}).text # TODO catch err
            with open(f"exchangerates_{today}", "w+") as file:
                file.write(ans)
        jsondict = json.load(open(f"./exchangerates_{today}"))
        self.rates = jsondict["rates"]
        self.base = jsondict["base"]

    def convert(self, amount: float, base: str, desired: list):
        # TODO fix the russian mess
        if base == "EUR":
            a = []
            for b in desired:
                try:
                    a.append({"amount": self.rates[b] * amount, "currency": b, "rate": self.rates[b]})
                except KeyError as ke:
                    whatever = str(ke).split("'")[1]
                    raise Exception(f'Keine Currency die {whatever} heißt. Wahrscheinlich ein schreibfehler in Zielwährung')
            return a
        elif base in self.rates:
            amountInEuro = amount / self.rates[base]
            a = []
            for b in desired:
                a.append({"amount": self.rates[b] * amountInEuro, "currency": b, "rate": (self.rates[b] * amountInEuro) / amount})
            return a
        else:
            raise ValueError("Couldn't find base currency")


if __name__ == "__main__":
    ccc = CurrencyConverterCrawler()
    ccc.crawl()
    print(ccc.convert(42.64442, "AED", ["EUR", "AFN", "ALL"]))
    # [42.64442, 1047.77026, 1213.19335]
    # [10.0, 1047.77026, 1213.19335]
