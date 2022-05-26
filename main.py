import requests
from twilio.rest import Client
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
account_sid = "Get from twilio API"
auth_token = "Get from twilio API"

STOCK_API_KEY = "Type your stocks API"
NEWS_API_KEY = "Type your news API"

# 1. Get yesterday's closing stock price.

parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY
}
response = requests.get(STOCK_ENDPOINT, params=parameters)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]

yesterday_closing_price = data_list[0]["4. close"]

# 2. Get the day before yesterday's closing stock price

day_before_yesterday_price = data_list[1]["4. close"]

# 3. Find the difference between 1 and 2

difference = float(yesterday_closing_price) - float(day_before_yesterday_price)
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

# 4. Find percentage difference in price between closing price yesterday and day before.

percentage_difference = round((difference / float(yesterday_closing_price)) * 100)
print(percentage_difference)

# 5. If TODO4 percentage is greater than 4 then get news from News API.
# 6. Use the News API to get articles related to the COMPANY_NAME.
if abs(percentage_difference) > 4:
    news_params = {
        "apikey": NEWS_API_KEY,
        "q": COMPANY_NAME
    }
    response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = response.json()["articles"]

# 7. Use Python slice operator to create a list that contains the first 3 articles.

three_articles = articles[:3]

# 8. Create a new list of the first three article headline and description.

format_articles = [f"{STOCK_NAME}: {up_down}{percentage_difference}%\nHeadline: {article['title']}. \nBrief: "
                   f"{article['description']}" for article in three_articles]
# 9. Send each article as a separate message via Twilio.

client = Client(account_sid, auth_token)
for article in format_articles:
    message = client.messages.create(
            body=article,
            from_='number from twilio API',
            to='number we want to send the sms'
        )