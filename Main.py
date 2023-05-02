from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton, QMainWindow, QTableWidget, QStatusBar, QTableWidgetItem, QDialog, QVBoxLayout, QComboBox, QToolBar, QMessageBox, QCheckBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon

from datetime import date
from PyQt6 import QtCore, QtWidgets

import sys
import sqlite3
from datetime import datetime


# day      397

class DatabaseConnection:
    def __init__(self, database_file="database.db"):
        self.database_file = database_file

    def connect(self):
        connection = sqlite3.connect(self.database_file)
        return connection

class MainWindow(QMainWindow):

    def __init__(self):          # Main window to display table.
        super().__init__()
        self.setWindowTitle("Pay Bills")
        self.setMinimumSize(800, 800)

        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        add_bill_action = QAction(QIcon("icons/icons/add.png"), "&Add Bill", self)
        file_menu_item.addAction(add_bill_action)
        add_bill_action.triggered.connect(self.insert)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.triggered.connect(self.about)

        search_action = QAction(QIcon("icons/icons/search.png"), "&Search", self)
        edit_menu_item.addAction(search_action)
        search_action.triggered.connect(self.search)

        legend_action = QAction(QIcon("icons/icons/Legend.png"), "&Legend", self)
        help_menu_item.addAction(legend_action)
        legend_action.triggered.connect(self.legend)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(("ID", "Balance", "payment", "remaining", "number", "Date"))  # add label and boxes for date option around 330 line
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        # create toolbar
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_bill_action)
        toolbar.addAction(search_action)
        toolbar.addAction(legend_action)

        # create status bar
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # detect a cell click
        self.table.cellClicked.connect(self.cell_clicked)

    def cell_clicked(self):
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit)

        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete)

        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)

    def load_data(self):         # connects the db and adds in the information.
        connection = DatabaseConnection().connect()
        result = connection.execute("SELECT * FROM students")
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        connection.close()

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    def search(self):
        dialog = SearchFun()
        dialog.exec()

    def edit(self):
        dialog = EditDialog()
        dialog.exec()

    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()

    def about(self):
        dialog = AboutDialog()
        dialog.exec()

    def legend(self):
        dialog = legend()
        dialog.exec()


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update Bill")

        vbl = QVBoxLayout()
        index = main_window.table.currentRow()
        balance = main_window.table.item(index, 1).text()
        payment = main_window.table.item(index, 2).text()
        remaining = main_window.table.item(index, 3).text()
        reference = main_window.table.item(index, 4).text()
        # date = main_window.table.item(index, 5).text()

        self.bill_id = main_window.table.item(index, 0).text()
        edit_ballabel = QLabel("Balance")
        self.edit_balance_vb = QLineEdit(balance)
        edit_paylabel = QLabel("Payment")
        self.edit_payment_vb = QLineEdit(payment)
        edit_remainlabel = QLabel("Remaining")
        self.edit_remain_vb = QLineEdit(remaining)
        edit_referelabel = QLabel("Reference")
        self.edit_reference_vb = QLineEdit(reference)
        edit_button_vb = QPushButton("Edit Record")
        # self.edit_date_vb = QLineEdit(date)
        edit_button_vb.clicked.connect(self.update_bill)

        vbl.addWidget(edit_ballabel)
        vbl.addWidget(self.edit_balance_vb)
        vbl.addWidget(edit_paylabel)
        vbl.addWidget(self.edit_payment_vb)
        vbl.addWidget(edit_remainlabel)
        vbl.addWidget(self.edit_remain_vb)
        vbl.addWidget(edit_referelabel)
        vbl.addWidget(self.edit_reference_vb)
        vbl.addWidget(edit_button_vb)
        #vbl.addWidget(self.edit_date_vb)

        self.setLayout(vbl)

    def update_bill(self):
        connection = DatabaseConnection().connect()
        #connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("UPDATE students SET Balance = ?, payment = ?, remaining = ?, number = ? WHERE id = ?",
                       (self.edit_balance_vb.text(),
                        self.edit_payment_vb.text(),
                        self.edit_remain_vb.text(),
                        self.edit_reference_vb.text(),
                        self.bill_id))
        connection.commit()
        cursor.close()
        connection.close()
        # refresh the table
        main_window.load_data()

        self.close()


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete Bill")

        layout = QGridLayout()
        confirmation = QLabel("Are you sure you want to delete?")
        yes = QPushButton("Yes")
        no = QPushButton("No")

        layout.addWidget(confirmation, 0, 0, 1, 2)
        layout.addWidget(yes, 1, 0)
        layout.addWidget(no, 1, 1)
        self.setLayout(layout)

        yes.clicked.connect(self.delete_student)

    def delete_student(self):
        # get selected row index and student id
        index = main_window.table.currentRow()
        bill_id = main_window.table.item(index, 0).text()

        connection = DatabaseConnection().connect()
        #connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("DELETE from students WHERE id = ?", (bill_id, ))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()

        self.close()

        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setText("The record was deleted successfully!")
        confirmation_widget.exec()


