from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QLineEdit, \
    QTextEdit, QVBoxLayout, QHBoxLayout, QWidget, QRadioButton, QGridLayout
from PyQt5.QtGui import QIcon
from wookutil import WookLog

class AnalyzerBase(QMainWindow, WookLog):
    def __init__(self, log):
        super().__init__()
        WookLog.custom_init(self, log)

        self.initUI()

    def initUI(self):
        self.central_widget = QWidget()

        self.init_data_scraping()

        # TextEdit
        self.te_info = QTextEdit()

        # Window setting
        # cw = QWidget()
        # cw.setLayout(self.data_scraping_vbox)
        # cw.setLayout(grid)
        self.setCentralWidget(self.central_widget)
        self.status_bar = self.statusBar()
        self.status_bar.showMessage('ready')
        self.setWindowTitle('Jaewook\'s algorithm analyzer')
        self.resize(700, 600)
        self.move(400, 200)
        self.setWindowIcon(QIcon('nyang1.ico'))
        self.show()

    def init_data_scraping(self):
        # Item infomation
        lb_item_code = QLabel('Item code')
        lb_item_name = QLabel('Item name')
        self.le_item_code = QLineEdit()
        self.le_item_name = QLineEdit()

        # Period
        lb_period = QLabel('Period')
        self.le_first_day = QLineEdit()
        lb_wave = QLabel('~')
        self.le_last_day = QLineEdit()

        # Destination Folder
        lb_destination_folder = QLabel('Destination folder')
        self.le_destination_folder = QLineEdit()

        # Minute data
        lb_minute = QLabel('Minute data')
        rb_1min = QRadioButton('1 min')
        rb_3min = QRadioButton('3 min')
        rb_5min = QRadioButton('5 min')
        rb_10min = QRadioButton('10 min')
        rb_15min = QRadioButton('15 min')
        rb_30min = QRadioButton('30 min')
        rb_45min = QRadioButton('45 min')
        rb_60min = QRadioButton('60 min')

        min_hbox = QHBoxLayout()
        min_hbox.addWidget(lb_minute)
        min_hbox.addWidget(rb_1min)
        min_hbox.addWidget(rb_3min)
        min_hbox.addWidget(rb_5min)
        min_hbox.addWidget(rb_10min)
        min_hbox.addWidget(rb_15min)
        min_hbox.addWidget(rb_30min)
        min_hbox.addWidget(rb_45min)
        min_hbox.addWidget(rb_60min)

        # grid layout
        grid = QGridLayout()
        grid.addWidget(lb_item_code,0,0)
        grid.addWidget(self.le_item_code,0,1)
        grid.addWidget(lb_item_name,0,2)
        grid.addWidget(self.le_item_name,0,3)

        grid.addWidget(lb_period,1,0)
        grid.addWidget(self.le_first_day,1,1)
        grid.addWidget(lb_wave,1,2)
        grid.addWidget(self.le_last_day,1,3)

        grid.addWidget(lb_destination_folder,2,0)
        grid.addWidget(self.le_destination_folder,2,1)

        # central widget
        self.central_widget.setLayout(grid)