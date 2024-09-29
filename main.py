import sys
import sqlite3
import json

from random import randint
from PyQt6 import QtCore, QtGui, uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QStackedWidget
from PyQt6.QtGui import QPixmap

def saveData(data):
    with open('data.json', 'w') as f:
        json.dump(data, f)
def loadData():
    with open('data.json', 'r') as f:
        d = json.load(f)
        return d

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
def count_died():
    cursor.execute('''
    SELECT COUNT(*)
    FROM resident WHERE status = 0
            ''')
    return cursor.fetchone()[0]

class Kingdom(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('kingdom.ui', self)
        self.image = 0
        self.id = -1
        self.name = 'Stranger'
        self.gender = '?'
        self.hunger = 0
        self.fatigue = 0
        self.health = 100
        self.Person = 0
        self.data = loadData()
        self.money_ending.setText(("???", "The Richest Ruller")[self.data["end1"]])
        self.people_ending.setText(("???", "The Greate Empire")[self.data["end2"]])
        self.bad_ending.setText(("???", "The Broken Crown")[self.data["end3"]])
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
        self.NewGame.clicked.connect(self.reset)
        self.EndingsPage.clicked.connect(self.Ending_list)
        self.Back_1.clicked.connect(self.BackToMain)
        self.BackE1.clicked.connect(self.Ending_list)
        self.BackE2.clicked.connect(self.Ending_list)
        self.BackE3.clicked.connect(self.Ending_list)
        self.ResetAll.clicked.connect(self.Full_Reset)
        self.people_ending.clicked.connect(self.People_End)
        self.money_ending.clicked.connect(self.Money_End)
        self.bad_ending.clicked.connect(self.Bad_End)
    def Money_End(self):
        if self.data['end1'] == 1:
            self.stackedWidget.setCurrentIndex(3)
    def Bad_End(self):
        if self.data['end3'] == 1:
            self.stackedWidget.setCurrentIndex(5)
    def Full_Reset(self):
        self.reset()
        self.data = {"money": 100,
            "end1": 0,
            "end2": 0,
            "end3": 0}
        saveData(self.data)
    def Ending_list(self):
        self.stackedWidget.setCurrentIndex(2)
    def reset(self):
        cursor.execute('''
        DELETE FROM resident
                ''')
        self.Money.display(100)
        self.data['money'] = 100
        saveData(self.data)
        connection.commit()
        self.image = 0
        self.id = -1
        self.name = 'Stranger'
        self.gender = '?'
        self.hunger = 0
        self.fatigue = 0
        self.health = 100
        self.Person = 0
        self.Dialog.setText("Welcome to your Kingdom, Your Majesty!")
        self.Fatigue.setText(str(self.fatigue))
        self.Gender.setText(self.gender)
        self.Health.setText(str(self.health))
        self.Hunger.setText(str(self.hunger))
        self.NamePerson.setText(self.name)
        self.Person_img.setPixmap(QPixmap('./images/person.png'))
    def People_End(self):
        if self.data['end2'] == 1:
            self.stackedWidget.setCurrentIndex(4)
    def Edit(self):
        if self.Money.intValue() >= 100:
            self.stackedWidget.setCurrentIndex(1)
            self.imagePerson.setPixmap(QPixmap('./images/Person'+str(self.image+1)+'.png'))
        else:
            self.Dialog.setText("We don\'t have enought money to attract new residents, Your Majesty.")
    def CreateNewPerson(self):
        self.name = self.new_name.text()
        self.gender = self.new_gender.currentText()
        self.id = count_residents()
        new(self.id, self.name, self.gender, self.image)
        self.data['money'] -= 100
        self.Money.display(self.data['money'])
        self.Person = 1
        if count_residents() == 25:
            self.data['end2'] = 1
            saveData(self.data)
            self.people_ending.setText("The Greate Empire")
            self.stackedWidget.setCurrentIndex(4)
        self.BackToMain()
        saveData(self.data)
    def NextPerson(self):
        if count_residents() > 0:
            self.Money.display(self.data['money'])
            self.id = (self.id+1) % count_residents()
            (self.name, self.gender, self.hunger, self.fatigue, self.health, self.Person, self.image) = load(self.id)
            self.Person_img.setPixmap(QPixmap('./images/Person'+str(self.image+1)+'.png'))
            self.Fatigue.setText(str(self.fatigue))
            self.Gender.setText(self.gender)
            self.Health.setText(str(self.health))
            self.Hunger.setText(str(self.hunger))
            self.NamePerson.setText(self.name)
            self.Dialog.setText(["Long life and prosperity, Your Majesty!", "Thank You for Your presence, Your Majesty!"][randint(0, 1)]) if self.Person else self.Dialog.setText(". . . \n\nThis resident died")
    def BackToMain(self):
        self.stackedWidget.setCurrentIndex(0)
    def ChangeAppearance(self):
        self.image = (self.image + 1)%4
        self.imagePerson.setPixmap(QPixmap('./images/Person'+str(self.image+1)+'.png'))
    def Work(self):
        self.fatigue = self.fatigue + 10
        if self.fatigue > 100:
            self.fatigue = 100
            self.Change_health()
        elif self.fatigue < 101 and self.Person:
            self.Fatigue.setText(str(self.fatigue))
            self.Money.display(self.Money.intValue() + 20)
            self.data['money'] = self.Money.intValue()
            self.Hungry()
            save(self.hunger, self.fatigue, self.health, self.Person, self.id)
            saveData(self.data)
            if self.data['money'] > 5000 and self.data['end1'] == 0:
                self.data['end1'] = 1
                saveData(self.data)
                self.money_ending.setText("The Richest Ruller")
                self.stackedWidget.setCurrentIndex(3)
    def Sleep(self):
        if self.Person:
            self.fatigue = self.fatigue - 30
            self.fatigue = self.fatigue if self.fatigue > 0 else 0
            self.Fatigue.setText(str(self.fatigue))
            self.Hungry()
            save(self.hunger, self.fatigue, self.health, self.Person, self.id)
            self.Dialog.setText(["With Your permission, I'll rest for a while.", "Thank You for your concern, Your Majesty!", "I will gain strength and I will definitely repay You for this favor, Your Majesty!"][randint(0, 2)])
        else:
            self.Change_health()
    def Feed(self):
        if self.Person:
            if self.Money.intValue() >= 20:
                self.hunger -= 30
                self.hunger = self.hunger if self.hunger > 0 else 0
                self.Hunger.setText(str(self.hunger))
                self.data['money'] -= 20
                self.Money.display(self.data['money'])
                saveData(self.data)
                self.Dialog.setText(["Thank You for Your generosity, Your Majesty!", "Oh, thank You, Your Majesty! You are so kind!", "Thanks to You, my family will not starve! Thank You, Your Majesty!"][randint(0, 2)])
    def Hungry(self):
        self.hunger += 5
        if self.hunger > 100:
            self.hunger = 100
            self.Change_health()
        self.Hunger.setText(str(self.hunger))
        save(self.hunger, self.fatigue, self.health, self.Person, self.id)
    def Change_health(self):
        self.health -= 5
        if self.health <= 0:
            self.health = 0
            self.hunger = 0
            self.fatigue = 0
            self.Person = 0
            self.Dialog.setText(". . . \n\nThis resident died")
            self.Hunger.setText("0")
            self.Fatigue.setText("0")
            if count_residents() == count_residents() and self.data['money'] < 100:
                self.data['end3'] = 1
                saveData(self.data)
                self.bad_ending.setText("The Broken Crown")
                self.stackedWidget.setCurrentIndex(5)
        self.Health.setText(str(self.health))
        save(self.hunger, self.fatigue, self.health, self.Person, self.id)




app = QApplication(sys.argv)
window = Kingdom()
window.setWindowIcon(QtGui.QIcon('./images/King_Icon.jpg'))
window.setWindowTitle("Your Kingdom")
window.Money.display(window.data['money'])
window.show()

app.exec()