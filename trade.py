import ccxt
import pyupbit
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv('bithumbconfig.env')
load_dotenv('upbitconfig.env')

# API 키 설정
BITHUMB_API_KEY = os.getenv('BITHUMB_API_KEY')
BITHUMB_API_SECRET = os.getenv('BITHUMB_API_SECRET')
UPBIT_API_KEY = os.getenv('UPBIT_API_KEY')
UPBIT_API_SECRET = os.getenv('UPBIT_API_SECRET')

# 빗썸 객체 설정
bithumb = ccxt.bithumb({
    'apiKey': BITHUMB_API_KEY,
    'secret': BITHUMB_API_SECRET,
})

# 업비트 객체 생성
upbit = pyupbit.Upbit(UPBIT_API_KEY, UPBIT_API_SECRET)

ticker ='USDT/KRW'

# 빗썸 매수 함수 (시장가 주문)
def bithumb_buy(ticker, amount):
    try:
        order = bithumb.create_market_buy_order(ticker, amount)
        print(f"매수 주문 완료: {order}")
    except Exception as e:
        print(f"매수 주문 실패: {e}")

# 빗썸 매도 함수 (시장가 주문)
def bithumb_sell(ticker, amount):
    try:
        order = bithumb.create_market_sell_order(ticker, amount)
        print(f"매도 주문 완료: {order}")
    except Exception as e:
        print(f"매도 주문 실패: {e}")

# 업비트 매수 함수 (시장가 주문)
def upbit_buy(ticker, amount):
    try:
        order = upbit.buy_market_order(ticker, amount)
        print(f"업비트 매수 주문 완료: {order}")
    except Exception as e:
        print(f"업비트 매수 주문 실패: {e}")

# 업비트 매도 함수 (시장가 주문)
def upbit_sell(ticker, amount):
    try:
        order = upbit.sell_market_order(ticker, amount)
        print(f"업비트 매도 주문 완료: {order}")
    except Exception as e:
        print(f"업비트 매도 주문 실패: {e}")        

# 빗썸 잔고 조회
def bithumb_get_balance(currency):
    try:
        balance = bithumb.fetch_balance()
        currency_balance = balance[currency]['free']
        print(f"{currency} 잔고: {currency_balance}")
        return currency_balance
    except Exception as e:
        print(f"잔고 조회 실패: {e}")

# 업비트 잔고 조회
def upbit_get_balance(currency):
    try:
        balance = upbit.get_balance(currency)
        print(f"{currency} 잔고: {balance}")
        return balance
    except Exception as e:
        print(f"업비트 잔고 조회 실패: {e}")
        return 0

# 모든 티커 조회 함수
def fetch_bithumb_tickers():
    try:
        # 빗썸에서 모든 시장 정보 가져오기
        markets = bithumb.load_markets()
        tickers = bithumb.fetch_tickers()
        
        print(f"총 {len(markets)}개의 티커가 거래 중입니다.\n")
        
        for symbol in tickers:
            ticker = tickers[symbol]
            print(f"종목: {symbol}")

    except Exception as e:
        print(f"티커 조회 실패: {e}")  

# 업비트 KRW 마켓 티커 조회
def fetch_upbit_tickers():
    try:
        tickers = pyupbit.get_tickers(fiat="KRW")
        print(f"업비트 KRW 마켓에 {len(tickers)}개의 티커가 있습니다:\n")
        for ticker in tickers:
            print(f"종목: {ticker}")
    except Exception as e:
        print(f"업비트 티커 조회 실패: {e}")        

# def main():
#     print("빗썸 거래소 전체 티커 조회 프로그램\n")
#     fetch_all_tickers()

# if __name__ == "__main__":
#     main()