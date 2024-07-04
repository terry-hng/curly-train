import requests
import datetime as dt
import pytz
import os

TICKER = "BTC"
NAME = "Bitcoin"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

ALPHAVANTAGE_API_KEY = os.environ.get("ALPHAVANTAGE_API_KEY")
NEWSAPI_API_KEY = os.environ.get("NEWSAPI_API_KEY")


alpha_vantage_params = {
    "function": "DIGITAL_CURRENCY_DAILY",
    "symbol": TICKER,
    "market": "USD",
    "apikey": NEWSAPI_API_KEY,
}

price_data = requests.get(url=STOCK_ENDPOINT, params=alpha_vantage_params).json()

# create a list of closing prices from 2 days before
closing_prices_list = [
    float(prices["4. close"])
    for (_, prices) in price_data["Time Series (Digital Currency Daily)"].items()
][:2]

amount_changed = round((closing_prices_list[0] - closing_prices_list[1]),2)
percent_changed = round(((closing_prices_list[0] / closing_prices_list[1]) - 1) * 100,2)

news_api_params = {"apiKey": NEWSAPI_API_KEY, "q": "bitcoin", "pageSize": 3} # get 3 latest news about bitcoin

news_list = [
    {
        "Headline": article["title"],
        "Link": article["url"],
        "Publish Date": article["publishedAt"].split("T")[0],
    }
    for article in requests.get(url=NEWS_ENDPOINT, params=news_api_params).json()[
        "articles"
    ]
]


message = f"> **Daily ₿itcoin Price Report** - {dt.datetime.now(pytz.timezone('Asia/Ho_Chi_Minh')).strftime("%A, %B %d")}\n\n"

if percent_changed > 0 and abs(percent_changed) > 5: 
    message += f"🟩   **+{percent_changed}%**\t|\t**+${amount_changed}**   ❗❗❗\n\n- Today's price: **${closing_prices_list[0]}**\n\n- Yesterday's price: **${closing_prices_list[1]}**"
elif percent_changed < 0 and abs(percent_changed) > 5: 
    message += f"🟥   **{percent_changed}%\t|\t-${abs(amount_changed)}**   ❗❗❗\n\n- Today's price: **${closing_prices_list[0]}**\n\n- Yesterday's price: **${closing_prices_list[1]}**"
elif percent_changed > 0:
    message += f"🟩   **+{percent_changed}%**\t|\t**+${amount_changed}**\n\n- Today's price: **${closing_prices_list[0]}**\n\n- Yesterday's price: **${closing_prices_list[1]}**"
elif percent_changed < 0:
    message += f"🟥   **{percent_changed}%\t|\t-${abs(amount_changed)}**\n\n- Today's price: **${closing_prices_list[0]}**\n\n- Yesterday's price: **${closing_prices_list[1]}**"
else:
    message += f"⬜   **{int(percent_changed)}%**"


if abs(percent_changed) > 5:
    message += f"❗\n\n- **Headline**: `{news_list[0]["Headline"]}`\n\n- **Article**: {news_list[0]["Link"]}\n\n- **Publish Date**: {news_list[0]["Publish Date"]}"


discord_channel_url = "https://discord.com/api/v9/channels/1258325947116163134/messages"
headers = {
    "Authorization": os.environ.get("DISCORD_AUTH_KEY")
}  # auth key needed to send messages through discord

payload = {"content": message + "\n\n-----------------------------------\n"}

requests.post(discord_channel_url, payload, headers=headers)