class InsertDialog(QDialog):    # window to fill in new information.

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Bill")

        layout = QGridLayout()

        today = date.today()
        d1 = today.strftime("%d/%m/%Y")


        # Small CC
        preSM_Citizens_CC_label = QLabel("Small Citizens CC Balance:")
        preSM_Citizens_CC_label.setHidden(True)
        self.preSM_Citizens_CC_edit = QLineEdit("0")
        preSM_cbox = QCheckBox("Add")
        preSM_Date = QLabel("Date:")
        self.preSM_Date_edit = QLineEdit(f"{d1}")
        layout.addWidget(preSM_Citizens_CC_label, 0, 0)
        layout.addWidget(self.preSM_Citizens_CC_edit, 0, 1)
        layout.addWidget(preSM_cbox, 0, 8)
        layout.addWidget(preSM_Date, 0, 9)
        layout.addWidget(self.preSM_Date_edit, 0, 10)

        sm_citiz_CC_label = QLabel("Small Citizens CC Payment:")
        sm_citiz_CC_label.setHidden(True)
        self.sm_citiz_CC_edit = QLineEdit("0")
        layout.addWidget(sm_citiz_CC_label, 0, 2)
        layout.addWidget(self.sm_citiz_CC_edit, 0, 3)

        postSM_citiz_CC_label = QLabel("Small Citizens CC Remaining:")
        postSM_citiz_CC_label.setHidden(True)
        self.postSM_citiz_CC_edit = QLineEdit("0")
        layout.addWidget(postSM_citiz_CC_label, 0, 4)
        layout.addWidget(self.postSM_citiz_CC_edit, 0, 5)

        smc_ref_label = QLabel("Small CC Reference number:")
        smc_ref_label.setHidden(True)
        self.sm_ref_num_edit = QLineEdit("0")
        layout.addWidget(smc_ref_label, 0, 6)
        layout.addWidget(self.sm_ref_num_edit, 0, 7)

        # Large CC

        preLG_Citizens_CC_label = QLabel("Large Citizens CC Balance:")
        preLG_Citizens_CC_label.setHidden(True)
        self.preLG_Citizens_CC_edit = QLineEdit("0")
        self.preLG_cbox = QCheckBox("Add")
        preLG_Date = QLabel("Date:")
        self.preLG_Date_edit = QLineEdit(f"{d1}")
        layout.addWidget(preLG_Citizens_CC_label, 1, 0)
        layout.addWidget(self.preLG_Citizens_CC_edit, 1, 1)
        layout.addWidget(self.preLG_cbox, 1, 8)
        layout.addWidget(preLG_Date, 1, 9)
        layout.addWidget(self.preLG_Date_edit, 1, 10)

        lgcitiz_CC_label = QLabel("Large Citizens CC Payment:")
        lgcitiz_CC_label.setHidden(True)
        self.lgcitiz_CC_edit = QLineEdit("0")
        layout.addWidget(lgcitiz_CC_label, 1, 2)
        layout.addWidget(self.lgcitiz_CC_edit, 1, 3)

        postLG_Citizens_CC_label = QLabel("Large Citizens CC Remaining:")
        postLG_Citizens_CC_label.setHidden(True)
        self.postLG_Citizens_CC_edit = QLineEdit("0")
        layout.addWidget(postLG_Citizens_CC_label, 1, 4)
        layout.addWidget(self.postLG_Citizens_CC_edit, 1, 5)

        lgc_ref_label = QLabel("Large CC Reference Number:")
        lgc_ref_label.setHidden(True)
        self.lgc_ref_edit = QLineEdit("0")
        layout.addWidget(lgc_ref_label, 1, 6)
        layout.addWidget(self.lgc_ref_edit, 1, 7)

        # Chase ending in 64
        pre64_Chase_CC_label = QLabel("Chase 64 CC Balance:")
        pre64_Chase_CC_label.setHidden(True)
        self.pre64_Chase_CC_edit = QLineEdit("0")
        self.pre64_cbox = QCheckBox("Add")
        pre64_Date = QLabel("Date:")
        self.pre64_Date_edit = QLineEdit(f"{d1}")
        layout.addWidget(pre64_Chase_CC_label, 2, 0)
        layout.addWidget(self.pre64_Chase_CC_edit, 2, 1)
        layout.addWidget(self.pre64_cbox, 2, 8)
        layout.addWidget(pre64_Date, 2, 9)
        layout.addWidget(self.pre64_Date_edit, 2, 10)

        chase64_CC_label = QLabel("Chase 64 CC Payment:")
        chase64_CC_label.setHidden(True)
        self.chase64_CC_edit = QLineEdit("0")
        layout.addWidget(chase64_CC_label, 2, 2)
        layout.addWidget(self.chase64_CC_edit, 2, 3)

        post64_Chase_CC_label = QLabel("Chase 64 CC Remaining:")
        post64_Chase_CC_label.setHidden(True)
        self.post64_Chase_CC_edit = QLineEdit("0")
        layout.addWidget(post64_Chase_CC_label, 2, 4)
        layout.addWidget(self.post64_Chase_CC_edit, 2, 5)

        ch64_ref_label = QLabel("Chase 64 CC Reference Number:")
        ch64_ref_label.setHidden(True)
        self.ch64_ref_edit = QLineEdit("0")
        layout.addWidget(ch64_ref_label, 2, 6)
        layout.addWidget(self.ch64_ref_edit, 2, 7)

        # Chase ending in 20
        pre20_Chase_CC_label = QLabel("Chase 20 Balance:")
        pre20_Chase_CC_label.setHidden(True)
        self.pre20_Chase_CC_edit = QLineEdit("0")
        self.pre20_cbox = QCheckBox("Add")
        pre20_Date = QLabel("Date:")
        self.pre20_Date_edit = QLineEdit(f"{d1}")
        layout.addWidget(pre20_Chase_CC_label, 3, 0)
        layout.addWidget(self.pre20_Chase_CC_edit, 3, 1)
        layout.addWidget(self.pre20_cbox, 3, 8)
        layout.addWidget(pre20_Date, 3, 9)
        layout.addWidget(self.pre20_Date_edit, 3, 10)

        chase20_CC_label = QLabel("Chase 20 CC Payment:")
        chase20_CC_label.setHidden(True)
        self.chase20_CC_edit = QLineEdit("0")
        layout.addWidget(chase20_CC_label, 3, 2)
        layout.addWidget(self.chase20_CC_edit, 3, 3)

        post20_Chase_CC_label = QLabel("Chase 20 C Remaining:")
        post20_Chase_CC_label.setHidden(True)
        self.post20_Chase_CC_edit = QLineEdit("0")
        layout.addWidget(post20_Chase_CC_label, 3, 4)
        layout.addWidget(self.post20_Chase_CC_edit, 3, 5)

        ch20_ref_label = QLabel("Chase 20 CC Reference Number:")
        ch20_ref_label.setHidden(True)
        self.ch20_ref_edit = QLineEdit("0")
        layout.addWidget(ch20_ref_label, 3, 6)
        layout.addWidget(self.ch20_ref_edit, 3, 7)

        # CapitalOne
        preCapital_CC_label = QLabel("Capital One Balance:")
        preCapital_CC_label.setHidden(True)
        self.preCapital_CC_edit = QLineEdit("0")
        self.preCapital_cbox = QCheckBox("Add")
        preCapital_Date = QLabel("Date:")
        self.preCapital_Date_edit = QLineEdit(f"{d1}")
        layout.addWidget(preCapital_CC_label, 4, 0)
        layout.addWidget(self.preCapital_CC_edit, 4, 1)
        layout.addWidget(self.preCapital_cbox, 4, 8)
        layout.addWidget(preCapital_Date, 4, 9)
        layout.addWidget(self.preCapital_Date_edit, 4, 10)

        capitalone_CC_label = QLabel("Capital One CC Payment:")
        capitalone_CC_label.setHidden(True)
        self.capitalone_CC_edit = QLineEdit("0")
        layout.addWidget(capitalone_CC_label, 4, 2)
        layout.addWidget(self.capitalone_CC_edit, 4, 3)

        postCapital_CC_label = QLabel("Capital One CC Remaining:")
        postCapital_CC_label.setHidden(True)
        self.postCapital_CC_edit = QLineEdit("0")
        layout.addWidget(postCapital_CC_label, 4, 4)
        layout.addWidget(self.postCapital_CC_edit, 4, 5)

        capitalone_ref_label = QLabel("Capital One CC Reference Number:")
        capitalone_ref_label.setHidden(True)
        self.capitalone_ref_edit = QLineEdit("0")
        layout.addWidget(capitalone_ref_label, 4, 6)
        layout.addWidget(self.capitalone_ref_edit, 4, 7)

        # Banking information before and after
        self.bank_total_label = QLabel("Bank Amount:")
        self.bank_total_edit = QLineEdit("0")
        layout.addWidget(self.bank_total_label, 7, 0)
        layout.addWidget(self.bank_total_edit, 7, 1)

        self.Bank_remaining_total_label = QLabel("Remaining Amount:")
        self.Bank_remaining_total_edit = QLineEdit("0")
        layout.addWidget(self.Bank_remaining_total_label, 7, 2)
        layout.addWidget(self.Bank_remaining_total_edit, 7, 3)

        # Buttons to add info to table and to see balance of my account after bills are paid

        button = QPushButton("Add to Table")
        button.clicked.connect(self.add_Bills)
        layout.addWidget(button, 6, 0)

        button1 = QPushButton("Calcuate")
        button1.clicked.connect(self.calcuate)
        layout.addWidget(button1, 6, 1)

        self.setLayout(layout)

    def add_Bills(self):          # below numbers to the table

        # smCitiz = "Small Card "
        # totamount = self.preSM_Citizens_CC_edit.text()
        # preSMbal = smCitiz + totamount

        # Small CC Citizensbank
        preSMbal = self.preSM_Citizens_CC_edit.text()
        sm_citiz_CCpay = self.sm_citiz_CC_edit.text()
        postSMrem = self.postSM_citiz_CC_edit.text()
        Smrefnum = self.sm_ref_num_edit.text()
        SMdate = self.preSM_Date_edit.text()

        # Large CC Citizensbank
        preLGbal = self.preLG_Citizens_CC_edit.text()
        lgcitiz_CCpay = self.lgcitiz_CC_edit.text()
        postLGrem = self.postLG_Citizens_CC_edit.text()
        lg_refnumb = self.lgc_ref_edit.text()
        LGdate = self.preLG_Date_edit.text()

        # Chase 64
        pre64bal = self.pre64_Chase_CC_edit.text()
        chase64pay = self.chase64_CC_edit.text()
        post64rem = self.post64_Chase_CC_edit.text()
        chase64numb = self.ch64_ref_edit.text()
        pre64date = self.pre64_Date_edit.text()

        # Chase 20
        pre20bal = self.pre20_Chase_CC_edit.text()
        chase20pay = self.chase20_CC_edit.text()
        post20rem = self.post20_Chase_CC_edit.text()
        chase20numb = self.ch20_ref_edit.text()
        pre20date = self.pre20_Date_edit.text()

        # CapitalOne
        precapital = self.preCapital_CC_edit.text()
        capitalpay = self.capitalone_CC_edit.text()
        postcapital = self.postCapital_CC_edit.text()
        capitalnumb = self.capitalone_ref_edit.text()
        capitaldate = self.preCapital_Date_edit.text()

        # ID", "Balance", "payment", "remaining", "number", "Date

        connection = DatabaseConnection().connect()
        #connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (Balance, payment, remaining, number, Date) VALUES (?, ?, ?, ?, ?)", (preSMbal, sm_citiz_CCpay, postSMrem, Smrefnum, SMdate))
        cursor.execute("INSERT INTO students (Balance, payment, remaining, number, Date) VALUES (?, ?, ?, ?, ?)", (preLGbal, lgcitiz_CCpay, postLGrem, lg_refnumb, LGdate))
        cursor.execute("INSERT INTO students (Balance, payment, remaining, number, Date) VALUES (?, ?, ?, ?, ?)", (pre64bal, chase64pay, post64rem, chase64numb, pre64date))
        cursor.execute("INSERT INTO students (Balance, payment, remaining, number, Date) VALUES (?, ?, ?, ?, ?)", (pre20bal, chase20pay, post20rem, chase20numb, pre20date))
        cursor.execute("INSERT INTO students (Balance, payment, remaining, number, Date) VALUES (?, ?, ?, ?, ?)", (precapital, capitalpay, postcapital, capitalnumb, capitaldate))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()

    def calcuate(self):
        billspayment = [self.sm_citiz_CC_edit.text(), self.lgcitiz_CC_edit.text(), self.chase64_CC_edit.text(), self.chase20_CC_edit.text(), self.capitalone_CC_edit.text()]
        pay_numbers = [int(x) for x in billspayment]
        sum_payments = sum(pay_numbers)

        smCitizpre = int(self.preSM_Citizens_CC_edit.text()) - int(self.sm_citiz_CC_edit.text())
        self.postSM_citiz_CC_edit.setText(f"{smCitizpre}")

        lgCitizpre = int(self.preLG_Citizens_CC_edit.text()) - int(self.lgcitiz_CC_edit.text())
        self.postLG_Citizens_CC_edit.setText(f"{lgCitizpre}")

        c64pre = int(self.pre64_Chase_CC_edit.text()) - int(self.chase64_CC_edit.text())
        self.post64_Chase_CC_edit.setText(f"{c64pre}")

        c20pre = int(self.pre20_Chase_CC_edit.text()) - int(self.chase20_CC_edit.text())
        self.post20_Chase_CC_edit.setText(f"{c20pre}")

        cappre = int(self.preCapital_CC_edit.text()) - int(self.capitalone_CC_edit.text())
        self.postCapital_CC_edit.setText(f"{cappre}")

        amount1 = int(self.bank_total_edit.text())
        amount2 = int(sum_payments)
        amount3 = amount1 - amount2
        self.Bank_remaining_total_edit.setText(f"{amount3}")


