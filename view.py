from PyQt6.QtWidgets import *
from PyQt6 import uic
import controller


class View(QMainWindow):
    def __init__(self, c: controller.Controller, items: list[str], items2: list[str]):
        super().__init__()
        uic.loadUi("currency_converter.ui", self)
        self.umrechnen.clicked.connect(c.umrechnen)
        self.zuruecksetzen.clicked.connect(self.reset)
        self.exit.clicked.connect(self.close)
        self.waehrung.addItems(items)
        items2.sort(reverse=False)
        self.listWidget.addItems(items2)

    def getAmount(self) -> int:
        return self.betrag.value()

    def getCurrency(self) -> str:
        return self.waehrung.currentText()

    def getDesiredCurrencies(self) -> str:
        # Quelle: https://www.geeksforgeeks.org/python-operation-to-each-element-in-list/
        # Quelle: https://stackoverflow.com/questions/12453580/how-to-concatenate-items-in-a-list-to-a-single-string
        return ','.join(a.text() for a in self.listWidget.selectedItems())

    def setStatusbar(self, text: str) -> None:
        self.statusbar.showMessage(text)

    def reset(self) -> None:
        self.betrag.setValue(0.0)
        self.waehrung.setCurrentIndex(-1)
        self.ergebnisAnzeige.setPlainText("")

    def setOutput(self, a: tuple[float, str], b: list[dict]) -> None: # TODO nameing
        s = f"<b>{a[0]} {a[1]}</b> entsprechen<ul>\n"
        for entry in b:
            s += f"\t<li> <b>{entry['amount']} {entry['currency']}</b> (Kurs: {entry['rate']})</li>\n"
        self.ergebnisAnzeige.setHtml(s + "</ul>Stand: heute")

    def getCheckButtonState(self):
        #print(self.checkBox.isChecked())
        return self.checkBox.isChecked()


if __name__ == "__main__":
    import sys
    app = QApplication([])
    v = View(controller.Controller())
    v.show()
    sys.exit(app.exec())

