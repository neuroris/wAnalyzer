from PyQt5.QtCore import QDate
from wookutil import WookMath, WookLog, WookUtil
from wookdata import *
import pandas
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import mplfinance
import math
import os

class DayAnalysis(WookMath, WookUtil):
    def __init__(self):
        self.date = None
        self.item_name = ''
        self.file_name = ''
        self.earning_count = 0
        self.loss_count = 0
        self.profit = 0
        self.profit_rate = 0.0
        self.net_profit = 0
        self.net_profit_rate = 0.0
        self.transaction_fee = 0
        self.tax = 0
        self.price_avg = 0

    def clear(self):
        self.date = None
        self.item_name = ''
        self.file_name = ''
        self.earning_count = 0
        self.loss_count = 0
        self.profit = 0
        self.profit_rate = 0.0
        self.net_profit = 0
        self.net_profit_rate = 0.0
        self.transaction_fee = 0
        self.tax = 0
        self.price_avg = 0

    def analyze(self, file_name, interval, loss_cut, fee_ratio):
        self.clear()
        self.file_name = file_name
        file = os.path.basename(file_name)
        self.item_name = file[:-17]
        self.date = QDate.fromString(file[-12:-4], 'yyyyMMdd')

        prices = self.get_simplified_prices(file_name, interval, loss_cut)
        previous_price = prices[0]
        for index, price in enumerate(prices[1:-1]):
            next_price = prices[index + 2]
            if price == (previous_price - interval):
                if price + interval == next_price:
                    self.earning_count += 1
                else:
                    self.loss_count += 1
            previous_price = price

        price_sum = 0
        for price in prices:
            price_sum += price
        self.price_avg = int(price_sum / len(prices))

        self.profit = (self.earning_count * interval) - (self.loss_count * loss_cut)
        self.profit_rate = round(self.profit / self.price_avg * 100, 2)
        transaction_number = self.earning_count + self.loss_count
        self.transaction_fee = round(transaction_number * self.price_avg * fee_ratio * 2 / 100, 2)
        self.net_profit = round(self.profit - self.transaction_fee, 2)
        self.net_profit_rate = round(self.net_profit / self.price_avg * 100, 2)

    def get_simplified_prices(self, file_name, interval, loss_cut):
        df = pandas.read_csv(file_name)
        df = self.normalize(file_name, df)
        open_price = df['Open']
        high_price = df['High']
        low_price = df['Low']
        close_price = df['Close']

        # Main engine
        prices = list()
        initial_price = open_price[0]
        prices.append(initial_price)
        get_floor = self.custom_get_floor(interval, loss_cut)
        get_ceiling = self.custom_get_ceiling(interval, loss_cut)
        at_cut_price = self.custom_at_cut_price(interval)
        for index in df.index:
            low_floor = get_floor(low_price[index])
            high_ceiling = get_ceiling(high_price[index])
            if open_price[index] < close_price[index]:
                while low_floor != get_floor(high_ceiling):
                    low_floor = get_ceiling(low_floor)
                    if prices[-1] != low_floor:
                        if not at_cut_price(low_floor):
                            prices.append(low_floor)
            else:
                while low_floor != get_floor(high_ceiling):
                    high_ceiling = get_floor(high_ceiling - 1)
                    if prices[-1] != high_ceiling:
                        if prices[-1] > high_ceiling:
                            prices.append(high_ceiling)
                        elif not at_cut_price(high_ceiling):
                            prices.append(high_ceiling)

        # Filter out descending loss cut
        processed_prices = list()
        processed_prices.append(initial_price)
        for index, price in enumerate(prices[1:-1]):
            if at_cut_price(price):
                ceiling = price + loss_cut
                floor = price - (interval - loss_cut)
                if not ((prices[index] == ceiling) and (prices[index + 2] == floor)):
                    processed_prices.append(price)
            else:
                processed_prices.append(price)
        processed_prices.append(prices[-1])
        return processed_prices

    def get_summary(self):
        summary = (self.item_name, self.date.toString('yyyy-MM-dd'), self.earning_count)
        summary += (self.loss_count, self.profit, self.profit_rate, self.transaction_fee)
        summary += (self.net_profit, self.net_profit_rate)
        return summary

