import ccxt
import requests
import time
import asyncio
from telegram import Bot
from telegram.constants import ParseMode
from dotenv import load_dotenv
import os

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
    url = "https://api.exchangerate-api.com/v4/latest/USD"
    response = requests.get(url)
    data = response.json()
    
    usd_to_krw = data['rates']['KRW']
    return usd_to_krw

def get_bithumb_usdt_price():
    bithumb = ccxt.bithumb()
    ticker = bithumb.fetch_ticker('USDT/KRW')
    return ticker['last']

async def main():
    while True:
        try:
            bithumb_price = get_bithumb_usdt_price()  
            usd_to_krw = get_usd_to_krw_rate()

        
            print(bithumb_price)
            print(usd_to_krw)
        
            difference = ((bithumb_price-usd_to_krw)/usd_to_krw)*100
            print(f"USDT Price Difference Percent: {difference:.2f} %") 
                
            # 알림 조건
            if difference >= -1:
                message = (f"🚨 Alert! USDT Price Difference(Bithumb-bybit): {difference:.2f}%\n")
                
                await send_telegram_alert(message)

        except Exception as e:
            print(f"Error: {e}")

        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())