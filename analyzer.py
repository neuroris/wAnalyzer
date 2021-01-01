from PyQt5.QtWidgets import QFileDialog, QTableWidgetSelectionRange
from PyQt5.QtCore import Qt, QDate, QModelIndex
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance
import math, os
from glob import glob
from analyzerbase import AnalyzerBase
from kiwoom import Kiwoom
from wookreport import WookAnalysis, DayAnalysis, WookChart
from wookdata import *

class Analyzer(AnalyzerBase):
    def __init__(self, log, key):
        self.kiwoom = Kiwoom(log, key)
        super().__init__(log)
        self.wook_analysis = WookAnalysis()
        self.wook_chart = WookChart(log)
        self.initKiwoom()

        self.te_info.append('===== Welcome to wAnalyzer =====')
        # self.connect_kiwoom()

        self.dte_first_day.setDate(QDate.fromString('20201201', 'yyyyMMdd'))

        # self.cbb_item_name.setCurrentIndex(3)
        # self.cbb_item_code.setCurrentText('101R3000')

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
        futures = False
        if self.cbb_item_code.currentText()[:3] == FUTURES_CODE:
            futures = True

        if self.rb_tick.isChecked() and futures:
            self.status_bar.showMessage('Getting futures stock prices (tick data)...')
            self.kiwoom.request_futures_stock_price_tick()
        elif self.rb_min.isChecked() and futures:
            self.status_bar.showMessage('Getting futures stock prices (minute data)...')
            self.kiwoom.request_futures_stock_price_min()
        elif self.rb_tick.isChecked():
            self.status_bar.showMessage('Getting stock prices (tick data)...')
            self.kiwoom.request_stock_price_tick()
        elif self.rb_min.isChecked():
            self.status_bar.showMessage('Getting stock prices (minute data)...')
            self.kiwoom.request_stock_price_min()
        elif self.rb_day.isChecked():
            self.status_bar.showMessage('Getting stock prices (day data)...')
            self.kiwoom.request_stock_price_day()

    def analyze(self):
        self.wook_analysis.clear()
        self.lb_analysis_item.setText('No Item')
        self.btn_candle_chart.setEnabled(False)
        self.btn_simplified_chart.setEnabled(False)

        folder = self.le_analysis_folder.text()
        interval = int(self.le_interval.text())
        loss_cut = int(self.le_loss_cut.text())
        fee_ratio = float(self.le_fee.text())
        files = glob(os.path.join(folder, '*.csv'))
        if len(files) == 0:
            self.status_bar.showMessage('No csv files in the folder')
            self.debug('No csv files in the folder')
            return

        target_files = list()
        if self.cb_all_days.isChecked():
            target_files = files
        else:
            first_day = self.dte_first_day.date()
            last_day = self.dte_last_day.date()
            for file in files:
                date = QDate.fromString(file[-12:-4], 'yyyyMMdd')
                if first_day <= date <= last_day:
                    target_files.append(file)

        for file in target_files:
            day_analysis = DayAnalysis()
            day_analysis.analyze(file, interval, loss_cut, fee_ratio)
            self.wook_analysis.add(day_analysis)
            self.debug(*day_analysis.get_summary())

        if not target_files:
            self.debug('No files available')
            return

        winning_number = self.wook_analysis.get_winning_count()
        analysis_count = self.wook_analysis.get_count()
        winning_ratio = round(winning_number / analysis_count, 2)
        total_profit = self.wook_analysis.get_total_profit()
        total_net_profit = int(self.wook_analysis.get_total_net_profit())

        report_title = '\n===== Report : interval({}), loss-cut({}), fee({}) ====='
        report_summary = report_title.format(str(interval), str(loss_cut), str(fee_ratio))
        self.display_report(self.wook_analysis.analyses)
        self.post(report_summary)
        self.post('Winning ratio', winning_number, '/', analysis_count, '=', winning_ratio)
        self.post('Total profit', self.formalize(total_profit))
        self.post('Total profit(net)', self.formalize(total_net_profit))
        self.info('Total profit', self.formalize(total_profit))
        self.info('Total profit(net)', self.formalize(total_net_profit))

    def go_candle_chart(self):
        interval = int(self.le_interval.text())
        load_folder = self.le_analysis_folder.text()
        all_files = glob(load_folder + '/' + '*.csv')
        first_day = QDate.fromString(self.lb_analysis_first_day.text(), 'yyyy-MM-dd')
        last_day = QDate.fromString(self.lb_analysis_last_day.text(), 'yyyy-MM-dd')
        files = list()
        if self.cb_all_days.isChecked():
            files = all_files
        else:
            for file in all_files:
                date = QDate.fromString(file[-12:-4], 'yyyyMMdd')
                if first_day <= date <= last_day:
                    files.append(file)

        if not files:
            self.debug('No file is available in the period')
            return

        if self.rb_show_chart.isChecked():
            self.wook_chart.show_candle_chart(files[0], interval)
        else:
            for file in files:
                self.wook_chart.save_candle_chart(file, interval)
            self.debug('All charts have been saved')

    def go_simplified_chart(self):
        if self.rb_show_chart.isChecked():
            self.show_simplified_chart()
        else:
            self.save_simplified_chart()

    def show_simplified_chart(self):
        date = QDate.fromString(self.lb_analysis_first_day.text(), 'yyyy-MM-dd')
        if not self.wook_analysis.has(date):
            self.status_bar.showMessage('No data at that date')
            self.debug('No data at that date')
            return

        interval = int(self.le_interval.text())
        loss_cut = int(self.le_loss_cut.text())
        day_analysis = self.wook_analysis.get_analysis(date)
        self.wook_chart.show_simplified_chart(day_analysis, interval, loss_cut)

    def save_simplified_chart(self):
        interval = int(self.le_interval.text())
        loss_cut = int(self.le_loss_cut.text())
        first_day = QDate.fromString(self.lb_analysis_first_day.text(), 'yyyy-MM-dd')
        last_day = QDate.fromString(self.lb_analysis_last_day.text(), 'yyyy-MM-dd')
        all_analyses = self.wook_analysis.get_analyses()
        analyses = list()
        if self.cb_all_days.isChecked():
            analyses = all_analyses
        else:
            for analysis in all_analyses:
                if first_day <= analysis.date <= last_day:
                    analyses.append(analysis)

        if not analyses:
            self.debug('No analysis is available in the period')
            return

        for analysis in analyses:
            self.wook_chart.save_simplified_chart(analysis, interval, loss_cut)
        self.debug('All charts have been saved')

    def display_report(self, analyses):
        self.clear_table(self.table_report)
        row = 0
        for row, analysis in enumerate(analyses.values()):
            self.table_report.insertRow(row)
            self.table_report.setRowHeight(row, 6)
            self.table_report.setItem(row, 0, self.to_item(analysis.item_name))
            self.table_report.setItem(row, 1, self.to_item(analysis.date.toString('yyyy-MM-dd')))
            self.table_report.setItem(row, 2, self.to_item_plain(analysis.earning_count))
            self.table_report.setItem(row, 3, self.to_item_plain(analysis.loss_count))
            self.table_report.setItem(row, 4, self.to_item_sign(analysis.profit))
            self.table_report.setItem(row, 5, self.to_item_sign(analysis.profit_rate))
            self.table_report.setItem(row, 6, self.to_item_plain(analysis.transaction_fee))
            self.table_report.setItem(row, 7, self.to_item_sign(analysis.net_profit))
            self.table_report.setItem(row, 8, self.to_item_sign(analysis.net_profit_rate))

        row += 1
        self.table_report.insertRow(row)
        self.table_report.setRowHeight(row, 6)
        self.table_report.setItem(row, 0, self.to_item('Total'))
        self.table_report.setItem(row, 1, self.to_item_plain(self.wook_analysis.get_count()))
        self.table_report.setItem(row, 2, self.to_item_plain(self.wook_analysis.get_earning_count()))
        self.table_report.setItem(row, 3, self.to_item_plain(self.wook_analysis.get_loss_count()))
        self.table_report.setItem(row, 4, self.to_item_sign(self.wook_analysis.get_total_profit()))
        self.table_report.setItem(row, 5, self.to_item_sign(self.wook_analysis.get_total_profit_rate()))
        self.table_report.setItem(row, 6, self.to_item_plain(self.wook_analysis.get_total_fee()))
        self.table_report.setItem(row, 7, self.to_item_sign(self.wook_analysis.get_total_net_profit()))
        self.table_report.setItem(row, 8, self.to_item_sign(self.wook_analysis.get_total_net_profit_rate()))

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
        self.kiwoom.item_code = item_code

    def on_select_item_name(self, name):
        item_name = self.cbb_item_name.currentText()
        item_code = self.kiwoom.get_item_code(item_name)
        self.cbb_item_code.setCurrentText(item_code)
        self.kiwoom.item_name = item_name

    def on_change_first_day(self, date):
        self.kiwoom.first_day = date.toString('yyyy-MM-dd')
        self.cb_all_days.setChecked(False)
        if self.cb_one_day.isChecked():
            self.dte_last_day.setDate(date)
        if self.rb_save_chart.isChecked():
            self.lb_analysis_first_day.setText(date.toString('yyyy-MM-dd'))
            self.lb_analysis_last_day.setText(self.dte_last_day.date().toString('yyyy-MM-dd'))

    def on_change_last_day(self, date):
        self.kiwoom.last_day = date.toString('yyyy-MM-dd')
        self.cb_all_days.setChecked(False)
        if self.cb_one_day.isChecked():
            self.dte_first_day.setDate(date)
        if self.rb_save_chart.isChecked():
            self.lb_analysis_first_day.setText(self.dte_first_day.date().toString('yyyy-MM-dd'))
            self.lb_analysis_last_day.setText(date.toString('yyyy-MM-dd'))

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
        home = self.le_analysis_folder.text()
        separate_home = home.split('/')
        new_home = '/'.join(separate_home[:-1])
        folder = QFileDialog.getExistingDirectory(self, 'Select folder', new_home)
        if folder != '':
            self.le_analysis_folder.setText(folder)

    def on_select_table_report(self, row, column):
        row_count = self.table_report.rowCount() - 1
        if row == row_count:
            return

        column_count = self.table_report.columnCount() - 1
        selection_range = QTableWidgetSelectionRange(row, 0, row, column_count)
        self.table_report.setRangeSelected(selection_range, True)

        item_name_column = 0
        item_name_item = self.table_report.item(row, item_name_column)
        self.lb_analysis_item.setText(item_name_item.text())

        time_column = 1
        time_item = self.table_report.item(row, time_column)
        time_text = time_item.text()
        self.lb_analysis_first_day.setText(time_text)
        self.lb_analysis_last_day.setText(time_text)
        self.btn_candle_chart.setEnabled(True)
        self.btn_simplified_chart.setEnabled(True)

    def on_select_save_chart(self):
        self.btn_candle_chart.setEnabled(True)
        self.btn_simplified_chart.setEnabled(True)
        self.lb_analysis_first_day.setText(self.dte_first_day.text())
        self.lb_analysis_last_day.setText(self.dte_last_day.text())

    def on_select_show_chart(self):
        time_column = 1
        index = self.table_report.selectedIndexes()[time_column]
        row = index.row()
        time_item = self.table_report.item(row, time_column)
        time_text = time_item.text()
        self.lb_analysis_first_day.setText(time_text)
        self.lb_analysis_last_day.setText(time_text)

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