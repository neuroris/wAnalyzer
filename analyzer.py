from PyQt5.QtWidgets import QApplication
from analyzerbase import AnalyzerBase
from kiwoom import Kiwoom
import argparse
import logging
import sys, time

class Analyzer(AnalyzerBase):
    def __init__(self, log, key):
        super().__init__(log)
        self.kiwoom = Kiwoom(log, key)

        # self.kiwoom.auto_login()
        # self.start_process()

    def start_process(self):
        print('Kiwoom test program started')
        # self.set_OCX()
        self.connect_slots()
        self.auto_login()
        # self.login()
        # self.set_account_password()
        self.get_account_list()
        self.request_account_deposit()
        self.request_stock_price()

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