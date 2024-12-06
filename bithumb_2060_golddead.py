import asyncio
import ccxt
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from telegram_send_alert import send_telegram_alert

# 빗썸 거래소 객체 생성
bithumb = ccxt.bithumb()

# KRW 마켓 티커 가져오기
def get_krw_tickers():
    markets = bithumb.load_markets()
    krw_tickers = [symbol for symbol in markets if symbol.endswith('/KRW')]
    return krw_tickers

# 과거 데이터 가져오기
def fetch_ohlcv(ticker, timeframe='1d', limit=60):
    try:
        ohlcv = bithumb.fetch_ohlcv(ticker, timeframe=timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df
    except Exception as e:
        print(f"데이터 가져오기 실패: {ticker}, {e}")
        return None

# 이동평균선 계산 및 크로스 감지
def detect_crosses(ticker):
    data = fetch_ohlcv(ticker, limit=60)
    if data is None or len(data) < 60:
        return None

    # 이동평균선 계산
    data['20_MA'] = data['close'].rolling(window=20).mean()
    data['60_MA'] = data['close'].rolling(window=60).mean()

    # 골든크로스 감지
    if (
        data['20_MA'].iloc[-1] > data['60_MA'].iloc[-1] and  # 현재 20일 > 60일
        data['20_MA'].iloc[-2] <= data['60_MA'].iloc[-2]    # 이전 20일 <= 60일
    ):
        return "GOLDEN"

    # 데드크로스 감지
    if (
        data['20_MA'].iloc[-1] < data['60_MA'].iloc[-1] and  # 현재 20일 < 60일
        data['20_MA'].iloc[-2] >= data['60_MA'].iloc[-2]    # 이전 20일 >= 60일
    ):
        return "DEAD"

    return None

# 메인 함수
async def main():
    while True:
        krw_tickers = get_krw_tickers()
        print(f"총 {len(krw_tickers)}개의 KRW 마켓 코인을 분석합니다.\n")
        
        for ticker in krw_tickers:
            print(f"분석 중: {ticker}")
            cross = detect_crosses(ticker)
            if cross == "GOLDEN":
                message = f"🔔 골든 크로스 발생: {ticker}\n"
                print(message)           
                await send_telegram_alert(message)
            elif cross == "DEAD":
                message = f"🔔 데드 크로스 발생: {ticker}\n"
                print(message)       
                await send_telegram_alert(message)    
            else:
                message = f"크로스 없음: {ticker}\n"
                print(message)

if __name__ == "__main__":
    asyncio.run(main())
