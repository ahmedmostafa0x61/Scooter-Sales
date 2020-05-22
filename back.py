from datetime import datetime, timedelta
import sys
from webbrowser import open
import MySQLdb
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
from texttable import Texttable

# from GUI import Ui_MainWindow as Program

Program, _ = loadUiType('GUI.ui')

my_db = MySQLdb.connect(host='localhost', user='root', password='159753852456', db='scooter')
my_db.set_character_set('utf8')

sell_list = [[]]
sell_list.clear()

buy_list = [[]]
buy_list.clear()


class MainApp(QMainWindow, Program):
    def __init__(self):
        super(MainApp, self).__init__()
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.showNormal()
        self.db = my_db

        self.ui_changes()
        self.buttons()

        # ---------------
        self.product_refresh()

        self.show_all_clients()
        self.show_client_name()
        # self.show_house_name()
        self.get_sales_date()

        self.auto_complete()

    # *******************************
    # *******************************
    #   Changes in UI
    # *******************************

    def main_tab_changes(self):
        self.mainTab.tabBar().setVisible(False)
        self.mainTab.setCurrentIndex(0)

    def client_tab_changes(self):
        self.clientTab.setCurrentIndex(0)

    def buy_table_changes(self):
        self.buy_table.verticalHeader().hide()
        # Column Size
        self.buy_table.setColumnWidth(0, 200)
        self.buy_table.setColumnWidth(1, 100)
        self.buy_table.setColumnWidth(2, 100)
        self.buy_table.setColumnWidth(3, 100)

    def sell_table_changes(self):
        self.sell_table.verticalHeader().hide()
        # Column Size
        self.sell_table.setColumnWidth(0, 200)
        self.sell_table.setColumnWidth(1, 100)
        self.sell_table.setColumnWidth(2, 100)
        self.sell_table.setColumnWidth(3, 100)
        self.sell_table.setColumnWidth(4, 100)

    def search_table_changes(self):
        self.search_table.verticalHeader().hide()
        self.search_table.setSortingEnabled(True)
        # Column size
        self.search_table.setColumnWidth(0, 50)
        self.search_table.setColumnWidth(1, 200)
        self.search_table.setColumnWidth(2, 100)
        self.search_table.setColumnWidth(3, 100)
        self.search_table.setColumnWidth(4, 100)

    def store_table_changes(self):
        self.store_table.verticalHeader().hide()
        self.store_table.setSortingEnabled(True)

        self.store_table.setColumnWidth(0, 50)
        self.store_table.setColumnWidth(0, 200)
        self.store_table.setColumnWidth(0, 100)
        self.store_table.setColumnWidth(0, 100)

    def house_table_changes(self):
        self.house_table.verticalHeader().hide()
        self.house_table.setSortingEnabled(True)

        self.house_table.setColumnWidth(0, 50)
        self.house_table.setColumnWidth(1, 200)
        self.house_table.setColumnWidth(2, 100)
        self.house_table.setColumnWidth(3, 100)

    def all_clients_table_changes(self):
        self.all_clients.verticalHeader().hide()
        self.all_clients.setColumnWidth(0, 175)
        self.all_clients.setColumnWidth(1, 100)
        self.all_clients.setColumnWidth(2, 100)
        self.all_clients.setColumnWidth(3, 80)
        self.all_clients.setColumnWidth(4, 100)
        self.all_clients.setColumnWidth(5, 300)

    def fixes_table_changes(self):
        self.fixes_table.verticalHeader().hide()

        self.fixes_table.setColumnWidth(0, 100)
        self.fixes_table.setColumnWidth(1, 100)
        self.fixes_table.setColumnWidth(2, 350)
        self.fixes_table.setColumnWidth(3, 100)
        # self.fixes_table.setColumnWidth(4, 100)

    def input_strict(self):
        self.sell_number.setValidator(QIntValidator())
        self.buy_number.setValidator(QIntValidator())
        self.house_number.setValidator(QIntValidator())

        self.buy_unit.setValidator(QDoubleValidator())
        self.sell_dis.setValidator(QDoubleValidator())
        self.all_sell_dis.setValidator(QDoubleValidator())

        # self.new_client_money.setValidator(QDoubleValidator())
        self.new_client_cost.setValidator(QDoubleValidator())
        # self.client_money.setValidator(QDoubleValidator())
        self.client_cost.setValidator(QDoubleValidator())

    def calender_today(self):
        self.new_client_fix_date.setDateTime(QDateTime.currentDateTime())
        self.client_fix_date.setDateTime(QDateTime.currentDateTime())

    def ui_changes(self):

        self.main_tab_changes()
        self.client_tab_changes()
        self.buy_table_changes()
        self.sell_table_changes()
        self.search_table_changes()
        self.store_table_changes()
        self.house_table_changes()
        self.all_clients_table_changes()
        self.fixes_table_changes()
        self.input_strict()
        self.calender_today()

        self.groupBox.setHidden(True)
        self.buying_group.setHidden(True)
        self.selling_group.setHidden(True)
        self.new_groupBox.setHidden(True)

    # *******************************
    #   Buttons
    # *******************************

    def main_buttons(self):
        self.buy_pb.clicked.connect(self.open_buy)
        self.search_pb.clicked.connect(self.open_search)
        self.sell_pb.clicked.connect(self.open_sell)
        self.store_pb.clicked.connect(self.open_store)
        self.house_pb.clicked.connect(self.open_house)
        self.client_pb.clicked.connect(self.open_clients)
        self.sales_pb.clicked.connect(self.open_sales)

    def search_buttons(self):
        self.search_name.textChanged.connect(self.search)

    def buy_buttons(self):
        self.buy_add.clicked.connect(self.buy_adding)
        self.buy_remove_ok.clicked.connect(self.buy_remove)
        self.buy_remove_all.clicked.connect(self.remove_all_buy)
        self.buy_ok.clicked.connect(self.print_buy_list)

        self.accept_box.accepted.connect(self.buy_confirm)
        self.accept_box.rejected.connect(self.hide_group)

    def sell_buttons(self):
        self.sell_add.clicked.connect(self.sell_adding)
        self.sell_remove_ok.clicked.connect(self.sell_remove)
        self.sell_remove_all.clicked.connect(self.remove_all_sell)
        self.sell_ok.clicked.connect(self.print_sell_list)

        self.sell_accept_box.accepted.connect(self.sell_confirm)
        self.sell_accept_box.rejected.connect(self.hide_sell_group)

        self.sell_name.textChanged.connect(self.show_avail)
        self.sell_number.textEdited.connect(self.calc_total)

        # Calculate The Discount
        self.sell_dis.textEdited.connect(self.calc_after)
        self.sell_pound.released.connect(self.calc_after)
        self.sell_per.released.connect(self.calc_after)

        #  Total Discount
        self.all_sell_dis.textEdited.connect(self.calc_dis_total)
        self.all_sell_pound.pressed.connect(self.calc_dis_total)
        self.all_sell_per.pressed.connect(self.calc_dis_total)

    def new_client_buttons(self):
        self.new_client_ok.clicked.connect(self.new_client)

        # Client Sell
        self.buttonBox.accepted.connect(self.go_to_sell)
        self.buttonBox.rejected.connect(self.hide_client_group)

    def client_buttons(self):
        self.client_ok.clicked.connect(self.new_fix)

        self.add_new_fix.clicked.connect(self.show_new_fix)

        self.client_change.clicked.connect(self.update_client)

    def sales_buttons(self):
        self.sales_date.currentTextChanged.connect(self.get_sales_date)
        self.save_operation.clicked.connect(self.add_operation)

    def buttons(self):
        self.main_buttons()
        self.search_buttons()
        self.buy_buttons()
        self.sell_buttons()
        self.new_client_buttons()
        self.client_buttons()
        self.sales_buttons()

        # House
        self.house_ok.clicked.connect(self.move_to_store)

        #  Current Client
        self.client_name.currentTextChanged.connect(self.current_client)

        # Facebook button
        self.pushButton.clicked.connect(lambda: open('https://www.facebook.com/techarenaeg'))
        self.pushButton.clicked.connect(lambda: open('https://www.facebook.com/techarenaeg'))

    # *******************************
    #   Opening  Tabs
    # *******************************

    def open_search(self):
        self.mainTab.setCurrentIndex(0)
        self.search_pb.setStyleSheet(
            " background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2980B9, stop: 1 #4286f4);")

        self.buy_pb.setStyleSheet("background-color: #F2F2F2;")
        self.sell_pb.setStyleSheet("background-color: #F2F2F2;")
        self.store_pb.setStyleSheet("background-color: #F2F2F2;")
        self.house_pb.setStyleSheet("background-color: #F2F2F2;")
        self.client_pb.setStyleSheet("background-color: #F2F2F2;")
        self.sales_pb.setStyleSheet("background-color: #F2F2F2;")

    def open_store(self):
        self.mainTab.setCurrentIndex(1)

        self.store_pb.setStyleSheet(
            " background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2980B9, stop: 1 #4286f4);")

        self.buy_pb.setStyleSheet("background-color: #F2F2F2;")
        self.sell_pb.setStyleSheet("background-color: #F2F2F2;")
        self.search_pb.setStyleSheet("background-color: #F2F2F2;")
        self.house_pb.setStyleSheet("background-color: #F2F2F2;")
        self.client_pb.setStyleSheet("background-color: #F2F2F2;")
        self.sales_pb.setStyleSheet("background-color: #F2F2F2;")

    def open_buy(self):
        self.mainTab.setCurrentIndex(2)
        self.buy_pb.setStyleSheet(
            " background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2980B9, stop: 1 #4286f4);")

        self.store_pb.setStyleSheet("background-color: #F2F2F2;")
        self.sell_pb.setStyleSheet("background-color: #F2F2F2;")
        self.search_pb.setStyleSheet("background-color: #F2F2F2;")
        self.house_pb.setStyleSheet("background-color: #F2F2F2;")
        self.client_pb.setStyleSheet("background-color: #F2F2F2;")
        self.sales_pb.setStyleSheet("background-color: #F2F2F2;")

    def open_sell(self):
        self.mainTab.setCurrentIndex(3)
        self.sell_pb.setStyleSheet(
            " background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2980B9, stop: 1 #4286f4);")

        self.store_pb.setStyleSheet("background-color: #F2F2F2;")
        self.buy_pb.setStyleSheet("background-color: #F2F2F2;")
        self.search_pb.setStyleSheet("background-color: #F2F2F2;")
        self.house_pb.setStyleSheet("background-color: #F2F2F2;")
        self.client_pb.setStyleSheet("background-color: #F2F2F2;")
        self.sales_pb.setStyleSheet("background-color: #F2F2F2;")

    def open_house(self):
        self.mainTab.setCurrentIndex(4)
        self.house_pb.setStyleSheet(
            " background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2980B9, stop: 1 #4286f4);")

        self.store_pb.setStyleSheet("background-color: #F2F2F2;")
        self.buy_pb.setStyleSheet("background-color: #F2F2F2;")
        self.search_pb.setStyleSheet("background-color: #F2F2F2;")
        self.sell_pb.setStyleSheet("background-color: #F2F2F2;")
        self.client_pb.setStyleSheet("background-color: #F2F2F2;")
        self.sales_pb.setStyleSheet("background-color: #F2F2F2;")

    def open_clients(self):
        self.mainTab.setCurrentIndex(5)
        self.client_pb.setStyleSheet(
            " background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2980B9, stop: 1 #4286f4);")

        self.store_pb.setStyleSheet("background-color: #F2F2F2;")
        self.buy_pb.setStyleSheet("background-color: #F2F2F2;")
        self.search_pb.setStyleSheet("background-color: #F2F2F2;")
        self.sell_pb.setStyleSheet("background-color: #F2F2F2;")
        self.house_pb.setStyleSheet("background-color: #F2F2F2;")
        self.sales_pb.setStyleSheet("background-color: #F2F2F2;")

    def open_sales(self):
        self.mainTab.setCurrentIndex(6)
        self.sales_pb.setStyleSheet(
            " background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2980B9, stop: 1 #4286f4);")

        self.store_pb.setStyleSheet("background-color: #F2F2F2;")
        self.buy_pb.setStyleSheet("background-color: #F2F2F2;")
        self.search_pb.setStyleSheet("background-color: #F2F2F2;")
        self.sell_pb.setStyleSheet("background-color: #F2F2F2;")
        self.house_pb.setStyleSheet("background-color: #F2F2F2;")
        self.client_pb.setStyleSheet("background-color: #F2F2F2;")

    # -----------------------------
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
        self.new_client_name.setText('')
        self.new_client_phone.setText('')
        self.new_client_bike.setText('')
        self.new_client_color.setText('')
        self.new_client_condition.setText('')
        self.new_client_fix.setText('')
        # self.new_client_money.setText('')
        # self.new_client_cost.setText('')
        self.show_client_name()
        self.show_all_clients()

    # *******************************
    #      Search
    # *******************************

    # def search_show_products(self):
    #
    #     self.cur = self.db.cursor()
    #     self.cur.execute('''SELECT p_name FROM products ''')
    #     data = self.cur.fetchall()
    #     if data:
    #         for item in data:
    #             self.search_name.addItem(item[0])

    def search(self):

        name = self.search_name.text()

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

    # *******************************
    #      Store
    # *******************************

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

    # *******************************
    #      Sell
    # *******************************

    def sell_show_products(self):

        self.cur = self.db.cursor()
        self.cur.execute('''SELECT p_name FROM products ''')
        data = self.cur.fetchall()
        if data:
            self.sell_name.clear()
            for item in data:
                self.sell_name.addItem(item[0])

    def sell_db(self):

        """Getting Data From DB
        Put Data in GUI
        Return Data
        """

        name = self.sell_name.text()
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
        self.sell_available.setStyleSheet('color:black')
        if number > number_stored:
            # ------------
            # ## Print No enough in store
            self.sell_available.setStyleSheet('color:red')
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

            self.sell_remove_name.clear()
            self.print_sell_table_data()
            self.calc_dis_total()
            self.sell_dis.setText('')

    def print_sell_table_data(self):

        """
        - Print sell_table data
        - Calc total and print
        - Add items in Remove ComboBox
        """

        global sell_list
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

    def sell_remove(self):
        global sell_list
        name = self.sell_remove_name.currentText()

        for item in sell_list:
            if item[0] == name:
                sell_list.remove(item)

        self.sell_remove_name.clear()
        self.print_sell_table_data()

        self.sell_dis.setText('')

    def sell_confirm(self):
        global sell_list

        total = self.all_sell_total_after.text()
        date = datetime.today()

        self.cur = self.db.cursor()

        for i in sell_list:
            self.cur.execute(f'''UPDATE products set s_number=%s WHERE p_name=%s ''', (i[2], i[0]))

        self.cur.execute('''INSERT INTO sales (sale_date, operation, paid, text) VALUES (%s,%s,%s,%s)''',
                         [date, 'sell', total, 'بيع'])

        self.db.commit()

        # self.sell_table.clear()
        self.sell_table.setRowCount(0)

        self.sell_number.setText('0')
        self.sell_total.setText('0')
        self.sell_dis.setText('0')
        self.sell_total_after.setText('0')
        self.all_sell_total.setText('0')
        self.all_sell_total_after.setText('0')

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
        fix_cost = float(self.new_client_cost.text())
        print(fix_cost)
        if fix_cost > 0:
            self.selling_label.setText(
                table.draw() + '\n\n\t\t' + f'منتجات = {x}' + '\n\t\t' +
                f'بعد الخصم = {self.all_sell_total_after.text()}' + '\n\t\t' + f'مصنعيه = {fix_cost}' +
                '\n\n\t\t' + f'الاجمالي = {x+fix_cost}')
        else:
            self.selling_label.setText(
                table.draw() + '\n\n\t\t' + f'الاجمالي = {x}' + '/n\t\t' +
                f'بعد الخصم = {self.all_sell_total_after.text()}')

    def show_avail(self):
        name = self.sell_name.text()

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
        self.calc_dis_total()

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

    # *******************************
    #      Buy
    # *******************************

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

        self.print_buy_table_data()

    def print_buy_table_data(self):

        """Print but_table Data
        Add items in Remove ComboBox
        """
        global buy_list
        self.buy_remove_name.clear()
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
        global buy_list

        name = self.buy_remove_name.currentText()
        for item in buy_list:
            if item[0] == name:
                buy_list.remove(item)

        self.print_buy_table_data()

    def buy_confirm(self):
        global buy_list

        self.cur = self.db.cursor()

        for i in buy_list:

            name = i[0]
            number = int(i[1])
            unit_price = float(i[2])
            place = i[3]

            self.cur.execute(f''' SELECT s_number,h_number FROM products WHERE p_name=%s''', [name])
            data = self.cur.fetchone()

            s_number = 0
            h_number = 0

            if data:

                s_number = int(data[0])
                h_number = int(data[1])

                if place == 'محل':
                    s_number += number

                else:
                    h_number += number

                self.cur.execute(
                    f'''UPDATE products SET p_price=%s,s_number=%s WHERE p_name=%s ''', (unit_price, s_number, name))

            else:
                if place == 'محل':
                    s_number += number

                else:
                    h_number += number

                self.cur.execute('''INSERT INTO products (p_name, p_price, s_number, h_number) VALUES (%s,%s,%s,%s)''',
                                 (name, unit_price, s_number, h_number))
            self.db.commit()

        self.buy_table.setRowCount(0)
        self.buy_remove_name.clear()
        self.buy_name.setText('')
        self.buy_number.setText('')
        self.buy_unit.setText('')

        self.product_refresh()
        self.hide_group()
        buy_list.clear()

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

    def remove_all_buy(self):
        self.buy_table.setRowCount(0)
        self.buy_remove_name.clear()
        buy_list.clear()

    # *******************************
    #      Warehouse
    # *******************************

    def house_db(self):
        self.cur = self.db.cursor()
        self.cur.execute(f''' SELECT id, p_name, h_number, p_price FROM products ''')
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

    # def show_house_name(self):
    #
    #     self.cur = self.db.cursor()
    #     self.cur.execute('''SELECT p_name,h_number FROM products''')
    #     data = self.cur.fetchall()
    #     if data:
    #         self.house_name.clear()
    #         for item in data:
    #             if int(item[1]) > 0:
    #                 self.house_name.addItem(item[0])

    def move_to_store(self):
        # Getting info from UI
        name = self.house_name.text()
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

    # *******************************
    #      Clients
    # *******************************

    def new_client(self):
        # Getting info from UI
        name = self.new_client_name.text().strip()
        number = self.new_client_phone.text().strip()
        bike = self.new_client_bike.text().strip()
        color = self.new_client_color.text().strip()
        condition = self.new_client_condition.text()
        fix_date = self.new_client_fix_date.date().toPyDate()
        fix = self.new_client_fix.text()
        # paid = float(self.new_client_money.text().strip())
        cost = float(self.new_client_cost.text().strip())
        added_time = datetime.now()

        self.cur = self.db.cursor()
        self.cur.execute(
            '''INSERT INTO clients (c_name,c_phone,bike,bike_color,bike_condition,fix,fix_date) 
            VALUES (%s,%s,%s,%s,%s,%s,%s)''', (name, number, bike, color, condition, fix, fix_date))

        self.cur.execute(
            '''INSERT INTO fixes (c_name,in_date,fix_date,fix,fix_cost) VALUES (%s,%s,%s,%s,%s)''',
            (name, added_time, fix_date, fix, cost))
        self.db.commit()
        self.new_groupBox.setHidden(False)

    def show_client_name(self):

        self.cur = self.db.cursor()
        self.cur.execute('''SELECT c_name FROM clients''')
        data = self.cur.fetchall()
        if data:
            self.client_name.clear()
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

        self.cur.execute(f'''SELECT in_date,fix_date,fix,fix_cost FROM fixes WHERE c_name=%s''', [name])
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
        # paid = float(self.client_money.text().strip())
        cost = float(self.client_cost.text().strip())
        added_time = datetime.now()

        self.cur = self.db.cursor()
        self.cur.execute(f'''INSERT INTO fixes (c_name,in_date,fix_date,fix,fix_cost) 
        VALUES (%s,%s,%s,%s,%s)''', [name, added_time, fix_date, fix, cost])

        self.cur.execute('''UPDATE clients SET fix=%s, fix_date=%s WHERE c_name=%s''', (fix, fix_date, name))
        self.db.commit()

        self.show_all_clients()
        self.current_client()
        self.groupBox.setHidden(True)
        self.client_fix.setText('')
        # self.client_money.setText('')
        self.client_cost.setText('')

    def update_client(self):
        name = self.client_name.currentText()
        phone = self.client_phone.text()
        bike = self.client_bike.text()
        color = self.client_color.text()
        condition = self.client_condition.text()

        self.cur = self.db.cursor()
        self.cur.execute(
            '''UPDATE clients SET c_phone=%s, bike=%s, bike_color=%s, bike_condition=%s WHERE c_name=%s''',
            [phone, bike, color, condition, name])
        self.db.commit()

    def show_all_clients(self):

        self.cur = self.db.cursor()
        self.cur.execute(f''' SELECT c_name, c_phone, bike, bike_color, fix_date, fix  FROM clients ''')
        client_data = self.cur.fetchall()

        if client_data:
            self.all_clients.setRowCount(0)
            self.all_clients.insertRow(0)
            for row, form in enumerate(client_data):
                name = form[0]
                phone = form[1]
                bike = form[2]
                color = form[3]
                fix_date = form[4]
                fix = form[5]
                self.all_clients.setItem(row, 0, QTableWidgetItem(str(name)))
                self.all_clients.setItem(row, 1, QTableWidgetItem(str(phone)))
                self.all_clients.setItem(row, 2, QTableWidgetItem(str(bike)))
                self.all_clients.setItem(row, 3, QTableWidgetItem(str(color)))
                self.all_clients.setItem(row, 4, QTableWidgetItem(str(fix_date)))
                self.all_clients.setItem(row, 5, QTableWidgetItem(str(fix)))

                row_pos = self.all_clients.rowCount()
                self.all_clients.insertRow(row_pos)

    def go_to_sell(self):
        self.mainTab.setCurrentIndex(3)
        self.new_client_name.setText('')
        self.new_client_phone.setText('')
        self.new_client_bike.setText('')
        self.new_client_color.setText('')
        self.new_client_condition.setText('')
        self.new_client_fix.setText('')
        # self.new_client_money.setText('')
        # cost = self.new_client_cost.text()
        self.show_client_name()
        self.show_all_clients()
        self.hide_client_group()

    # *******************************
    #   Reshow Products Data
    # *******************************

    def product_refresh(self):
        # self.search_show_products()
        self.search()
        self.store_db()
        # self.sell_show_products()
        self.show_avail()
        self.house_db()
        # self.show_house_name()

    # *******************************
    #   Sales
    # *******************************

    def get_sales_date(self):

        date = self.sales_date.currentIndex()
        today = datetime.today()

        if date == 0:
            today = today.date()
        elif date == 1:
            today = (today - timedelta(days=30)).date()
        elif date == 2:
            today = (today - timedelta(days=180)).date()
        elif date == 3:
            today = (today - timedelta(days=365)).date()
        elif date == 4:
            today = (today - timedelta(weeks=10000)).date()

        self.cur = self.db.cursor()
        self.cur.execute('''SELECT sale_date, paid, text FROM sales WHERE sale_date>=%s ORDER BY  sale_date DESC''',
                         [today])

        data = self.cur.fetchall()

        if data:
            self.sales_table.setRowCount(0)
            for row in data:
                date = row[0]
                money = row[1]
                text = row[2]

                row_pos = self.sales_table.rowCount()
                self.sales_table.insertRow(row_pos)
                self.sales_table.setItem(row_pos, 0, QTableWidgetItem(str(date)))
                self.sales_table.setItem(row_pos, 2, QTableWidgetItem(str(money)))
                self.sales_table.setItem(row_pos, 1, QTableWidgetItem(str(text)))
            self.calc_sales_total()

    def add_operation(self):
        money = self.op_money.text()
        operation = self.operation.currentIndex()
        text = self.op_text.text()
        date = datetime.today()

        self.cur = self.db.cursor()
        self.cur.execute('''INSERT INTO sales (sale_date, operation, paid, text) VALUES (%s,%s,%s,%s)''',
                         (date, operation, money, text))
        self.db.commit()
        self.calc_sales_total()
        self.get_sales_date()

        self.op_money.setText('')
        self.op_text.setText('')

    def calc_sales_total(self):

        self.cur = self.db.cursor()
        self.cur.execute('''SELECT paid,operation FROM sales''')
        data = self.cur.fetchall()
        total = 0
        if data:
            for item in data:
                paid = float(item[0])
                operation = item[1]
                if operation == '0' or operation == 'buy':
                    total -= paid
                elif operation == '1' or operation == 'sell':
                    total += paid

        self.sales_total.setText(f'{total}')

    # *******************************************
    # *******************************************
    # *******************************************
    # *******************************************

    def get_prod_name(self):
        self.cur = self.db.cursor()
        self.cur.execute('''SELECT p_name FROM products''')
        data = self.cur.fetchall()
        a = []
        if data:
            for i in data:
                a.append(i[0])
        return a

    def auto_complete(self):
        a = self.get_prod_name()
        com = QCompleter(a)
        self.search_name.setCompleter(com)
        self.sell_name.setCompleter(com)
        self.house_name.setCompleter(com)
        self.buy_name.setCompleter(com)
        # ///////////////////////



def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.setWindowTitle('TA-System')
    window.setWindowIcon(QIcon('pic\ico.jpg'))
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
