from flask import Flask, render_template_string, request
import requests

API_KEY = "d18v5i1r01qkcat52pbgd18v5i1r01qkcat52pc0"  # Replace with your actual API key

app = Flask(__name__)

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

HTML_TEMPLATE = """
<!doctype html>
<title>Stock News</title>
<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
<h1>Get Latest Analyst News for a Stock</h1>
<form method="post">
    <input name="symbol" placeholder="Enter stock symbol" value="{{ symbol|default('') }}">
    <input type="submit" value="Get News">
</form>
{% if error %}
    <p style="color:red;">{{ error }}</p>
{% endif %}
{% if news %}
    <h2>Analyst News for {{ symbol.upper() }}</h2>
    {% for article in news %}
        <div style="margin-bottom:20px;">
            <strong><h3>{{ article.title }}</h3></strong>
            <em>{{ article.time_published }}</em><br>
            <p>{{ article.summary }}</p>
            <a href="{{ article.url }}" target="_blank">Read more</a>
        </div>
    {% else %}
        <p>No analyst news found.</p>
    {% endfor %}
{% endif %}
"""

@app.route("/", methods=["GET", "POST"])
def index():
    news = []
    error = None
    symbol = ""
    if request.method == "POST":
        symbol = request.form.get("symbol", "").upper()
        if not symbol:
            error = "ENTER VALID SYMBOL!"
        elif not symbol.isalpha():
            error = "SYMBOL MUST BE ALPHABETIC!"
        else:
            all_news = get_latest_news(symbol, API_KEY)
            if isinstance(all_news, list):
                news = [article for article in all_news if "analyst" in article.get('title', '').lower()]
            else:
                error = all_news
    return render_template_string(HTML_TEMPLATE, news=news, error=error, symbol=symbol)

if __name__ == "__main__":
    app.run(debug=True)