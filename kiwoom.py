from PyQt5.QAxContainer import QAxWidget
from kiwoombase import KiwoomBase
from wookauto import LoginPasswordThread, AccountPasswordThread
from wookdata import *
import time, os, re

class Kiwoom(QAxWidget, KiwoomBase):
    def __init__(self, log, key):
        super().__init__()
        KiwoomBase.custom_init(self, log, key)

        self.info('Kiwoom initializing...')
        self.set_OCX()
        self.connect_slots()

        # self.request_stock_price()

    def set_OCX(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")
        self.info('OCX set')

    def connect_slots(self):
        self.OnEventConnect.connect(self.on_login)
        self.OnReceiveTrData.connect(self.on_receive_tr_data)
        self.OnReceiveMsg.connect(self.on_receive_msg)
        self.OnReceiveConditionVer.connect(self.on_receive_condition_ver)

    def connect(self, auto_login):
        if auto_login:
            self.auto_login()
        else:
            self.login()
            self.set_account_password()
        self.info('Logged in to Kiwoom server')

        self.get_account_list()

        return self.login_status

    def auto_login(self):
        self.dynamicCall('CommConnect()')
        self.login_event_loop.exec()

    def login(self):
        self.dynamicCall("CommConnect()")
        log_passwd_thread = LoginPasswordThread(self.event_loop, self.login_id, self.login_password, self.certificate_password)
        log_passwd_thread.start()
        self.event_loop.exec()
        self.login_event_loop.exec()

    def set_account_password(self):
        acc_psword_thread = AccountPasswordThread(self.event_loop, self.account_password)
        acc_psword_thread.start()
        self.event_loop.exec()

        # self.KOA_Functions('ShowAccountWindow', '')

    def get_account_list(self):
        account_list = self.dynamic_call('GetLoginInfo()', 'ACCLIST')
        self.account_list = account_list.split(';')
        self.account_list.pop()
        self.account_number = self.account_list[0]

        for index, account in enumerate(self.account_list):
            print("Account {} : {}".format(index+1, account))

        self.info('Account information acquired')

    def request_stock_price(self, reference_date=None, sPrevNext='0'):
        if reference_date is None:
            reference_date = time.strftime('%Y%m%d')
        code_list = self.get_code_list_by_market(MARKET_KOSDAQ)
        num_list = len(code_list)

        kodex_leverage = '122630'
        self.request_stock_price_min_proper(kodex_leverage, sPrevNext)
        kodex_inverse = '252670'
        self.request_stock_price_min_proper(kodex_inverse, sPrevNext)
        self.init_screen_no(self.screen_no_stock_price)

    def request_stock_price_proper(self, item_code, reference_date, sPrevNext='0'):
        self.set_input_value(ITEM_CODE, item_code)
        self.set_input_value(REFERENCE_DATE, reference_date)
        self.set_input_value(CORRECTED_PRICE_TYPE, '1')
        self.comm_rq_data('stock price', REQUEST_DAY_PRICE, sPrevNext, self.screen_no_stock_price)
        self.event_loop.exec()

    def request_stock_price_min_proper(self, item_code, sPrevNext='0'):
        self.set_input_value(ITEM_CODE, item_code)
        self.set_input_value(TIC_RANGE, ONE_MIN)
        self.set_input_value(CORRECTED_PRICE_TYPE, '1')
        self.comm_rq_data('stock price', REQUEST_MINUTE_PRICE, sPrevNext, self.screen_no_stock_price)
        self.event_loop.exec()

    def on_login(self, err_code):
        self.login_status = err_code
        self.info('Login status code :', err_code)
        self.login_event_loop.exit()

    def on_receive_tr_data(self, sScrNo, sRQName, sTrCode, sRecordName, sPrevNext):
        if sRQName == 'stock price':
            self.get_stock_price(sTrCode, sRQName, sPrevNext)

        if sPrevNext != '2':
            self.init_screen_no(sScrNo)
            self.event_loop.exit()

    def on_receive_msg(self, sScrNo, sRQName, sTrCode, sMsg):
        print('Receiving message', sScrNo, sRQName, sTrCode, sMsg)

    def get_stock_price(self, sTrCode, sRQName, sPrevNext):
        item_code = self.get_comm_data(sTrCode, sRQName, 0, ITEM_CODE)
        # data = self.get_comm_data_ex(sTrCode, sRQName)

        get_comm_data = self.new_get_comm_data(sTrCode, sRQName)

        number_of_item = self.get_repeat_count(sTrCode, sRQName)
        print(number_of_item)

        day = '20201008'
        day_re = re.compile(day+'.*')

        if item_code == 122630:
            file_name = 'D:/Algorithm/leverage minute/' + day + '.csv'
        elif item_code == 252670:
            file_name = 'D:/Algorithm/inverse minute/' + day + '.csv'
        else:
            print('wrong code')

        if os.path.exists(file_name):
            os.remove(file_name)
        file = open(file_name, 'a')
        file.write('time,opening,highest,lowest,current\n')
        data_list = list()

        for count in range(number_of_item):
            date = self.get_comm_data(sTrCode, sRQName, count, DATE)
            time = str(get_comm_data(count, TRANSACTION_TIME))

            # if not day_re.match(time):
            #     continue

            opening_price = str(abs(get_comm_data(count, OPENING_PRICE)))
            highest_price = str(abs(get_comm_data(count, HIGHEST_PRICE)))
            lowest_price = str(abs(get_comm_data(count, LOWEST_PRICE)))
            current_price = str(abs(get_comm_data(count, CURRENT_PRICE)))

            price = ['t'+time, opening_price, highest_price, lowest_price, current_price]
            data = ','.join(price)
            print(data)
            data_list.append(data)
        data_list.reverse()
        file_data = '\n'.join(data_list)
        file.write(file_data)
        file.close()

        if sPrevNext == '2':
            self.request_stock_price_min_proper(item_code, sPrevNext)
            print(item_code, sPrevNext)

    def get_code_list_by_market(self, market_code):
        code_str = self.dynamic_call('GetCodeListByMarket', market_code)
        code_list = code_str.split(';')
        code_list.pop()
        return code_list

    def init_screen_no(self, sScrNo):
        self.dynamic_call('DisconnectRealData', sScrNo)

    def on_receive_condition_ver(self, IRet, sMsg):
        print(IRet, sMsg)
        print('receive condition ver')

    def close_process(self):
        pass
        # self.save_intesting_stocks()
        # self.dynamic_call('SetRealRemove', 'ALL', 'ALL')