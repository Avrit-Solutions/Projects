import requests
import datetime as dt
from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

stock_api = os.getenv("STOCK_API")

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": stock_api,
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
response.raise_for_status()
stock_data = response.json()


yesterday = str(dt.date.today() - dt.timedelta(days=1))
day_before = str(dt.date.today() - dt.timedelta(days=2))

# Find yesterday's price
yesterday_price = float((stock_data["Time Series (Daily)"][yesterday]["4. close"]))

# Find the price two days ago
day_before_price = float((stock_data["Time Series (Daily)"][day_before]["4. close"]))

# Stock Price Difference
pos_difference = round(abs(yesterday_price - day_before_price), 2)

difference = round((pos_difference / day_before_price * 100), 2)

# If stock price difference is greater than 5% of the overall value, send a Whatsapp message via Twilio containing the
# first 3 news pieces for the company and the difference in price

if difference > 5:

    news_api = "e0b0c38beb5447d58fbdecd7abaf565d"

    news_params = {
        "q": COMPANY_NAME,
        "apiKey": news_api,
        "pageSize": 3
    }

    response = requests.get(NEWS_ENDPOINT, params=news_params)
    response.raise_for_status()
    news_data = response.json()

    all_articles = []
    all_headlines = []

    for articles in range(3):
        all_articles.append(news_data["articles"][articles]["description"])

    for headlines in range(3):
        all_headlines.append(news_data["articles"][headlines]["title"])

    txt_messages = {key: value for key, value in zip(all_headlines, all_articles)}

    account_sid = os.getenv("ACCOUNT_SID")
    auth_token = os.getenv("AUTH_TOKEN")
    phone = f"whatsapp:+{os.getenv("WHATS_APP_NUMBER")}"

    for key, value in txt_messages.items():
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=f"{STOCK_NAME}: {difference}% \n\nHeadline: {key} \n\nBrief: {value}",
            from_= phone,
            to="whatsapp:+15305144259",
        )
        print(message.status)

