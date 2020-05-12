import datetime
import sys

import MySQLdb
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
from texttable import Texttable


# from finalui import Ui_MainWindow as Program

Program, _ = loadUiType('GUI.ui')

my_db = MySQLdb.connect(host='localhost', user='root', password='159753852456', db='scooter')
my_db.set_character_set('utf8')

sell_list = [[]]
sell_list.clear()

buy_list = [[]]
buy_list.clear()

client_sell_list = [[]]
client_sell_list.clear()


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

        self.store_db()
        self.show_all_clients()
        self.sell_show_products()
        # ---------------
        self.search_show_products()
        self.search()
        # ---------------
        self.house_db()
        self.show_client_sell_products()
        self.show_client_name()
        self.show_house_name()

    def ui_changes(self):
        # Hiding Tab head
        self.mainTab.tabBar().setVisible(False)

        self.buy_table.verticalHeader().hide()
        self.sell_table.verticalHeader().hide()
        self.search_table.verticalHeader().hide()
        self.store_table.verticalHeader().hide()
        self.house_table.verticalHeader().hide()

        self.sell_number.setValidator(QIntValidator())
        self.buy_number.setValidator(QIntValidator())
        self.house_number.setValidator(QIntValidator())

        self.buy_unit.setValidator(QDoubleValidator())
        self.sell_dis.setValidator(QDoubleValidator())
        self.all_sell_dis.setValidator(QDoubleValidator())

        self.new_client_money.setValidator(QDoubleValidator())
        self.new_client_cost.setValidator(QDoubleValidator())
        self.client_money.setValidator(QDoubleValidator())
        self.client_cost.setValidator(QDoubleValidator())

        # Show sorting
        self.search_table.setSortingEnabled(True)
        self.store_table.setSortingEnabled(True)
        self.house_table.setSortingEnabled(True)

        # init calender
        self.new_client_fix_date.setDateTime(QDateTime.currentDateTime())
        self.client_fix_date.setDateTime(QDateTime.currentDateTime())

        self.groupBox.setHidden(True)
        self.buying_group.setHidden(True)
        self.selling_group.setHidden(True)
        self.new_groupBox.setHidden(True)

        # LCD Numbers
        # self.lcdNumber.display(int(self.come))

    def init_tabs(self):
        self.mainTab.setCurrentIndex(0)
        self.clientTab.setCurrentIndex(0)

    def buttons(self):

        # Opening Tabs

        self.buy_pb.clicked.connect(self.open_buy)
        self.search_pb.clicked.connect(self.open_search)
        self.sell_pb.clicked.connect(self.open_sell)
        self.store_pb.clicked.connect(self.open_store)
        self.house_pb.clicked.connect(self.open_house)
        self.client_pb.clicked.connect(self.open_clients)

        # ---------------
        # Tasks
        # ---------------

        # # Search OK
        self.search_name.currentTextChanged.connect(self.search)

        #
        # # Sell OK
        self.sell_name.currentTextChanged.connect(self.show_avail)
        self.sell_number.textEdited.connect(self.calc_total)

        # Calculate The Discount
        self.sell_dis.textEdited.connect(self.calc_after)
        self.sell_pound.released.connect(self.calc_after)
        self.sell_per.released.connect(self.calc_after)

        # Complete Sell Functions
        self.sell_add.clicked.connect(self.sell_adding)
        self.sell_remove_ok.clicked.connect(self.sell_remove)
        self.sell_ok.clicked.connect(self.print_sell_list)
        self.sell_remove_all.clicked.connect(self.remove_all_sell)

        self.sell_accept_box.accepted.connect(self.sell_confirm)
        self.sell_accept_box.rejected.connect(self.hide_sell_group)

        # # #  Total Discount
        self.all_sell_dis.textEdited.connect(self.calc_dis_total)
        self.all_sell_pound.pressed.connect(self.calc_dis_total)
        self.all_sell_per.pressed.connect(self.calc_dis_total)

        #
        # # Buy OK
        self.buy_add.clicked.connect(self.buy_adding)
        self.buy_remove_ok.clicked.connect(self.buy_remove)
        self.buy_ok.clicked.connect(self.print_buy_list)
        self.buy_remove_all.clicked.connect(self.remove_all_buy)

        self.accept_box.accepted.connect(self.buy_confirm)
        self.accept_box.rejected.connect(self.hide_group)

        #
        # # House OK
        self.house_ok.clicked.connect(self.move_to_store)
        #
        # # New Client OK
        self.new_client_ok.clicked.connect(self.new_client)
        #
        #  Clients New Fix
        self.client_ok.clicked.connect(self.new_fix)
        #
        #  Current Client
        self.client_name.currentTextChanged.connect(self.current_client)
        #
        #  New Fix ?
        self.add_new_fix.clicked.connect(self.show_new_fix)
        #  Add New Fix
        # self.client_ok.clicked.connect(self.new_fix)
        #
        # # Sell OK
        self.client_sell_add.clicked.connect(self.client_sell_adding)
        # self.client_sell_remove.clicked.connect(self.client_sell_remove)
        self.client_sell_ok.clicked.connect(self.client_sell_confirm)
        # Client Sell
        self.buttonBox.accepted.connect(self.go_to_sell)
        self.buttonBox.rejected.connect(self.hide_client_group)

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

    def open_search(self):
        self.mainTab.setCurrentIndex(0)

    def open_store(self):
        self.mainTab.setCurrentIndex(1)

    def open_sell(self):
        self.mainTab.setCurrentIndex(2)

    def open_buy(self):
        self.mainTab.setCurrentIndex(3)

    def open_house(self):
        self.mainTab.setCurrentIndex(4)

    def open_clients(self):
        self.mainTab.setCurrentIndex(5)

    def show_new_fix(self):
        if self.groupBox.isHidden():
            self.groupBox.setHidden(False)
        else:
            self.groupBox.setHidden(True)

    def hide_group(self):
        self.buying_group.setHidden(True)

    def hide_sell_group(self):
        self.selling_group.setHidden(True)

    def hide_client_group(self):
        self.new_groupBox.setHidden(True)

    # *******************************
    # *******************************
    # *******************************

    def search_show_products(self):

        self.cur = self.db.cursor()
        self.cur.execute('''SELECT p_name FROM products ''')
        data = self.cur.fetchall()
        if data:
            for item in data:
                self.search_name.addItem(item[0])

    def search(self):
        name = self.search_name.currentText()

        self.cur = self.db.cursor()

        if name == 'الكل':
            self.cur.execute(f'''SELECT * FROM products''')
        else:
            self.cur.execute(f'''SELECT * FROM products WHERE p_name=%s''', [name])

        data = self.cur.fetchall()
        if data:
            self.search_table.setRowCount(0)
            self.search_table.insertRow(0)
            for row, form in enumerate(data):
                for col, item in enumerate(form):
                    self.search_table.setItem(row, col, QTableWidgetItem(str(item)))
                    col += 1
                row_pos = self.search_table.rowCount()
                self.search_table.insertRow(row_pos)

    # -------------------------------
    # -------------------------------
    # -------------------------------

    def store_db(self):

        self.cur = self.db.cursor()
        self.cur.execute(f''' SELECT id, p_name, s_number, p_price FROM products ''')
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

    # -------------------------------
    # -------------------------------
    # -------------------------------

    def sell_show_products(self):

        self.cur = self.db.cursor()
        self.cur.execute('''SELECT p_name FROM products ''')
        data = self.cur.fetchall()
        if data:
            self.sell_name.clear()
            for item in data:
                self.sell_name.addItem(item[0])

    def sell_db(self):

        """Done .
        All things of Sell tab
        """

        name = self.sell_name.currentText()
        if len(self.sell_number.text().strip()) > 0:
            number = int(self.sell_number.text().strip())
        else:
            number = 0

        if len(self.sell_dis.text()):
            discount = float(self.sell_dis.text().strip())
        else:
            discount = 0

        self.cur = self.db.cursor()
        self.cur.execute(
            f'''SELECT p_price,s_number FROM products WHERE p_name=%s''', [name])
        data = self.cur.fetchone()

        # Check if there is Enough
        if data:
            unit_price = float(data[0])
            number_stored = int(data[1])
            # ------------
            # ## Print Number on digital screen  and Unit Price
            self.sell_unit.setText(f'{unit_price}')
            total = number * unit_price
            self.sell_total.setText(f'{total}')
            # -------------
            total_after = total
            if self.sell_pound.isChecked():
                total_after = total - discount

            if self.sell_per.isChecked():
                total_after = total - (total * discount / 100)

            self.sell_total_after.setText(f'{total_after}')

            for i in sell_list:
                if i[0] == name:
                    number_stored = i[2]

            self.sell_available.display(number_stored)

            return name, number, number_stored, unit_price, total, total_after

    def sell_adding(self):
        global sell_list
        name, number, number_stored, unit_price, total, total_after = self.sell_db()

        remaining = number_stored

        if number > number_stored:
            # ------------
            # ## Print No enough in store
            print(f'No enough units of {name}, Only {number_stored} left')
            # --------------

        else:
            remaining -= number

            self.sell_available.display(remaining)

            for i in range(len(sell_list)):
                if (sell_list[i][0] == name) and (
                        round(sell_list[i][5] / sell_list[i][1], 2) == round(total_after / number, 2)):
                    sell_list[i][1] += number  # number
                    sell_list[i][2] -= number  # Remaining
                    sell_list[i][4] += total  # Total
                    sell_list[i][5] += total_after  # Total After

                    break
            else:
                sell_list.append([name, number, remaining, unit_price, total, total_after])

            x = 0
            self.sell_table.setRowCount(0)

            for i in sell_list:
                row_pos = self.sell_table.rowCount()
                self.sell_table.insertRow(row_pos)
                self.sell_table.setItem(row_pos, 0, QTableWidgetItem(str(i[0])))
                self.sell_table.setItem(row_pos, 1, QTableWidgetItem(str(i[1])))
                self.sell_table.setItem(row_pos, 2, QTableWidgetItem(str(i[3])))
                self.sell_table.setItem(row_pos, 3, QTableWidgetItem(str(i[4])))
                self.sell_table.setItem(row_pos, 4, QTableWidgetItem(str(i[5])))

                self.sell_remove_name.addItem(i[0])
                x += i[5]
                self.all_sell_total.setText(str(x))
            self.sell_dis.setText('')

    def sell_remove(self):
        global sell_list
        name = self.sell_remove_name.currentText()
        found = self.sell_table.findItems(name)
        idx = found.row()
        self.sell_table.removeRow(idx)

        for i in sell_list:
            if i[0] == name:
                sell_list.remove(i)

    def sell_confirm(self):
        global sell_list

        self.cur = self.db.cursor()

        for i in sell_list:
            self.cur.execute(f'''UPDATE products set s_number=%s WHERE p_name=%s ''', (i[2], i[0]))
        self.db.commit()

        # self.sell_table.clear()
        self.sell_table.setRowCount(0)

        self.sell_number.setText('0')
        self.sell_total.setText('0')
        self.sell_dis.setText('0')
        self.sell_total_after.setText('0')

        self.sell_remove_name.clear()

        sell_list.clear()
        self.hide_sell_group()

        self.product_refresh()

    def print_sell_list(self):

        global sell_list

        self.selling_group.setHidden(False)

        table = Texttable()
        table.set_cols_width([20, 7, 8, 9, 9])
        # table.set_cols_align(["r", "r", "r", "r"])

        table.header(["المنتج", "العدد", "سعر القطعه", "الاجمالي", "بعد الخصم"])
        x = 0
        for item in sell_list:
            name = item[0]
            number = item[1]
            unit_price = item[3]
            total = item[4]
            last_price = item[5]
            x += int(total)
            table.add_row([name, number, unit_price, total, last_price])

        self.selling_label.setText(table.draw() + '\n' + f'الاجالي = {x}')

        print(table.draw())

    # -------------------------------
    # -------------------------------
    # -------------------------------

    def buy_adding(self):
        global buy_list
        """Done .
        All things of Sell tab
        """
        # Getting info from UI
        name = self.buy_name.text().strip()
        number = self.buy_number.text().strip()
        unit_price = self.buy_unit.text().strip()
        place = self.buy_place.currentText()

        for i in range(len(buy_list)):
            if buy_list[i][0] == name and buy_list[i][3] == place:
                buy_list[i][1] += int(number)
                break

        else:
            buy_list.append([name, int(number), float(unit_price), place])
        self.buy_table.setRowCount(0)
        for i in buy_list:
            row_pos = self.buy_table.rowCount()
            self.buy_table.insertRow(row_pos)
            self.buy_table.setItem(row_pos, 0, QTableWidgetItem(str(i[0])))
            self.buy_table.setItem(row_pos, 1, QTableWidgetItem(str(i[1])))
            self.buy_table.setItem(row_pos, 2, QTableWidgetItem(str(i[2])))
            self.buy_table.setItem(row_pos, 3, QTableWidgetItem(str(i[3])))

            self.buy_remove_name.addItem(i[0])

    def buy_remove(self):

        name = self.buy_remove_name.currentText()
        found = self.sell_table.findItems(name)
        idx = found.row()
        self.buy_table.removeRow(idx)

    def buy_confirm(self):
        global buy_list

        self.cur = self.db.cursor()

        for i in buy_list:

            name = i[0]
            number = int(i[1])
            unit_price = float(i[2])
            place = i[3]

            self.cur.execute(f''' SELECT p_price,s_number,h_number FROM products WHERE p_name=%s''', [name])
            data = self.cur.fetchone()

            s_number = 0
            h_number = 0

            if data:
                p_price = float(data[0])
                s_number = int(data[1])
                h_number = int(data[2])

                if p_price == unit_price:
                    if place == 'محل':
                        s_number += number

                    else:
                        h_number += number
                else:
                    # --------------
                    # --------------
                    print(' Different Prices')
                    # check if yes set unit_price else p_price
                    if ((True)):  # Don't change the price
                        unit_price = p_price

                    # ----------------
                    # ----------------

                self.cur.execute(
                    f'''UPDATE products SET p_price=%s,s_number=%s WHERE p_name=%s ''', (unit_price, s_number, name))
                # -------------

            else:
                if place == 'محل':
                    s_number += number

                else:
                    h_number += number
                self.cur.execute('''INSERT INTO products (p_name, p_price, s_number, h_number) VALUES (%s,%s,%s,%s)''',
                                 (name, unit_price, s_number, h_number))
            self.db.commit()

        # self.buy_table.clear()
        self.buy_table.setRowCount(0)
        self.buy_remove_name.clear()

        self.product_refresh()
        buy_list.clear()
        self.hide_group()

    def print_buy_list(self):
        global buy_list

        self.buying_group.setHidden(False)

        table = Texttable()
        table.set_cols_width([25, 10, 10, 10])
        # table.set_cols_align(["r", "r", "r", "r"])

        table.header(["المنتج", "العدد", "المكان", "سعر القطعه"])
        # table.set_cols_align(["c", "c", "c", "l"])

        for item in buy_list:
            table.set_cols_align(["c", "l", "l", "l"])

            name = item[0]
            number = item[1]
            unit_price = item[2]
            place = item[3]
            table.add_row([name, number, place, unit_price])

        self.label_9.setText(table.draw())

        print(table.draw())


        # self.buy_lst.append(table.draw())

    # -------------------------------
    # -------------------------------
    # -------------------------------

    def house_db(self):

        self.cur = self.db.cursor()
        self.cur.execute(f''' SELECT id, p_name, h_number, p_price FROM products ''')
        data = self.cur.fetchall()
        if data:
            self.house_table.setRowCount(0)
            self.house_table.insertRow(0)
            for row, form in enumerate(data):
                print(form)

                for col, item in enumerate(form):
                    self.house_table.setItem(row, col, QTableWidgetItem(str(item)))
                    col += 1
                row_pos = self.house_table.rowCount()
                self.house_table.insertRow(row_pos)

    def show_house_name(self):

        self.cur = self.db.cursor()
        self.cur.execute('''SELECT p_name,h_number FROM products''')
        data = self.cur.fetchall()
        if data:
            self.house_name.clear()
            for item in data:
                if int(item[1]) > 0:
                    self.house_name.addItem(item[0])

    def move_to_store(self):
        # Getting info from UI
        name = self.house_name.currentText()
        number = int(self.house_number.text().strip())

        self.cur = self.db.cursor()
        self.cur.execute(f'''SELECT h_number,s_number FROM products WHERE p_name=%s''', [name])
        data = self.cur.fetchone()

        if data:
            h_number = int(data[0])
            s_number = int(data[1])

            if number > h_number:
                # ---------------
                print("Not Enough")
                # ---------------
            else:
                h_number -= number
                s_number += number
                self.cur.execute(f'''UPDATE products set h_number=%s,s_number=%s WHERE p_name=%s''',
                                 (h_number, s_number, name))
                self.db.commit()
                self.product_refresh()

    def remove_product(self):
        pass

    # -------------------------------
    # ------   Clients  -------------
    # -------------------------------

    def new_client(self):
        # Getting info from UI
        name = self.new_client_name.text().strip()
        number = self.new_client_phone.text().strip()
        bike = self.new_client_bike.text().strip()
        color = self.new_client_color.text().strip()
        condition = self.new_client_condition.text()
        fix_date = self.new_client_fix_date.date().toPyDate()
        fix = self.new_client_fix.text()
        paid = float(self.new_client_money.text().strip())
        cost = float(self.new_client_cost.text().strip())
        added_time = datetime.datetime.now()

        self.cur = self.db.cursor()
        self.cur.execute(
            '''INSERT INTO clients (c_name,c_phone,bike,bike_color,bike_condition) VALUES (%s,%s,%s,%s,%s)''',
            (name, number, bike, color, condition))

        self.cur.execute(
            '''INSERT INTO fixes (c_name,in_date,fix_date,fix,paid,fix_cost) VALUES (%s,%s,%s,%s,%s,%s)''',
            (name, added_time, fix_date, fix, paid, cost))
        self.db.commit()
        self.new_groupBox.setHidden(False)

    def show_client_name(self):

        self.cur = self.db.cursor()
        self.cur.execute('''SELECT c_name FROM clients''')
        data = self.cur.fetchall()
        if data:
            for item in data:
                self.client_name.addItem(item[0])

    def current_client(self):
        # Getting info from UI
        name = self.client_name.currentText()

        self.cur = self.db.cursor()
        self.cur.execute(f''' SELECT c_phone, bike, bike_color, bike_condition FROM clients WHERE c_name=%s''', [name])
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

        self.cur.execute(f'''SELECT in_date,fix_date,fix,paid,fix_cost FROM fixes WHERE c_name=%s''', [name])
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
        name = self.client_name.currentText()
        fix_date = self.client_fix_date.date().toPyDate()
        fix = self.client_fix.text()
        paid = float(self.client_money.text().strip())
        cost = float(self.client_cost.text().strip())
        added_time = datetime.datetime.now()

        self.cur = self.db.cursor()
        self.cur.execute(f'''INSERT INTO fixes (c_name,in_date,fix_date,fix,paid,fix_cost) 
        VALUES (%s,%s,%s,%s)''', (name, added_time, fix_date, fix, paid, cost))
        self.db.commit()

    def show_all_clients(self):

        self.cur = self.db.cursor()
        self.cur.execute(f''' SELECT c_name, c_phone,bike FROM clients ''')
        client_data = self.cur.fetchall()

        self.cur.execute(f''' SELECT c_name, fix,fix_date FROM fixes ''')
        fix_data = self.cur.fetchall()

        # Make data in the same list
        # n = 0
        # for i, j in zip(client_data, fix_data):
        #     for item in j:
        #         client_data[n].append(item)
        #     n += 1

        if client_data:
            self.all_clients.setRowCount(0)
            self.all_clients.insertRow(0)
            for row, form in enumerate(client_data):
                name = form[0]
                phone = form[1]
                bike = form[2]
                self.all_clients.setItem(row, 0, QTableWidgetItem(str(name)))
                self.all_clients.setItem(row, 1, QTableWidgetItem(str(phone)))
                self.all_clients.setItem(row, 2, QTableWidgetItem(str(bike)))

                # for col, item in enumerate(form):
                #     self.store_table.setItem(row, col, QTableWidgetItem(str(item)))
                #     col += 1
                row_pos = self.all_clients.rowCount()
                self.all_clients.insertRow(row_pos)

    def show_client_sell_products(self):

        self.cur = self.db.cursor()
        self.cur.execute('''SELECT p_name FROM products''')
        data = self.cur.fetchall()
        if data:
            for item in data:
                self.client_sell_product.addItem(item[0])

    # -------------------------------
    # -------------------------------
    # -------------------------------

    # *******************************
    #   Settings
    # *******************************
    def product_refresh(self):
        self.search_show_products()
        self.search()
        self.store_db()
        self.sell_show_products()
        self.show_avail()
        self.house_db()
        self.show_house_name()

    def show_avail(self):
        name = self.sell_name.currentText()

        self.cur = self.db.cursor()
        self.cur.execute(
            f'''SELECT p_price,s_number FROM products WHERE p_name=%s''', [name])
        data = self.cur.fetchone()

        # Check if there is Enough
        if data:
            unit_price = data[0]
            number_stored = data[1]
            # ------------
            # ## Print Number on digital screen  and Unit Price
            for i in sell_list:
                if i[0] == name:
                    number_stored = i[2]

            self.sell_available.display(number_stored)
            self.sell_unit.setText(f'{unit_price}')

    def calc_total(self):
        if len(self.sell_number.text()) > 0:
            number = int(self.sell_number.text())
        else:
            number = 0

        unit_price = float(self.sell_unit.text())

        total = number * unit_price
        self.sell_total.setText(f'{total}')
        self.all_sell_total.setText(f'{total}')

    def calc_dis_total(self):
        global sell_list
        # total = 0
        # for item in sell_list:
        #     total += item[5]
        total = float(self.all_sell_total.text())

        all_sell_dis = self.all_sell_dis.text()
        if len(all_sell_dis) > 0:
            discount = float(all_sell_dis)
        else:
            discount = 0

        total_after = total
        if self.all_sell_pound.isChecked():
            total_after = total - discount

        if self.all_sell_per.isChecked():
            total_after = total - (total * discount / 100)

        self.all_sell_total_after.setText(f'{total_after}')

        # ## Return Total and Total After Discount

    def calc_after(self):
        total = float(self.sell_total.text())
        discount = self.sell_dis.text()
        if len(discount) > 0:
            discount = float(discount)
        else:
            discount = 0

        total_after = total
        if self.sell_pound.isChecked():
            total_after = total - discount

        if self.sell_per.isChecked():
            total_after = total - (total * discount / 100)

        self.sell_total_after.setText(f'{total_after}')

    def remove_all_sell(self):
        self.sell_table.setRowCount(0)
        self.sell_remove_name.clear()
        sell_list.clear()

    def remove_all_buy(self):
        self.buy_table.setRowCount(0)
        self.buy_remove_name.clear()
        buy_list.clear()

    def go_to_sell(self):
        self.mainTab.setCurrentIndex(2)
        self.new_client_name.setText('')
        self.new_client_phone.setText('')
        self.new_client_bike.setText('')
        self.new_client_color.setText('')
        self.new_client_condition.setText('')
        self.new_client_fix.setText('')
        self.new_client_money.setText('')
        self.new_client_cost.setText('')
        self.show_client_name()
        self.show_all_clients()


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.setWindowTitle('TA-System')
    window.setWindowIcon(QIcon('pic\ico.jpg'))
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
