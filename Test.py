import requests

API_KEY = "d18v5i1r01qkcat52pbgd18v5i1r01qkcat52pc0"  # Replace with your actual API key

def get_latest_news(symbol, api_key):
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "NEWS_SENTIMENT",
        "tickers": symbol,
        "apikey": api_key
    }
    response = requests.get(url, params=params)
    data = response.json()
    if "feed" in data:
        return data["feed"]
    else:
        return data.get("Note", "No news found.")

if __name__ == "__main__":
    symbol = input("Enter stock symbol: ").upper()
    if symbol == "":
        print("ENTER VALID SYMBOL!")
    elif not symbol.isalpha():
        print("SYMBOL MUST BE ALPHABETIC!")
    elif not symbol: 
        exit()
    news = get_latest_news(symbol, API_KEY)
    if isinstance(news, list):
        for article in news:
            print(f"Title: {article.get('title')}")
            print(f"Date: {article.get('time_published')}")
            print(f"Summary: {article.get('summary')}")
            print(f"Link: {article.get('url')}\n")
    else:
        print(news)
