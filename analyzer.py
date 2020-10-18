from PyQt5.QtWidgets import QApplication
from analyzerbase import AnalyzerBase
from kiwoom import Kiwoom
import argparse
import logging
import sys, time
from wookdata import *

class Analyzer(AnalyzerBase):
    def __init__(self, log, key):
        super().__init__(log)
        self.kiwoom = Kiwoom(log, key)

        # fields
        self.item_code = self.cbb_item_code.currentText()

        # Control slot connection
        self.btn_login.clicked.connect(self.connect_kiwoom)
        self.cbb_item_code.currentTextChanged.connect(self.on_item_code_selection)
        self.cbb_item_name.currentTextChanged.connect(self.on_item_name_selection)

    def test(self):
        self.debug('test button clicked')

        self.get_stock_price_data()

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

    def connect_kiwoom(self):
        self.kiwoom.connect(self.cb_auto_login.isChecked())
        self.cbb_account.addItems(self.kiwoom.account_list)

    def get_stock_price_data(self):
        self.kiwoom.request_stock_price()
        self.info('Data acquired and saved')

    def closeEvent(self, event):
        self.info('Closing process initializing...')

if __name__ == '__main__':
    log_folder = 'D:/Programming/PC/wAnalyzer/log/'
    log_file = time.strftime('%Y%m%d_log.txt')

    parser = argparse.ArgumentParser(description='argument description')
    parser.add_argument('--log', required=False, default='debug', help='logging level')
    parser.add_argument('--key', required=True, help='raw key')
    args = parser.parse_args()
    log_level = args.log.upper()
    key = args.key

    # console_formatter = logging.Formatter('\033[33m%(funcName)s (line: %(lineno)s)\n\033[31m%(levelname)s \033[30m%(message)s\033[0m')
    console_formatter = logging.Formatter('\033[31m%(levelname)s \033[30m%(message)s\033[0m')
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(console_formatter)
    file_formatter = logging.Formatter('%(asctime)s %(message)s')
    file_handler = logging.FileHandler(log_folder+log_file, mode='w')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(file_formatter)
    log = logging.getLogger('kiwoom')
    log.addHandler(console_handler)
    log.addHandler(file_handler)
    log.setLevel(log_level)

    app = QApplication(sys.argv)
    analyzer = Analyzer(log, key)
    app.exec()