class WookAnalysis:
    def __init__(self):
        self.analyses = dict()

    def add(self, analysis):
        self.analyses[analysis.date] = analysis

    def remove(self, analysis_time):
        del self.analyses[analysis_time]

    def clear(self):
        self.analyses.clear()

    def has(self, analysis_date):
        has_it = False
        if analysis_date in self.analyses:
            has_it = True
        return has_it

    def get_analysis(self, analysis_date):
        return self.analyses[analysis_date]

    def get_analyses(self):
        return self.analyses.values()

    def get_count(self):
        return len(self.analyses)

    def get_earning_count(self):
        earning_count = 0
        for analysis in self.analyses.values():
            earning_count += analysis.earning_count
        return earning_count

    def get_loss_count(self):
        loss_count = 0
        for analysis in self.analyses.values():
            loss_count += analysis.loss_count
        return loss_count

    def get_total_fee(self):
        fee = 0
        for analysis in self.analyses.values():
            fee += analysis.transaction_fee
        return int(fee)

    def get_winning_count(self):
        count = 0
        for analysis in self.analyses.values():
            if analysis.profit > 0:
                count += 1
        return count

    def get_winning_day_ratio(self):
        winning_count = self.get_winning_count()
        analysis_count = self.get_count()
        winning_ratio = winning_count / analysis_count
        return winning_ratio

    def get_total_profit(self):
        profit = 0
        for analysis in self.analyses.values():
            profit += analysis.profit
        return profit

    def get_average_price(self):
        price_sum = 0
        for analysis in self.analyses.values():
            price_sum += analysis.price_avg
        average_price = price_sum / self.get_count()
        return average_price

    def get_total_profit_rate(self):
        profit = self.get_total_profit()
        profit_rate = round(profit / self.get_average_price() * 100, 2)
        return profit_rate

    def get_total_net_profit(self):
        profit = self.get_total_profit()
        fee = self.get_total_fee()
        net_profit = round(profit - fee, 2)
        return net_profit

    def get_total_net_profit_rate(self):
        net_profit = self.get_total_net_profit()
        net_profit_rate = round(net_profit / self.get_average_price() * 100, 2)
        return net_profit_rate

class WookChart(WookLog, WookUtil):
    def __init__(self, log):
        WookUtil.__init__(self)
        WookLog.custom_init(self, log)

    def show_candle_chart(self, file_name, interval):
        setup = dict(figscale=1.5)
        self.set_candle_chart(file_name, interval, setup)
        self.debug('Candle chart displayed')

    def save_candle_chart(self, file_name, interval):
        save_file = file_name[:-4] + '.png'
        setup = dict(savefig=save_file, figscale=2)
        self.set_candle_chart(file_name, interval, setup)
        self.debug('Candle chart saved', save_file)

    def set_candle_chart(self, file_name, interval, setup):
        df = pandas.read_csv(file_name, index_col=0, parse_dates=True)
        df = self.normalize(file_name, df)
        max_price = df['High'].max()
        min_price = df['Low'].min()
        max_ceiling = math.ceil(max_price / interval) * interval
        min_floor = math.floor(min_price / interval) * interval
        yticks = list(range(min_floor, max_ceiling + interval, interval))

        mpl_color = mplfinance.make_marketcolors(up='tab:red', down='tab:blue', volume='Goldenrod')
        mpl_style = mplfinance.make_mpf_style(base_mpl_style='seaborn', marketcolors=mpl_color)
        setup.update(dict(type='candle', style=mpl_style, tight_layout=True))
        setup.update(dict(figratio=(1920, 1080), volume=True))
        setup.update(dict(hlines=dict(hlines=yticks[:-1], linewidths=0.1, colors='silver', alpha=1)))
        mplfinance.plot(df, **setup)

    def show_simplified_chart(self, day_analysis, interval, loss_cut):
        self.set_simplified_chart(day_analysis, interval, loss_cut)
        plt.show()
        self.debug('Simplified chart displayed')

    def save_simplified_chart(self, day_analysis, interval, loss_cut):
        self.set_simplified_chart(day_analysis, interval, loss_cut)
        file_name = day_analysis.file_name
        save_file = file_name[:-12] + 'simplified ' + file_name[-12:-4] + '.png'
        plt.savefig(save_file)
        self.debug('Simplified chart saved', save_file)

    def set_simplified_chart(self, day_analysis, interval, loss_cut):
        file_name = day_analysis.file_name
        date = os.path.basename(file_name)[-12:-4]
        prices = day_analysis.get_simplified_prices(file_name, interval, loss_cut)
        df = pandas.read_csv(file_name)
        df = self.normalize(file_name, df)
        max_price = df['High'].max()
        min_price = df['Low'].min()
        max_limit = math.ceil(max_price / interval) * interval
        min_limit = math.floor(min_price / interval) * interval
        ortho_prices = list(range(min_limit, max_limit + interval, interval))
        cut_prices = [value + interval - loss_cut for value in ortho_prices[:-1]]

        plt.style.use('seaborn')
        fig = plt.figure(figsize=(17, 8))
        ax = fig.add_subplot()
        ax.plot(prices, linewidth=2, color='peru', label='price')
        ax.set_title('Processed price')
        ax.set_xlabel('Time')
        ax.set_ylabel('Price')
        ax.legend(labels=[date], loc='best')
        ax.set_ylim(min_limit, max_limit)
        ax.set_yticks(ortho_prices)
        for value in ortho_prices:
            ax.axhline(y=value, color='blue', linewidth=0.3)
        for value in cut_prices:
            ax.axhline(y=value, color='red', linewidth=0.1)