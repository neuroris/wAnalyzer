from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import Qt
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

        # Analyzer fields
        self.winning_number = 0
        self.analysis_count = 0
        self.total_profit = 0
        self.total_profit_with_fee = 0.0

        # self.connect_kiwoom()

    def test(self):
        self.debug('test button clicked')

    def initKiwoom(self):
        self.kiwoom.log = self.on_kiwoom_log
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

        self.get_account_list()

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

    def get_chart(self):
        interval = int(self.le_interval.text())
        load_folder = self.le_analysis_folder.text()
        all_files = glob(load_folder + '/' + '*.csv')
        first_day = int(self.dte_first_day.text().replace('-', ''))
        last_day = int(self.dte_last_day.text().replace('-', ''))
        load_files = list()
        if self.cb_analyze_all.isChecked():
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
            self.kiwoom.log('Chart converting', file)
        self.kiwoom.log('Getting charts has been done')

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

    def custom_get_floor(self, interval, loss_cut):
        def new_get_floor(price):
            result = self.get_floor(price, interval, loss_cut)
            return result
        return new_get_floor

    def custom_get_ceiling(self, interval, loss_cut):
        def new_get_ceiling(price):
            result = self.get_ceiling(price, interval, loss_cut)
            return result
        return new_get_ceiling

    def at_cut_price(self, price):
        check_result = False
        if price % 50:
            check_result = True
        return check_result

    def get_essential_prices(self, file_name, interval, loss_cut):
        df = pd.read_csv(file_name)
        initial_price = df.loc[0, 'Open']
        high_price = df['High']
        low_price = df['Low']
        open_price = df['Open']
        close_price = df['Close']

        prices = list()
        prices.append(initial_price)

        get_floor = self.custom_get_floor(interval, loss_cut)
        get_ceiling = self.custom_get_ceiling(interval, loss_cut)
        for index in df.index:
            low_floor = get_floor(low_price[index])
            high_ceiling = get_ceiling(high_price[index])

            if open_price[index] < close_price[index]:
                while low_floor != get_floor(high_ceiling):
                    low_floor = get_ceiling(low_floor)
                    if prices[-1] != low_floor:
                        if not ((prices[-1] == get_floor(low_floor)) and self.at_cut_price(low_floor)):
                            prices.append(low_floor)
            else:
                while low_floor != get_floor(high_ceiling):
                    high_ceiling = get_floor(high_ceiling - 1)
                    if prices[-1] != high_ceiling:
                        if not ((prices[-1] == get_floor(high_ceiling)) and self.at_cut_price(high_ceiling)):
                            prices.append(high_ceiling)

        processed_prices = list()
        processed_prices.append(initial_price)
        for index, price in enumerate(prices[1:-1]):
            if self.at_cut_price(price):
                ceiling_criteria = price + loss_cut
                floor_criteria = price - (interval - loss_cut)
                if not ((prices[index] == ceiling_criteria) and (prices[index+2] == floor_criteria)):
                    processed_prices.append(price)
            else:
                processed_prices.append(price)
        processed_prices.append(prices[-1])

        return processed_prices

    def get_report(self, file_name, interval, loss_cut, fee_ratio):
        earning = 0
        loss = 0
        trading_period = file_name[-12:-4]
        prices = self.get_essential_prices(file_name, interval, loss_cut)
        previous_price = prices[0]
        for index, price in enumerate(prices[1:-1]):
            next_price = prices[index + 2]
            if price == previous_price - interval:
                if price + interval == next_price:
                    earning += 1
                else:
                    loss += 1
            previous_price = price

        profit = earning * interval - loss * loss_cut
        profit_rate = round(profit / previous_price * 100, 2)
        transaction_number = earning + loss
        fee = round(transaction_number * previous_price * fee_ratio / 100, 2)
        net_profit = round(profit - fee, 2)
        net_profit_rate = round(net_profit / previous_price * 100, 2)
        self.total_profit += profit
        self.total_profit_with_fee += net_profit
        self.analysis_count += 1
        if profit > 0:
            self.winning_number += 1
        report = [trading_period, earning, loss, profit, profit_rate]
        report += [fee, net_profit, net_profit_rate]

        self.debug(report)
        return report

    def analyze(self):
        self.analysis_count = 0
        self.winning_number = 0
        self.total_profit = 0
        self.total_profit_with_fee = 0

        analysis_folder = self.le_analysis_folder.text()

        interval = int(self.le_interval.text())
        loss_cut = int(self.le_loss_cut.text())
        fee = float(self.le_fee.text())
        files = glob(analysis_folder + '/' + '*.csv')
        target_files = list()
        if self.cb_analyze_all.isChecked():
            target_files = files
        else:
            first_day = int(self.dte_first_day.text().replace('-',''))
            last_day = int(self.dte_last_day.text().replace('-', ''))
            for file in files:
                date = int(file[-12:-4])
                if first_day <= date <= last_day:
                    target_files.append(file)

        report = list()
        for file in target_files:
            individual_report = self.get_report(file, interval, loss_cut, fee)
            report.append(individual_report)

        winning_ratio = round(self.winning_number / self.analysis_count, 2)

        report_title = '===== Report : interval({}), loss-cut({}), fee({}) ====='
        report_summary = report_title.format(str(interval), str(loss_cut), str(fee))
        self.display_report(report)
        self.post(report_summary)
        self.post('Winning ratio', self.winning_number, '/', self.analysis_count, '=', winning_ratio)
        self.post('Total profit', self.formalize(self.total_profit))
        self.post('Total profit (Fee)', self.formalize(int(self.total_profit_with_fee)))
        self.post('')
        self.info('Total profit', self.total_profit)
        self.info('Total profit (Fee)', self.formalize(int(self.total_profit_with_fee)))

    def display_report(self, reports):
        self.clear_table(self.table_report)
        for row, report in enumerate(reports):
            self.table_report.insertRow(row)
            self.table_report.setRowHeight(row, 6)
            self.table_report.setItem(row, 0, self.to_item(report[0]))
            self.table_report.setItem(row, 1, self.to_item_plain(report[1]))
            self.table_report.setItem(row, 2, self.to_item_plain(report[2]))
            self.table_report.setItem(row, 3, self.to_item_sign(report[3]))
            self.table_report.setItem(row, 4, self.to_item_sign(report[4]))
            self.table_report.setItem(row, 5, self.to_item_plain(report[5]))
            self.table_report.setItem(row, 6, self.to_item_sign(report[6]))
            self.table_report.setItem(row, 7, self.to_item_sign(report[7]))
        # self.table_report.sortItems(0, Qt.DescendingOrder)

    def clear_table(self, table):
        for row in range(table.rowCount()):
            table.removeRow(0)

    def on_select_account(self, account):
        self.kiwoom.account_number = int(account)

    def on_select_item_code(self, item_code):
        item_name = CODES.get(item_code)
        if item_name is None:
            item_name = self.kiwoom.get_item_name(item_code)
            if item_name != '':
                CODES[item_code] = item_name
                self.cbb_item_code.addItem(item_code)
                self.cbb_item_name.addItem(item_name)

        self.cbb_item_name.setCurrentText(item_name)

    def on_select_item_name(self, name):
        item_name = self.cbb_item_name.currentText()
        item_code = self.kiwoom.get_item_code(item_name)
        self.cbb_item_code.setCurrentText(item_code)

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

    def on_change_analysis_folder(self):
        folder = QFileDialog.getExistingDirectory(self, 'Select folder', self.analysis_folder.text())
        if folder != '':
            self.analysis_folder.setText(folder)

    def edit_setting(self):
        self.debug('setting')

    def post(self, *args):
        message = str(args[0])
        for arg in args[1:]:
            message += ' ' + str(arg)
        self.te_info.append(message)

    def on_kiwoom_log(self, *args):
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
        self.kiwoom.log('Closing process initializing...')
        self.kiwoom.close_process()
        self.kiwoom.clear()
        self.kiwoom.deleteLater()
        self.deleteLater()