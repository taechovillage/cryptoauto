import ccxt
import requests
import time
import asyncio
from telegram import Bot
from telegram.constants import ParseMode
from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup

# .env 파일 로드
load_dotenv('config.env')

# 텔레그램 봇 설정
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
bot = Bot(token=TELEGRAM_TOKEN)

# 알림 함수 (비동기)
async def send_telegram_alert(message):
    await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode=ParseMode.HTML)

# KRW 환율 가져오기
def get_usd_to_krw_rate():

    # 네이버 금융 환율 정보 가져오기
    response = requests.get("https://finance.naver.com/marketindex/exchangeList.naver")
    soup = BeautifulSoup(response.content, "html.parser")

    # 테이블의 각 행 가져오기
    rows = soup.find_all("tr")

    # USD 정보만 출력
    for row in rows:
        columns = row.find_all("td")

        # 필요한 열 수 확인 (7개 이상인지 체크)
        if len(columns) >= 7:
            country = columns[0].text.strip()  # 통화명
        
            if "미국 USD" in country:  # 미국 USD만 필터링
                exchange_rate = columns[1].text.strip()  # 매매기준율 (기준환율)
                exchange_rate = exchange_rate.replace(',', '')  # 쉼표 제거
                return float(exchange_rate)  # 문자열을 float로 변환

def get_bithumb_usdt_price():
    bithumb = ccxt.bithumb()
    ticker = bithumb.fetch_ticker('USDT/KRW')
    return ticker['last']

async def main():
    while True:
        try:
            bithumb_price = get_bithumb_usdt_price()  
            usd_to_krw = get_usd_to_krw_rate()
            #get_usd_to_krw_rate()
            #usd_to_krw = 1405
        
            print(bithumb_price)
            print(usd_to_krw)
        
            difference = ((bithumb_price-usd_to_krw)/usd_to_krw)*100
            print(f"USDT Price Difference Percent: {difference:.2f} %") 
                
            # 알림 조건
            if difference <= -1.5:
                message = (f"🚨 Alert! USDT Price Difference(Bithumb-bybit): {difference:.2f}%\n")
                
                await send_telegram_alert(message)

        except Exception as e:
            print(f"Error: {e}")

        await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(main())