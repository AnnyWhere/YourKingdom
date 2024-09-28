import sys
import sqlite3
import json

from random import randint
from PyQt6 import QtCore, QtGui, uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QStackedWidget
from PyQt6.QtGui import QPixmap

def saveMoney(money):
    with open('wallet.json', 'w') as f:
        json.dump({'money': money}, f)
def loadMoney():
    with open('wallet.json', 'r') as f:
        M = json.load(f)
        return M.get('money', 0)

connection = sqlite3.connect("Kingdom.db")
cursor = connection.cursor()
def save(hunger, fatigue, health, Person, id):
    cursor.execute('''
    UPDATE resident SET
        hunger = ?,
        fatigue = ?,
        health = ?,
        status = ?
    WHERE id = ?;
        ''', (hunger, fatigue, health, Person, id))
    connection.commit()
def new(id, name, gender, image, hunger=0, fatigue=0, health=100):
    cursor.execute('''
    INSERT INTO resident(id, name, gender, hunger, fatigue, health, status, image) VALUES
        (?, ?, ?, ?, ?, ?, 1, ?)
        ''', (id, name, gender, hunger, fatigue, health, image))
    connection.commit()
def load(id):
    cursor.execute('''
    SELECT name, gender, hunger, fatigue, health, status, image
    FROM resident WHERE id = ?
            ''', (id,))
    result = cursor.fetchone()
    if result != None:
        return result
    else:
        load(1)
def count_residents():
    cursor.execute('''
    SELECT COUNT(*)
    FROM resident
            ''')
    return cursor.fetchone()[0]


class Kingdom(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUi()
        uic.loadUi('kingdom.ui', self)
        self.image = 0
        self.id = -1
        self.name = 'Niko'
        self.gender = 'm'
        self.hunger = 0
        self.fatigue = 0
        self.health = 100
        self.Person = 0
        self.new_gender.addItems(['Male', 'Female'])
        self.setCentralWidget(self.stackedWidget)
        self.act_work.clicked.connect(self.Work)
        self.act_sleep.clicked.connect(self.Sleep)
        self.act_feed.clicked.connect(self.Feed)
        self.NewPerson.clicked.connect(self.Edit)
        self.Back.clicked.connect(self.BackToMain)
        self.SwitchPerson.clicked.connect(self.NextPerson)
        self.Create_button.clicked.connect(self.CreateNewPerson)
        self.Change_appearance.clicked.connect(self.ChangeAppearance)
    def initUi(self):
        self.setWindowTitle("YourKingdom")
        self.setWindowIcon(QtGui.QIcon('King_Icon.jpg'))
    def Edit(self):
        if self.Money.intValue() >= 100:
            self.stackedWidget.setCurrentIndex(1)
            self.imagePerson.setPixmap(QPixmap('Person'+str(self.image+1)+'.png'))
        else:
            self.Dialog.setText("We don\'t have enought money to attract new residents, Your Majesty.")
    def CreateNewPerson(self):
        self.name = self.new_name.text()
        self.gender = self.new_gender.currentText()
        self.id = count_residents()
        new(self.id, self.name, self.gender, self.image)
    def NextPerson(self):
        self.Money.display(loadMoney())
        self.id = (self.id+1) % count_residents()
        (self.name, self.gender, self.hunger, self.fatigue, self.health, self.Person, self.image) = load(self.id)
        self.Person_img.setPixmap(QPixmap('Person'+str(self.image+1)+'.png'))
        self.Fatigue.setText(str(self.fatigue))
        self.Gender.setText(self.gender)
        self.Health.setText(str(self.health))
        self.Hunger.setText(str(self.hunger))
        self.NamePerson.setText(self.name)
    def BackToMain(self):
        self.stackedWidget.setCurrentIndex(0)
    def ChangeAppearance(self):
        self.image = (self.image + 1)%4
        self.imagePerson.setPixmap(QPixmap('Person'+str(self.image+1)+'.png'))
    def Work(self):
        res = int(self.Fatigue.text()) + 10
        if res > 100:
            self.Change_health()
        elif res < 101 and self.Person:
            self.Fatigue.setText(str((res if res < 100 else 100) if res > 0 else 0))
            self.Money.display(self.Money.intValue() + 20)
            saveMoney(self.Money.intValue())
            self.Hungry()
            save(self.hunger, self.fatigue, self.health, self.Person, self.id)
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
            self.Change_health()
        else:
            self.Hunger.setText(str((res if res < 100 else 100) if res > 0 else 0))
    def Change_health(self):
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