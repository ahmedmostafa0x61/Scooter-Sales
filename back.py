import datetime
import sys

import MySQLdb
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType

# from finalui import Ui_MainWindow as Program

Program, _ = loadUiType('GUI.ui')

my_db = MySQLdb.connect(host='localhost', user='root', password='159753852456', db='project')
my_db.set_character_set('utf8')


class MainApp(QMainWindow, Program):
    def __init__(self):
        super(MainApp, self).__init__()
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.showMaximized()
        self.db = my_db
        self.ui_changes()
        self.buttons()
        self.init_tabs()

        # self.show_all_students()
        # self.show_all_employees()

    def ui_changes(self):
        # Hiding Tab head
        self.mainTab.tabBar().setVisible(False)

        # Show sorting
        # self.store_table.setSortingEnabled(True)

        # init calender
        self.new_client_fix_date.setDateTime(QDateTime.currentDateTime())
        self.client_fix_date.setDateTime(QDateTime.currentDateTime())

        self.groupBox.setHidden(False)

        # LCD Numbers
        # self.lcdNumber.display(int(self.come))

    def init_tabs(self):
        self.mainTab.setCurrentIndex(0)
        self.clientTab.setCurrentIndex(0)

    def buttons(self):

        # Opening Tabs

        self.store_pb.clicked.connect(self.open_store)
        self.sell_pb.clicked.connect(self.open_sell)
        self.buy_pb.clicked.connect(self.open_buy)
        self.house_pb.clicked.connect(self.open_house)
        self.client_pb.clicked.connect(self.open_clients)

        # ---------------
        # Tasks
        # ---------------

        # # Sell OK
        self.sell_ok.clicked.connect(self.sell_db)
        #
        # # Buy OK
        self.buy_ok.clicked.connect(self.buy_db)
        #
        # # House OK
        self.house_ok.clicked.connect(self.move_to_store)
        #
        # # New Client OK
        self.new_client_ok.clicked.connect(self.new_client)
        #
        # # Clients New Fix ??
        self.new_fix_pb.clicked.connect(self.new_fix)
        #

        # dealing with users
        # self.pushButton_17.clicked.connect(self.new_user)
        # self.pushButton_18.clicked.connect(self.delete_user)
        # self.pushButton_19.clicked.connect(self.edit_user)
        # self.pushButton_20.clicked.connect(self.search_user)
        #
        # # login
        # self.pushButton_27.clicked.connect(self.login)

    # *******************************
    #   Opening  Tabs
    # *******************************

    def open_store(self):
        self.mainTab.setCurrentIndex(0)

    def open_sell(self):
        self.mainTab.setCurrentIndex(1)

    def open_buy(self):
        self.mainTab.setCurrentIndex(2)

    def open_house(self):
        self.mainTab.setCurrentIndex(3)

    def open_clients(self):
        self.mainTab.setCurrentIndex(4)

    # *******************************
    #   Reading Inputs
    # *******************************

    def buy_db(self):

        """Done .
        All things of Sell tab
        """
        # Getting info from UI
        name = self.buy_name.text()
        number = self.buy_number.text()
        unit_price = self.buy_unit.text()
        place = self.buy_place.currentText()

        self.cur = self.db.cursor()
        self.cur.execute(f''' SELECT p_price,s_number,h_number FROM products WHERE p_name={name}''')
        data = self.cur.fetchone()

        s_number = 0
        h_number = 0

        if data:
            p_price = data[0]
            s_number = data[1]
            h_number = data[2]

            if p_price == unit_price:
                if place == 'محل':
                    s_number += number

                else:
                    h_number += number
            else:
                # --------------
                print(' Different Prices')
                self.cur.execute(
                    f'''UPDATE products SET p_price={unit_price},s_number={s_number} WHERE p_name={name}''')
                # -------------

        else:
            if place == 'محل':
                s_number += number

            else:
                h_number += number
            self.cur.execute('''INSERT INTO products (p_name, p_price, s_number, h_number) VALUES (%s,%s,%s,%s)''',
                             (name, unit_price, s_number, h_number))
        self.db.commit()

    def sell_db(self):

        """Done .
        All things of Sell tab
        """
        name = self.sell_name.text()
        number = self.sell_number.text()

        self.cur = self.db.cursor()
        self.cur.execute(
            f'''SELECT p_name,p_price,s_number FROM products WHERE p_name={name}''')
        data = self.cur.fetchone()

        # Check if there is Enough
        if data:
            unit_price = data[1]
            number_stored = data[2]
            # ------------
            ### Print Number on digital screen  and Unit Price
            total = number * unit_price
            self.sell_available.display(number_stored)
            self.sell_unit.setText(f'{unit_price}')
            self.sell_total.setText(f'{total}')
            # -------------

            if number > number_stored:
                # ------------
                ### Print No enough in store
                print(f'No enough units of {name}, Only {number_stored} left')
                # --------------

            else:
                ### Confirm and move to Database
                number_stored -= number

                self.cur.execute('''UPDATE products SET s_number=%s WHERE p_name=%s''', (number_stored, name))
                self.db.commit()

    def store_db(self):

        self.cur = self.db.cursor()
        self.cur.execute(f''' SELECT p_name, p_price,s_number FROM products ''')
        data = self.cur.fetchall()
        if data:
            self.store_table.setRowCount(0)
            self.store_table.insertRow(0)
            for row, form in enumerate(data):
                for col, item in enumerate(form):
                    self.store_table.setItem(row, col, QTableWidgetItem(str(item)))
                    col += 1
                row_pos = self.store_table.rowCount()
                self.store_table.insertRow(row_pos)

    def house_db(self):

        self.cur = self.db.cursor()
        self.cur.execute(f''' SELECT p_name, p_price,h_number FROM products ''')
        data = self.cur.fetchall()
        if data:
            self.house_table.setRowCount(0)
            self.house_table.insertRow(0)
            for row, form in enumerate(data):
                for col, item in enumerate(form):
                    self.house_table.setItem(row, col, QTableWidgetItem(str(item)))
                    col += 1
                row_pos = self.house_table.rowCount()
                self.house_table.insertRow(row_pos)

    def move_to_store(self):
        # Getting info from UI
        name = self.house_name.text()
        number = self.house_number.text()

        self.cur = self.db.cursor()
        self.cur.execute(f'''SELECT h_number,s_number FROM products WHERE p_name={name} ''')
        data = self.cur.fetchone()

        if data:
            h_number = data[0]
            s_number = data[2]

            if number > h_number:
                # ---------------
                print("Not Enough")
                # ---------------
            else:
                h_number -= number
                s_number += number
                self.cur.execute(f'''UPDATE products set h_number=%s,s_number=%s''', (h_number, s_number))
                self.db.commit()

    def new_client(self):
        # Getting info from UI
        name = self.new_client_name.text()
        number = self.new_client_phone.text()
        bike = self.new_client_bike.text()
        color = self.new_client_color.text()
        condition = self.new_client_condition.text()
        fix_date = self.new_client_fix_date.date().toPyDate()
        fix = self.new_client_fix.text()
        added_time = datetime.datetime.now()

        self.cur = self.db.cursor()
        self.cur.execute(
            '''INSERT INTO clients (c_name,c_phone,bike,bike_color,bike_condition VALUES (%s,%s,%s,%s,%s)'''
            , (name, number, bike, color, condition))

        self.cur.execute(
            '''INSERT INTO fixes (c_name,in_date,fix_date,fix) VALUES (%s,%s,%s,%s)'''
            , (name, added_time, fix_date, fix))
        self.db.commit()

    def current_client(self):
        # Getting info from UI
        name = self.client_name.currentText()

        self.cur = self.db.cursor()
        self.cur.execute(f''' SELECT c_phone, bike, bike_color, bike_condition FROM clients WHERE c_name={name}''')
        client_data = self.cur.fetchone()
        if client_data:
            phone = client_data[0]
            bike = client_data[1]
            bike_color = client_data[2]
            bike_condition = client_data[3]

            self.client_phone.setText(phone)
            self.client_bike.setText(bike)
            self.client_color.setText(bike_color)
            self.client_condition.setText(bike_condition)

        self.cur.execute(f'''SELECT in_date,fix_date,fix FROM fixes WHERE c_name={name}''')
        fix_data = self.cur.fetchall()
        if fix_data:
            self.fixes_table.setRowCount(0)
            self.fixes_table.insertRow(0)
            for row, form in enumerate(fix_data):
                for col, item in enumerate(form):
                    self.fixes_table.setItem(row, col, QTableWidgetItem(str(item)))
                    col += 1
                row_pos = self.fixes_table.rowCount()
                self.fixes_table.insertRow(row_pos)

    def new_fix(self):

        # Getting info from UI
        name = self.new_client_name.text()
        fix_date = self.client_fix_date.date().toPyDate()
        fix = self.client_fix.text()
        added_time = datetime.datetime.now()

        self.cur = self.db.cursor()
        self.cur.execute(f'''INSERT INTO fixes (c_name,in_date,fix_date,fix) 
        VALUES (%s,%s,%s,%s)''', (name, added_time, fix_date, fix))
        self.db.commit()

    # *******************************
    #   Settings
    # *******************************

    def new_user(self):
        # Database connections
        self.cur = self.db.cursor()
        # Getting info from UI
        user_name = self.lineEdit_47.text()
        password = self.lineEdit_49.text()
        password_2 = self.lineEdit_51.text()
        permission = self.comboBox_13.currentText()

        if password == password_2:
            warning = QMessageBox.warning(self, 'Warning', 'اضافه مستخدم جديد؟', QMessageBox.Yes, QMessageBox.No)
            if warning == QMessageBox.Yes:
                self.cur.execute('''SELECT username FROM users ''')
                data = self.cur.fetchone()
                if not data:
                    self.cur.execute('''
                        INSERT INTO users (username,password,permission) 
                        VALUES (%s,%s,%s)''', (user_name, password, permission))
                    self.db.commit()
                    self.statusBar().showMessage('New user Added!')
                else:
                    self.statusBar().showMessage('User Already exist!')

        else:
            self.label_53.setText('Password Don\'t Match!')

    def search_user(self):
        username = self.lineEdit_48.text()
        self.cur = self.db.cursor()
        self.cur.execute('''SELECT username FROM users WHERE username=%s''', [username])
        data = self.cur.fetchone()
        if data:
            self.statusBar().showMessage('User Found, Edit Info')

        else:
            self.statusBar().showMessage('No User Found !')

    def edit_user(self):
        self.cur = self.db.cursor()
        username = self.lineEdit_48.text()
        password = self.lineEdit_50.text()
        password_2 = self.lineEdit_52.text()
        permission = self.comboBox_14.currentText()

        if password == password_2:
            warning = QMessageBox.warning(self, 'Warning', 'تعديل البيانات ؟', QMessageBox.Yes, QMessageBox.No)
            if warning == QMessageBox.Yes:
                self.cur.execute('''
                            UPDATE users SET password=%s,permission=%s
                            WHERE username=%s''', (password, permission, username))
                self.db.commit()
                self.statusBar().showMessage('تم تعديل البيانات')
        else:
            self.label_97.setText('Password Don\'t Match!')

    def delete_user(self):
        self.cur = self.db.cursor()
        username = self.lineEdit_48.text()
        warning = QMessageBox.warning(self, 'Warning', 'حذف المستخدم ؟', QMessageBox.Yes, QMessageBox.No)
        if warning == QMessageBox.Yes:
            self.cur.execute('''DELETE FROM users WHERE username=%s''', [username])
            self.statusBar().showMessage('تم حذف المستخدم')

    def login(self):
        self.cur = self.db.cursor()
        username = self.lineEdit_54.text()
        password = self.lineEdit_66.text()
        self.cur.execute('''SELECT * FROM users WHERE username=%s''', [username])
        data = self.cur.fetchone()
        if data:
            if data[2] == password:
                if data[3] == 'موظف':
                    self.groupBox.setHidden(False)
                    self.groupBox_2.setHidden(True)
                    self.statusBar().showMessage('Welcome')
                    self.pushButton_3.setVisible(False)
                    self.pushButton_4.setVisible(False)
                    self.pushButton_6.setVisible(False)
                elif data[3] == 'مدير':
                    self.groupBox.setHidden(False)
                    self.groupBox_2.setHidden(True)
                    self.statusBar().showMessage('Welcome')
                else:
                    self.statusBar().showMessage('!!!!!')

            else:
                self.statusBar().showMessage('Wrong Username and Password!')

        else:
            self.statusBar().showMessage('Not Found !')


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.setWindowTitle('TA-System')
    window.setWindowIcon(QIcon('pic\ico.jpg'))
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
