from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import sys
import os
import tact

# Алгоритм шифрования
def shifr_data(username, password):
    alfavit_eng = 'ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'
    alfavit_rus = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюяабвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    text1 = username
    text2 = password
    username = ''
    password = ''
    j = 0
    for j in range(len(text1)):
        i = text1[j]
        if text1[j] in text1:
            if text1[j] in alfavit_rus:
                username += alfavit_rus[alfavit_rus.find(i) + 2]
            elif text1[j] in alfavit_eng:
                username += alfavit_eng[alfavit_eng.find(i) + 2]
            else:
                username += i
    for j in range(len(text2)):
        i = text2[j]
        if text2[j] in text2:
            if text2[j] in alfavit_rus:
                password += alfavit_rus[alfavit_rus.find(i) + 2]
            elif text2[j] in alfavit_eng:
                password += alfavit_eng[alfavit_eng.find(i) + 2]
            else:
                password += i
    return username, password

# Проверка авторизации
def check_login(username, password):
    if len(username) <= 4 or len(username) > 20 or len(password) < 8 or len(password) > 20:
        return False
    try:
        find_login = False
        username, password = shifr_data(username, password)
        with open('logdata.txt', 'r', encoding='utf8') as login_file:
            for line in login_file:
                if (username + " " + password) in line:
                    find_login = True
            if find_login:
                return True
            return False
    except:
        return False
# Проверка регистрации
def check_registr(username, password):
    if (len(username) <= 4 or len(username) > 20) and (len(password) < 8 or len(password) > 20) :
        return False
    try:
        username, password = shifr_data(username, password)
        flag_login = False
        with open('logdata.txt', 'r+', encoding='utf8') as login_file:
            for line in login_file:
                if (username in line) or (password in line):
                    flag_login = True
                    break
            if flag_login:
                return False
            new_login = "\n" + username + " " + password
            login_file.write(new_login)
            return True
    except:
        return False
# Класс отвечающий за стартовое окно
class Login(QMainWindow):
    def __init__(self):
        super(Login, self).__init__()
        loadUi("logmain.ui", self)
        self.setMinimumSize(QtCore.QSize(700, 500))
        self.pass_line.setEchoMode(QtWidgets.QLineEdit.Password)
        self.logbtn.clicked.connect(self.personal_ac)
        self.regbtn.clicked.connect(self.registr)

    def personal_ac(self):
        global username
        username = self.login_line.text().strip()
        password = self.pass_line.text()
        if check_login(username, password):
            widget.addWidget(account_window)
            widget.setFixedWidth(850)
            widget.setFixedHeight(700)
            widget.setCurrentWidget(account_window)
        else:
            error = QMessageBox()
            error.setWindowTitle("Ошибка\t\t\t\t\t")
            error.setText("Введен неверный логин или пароль.")
            error.setIcon(QMessageBox.Warning)
            error.setStandardButtons(QMessageBox.Ok)
            error.exec_()
    def registr(self):
        widget.setCurrentWidget(new_ac_window)

# Класс отвечающий за окно регистрации
class Registration(QMainWindow):
    def __init__(self):
        super(Registration, self).__init__()
        loadUi("regmain.ui", self)
        self.password_line.setEchoMode(QtWidgets.QLineEdit.Password)
        self.replay_pas_line.setEchoMode(QtWidgets.QLineEdit.Password)
        self.registr_btn.clicked.connect(lambda: self.reg_window(True))
        self.cancel.clicked.connect(lambda: self.reg_window(False))

    def reg_window(self, flag):
        if flag == True:
            username = self.newlogin.text().strip()
            password = self.password_line.text()
            replay_password = self.replay_pas_line.text()
            if password != replay_password:
                error = QMessageBox()
                error.setWindowTitle("Ошибка\t\t\t\t\t")
                error.setText("Пароли не совпадают!")
                error.setIcon(QMessageBox.Warning)
                error.setStandardButtons(QMessageBox.Ok)
                error.exec_()
                return False
            registr_ch = check_registr(username, password)
            if registr_ch == True:
                flag = False
            else:
                error = QMessageBox()
                error.setWindowTitle("Ошибка")
                error.setIcon(QMessageBox.Warning)
                error.setStandardButtons(QMessageBox.Ok)
                error.setText(" Вы ввели неверные данные!\n Проверьте:\n 1) Пароль может содержать: \n цифры (0-9)\n латинские буквы (a-z; A-Z)\n знаки препинания ('.', '!', '?', ',', '_')\n Либо длина пароля меньше 8 или больше 20\n 2) Длина логина должна быть не менее 5 и не более 20\n 3) Пользователь с такими данными уже существует")
                error.exec_()
        if not flag:
           return widget.setCurrentWidget(login_window)

class Personal_account(QMainWindow):
    def __init__(self):
        super(Personal_account, self).__init__()
        loadUi("lk.ui", self)
        self.play_ii_btn.clicked.connect(lambda: tact.start(1))
        self.play_i_btn.clicked.connect(lambda: tact.start(2))
        self.exit_btn.clicked.connect(lambda: self.exit())

    def exit(self):
        error = QMessageBox()
        error.setWindowTitle("Предупреждение")
        error.setText("Вы уверены, что хотите выйти из личного кабинета?")
        error.setStandardButtons(QMessageBox.Ok|QMessageBox.Cancel)
        error.buttonClicked.connect(self.click_btn)
        error.exec_()

    def click_btn(self, btn):
        if btn.text() == 'OK':
            widget.removeWidget(account_window)
            widget.setFixedWidth(560)
            widget.setFixedHeight(350)
            widget.setCurrentWidget(login_window)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = Login()
    new_ac_window = Registration()
    account_window = Personal_account()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(login_window)
    widget.addWidget(new_ac_window)
    widget.show()
    sys.exit(app.exec_())

