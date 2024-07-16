import requests
import datetime as dt
import pytz
import os

PRICE_ENDPOINT = "https://data-api.binance.vision/api/v3/ticker/24hr"

parameters = {
    "symbol": "BTCUSDT"
}

# create a list of closing prices from 2 days before
response = requests.get(url=PRICE_ENDPOINT, params=parameters)
response.raise_for_status()

price_data = response.json()

previous_close_price = format(round(float(price_data["prevClosePrice"]),3), ",")
last_price = format(round(float(price_data["lastPrice"]),3), ",")
amount_changed = format(float(price_data["priceChange"]), ",")
percent_changed = float(price_data["priceChangePercent"])

message = f"> **Daily ₿itcoin Price Report** - {dt.datetime.now(pytz.timezone('Asia/Ho_Chi_Minh')).strftime("%A, %B %d")}\n\n"

if percent_changed > 0 and abs(percent_changed) > 5: 
    message += f"🟩   **+{percent_changed}%**\t|\t**+${amount_changed}**   ❗❗❗\n\n- Current price: **${last_price}**\n\n- Yesterday's close: **${previous_close_price}**"
elif percent_changed < 0 and abs(percent_changed) > 5: 
    message += f"🟥   **{percent_changed}%\t|\t-${abs(amount_changed)}**   ❗❗❗\n\n- Current price: **${last_price}**\n\n- Yesterday's close: **${previous_close_price}**"
elif percent_changed > 0:
    message += f"🟩   **+{percent_changed}%**\t|\t**+${amount_changed}**\n\n- Current price: **${last_price}**\n\n- Yesterday's close: **${previous_close_price}**"
elif percent_changed < 0:
    message += f"🟥   **{percent_changed}%\t|\t-${abs(amount_changed)}**\n\n- Current price: **${last_price}**\n\n- Yesterday's close: **${previous_close_price}**"
else:
    message += f"⬜   **{int(percent_changed)}%**"

discord_channel_url = "https://discord.com/api/v9/channels/1258325947116163134/messages"
headers = {
    "Authorization": os.environ.get("DISCORD_AUTH_KEY")
}  # auth key needed to send messages through discord

payload = {"content": message + "\n\n-----------------------------------\n"}

requests.post(discord_channel_url, payload, headers=headers)
