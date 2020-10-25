from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QLineEdit, \
    QTextEdit, QVBoxLayout, QHBoxLayout, QWidget, QRadioButton, QGridLayout, \
    QCheckBox, QComboBox, QGroupBox, QDateTimeEdit, QAction, QDockWidget
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtGui import QIcon
import json
from wookutil import WookLog
from wookdata import *

class AnalyzerBase(QMainWindow, WookLog):
    def __init__(self, log):
        super().__init__()
        WookLog.custom_init(self, log)

        with open('setting.json') as r_file:
            self.setting = json.load(r_file)

        self.initUI()

        # self.setStyleSheet('background:rgb(0,120,120)')


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
        self.cbb_item_code.currentTextChanged.connect(self.on_item_code_selection)
        self.cbb_item_name.currentTextChanged.connect(self.on_item_name_selection)
        self.cbb_item_code.addItem(CODE_KODEX_LEVERAGE)
        self.cbb_item_code.addItem(CODE_KODEX_INVERSE_2X)
        self.cbb_item_name.addItem(NAME_KODEX_LEVERAGE)
        self.cbb_item_name.addItem(NAME_KODEX_INVERSE_2X)

        # Period
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
        self.cb_one_day = QCheckBox('1-day')
        self.cb_one_day.setChecked(self.setting['one_day'])

        # Save Folder
        lb_save_folder = QLabel('Save')
        self.le_save_folder = QLineEdit()
        self.le_save_folder.setText(self.setting['save_folder'])

        # Item grid layout
        item_grid = QGridLayout()
        item_grid.addWidget(lb_item_code, 0, 0)
        item_grid.addWidget(self.cbb_item_code, 0, 1)
        item_grid.addWidget(lb_item_name, 0, 2, 1, 2)
        item_grid.addWidget(self.cbb_item_name, 0, 4, 1, 2)

        item_grid.addWidget(lb_period, 1, 0)
        item_grid.addWidget(self.dte_first_day, 1, 1, 1, 2)
        item_grid.addWidget(lb_wave, 1, 3, Qt.AlignCenter)
        item_grid.addWidget(self.dte_last_day, 1, 4, 1, 1)
        item_grid.addWidget(self.cb_one_day, 1, 5)

        item_grid.addWidget(lb_save_folder, 2, 0)
        item_grid.addWidget(self.le_save_folder, 2, 1, 1, 4)

        item_gbox = QGroupBox('Item information')
        item_gbox.setLayout(item_grid)

        # Data type selection
        self.rb_tick = QRadioButton('Tick')
        self.rb_min = QRadioButton('Min')
        self.rb_day = QRadioButton('Day')
        self.cbb_tick = QComboBox()
        self.cbb_min = QComboBox()
        self.rb_min.setChecked(True)

        self.cbb_tick.addItem('1')
        self.cbb_tick.addItem('3')
        self.cbb_tick.addItem('5')
        self.cbb_tick.addItem('10')
        self.cbb_tick.addItem('30')

        self.cbb_min.addItem('1')
        self.cbb_min.addItem('3')
        self.cbb_min.addItem('5')
        self.cbb_min.addItem('10')
        self.cbb_min.addItem('15')
        self.cbb_min.addItem('30')
        self.cbb_min.addItem('60')

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
        vbox.addLayout(top_hbox)
        vbox.addWidget(self.te_info)
        vbox.addWidget(self.btn_test)

        # Central widget
        cw = QWidget()
        cw.setLayout(vbox)

        # Menu bar
        menu_bar = self.menuBar()
        menu_bar.setStyleSheet('background:rgb(140,230,255)')
        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        file_menu = menu_bar.addMenu('&File')
        file_menu.addAction(exit_action)

        setting_action = QAction('Setting', self)
        setting_action.triggered.connect(self.edit_setting)
        edit_menu = menu_bar.addMenu('&Edit')
        edit_menu.addAction(setting_action)

        # Window setting
        self.setCentralWidget(cw)
        self.status_bar = self.statusBar()
        self.status_bar.showMessage('ready')
        self.setWindowTitle('wook\'s algorithm analyzer')
        self.resize(700, 600)
        self.move(300, 150)
        self.setWindowIcon(QIcon('nyang1.ico'))
        self.show()

    def edit_setting(self):
        self.debug('setting')

    def on_item_code_selection(self, code):
        self.item_code = code
        if code == CODE_KODEX_LEVERAGE:
            self.cbb_item_name.setCurrentText(NAME_KODEX_LEVERAGE)
        elif code == CODE_KODEX_INVERSE_2X:
            self.cbb_item_name.setCurrentText(NAME_KODEX_INVERSE_2X)
        else:
            self.cbb_item_name.setCurrentText('')

    def on_item_name_selection(self, name):
        if name == NAME_KODEX_LEVERAGE:
            self.cbb_item_code.setCurrentText(CODE_KODEX_LEVERAGE)
            self.item_code = CODE_KODEX_LEVERAGE
        elif name == NAME_KODEX_INVERSE_2X:
            self.cbb_item_code.setCurrentText(CODE_KODEX_INVERSE_2X)
            self.item_code = CODE_KODEX_INVERSE_2X
        else:
            self.cbb_item_code.setCurrentText('')