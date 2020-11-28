from datetime import datetime
from analyzerbase import AnalyzerBase
from kiwoom import Kiwoom
from wookdata import *

class Analyzer(AnalyzerBase):
    def __init__(self, log, key):
        self.kiwoom = Kiwoom(log, key)
        super().__init__(log)
        self.initKiwoom()

        # Initial work
        self.connect_kiwoom()
        self.get_account_list()

    def test(self):
        self.debug('test button clicked')

    def initKiwoom(self):
        self.kiwoom.signal = self.on_kiwoom_signal
        self.kiwoom.status = self.on_kiwoom_status
        self.kiwoom.item_code = self.cbb_item_code.currentText()
        self.kiwoom.item_name = self.cbb_item_name.currentText()
        self.kiwoom.first_day = self.dte_first_day.text()
        self.kiwoom.last_day = self.dte_last_day.text()
        self.kiwoom.save_folder = self.le_save_folder.text()
        self.kiwoom.tick_type = self.cbb_tick.currentText()
        self.kiwoom.min_type = self.cbb_min.currentText()
        self.kiwoom.day_type = self.cbb_day.currentText()

    def connect_kiwoom(self):
        if self.cb_auto_login.isChecked():
            self.kiwoom.auto_login()
        else:
            self.kiwoom.login()
            self.kiwoom.set_account_password()

    def get_account_list(self):
        account_list = self.kiwoom.get_account_list()
        if account_list is not None:
            self.cbb_account.addItems(self.kiwoom.account_list)

    def get_stock_price(self):
        self.info('Getting stock prices...')
        if self.rb_tick.isChecked():
            self.status_bar.showMessage('Getting stock prices (tick data)...')
            self.kiwoom.request_stock_price_tick()
        elif self.rb_min.isChecked():
            self.status_bar.showMessage('Getting stock prices (minute data)...')
            self.kiwoom.request_stock_price_min()
        elif self.rb_day.isChecked():
            self.status_bar.showMessage('Getting stock prices (day data)...')
            self.kiwoom.request_stock_price_day()

    def on_select_account(self, account):
        self.kiwoom.account_number = int(account)

    def on_select_item_code(self, code):
        self.kiwoom.item_code = int(code)
        if code == CODE_KODEX_LEVERAGE:
            self.cbb_item_name.setCurrentText(NAME_KODEX_LEVERAGE)
        elif code == CODE_KODEX_INVERSE_2X:
            self.cbb_item_name.setCurrentText(NAME_KODEX_INVERSE_2X)
        else:
            self.cbb_item_name.setCurrentText('')

    def on_select_item_name(self, name):
        self.kiwoom.item_name = name
        if name == NAME_KODEX_LEVERAGE:
            self.cbb_item_code.setCurrentText(CODE_KODEX_LEVERAGE)
        elif name == NAME_KODEX_INVERSE_2X:
            self.cbb_item_code.setCurrentText(CODE_KODEX_INVERSE_2X)
        else:
            self.cbb_item_code.setCurrentText('')

    def on_change_first_day(self, date):
        self.kiwoom.first_day = date.toString('yyyy-MM-dd')
        if self.cb_one_day.isChecked():
            self.dte_last_day.setDate(date)

    def on_change_last_day(self, date):
        self.kiwoom.last_day = date.toString('yyyy-MM-dd')
        if self.cb_one_day.isChecked():
            self.dte_first_day.setDate(date)

    def on_edit_save_folder(self):
        folder = self.le_save_folder.text()
        self.kiwoom.save_folder = folder

    def on_change_save_folder(self):
        folder = QFileDialog.getExistingDirectory(self, 'Select folder', self.le_save_folder.text())
        if folder != '':
            self.le_save_folder.setText(folder)
            self.kiwoom.save_folder = folder

    def on_change_tick(self, index):
        self.rb_tick.setChecked(True)
        self.kiwoom.tick_type = self.cbb_tick.itemText(index)

    def on_change_min(self, index):
        self.rb_min.setChecked(True)
        self.kiwoom.min_type = self.cbb_min.itemText(index)

    def on_change_day(self, index):
        self.rb_day.setChecked(True)
        self.kiwoom.day_type = self.cbb_day.itemText(index)

    def edit_setting(self):
        self.debug('setting')

    def on_kiwoom_signal(self, *args):
        message = str(args[0])
        for arg in args[1:]:
            message += ' ' + str(arg)

        time = datetime.now().strftime('%H:%M:%S') + ' '
        self.te_info.append(time + message)
        self.info(message)

    def on_kiwoom_status(self, *args):
        message = str(args[0])
        for arg in args[1:]:
            message += ' ' + str(arg)
        self.status_bar.showMessage(message)

    def closeEvent(self, event):
        self.kiwoom.signal('Closing process initializing...')
        self.kiwoom.close_process()
        self.kiwoom.clear()
        self.kiwoom.deleteLater()
        self.deleteLater()