import os
import sys
import sqlite3
from datetime import date
from datetime import datetime
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType

ui, _ = loadUiType('assets/ui/stocking.ui')
db_path = os.path.join('database/', 'stocking.db')

class Color:
    RED = '\033[91m'
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

class MainApp(QMainWindow, ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.tabWidget.setCurrentIndex(0)
        self.login_button.clicked.connect(self.login)
        
        self.logout_1.clicked.connect(self.logout)
        self.logout_2.clicked.connect(self.logout)
        self.logout_3.clicked.connect(self.logout)
        
        self.order_entry_1.clicked.connect(self.showOrderEntry)
        self.order_entry_2.clicked.connect(self.showOrderEntry)
        self.order_entry_3.clicked.connect(self.showOrderEntry)
        
        self.edit_orders_1.clicked.connect(self.showEditOrders)
        self.edit_orders_2.clicked.connect(self.showEditOrders)
        self.edit_orders_3.clicked.connect(self.showEditOrders)
        
        self.orders_1.clicked.connect(self.showOrders)
        self.orders_2.clicked.connect(self.showOrders)
        self.orders_3.clicked.connect(self.showOrders)

        self.oe_button_1.clicked.connect(self.orderPlus)
        self.oe_button_2.clicked.connect(self.orderNext)
        
        try:
            db_chk = sqlite3.connect(db_path)
            db_chk.execute("CREATE TABLE IF NOT EXISTS order_data(order_id INTEGER, cx_name TEXT, cx_phno TEXT, product_id INTEGRER, quantity INTEGER, order_date TEXT)")
            db_chk.commit()
            print(Color.GREEN + "Created database sucessfully" + Color.RESET)
        except:
            print(db_chk.Error)
        
        self.genOrderId()
        self.editOidLoad()

    def login(self):
        usr_pwd = self.login_input.text()
        if usr_pwd == "sagayam":
            self.login_info.setText("")
            self.login_input.setText("")
            self.tabWidget.setCurrentIndex(1)
        else:
            self.login_info.setText("Wrong Password!")
        
    def logout(self):
        self.tabWidget.setCurrentIndex(0)
        
    def showOrderEntry(self):
        self.tabWidget.setCurrentIndex(1)
        
    def showEditOrders(self):
        self.tabWidget.setCurrentIndex(2)
        
    def showOrders(self):
        self.tabWidget.setCurrentIndex(3)

    def genOrderId(self):
        order_gen = 0
        try:
            oid_db = sqlite3.connect(db_path)
            cursor = oid_db.execute("SELECT MAX(order_id) FROM order_data")
            result = cursor.fetchall()
            if result:
                for maxid in result:
                    order_gen = maxid[0] + 1
                self.order_id.setText(str(order_gen))
        except:
            order_gen = 1001
            self.order_id.setText(str(order_gen))

    def orderNext(self):
        self.genOrderId()
        try:
            oe_db = sqlite3.connect(db_path)
            # order_id INTEGER, cx_name TEXT, cx_phno TEXT, product_id INTEGRER, quantity INTEGER, order_date TEXT, order_time TEXT
            oe_db.execute("INSERT INTO order_data VALUES ("+ self.order_id.text() +", '"+ self.oe_input_1.text() +"', '"+ self.oe_input_3.text() +"', "+ self.oe_input_2.text() +", "+ self.oe_input_4.text() +", '"+ str(date.today()) +"')")
            oe_db.commit()
        except:
            print(Color.RED + "Can't insert values into table" + Color.RESET)
        
        self.order_id.setText("")
        self.oe_input_1.setText("")
        self.oe_input_2.setText("")
        self.oe_input_3.setText("")
        self.oe_input_4.setText("")
        self.genOrderId()
        self.editOidLoad()

    def orderPlus(self):
        self.genOrderId()
        try:
            oe_db = sqlite3.connect(db_path)
            # order_id INTEGER, cx_name TEXT, cx_phno TEXT, product_id INTEGRER, quantity INTEGER, order_date TEXT, order_time TEXT
            oe_db.execute("INSERT INTO order_data VALUES ("+ self.order_id.text() +", '"+ self.oe_input_1.text() +"', '"+ self.oe_input_3.text() +"', "+ self.oe_input_2.text() +", "+ self.oe_input_4.text() +", '"+ str(date.today()) +"')")
            oe_db.commit()
        except:
            print(Color.RED + "Can't insert values into table" + Color.RESET)
        
        self.oe_input_2.setText("")
        self.oe_input_4.setText("")
        self.genOrderId()
        self.editOidLoad()

    def editOidLoad(self):
        try:
            self.select_oid.clear()
            updt_db = sqlite3.connect(db_path)
            cursor = updt_db.execute("SELECT order_id FROM order_data")
            result = cursor.fetchall()
            if result:
                for ids in result:
                    self.select_oid.addItem(str(ids[0]))
        except:
            print(Color.RED + "Can't load values into combo box" + Color.RESET)
            
            
def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()