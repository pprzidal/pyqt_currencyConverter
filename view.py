from PyQt6.QtWidgets import *
from PyQt6 import uic
import controller


class View(QMainWindow):
    def __init__(self, c: controller.Controller):
        super().__init__()
        uic.loadUi("currency_converter.ui", self)
        self.umrechnen.clicked.connect(c.umrechnen)
        self.zuruecksetzen.clicked.connect(self.reset)
        self.exit.clicked.connect(self.close)

    def getAmount(self) -> int:
        return self.betrag.value()

    def getCurrency(self) -> str:
        return self.waehrung.text()

    def getDesiredCurrencies(self) -> str:
        return self.zielwaehrung.text()

    def setStatusbar(self, text: str) -> None:
        self.statusbar.showMessage(text)

    def reset(self) -> None:
        self.betrag.setValue(0.0)
        self.waehrung.setText("")
        self.zielwaehrung.setText("")
        self.ergebnisAnzeige.setPlainText("")

    def setOutput(self, a: tuple[float, str], b: list[dict]) -> None: # TODO nameing
        s = f"{a[0]} {a[1]} entsprechen\n"
        for entry in b:
            s += f"\t{entry['amount']} {entry['currency']} (Kurs: {entry['rate']})\n"
        self.ergebnisAnzeige.setPlainText(s + "Stand: heute")


if __name__ == "__main__":
    import sys
    app = QApplication([])
    v = View(controller.Controller())
    v.show()
    sys.exit(app.exec())