class SearchFun(QDialog):       # window to fill in new information.

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search for Bill")

        layout = QVBoxLayout()

        billlabel = QLabel("<center>Bill Name</center>")
        self.bill_edit = QLineEdit()

        billsearch = QPushButton("Search")
        billsearch.clicked.connect(self.search)

        layout.addWidget(billlabel)
        layout.addWidget(self.bill_edit)
        layout.addWidget(billsearch)

        self.setLayout(layout)

    def search(self):
        Balance = self.bill_edit.text()
        connection = DatabaseConnection().connect()
        #connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM students WHERE Balance = ?", (Balance,))
        rows = list(result)
        print(rows)
        items = main_window.table.findItems(Balance, Qt.MatchFlag.MatchContains)  # Qt.MatchFlag.MatchFixedString)
        for item in items:
            print(item)
            main_window.table.item(item.row(), 1).setSelected(True)

        cursor.close()
        connection.close()


class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")

        about = "This is the about section.  This program is design to store and recall previous payments and confirmation numbers.  Able to add, delete and edit all data."

        self.setText(about)

class legend(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Legend")

        legend = "Working to be changed.  First Row is CC.  Second Row is CC.  Third Row is CC.  Fourth Row is CC.  Fifth Row is CC."

        self.setText(legend)


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())
