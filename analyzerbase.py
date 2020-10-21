from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QLineEdit, \
    QTextEdit, QVBoxLayout, QHBoxLayout, QWidget, QRadioButton, QGridLayout, \
    QCheckBox, QComboBox, QGroupBox, QDateTimeEdit
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtGui import QIcon
from wookutil import WookLog
from wookdata import *

class AnalyzerBase(QMainWindow, WookLog):
    def __init__(self, log):
        super().__init__()
        WookLog.custom_init(self, log)
        self.initUI()

    def initUI(self):
        # Test Button
        self.btn_test = QPushButton('Test')
        self.btn_test.clicked.connect(self.test)

        # Account information
        self.cb_auto_login = QCheckBox('Auto')
        self.btn_login = QPushButton('Login', self)
        lb_account = QLabel('Account')
        self.cbb_account = QComboBox()
        self.cb_auto_login.setChecked(True)

        account_grid = QGridLayout()
        account_grid.addWidget(self.cb_auto_login, 0, 0)
        account_grid.addWidget(self.btn_login, 0, 1)
        account_grid.addWidget(lb_account, 1, 0)
        account_grid.addWidget(self.cbb_account, 1, 1, 1, 2)
        account_grid.setColumnMinimumWidth(2, 10)

        account_gbox = QGroupBox('Account Information')
        account_gbox.setLayout(account_grid)

        # Item infomation
        lb_item_code = QLabel('Code')
        lb_item_name = QLabel('Name')
        self.cbb_item_code = QComboBox()
        self.cbb_item_name = QComboBox()
        self.cbb_item_code.setEditable(True)
        self.cbb_item_name.setEditable(True)
        self.cbb_item_code.addItem(CODE_KODEX_LEVERAGE)
        self.cbb_item_code.addItem(CODE_KODEX_INVERSE_2X)
        self.cbb_item_name.addItem(NAME_KODEX_LEVERAGE)
        self.cbb_item_name.addItem(NAME_KODEX_INVERSE_2X)

        current_date = QDateTime.currentDateTime()
        lb_period = QLabel('Period')
        self.dte_first_day = QDateTimeEdit()
        self.dte_first_day.setCalendarPopup(True)
        self.dte_first_day.setDisplayFormat('yyyy-MM-dd')
        self.dte_first_day.setDateTime(current_date)
        lb_wave = QLabel('~')
        self.le_last_day = QLineEdit()
        self.dte_last_day = QDateTimeEdit()
        self.dte_last_day.setCalendarPopup(True)
        self.dte_last_day.setDisplayFormat('yyyy-MM-dd')
        self.dte_last_day.setDateTime(current_date)

        lb_destination_folder = QLabel('Save Folder')
        self.le_destination_folder = QLineEdit()

        # Item grid layout
        item_grid = QGridLayout()
        item_grid.addWidget(lb_item_code, 0, 0)
        item_grid.addWidget(self.cbb_item_code, 0, 1)
        item_grid.addWidget(lb_item_name, 0, 2)
        item_grid.addWidget(self.cbb_item_name, 0, 3)

        item_grid.addWidget(lb_period, 1, 0)
        item_grid.addWidget(self.dte_first_day, 1, 1)
        item_grid.addWidget(lb_wave, 1, 2, Qt.AlignCenter)
        item_grid.addWidget(self.dte_last_day, 1, 3)


        item_grid.addWidget(lb_destination_folder, 2, 0)
        item_grid.addWidget(self.le_destination_folder, 2, 1)

        item_gbox = QGroupBox('Item information')
        item_gbox.setLayout(item_grid)

        # Data type selection
        self.rb_tick = QRadioButton('Tick')
        self.rb_min = QRadioButton('Minute')
        self.rb_day = QRadioButton('1-Day')
        self.cbb_tick = QComboBox()
        self.cbb_min = QComboBox()
        self.rb_min.setChecked(True)

        self.cbb_tick.addItem('1 tick')
        self.cbb_tick.addItem('3 tick')
        self.cbb_tick.addItem('5 tick')
        self.cbb_tick.addItem('10 tick')
        self.cbb_tick.addItem('30 tick')

        self.cbb_min.addItem('1 min')
        self.cbb_min.addItem('3 min')
        self.cbb_min.addItem('5 min')
        self.cbb_min.addItem('10 min')
        self.cbb_min.addItem('15 min')
        self.cbb_min.addItem('30 min')
        self.cbb_min.addItem('60 min')

        data_type_grid = QGridLayout()
        data_type_grid.addWidget(self.rb_tick, 0, 0)
        data_type_grid.addWidget(self.cbb_tick, 0, 1)
        data_type_grid.addWidget(self.rb_min, 1, 0)
        data_type_grid.addWidget(self.cbb_min, 1, 1)
        data_type_grid.addWidget(self.rb_day, 2, 0)

        data_type_gbox = QGroupBox('Data Type')
        data_type_gbox.setLayout(data_type_grid)

        # TextEdit
        self.te_info = QTextEdit()

        # Central Layout
        top_hbox = QHBoxLayout()
        top_hbox.addWidget(account_gbox)
        top_hbox.addWidget(item_gbox)
        top_hbox.addWidget(data_type_gbox)
        top_hbox.addStretch()

        vbox = QVBoxLayout()
        vbox.addWidget(self.btn_test)
        vbox.addLayout(top_hbox)
        vbox.addWidget(self.te_info)

        # Central widget
        cw = QWidget()
        cw.setLayout(vbox)

        # Window setting
        self.setCentralWidget(cw)
        self.status_bar = self.statusBar()
        self.status_bar.showMessage('ready')
        self.setWindowTitle('Jaewook\'s algorithm analyzer')
        self.resize(700, 600)
        self.move(300, 150)
        self.setWindowIcon(QIcon('nyang1.ico'))
        self.show()