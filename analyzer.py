from PyQt5.QtWidgets import QApplication, QMessageBox
from analyzerbase import AnalyzerBase
import argparse
import logging
import sys, time

class Analyzer(AnalyzerBase):
    def __init__(self, log, key):
        super().__init__(log, key)

        # Auto login
        self.on_connect_kiwoom()

    def test(self):
        self.debug('test button clicked')


    def on_connect_kiwoom(self):
        login_status = self.kiwoom.connect(self.cb_auto_login.isChecked())
        if login_status != 0:
            self.status_bar.showMessage('Something is wrong during log-in')
            self.error('Login error', login_status)
            return

        self.status_bar.showMessage('Log in success')
        self.cbb_account.addItems(self.kiwoom.account_list)

    def get_stock_price(self):
        self.info('Getting stock price...')
        if self.rb_tick.isChecked():
            self.status_bar.showMessage('Getting stock prices (tick data)')
            self.kiwoom.request_stock_price_tick()
        elif self.rb_min.isChecked():
            self.status_bar.showMessage('Getting stock prices (minute data)')
            self.kiwoom.request_stock_price_min()
        elif self.rb_day.isChecked():
            self.status_bar.showMessage('Getting stock prices (day data)')
            self.kiwoom.request_stock_price_day()

    def closeEvent(self, event):
        self.info('Closing process initializing...')
        self.kiwoom.clear()
        self.kiwoom.deleteLater()
        self.deleteLater()

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