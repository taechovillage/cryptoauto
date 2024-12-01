import ccxt
import requests
import time

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

def main():
    while True:
        bithumb_price = get_bithumb_usdt_price()  
        usd_to_krw = get_usd_to_krw_rate()

    
        print(bithumb_price)
        print(usd_to_krw)
    
        difference = ((bithumb_price-usd_to_krw)/usd_to_krw)*100
        print(f"USDT Price Difference Percent: {difference:.2f} %") 
        time.sleep(1) 

if __name__ == "__main__":
    main()