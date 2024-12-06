from telegram import Bot
from telegram.constants import ParseMode
from dotenv import load_dotenv
import os

# .env 파일에서 환경 변수 로드
load_dotenv('config.env')

# 텔레그램 봇 설정
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
bot = Bot(token=TELEGRAM_TOKEN)


# 알림 함수 (비동기)
async def send_telegram_alert(message):
    await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode=ParseMode.HTML)