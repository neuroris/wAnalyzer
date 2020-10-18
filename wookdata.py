DEPOSIT = '예수금'
WITHDRAWABLE = '출금가능금액'
TOTAL_PURCHASE_SUM = '총매입금액'
TOTAL_PROFIT_EVALUATED = '총평가손익금액'
TOTAL_PROFIT_RATE = '총수익률(%)'

ACCOUNT_NUMBER = '계좌번호'
PASSWORD = '비밀번호'
PASSWORD_MEDIA_TYPE = '비밀번호입력매체구분'
INQUIRY_TYPE = '조회구분'
CONCLUSION_TYPE = '체결구분'
TRADING_TYPE = '매매구분'
CORRECTED_PRICE_TYPE = '수정주가구분'

ITEM_CODE = '종목코드'
ITEM_NUMBER = '종목번호'
ITEM_NAME = '종목명'
PURCHASE_AMOUNT = '보유수량'
PURCHASE_PRICE = '매입가'
CURRENT_PRICE = '현재가'
PURCHASE_SUM = '매입금액'
PROFIT_RATE = '수익률(%)'
SELLABLE_AMOUNT = '매매가능수량'
ORDER_NUMBER = '주문번호'
ORDER_STATE = '주문상태'
ORDER_AMOUNT = '주문수량'
ORDER_PRICE = '주문가격'
ORDER_TYPE = '주문구분'
UNCONCLUDED_AMOUNT = '미체결수량'
CONCLUDED_AMOUNT = '체결량'
REFERENCE_DATE = '기준일자'
DATE = '일자'

REQUEST_DEPOSIT_INFO = 'opw00001'
REQUEST_PORTFOLIO_INFO = 'opw00018'
REQUEST_UNCONCLUDED_ORDER = 'opt10075'
REQUEST_MINUTE_PRICE = 'opt10080'
REQUEST_DAY_PRICE = 'opt10081'

REAL_MARKET_OPENING_TIME = '장시작시간'
REAL_CONCLUSION_TIME = '체결시간'

TIC_RANGE = '틱범위'
ONE_MIN = '1:1분'

TRANSACTION_TIME = '체결시간'
OPENING_PRICE = '시가'
HIGHEST_PRICE = '고가'
LOWEST_PRICE = '저가'

ALL = '0'
UNCONCLUDED = '1'
CONCLUDED = '2'
SELL = '1'
BUY = '2'

MARKET_KOSDAQ = '10'
MARKET_KOSPI = '0'
MARKET_ETF = '8'


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
    HIGHEST_PRICE = ' 17'
    LOWEST_PRICE = '18'
    OPENING_PRICE = '16'

    # 장시작시간
    MARKET_OPERATION_STATE = '215'

    # 주문체결
    ACCOUNT_NUMBER = '9201'
    ORDER_NUMBER = '9203'
    ITEM_CODE = '9001'
    ITEM_NAME = '302'
    ORDER_STATE = '913'
    ORDER_AMOUNT = '900'
    ORDER_PRICE = '901'
    UNCONCLUDED_AMOUNT = '902'
    ORIGINAL_ORDER_NUMBER = '904'
    ORDER_TYPE = '905'
    ORDER_TRANSACTION_TIME = '908'
    TRANSACTION_PRICE = '910'
    TRANSACTION_AMOUNT = '911'
    # CURRENT_PRICE = '10'
    # ASK_PRICE = '27'
    # BID_PRICE = '28'

    # 잔고
    HOLDING_AMOUNT = '930'
    PURCHASE_PRICE = '931'
    PURCHASE_SUM = '932'
    ORDERABLE_AMOUNT = '933'
    ASK_BID = '946'


class TRADE_TYPE:
    BID = 1
    ASK = 2
    CANCEL_BID = 3
    CANCEL_ASK = 4
    CORRECT_BID = 5
    CORRECT_ASK = 6

class ORDER_TYPE:
    LIMIT = '00'
    MARKET = '03'
    CONDITIONAL = '05'
    COVER = '06'
    MARGINAL = '07'
    BEFORE = '61'
    CLOSING = '62'
    AFTER = '81'

CODE_KODEX_LEVERAGE = '122630'
CODE_KODEX_INVERSE_2X = '252670'
NAME_KODEX_LEVERAGE = 'KODEX 레버리지'
NAME_KODEX_INVERSE_2X = 'KODEX 인버스2X'