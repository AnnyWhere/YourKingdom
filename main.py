import sys
import psycopg2

from random import randint
from PyQt6 import QtCore, QtGui, uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget



class Kingdom(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUi()
        uic.loadUi('king.ui', self)
        self.act_work.clicked.connect(self.Work)
        self.act_sleep.clicked.connect(self.Sleep)
        self.act_feed.clicked.connect(self.Feed)
        self.Person = True
    def initUi(self):
        self.setWindowTitle("YourKingdom")
        self.setWindowIcon(QtGui.QIcon('King_Icon.jpg'))
    def Work(self):
        res = int(self.Fatigue.text()) + 10
        if res > 100:
            self.health()
        elif res < 101 and self.Person:
            self.Fatigue.setText(str((res if res < 100 else 100) if res > 0 else 0))
            self.Money.display(self.Money.intValue() + 20)
            self.Hungry()
    def Sleep(self):
        if self.Person:
            res = int(self.Fatigue.text()) - 30
            self.Fatigue.setText(str((res if res < 100 else 100) if res > 0 else 0))
            self.Hungry()
            self.Dialog.setText(["With your permission, I'll rest for a while.", "Thank you for your concern, Your Majesty!", "I will gain strength and I will definitely repay you for this favor, Your Majesty!"][randint(0, 2)])
    def Feed(self):
        if self.Person:
            res = int(self.Hunger.text()) - 30
            if self.Money.intValue() >= 20:
                self.Hunger.setText(str((res if res < 100 else 100) if res > 0 else 0))
                self.Money.display(self.Money.intValue() - 20)
                self.Dialog.setText(["Thank you for your generosity, Your Majesty!", "Oh, thank you, Your Majesty! You are so kind!", "Thanks to you, my family will not starve! Thank you, Your Majesty!"][randint(0, 2)])
    def Hungry(self):
        res = int(self.Hunger.text()) + 5
        if res > 100:
            self.health()
        else:
            self.Hunger.setText(str((res if res < 100 else 100) if res > 0 else 0))
    def health(self):
        res = int(self.Health.text()) - 5
        if res <= 0:
            self.Dialog.setText(". . . \n\nThis resident died")
            self.Person = False
            self.Hunger.setText("0")
            self.Fatigue.setText("0")
            self.Health.setText("0")
        else:
            self.Health.setText(str(int(self.Health.text()) - 5))



app = QApplication(sys.argv)
window = Kingdom()
window.show()

app.exec()