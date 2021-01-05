# Korean parameters
DEPOSIT = '예수금'
WITHDRAWABLE = '출금가능금액'
ORDERABLE = '주문가능금액'
TOTAL_PURCHASE_SUM = '총매입금액'
TOTAL_PROFIT_EVALUATED = '총평가손익금액'
TOTAL_PROFIT_RATE = '총수익률(%)'
ACCOUNT_NUMBER = '계좌번호'
PASSWORD = '비밀번호'
PASSWORD_MEDIA_TYPE = '비밀번호입력매체구분'
INQUIRY_TYPE = '조회구분'
CORRECTED_PRICE_TYPE = '수정주가구분'
RECEIPT = '접수'
CONFIRMED = '확인'
ORDER_EXECUTED = '체결'
ORDER_PRICE = '주문가격'
PURCHASE = '매수'
SELL = '매도'
CANCEL_PURCHASE = '매수취소'
CANCEL_SELL = '매도취소'
CORRECT_PURCHASE = '매수정정'
CORRECT_SELL = '매도정정'
REFERENCE_DATE = '기준일자'
END_DATE = '끝일자'
DATE = '일자'
TRANSACTION_TIME = '체결시간'
OPEN_PRICE = '시가'
HIGH_PRICE = '고가'
LOW_PRICE = '저가'
VOLUME = '거래량'
TICK_RANGE = '틱범위'
# TICK_1 = '1:1틱'
# TICK_3 = '3:3틱'
# TICK_5 = '5:5틱'
# TICK_10 = '10:10틱'
# TICK_30 = '30:30틱'
# MIN_1 = '1:1분'
# MIN_3 = '3:3분'
# MIN_5 = '5:5분'
# MIN_10 = '10:10분'
# MIN_15 = '15:15분'
# MIN_30 = '30:30분'
# MIN_45 = '45:45분'
# MIN_60 = '60:60분'
DAY_DATA = '일'
WEEK_DATA = '주'
MONTH_DATA = '월'
YEAR_DATA = '년'
TIME_UNIT = '시간단위'
MIN = ['1:1분', '3:3분', '5:5분', '10:10분', '15:15분', '30:30분', '45:45분', '60:60분']
TICK = ['1:1틱', '3:3틱', '5:5틱', '10:10틱', '30:30틱']
# MIN_FUTURES = ['1분:1', '3분:3', '5분:5', '10분:10', '15분:15', '30분:30', '60분:60', '120분:120']
FUTURES_CODE = '101'
FUTURES_NAME = 'F '

# Korean parameters with subfields
TRADE_POSITION = '매매구분'
class POSITION:
    ALL = '0'
    SELL = '1'
    BUY = '2'

ALL_OR_INDIVIDUAL = '전체종목구분'
ALL = '0'
INDIVIDUAL = '1'

ORDER_EXECUTION_TYPE = '체결구분'
class ORDER:
    ALL = '0'
    OPEN = '1'
    EXECUTED = '2'

ORDER_POSITION = '주문구분'
ORDER_POSITION_DICT = {
    'BUY': '1',
    'SELL': '2',
    'CANCEL BUY': '3',
    'CANCEL SELL': '4',
    'CORRECT BUY': '5',
    'CORRECT SELL': '6'
}

ORDER_TYPE = {
    'LIMIT': '00',
    'MARKET': '03',
    'CONDITIONAL': '05',
    'COVER': '06',
    'MARGINAL': '07',
    'BEFORE': '61',
    'CLOSING': '62',
    'AFTER': '81',
}

# Request codes
REQUEST_DEPOSIT_INFO = 'opw00001'
REQUEST_PORTFOLIO_INFO = 'opw00018'
REQUEST_OPEN_ORDER = 'opt10075'
REQUEST_EXECUTED_ORDER = 'opt10076'
REQUEST_TICK_PRICE = 'opt10079'
REQUEST_MINUTE_PRICE = 'opt10080'
REQUEST_DAY_PRICE = 'opt10081'
REQUEST_WEEK_PRICE = 'opt10082'
REQUEST_MONTH_PRICE = 'opt10083'
REQUEST_YEAR_PRICE = 'opt10094'
REQUEST_FUTURE_TICK = 'opt50028'
REQUEST_FUTURE_MIN = 'OPT50029'

# Real types
REAL_TYPE_STOCK_TRADED = '주식체결'
REAL_TYPE_MARKET_OPENING_TIME = '장시작시간'
REAL_TYPE_BALANCE = '잔고'

# Chejan codes
CHEJAN_EXECUTED_ORDER = '0'
CHEJAN_BALANCE = '1'

