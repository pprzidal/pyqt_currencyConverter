import requests.exceptions
from PyQt6.QtWidgets import QApplication
import model, view, sys, json, datetime


class Controller:
    WAEHRUNG = ["EUR", "USD", "CHF"]

    def __init__(self):
        self.model = model.CurrencyConverterCrawler()
        # TODO ändern breakt wenn das file nicht existiert
        self.view = view.View(self, Controller.WAEHRUNG, list(json.load(open(f"./exchangerates_{datetime.datetime.today().strftime('%Y-%m-%d')}"))['rates'].keys()))

    def umrechnen(self):
        try:
            self.model.crawl(renew=self.view.getCheckButtonState())
        except requests.exceptions.ConnectionError or requests.exceptions.Timeout:
            self.view.setStatusbar("Abfrage nicht ok. ConnectionError oder Timeout")
            return
        amount = self.view.getAmount()
        currency = self.view.getCurrency()
        print(self.view.getDesiredCurrencies())
        try:
            erg = self.model.convert(amount, currency, (self.view.getDesiredCurrencies().replace(" ", "").upper()).split(","))
        except Exception as e:
            self.view.setStatusbar(str(e))
        else:
            self.view.setOutput((amount, currency), erg)
            self.view.setStatusbar("Abfrage ok")


if __name__ == "__main__":
    app = QApplication([])
    c = Controller()
    c.view.show()
    sys.exit(app.exec())