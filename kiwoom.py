from PyQt5.QtWidgets import QApplication
from PyQt5.QAxContainer import QAxWidget
from errorcode import errors
from kiwoombase import KiwoomBase
from wookauto import LoginPasswordThread, AccountPasswordThread
from wookstock import Stock
from wookdata import *
import time, os
import re

class Kiwoom(QAxWidget, KiwoomBase):
    def __init__(self, log, key):
        super().__init__()
        KiwoomBase.custom_init(self, log, key)

        self.info('Kiwoom initializing...')
        self.set_OCX()
        self.connect_slots()

        # self.request_account_deposit()
        # self.request_stock_price()

        # self.close_process()

    def set_OCX(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")
        self.info('OCX set')

    def connect_slots(self):
        self.OnEventConnect.connect(self.on_login)
        self.OnReceiveTrData.connect(self.on_receive_tr_data)
        self.OnReceiveRealData.connect(self.on_receive_real_data)
        self.OnReceiveChejanData.connect(self.on_receive_chejan_data)
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

    def request_account_deposit(self, sPrevNext='0'):
        self.set_input_values()
        self.comm_rq_data('deposit', REQUEST_DEPOSIT_INFO, sPrevNext, self.screen_no_account)
        self.event_loop.exec()

    def request_account_portfolio(self, sPrevNext='0'):
        self.set_input_values()
        self.comm_rq_data('portfolio', REQUEST_PORTFOLIO_INFO, sPrevNext, self.screen_no_account)
        self.event_loop.exec()

    def request_unconcluded_order(self, sPrevNext='0'):
        self.set_input_value(ACCOUNT_NUMBER, self.account_number)
        self.set_input_value(CONCLUSION_TYPE, UNCONCLUDED)
        self.set_input_value(TRADING_TYPE, ALL)
        self.comm_rq_data('inconclusion', REQUEST_UNCONCLUDED_ORDER, sPrevNext, self.screen_no_inconclusion)
        self.event_loop.exec()

    def request_stock_price(self, reference_date=None, sPrevNext='0'):
        if reference_date is None:
            reference_date = time.strftime('%Y%m%d')
        code_list = self.get_code_list_by_market(MARKET_KOSDAQ)
        num_list = len(code_list)
        # for count, item_code in enumerate(code_list):
        #     print('KOSDAQ({}/{}) code : {}'.format(count, num_list, item_code))
        #     self.request_stock_price_proper(item_code, reference_date, sPrevNext)
        #     self.init_screen_no(self.screen_no_stock_price)

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

    def demand_market_operation_state(self):
        self.set_real_reg(self.screen_no_operation_state, ' ', FID.MARKET_OPERATION_STATE, '0')

    def demand_interesting_items_update(self):
        self.set_real_reg(self.screen_no_interesting_items, '122630', FID.TRANSACTION_TIME)

    def on_login(self, err_code):
        self.info('Login status code :', err_code)
        self.login_event_loop.exit()

    def on_receive_tr_data(self, sScrNo, sRQName, sTrCode, sRecordName, sPrevNext):
        if sRQName == 'deposit':
            self.get_account_deposit(sTrCode, sRQName)
        elif sRQName == 'portfolio':
            self.get_account_portfolio(sTrCode, sRQName, sPrevNext)
        elif sRQName == 'inconclusion':
            self.get_unconcluded_order(sTrCode, sRQName, sPrevNext)
        elif sRQName == 'stock price':
            self.get_stock_price(sTrCode, sRQName, sPrevNext)

        if sPrevNext != '2':
            self.init_screen_no(sScrNo)
            self.event_loop.exit()

    def on_receive_real_data(self, sCode, sRealType, sRealData):
        print(sCode, sRealType, sRealData)

        if sRealType == REAL_MARKET_OPENING_TIME:
            self.get_market_operation_state(sCode)
        elif sRealType == REAL_CONCLUSION_TIME:
            self.update_interesting_items(sCode)

    def on_receive_chejan_data(self, sGubun, nItemCnt, nFidList):
        print(sGubun, nItemCnt, nFidList)

        if sGubun == '0':
            account_number = self.get_chejan_data(FID.ACCOUNT_NUMBER)
            item_code = self.get_chejan_data(FID.ITEM_CODE)
            item_name = self.get_chejan_data(FID.ITEM_NAME)
            original_order_number = self.get_chejan_data(FID.ORIGINAL_ORDER_NUMBER)
            order_number = self.get_chejan_data(FID.ORDER_NUMBER)
            order_state = self.get_chejan_data(FID.ORDER_STATE)
            order_amount = self.get_chejan_data(FID.ORDER_AMOUNT)
            order_price = self.get_chejan_data(FID.ORDER_PRICE)
            unconcluded_amount = self.get_chejan_data(FID.UNCONCLUDED_AMOUNT)
            order_type = self.get_chejan_data(FID.ORDER_TYPE)
            order_transaction_time = self.get_chejan_data(FID.ORDER_TRANSACTION_TIME)
            transaction_price = self.get_chejan_data(FID.TRANSACTION_PRICE)
            transaction_amount = self.get_chejan_data(FID.TRANSACTION_AMOUNT)
            current_price = self.get_chejan_data(FID.CURRENT_PRICE)
            ask_price = self.get_chejan_data(FID.ASK_PRICE)
            bid_price = self.get_chejan_data(FID.BID_PRICE)
        elif sGubun == '1':
            account_number = self.get_chejan_data(FID.ACCOUNT_NUMBER)
            item_code = self.get_chejan_data(FID.ITEM_CODE)
            item_name = self.get_chejan_data(FID.ITEM_NAME)
            current_price = self.get_chejan_data(FID.CURRENT_PRICE)
            holding_amount = self.get_chejan_data(FID.HOLDING_AMOUNT)
            orderabel_amount = self.get_chejan_data(FID.ORDERABLE_AMOUNT)
            purchase_amount = self.get_chejan_data(FID.PURCHASE_PRICE)
            purchase_sum = self.get_chejan_data(FID.PURCHASE_SUM)
            ask_bid = self.get_chejan_data(FID.ASK_BID)
            ask_price = self.get_chejan_data(FID.ASK_PRICE)
            bid_price = self.get_chejan_data(FID.BID_PRICE)

    def on_receive_msg(self, sScrNo, sRQName, sTrCode, sMsg):
        print('Receiving message', sScrNo, sRQName, sTrCode, sMsg)

    def get_account_deposit(self, sTrCode, sRQName):
        get_comm_data = self.new_get_comm_data(sTrCode, sRQName, 0)
        self.deposit = get_comm_data(DEPOSIT)
        self.withdrawable = get_comm_data(WITHDRAWABLE)
        print('Deposit :', self.formalize_int(self.deposit))
        print('Withdrawable :', self.formalize_int(self.withdrawable))

    def get_account_portfolio(self, sTrCode, sRQName, sPrevNext):
        header = Stock().get_header()
        print(header)

        number_of_item = self.get_repeat_count(sTrCode, sRQName)
        for count in range(number_of_item):
            get_comm_data = self.new_get_comm_data(sTrCode, sRQName, count)

            stock = Stock()
            stock.item_number = get_comm_data(ITEM_NUMBER)
            stock.item_name = get_comm_data(ITEM_NAME)
            stock.purchase_amount = get_comm_data(PURCHASE_AMOUNT)
            stock.purchase_price = get_comm_data(PURCHASE_PRICE)
            stock.current_price = get_comm_data(CURRENT_PRICE)
            stock.purchase_sum = get_comm_data(PURCHASE_SUM)
            stock.profit_rate = get_comm_data(PROFIT_RATE)
            stock.sellable_amount = get_comm_data(SELLABLE_AMOUNT)
            self.stocks.append(stock)

            stock_arranged_info = stock.get_arranged_info()
            print(stock_arranged_info)

        if sPrevNext == '2':
            self.request_account_portfolio(sPrevNext)
        else:
            self.get_account_overall_status(sTrCode, sRQName)

    def get_account_overall_status(self, sTrCode, sRQName):
        get_comm_data = self.new_get_comm_data(sTrCode, sRQName, 0)
        self.total_purchase_sum = get_comm_data(TOTAL_PURCHASE_SUM)
        self.total_profit_evaluated = get_comm_data(TOTAL_PROFIT_EVALUATED)
        self.total_profit_rate = get_comm_data(TOTAL_PROFIT_RATE)
        print('Total Purchase Sum :', self.formalize_int(self.total_purchase_sum))
        print('Total Profit Evaluated :', self.formalize_int(self.total_profit_evaluated))
        print('Total Profit Rate :', self.formalize_float(self.total_profit_rate))

    def get_unconcluded_order(self, sTrCode, sRQName, sPrevNext):
        number_of_item = self.get_repeat_count(sTrCode, sRQName)
        for count in range(number_of_item):
            get_comm_data = self.new_get_comm_data(sTrCode, sRQName, count)

            stock = Stock()
            stock.item_code = get_comm_data(ITEM_CODE)
            stock.item_name = get_comm_data(ITEM_NAME)
            stock.order_number = get_comm_data(ORDER_NUMBER)
            stock.order_state = get_comm_data(ORDER_STATE)
            stock.order_amount = get_comm_data(ORDER_AMOUNT)
            stock.order_price = get_comm_data(ORDER_PRICE)
            stock.order_type = get_comm_data(ORDER_TYPE)
            stock.unconcluded_amount = get_comm_data(UNCONCLUDED_AMOUNT)
            stock.concluded_amount = get_comm_data(CONCLUDED_AMOUNT)

            self.unconcluded_stocks.append(stock)

        if sPrevNext == '2':
            self.request_unconcluded_order(sPrevNext)

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

    def get_market_operation_state(self, sCode):
        operation_state = self.get_comm_real_data(sCode, FID.MARKET_OPERATION_STATE)
        if operation_state == '0':
            print('it is before market opening!')
        elif operation_state == '3':
            print('it is market opening hours')
        elif operation_state == '2':
            print('market is closed')
        elif operation_state == '4':
            print('single price market is over')

    def update_interesting_items(self, sCode):
        get_comm_real_data = self.new_get_comm_real_data(sCode)
        transaction_time = get_comm_real_data(FID.TRANSACTION_TIME)
        current_price = get_comm_real_data(FID.CURRENT_PRICE)
        price_increase_amount = get_comm_real_data(FID.PRICE_INCREASE_AMOUNT)
        price_increase_ratio = get_comm_real_data(FID.PRICE_INCREASE_RATIO)
        ask_price = get_comm_real_data(FID.ASK_PRICE)
        bid_price = get_comm_real_data(FID.BID_PRICE)
        volume = get_comm_real_data(FID.VOLUME)
        accumulated_volume = get_comm_real_data(FID.ACCUMULATED_VOLUME)
        highest_price = get_comm_real_data(FID.HIGHEST_PRICE)
        lowest_price = get_comm_real_data(FID.LOWEST_PRICE)
        opening_price = get_comm_real_data(FID.OPENING_PRICE)

        print(transaction_time)
        print(current_price)
        print(price_increase_amount)
        print(price_increase_ratio)
        print(ask_price)
        print(bid_price)
        print(volume)
        print(accumulated_volume)
        print(highest_price)
        print(lowest_price)
        print(opening_price)

    def init_screen_no(self, sScrNo):
        self.dynamic_call('DisconnectRealData', sScrNo)

    def on_receive_condition_ver(self, IRet, sMsg):
        print(IRet, sMsg)
        print('receive condition ver')

    def do(self):
        item_code = '005930'
        quantity = 1
        price = 40000
        send_order = self.new_send_order('new order', self.screen_no_bid, self.account_number)
        result = send_order(TRADE_TYPE.BID, item_code, quantity, price, ORDER_TYPE.MARGINAL)

        print(result)

    def close_process(self):
        self.save_intesting_stocks()
        self.dynamic_call('SetRealRemove', 'ALL', 'ALL')