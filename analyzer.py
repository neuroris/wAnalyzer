from PyQt5.QtWidgets import QFileDialog
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance
import math
from glob import glob
from analyzerbase import AnalyzerBase
from kiwoom import Kiwoom
from wookdata import *

class Analyzer(AnalyzerBase):
    def __init__(self, log, key):
        self.kiwoom = Kiwoom(log, key)
        super().__init__(log)
        self.initKiwoom()

        # Initial work
        # self.connect_kiwoom()
        # self.get_account_list()

        # self.get_graph()

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

    def get_floor(self, price, interval, loss_cut):
        cut_value = interval - loss_cut
        quotient, remainder = divmod(price - 1, interval)
        fraction = remainder / cut_value
        factor = int(fraction)
        if factor:
            factor = cut_value
        processed_price = quotient * interval + factor

        return processed_price

    def get_ceiling(self, price, interval, loss_cut):
        cut_value = interval - loss_cut
        quotient, remainder = divmod(price, interval)
        fraction = remainder / cut_value
        factor = int(fraction)
        if factor:
            factor = loss_cut
        processed_price = quotient * interval + cut_value + factor

        return processed_price

    def at_cut_price(price):
        check_result = False
        if price % 50:
            check_result = True
        return check_result

    def get_graph(self):
        interval = int(self.le_price_interval.text())
        load_folder = self.le_load_folder.text()
        all_files = glob(load_folder + '/' + '*.csv')
        first_day = int(self.dte_first_day.text().replace('-', ''))
        last_day = int(self.dte_last_day.text().replace('-', ''))
        load_files = list()
        if self.cb_load_all.isChecked():
            load_files = all_files
        else:
            for file in all_files:
                date = int(file[-12:-4])
                if first_day <= date <= last_day:
                    load_files.append(file)

        mpl_color = mplfinance.make_marketcolors(up='tab:red', down='tab:blue', volume='Goldenrod')
        mpl_style = mplfinance.make_mpf_style(base_mpl_style='seaborn', marketcolors=mpl_color)
        # setup.update(dict(figscale=1.5, figratio=(1920, 1080), volume=True))

        for file in load_files:
            save_file = file[:-4] + '.png'
            df = pd.read_csv(file, index_col=0, parse_dates=True)
            max = df['High'].max()
            min = df['Low'].min()
            max_ceiling = math.ceil(max / interval) * interval
            min_floor = math.floor(min / interval) * interval
            yticks = list(range(min_floor, max_ceiling + interval, interval))
            # setup = dict(type='candle', style=mpl_style, tight_layout=True, title=fig_title)
            setup = dict(type='candle', style=mpl_style, tight_layout=True)
            setup.update(dict(savefig=save_file, figscale=2, figratio=(1920, 1080), volume=True))
            setup.update(dict(hlines=dict(hlines=yticks[:-1], linewidths=0.1, colors='silver', alpha=1)))
            mplfinance.plot(df, **setup)
            self.kiwoom.signal('Graph:', file)
        self.kiwoom.signal('Getting graphs is done')

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

    def on_change_load_folder(self):
        folder = QFileDialog.getExistingDirectory(self, 'Select folder', self.le_load_folder.text())
        if folder != '':
            self.le_load_folder.setText(folder)

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