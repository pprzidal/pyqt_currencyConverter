import requests.exceptions
from PyQt6.QtWidgets import QApplication
import model, view, sys


class Controller:
    def __init__(self):
        self.model = model.CurrencyConverterCrawler()
        self.view = view.View(self)

    def umrechnen(self):
        try:
            self.model.crawl()
        except requests.exceptions.ConnectionError or requests.exceptions.Timeout:
            self.view.setStatusbar("Abfrage nicht ok. ConnectionError oder Timeout")
            return
        amount = self.view.getAmount()
        currency = self.view.getCurrency()
        print(self.view.getDesiredCurrencies())
        try:
            erg = self.model.convert(amount, currency, (self.view.getDesiredCurrencies()).split(","))
        except Exception as e:
            self.view.setStatusbar(str(e))
            return
        self.view.setOutput((amount, currency), erg)
        self.view.setStatusbar("Abfrage ok")


if __name__ == "__main__":
    app = QApplication([])
    c = Controller()
    c.view.show()
    sys.exit(app.exec())