# 계좌평가잔고내역요청 (opw00018)
ITEM_CODE = '종목코드'
ITEM_NUMBER = '종목번호'
ITEM_NAME = '종목명'
PROFIT = '평가손익'
PROFIT_RATE = '수익률(%)'
PURCHASE_PRICE = '매입가'
REFERENCE_PRICE = '전일종가'
HOLDING_AMOUNT = '보유수량'
SELLABLE_AMOUNT = '매매가능수량'
CURRENT_PRICE = '현재가'
PURCHASE_SUM = '매입금액'
EVALUATION_SUM = '평가금액'
EVALUATION_FEE = '평가수수료'
TAX = '세금'
TOTAL_FEE = '수수료합'
HOLDING_RATIO = '보유비중(%)'

# 실시간미체결요청 (opt10075)
ACCOUNT_NUMBER = '계좌번호'
ORDER_NUMBER = '주문번호'
ITEM_CODE = '종목코드'
ORDER_STATE = '주문상태'
ITEM_NAME = '종목명'
ORDER_AMOUNT = '주문수량'
OPEN_AMOUNT = '미체결수량'
EXECUTED_SUM = '체결누계금액'
ORIGINAL_ORDER_NUMBER = '원주문번호'
ORDER_POSITION = '주문구분'
TRADE_POSITION = '매매구분'
TIME = '시간'
EXECUTED_ORDER_NUMBER = '체결번호'
EXECUTED_ORDER_PRICE = '체결가'
EXECUTED_ORDER_AMOUNT = '체결량'
TRANSACTION_FEE_TODAY = '당일매매수수료'
TAX_TODAY = '당일매매세금'

# 선물틱차트요청
CURRENT_PRICE = '현재가'
VOLUME = '거래량'
TRANSACTION_TIME = '체결시간'
OPEN_PRICE = '시가'
HIGH_PRICE = '고가'
LOW_PRICE = '저가'
LAST_DAY_CLOSE_PRICE = '전일종가'

# 선물옵션분차트요청
CURRENT_PRICE = '현재가'
VOLUME = '거래량'
TRANSACTION_TIME = '체결시간'
OPEN_PRICE = '시가'
HIGH_PRICE = '고가'
LOW_PRICE = '저가'
LAST_DAY_CLOSE_PRICE = '전일종가'

class FID:
    # 주식체결
    TRANSACTION_TIME = '20'
    CURRENT_PRICE = '10'
    PRICE_INCREASE_AMOUNT = '11'
    PRICE_INCREASE_RATIO = '12'
    ASK_PRICE = '27'
    BID_PRICE = '28'
    VOLUME = '15'
    ACCUMULATED_VOLUME = '13'
    HIGH_PRICE = '17'
    LOW_PRICE = '18'
    OPEN_PRICE = '16'

    # 장시작시간
    MARKET_OPERATION_STATE = '215'
    MARKET_OPERATION_REMAINING_TIME = '214'

    # 주문체결
    ACCOUNT_NUMBER = '9201'
    ORDER_NUMBER = '9203'
    ITEM_CODE = '9001'
    ITEM_NAME = '302'
    ORDER_STATE = '913'
    ORDER_AMOUNT = '900'
    ORDER_PRICE = '901'
    OPEN_AMOUNT = '902'
    ORIGINAL_ORDER_NUMBER = '904'
    ORDER_POSITION = '905'
    ORDER_EXECUTED_TIME = '908'
    TRANSACTION_TYPE = '906'
    EXECUTED_ORDER_NUMBER = '909'
    EXECUTED_PRICE = '910'
    EXECUTED_AMOUNT = '911'
    CURRENT_PRICE = '10'
    ASK_PRICE = '27'
    BID_PRICE = '28'
    TRANSACTION_FEE = '938'
    TRANSACTION_TAX = '939'

    # 잔고
    ACCOUNT_NUMBER = '9201'
    ITEM_CODE = '9001'
    ITEM_NAME = '302'
    CURRENT_PRICE = '10'
    HOLDING_AMOUNT = '930'
    PURCHASE_PRICE_AVG = '931'
    PURCHASE_SUM = '932'
    ORDERABLE_AMOUNT = '933'
    PURCHASE_AMOUNT_NET_TODAY = '945'
    BUY_OR_SELL = '946'
    PROFIT_NET_TODAY = '950'
    DEPOSIT = '951'
    REFERENCE_PRICE = '307'
    PROFIT_RATE = '8019'
    PROFIT_REALIZATION = '990'
    PROFIT_REALIZATION_RATE = '991'

# class TRADE_TYPE:
#     BID = 1
#     ASK = 2
#     CANCEL_BID = 3
#     CANCEL_ASK = 4
#     CORRECT_BID = 5
#     CORRECT_ASK = 6

# Market codes
MARKET_KOSDAQ = '10'
MARKET_KOSPI = '0'
MARKET_ETF = '8'

# Item code list
CODES = {
    '122630': 'KODEX 레버리지',
    '252670': 'KODEX 200선물인버스2X',
    '048260': '오스템임플란트',
    '101R3000': 'F 202103'
}