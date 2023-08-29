from flask import Flask, jsonify, request
import finnhub
import os
from dotenv import load_dotenv
from flask_cors import CORS, cross_origin    

app = Flask(__name__)
CORS(app)

load_dotenv()
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)

@app.route('/getPatentNo', methods=['GET'])
def get_patent_no():
    ticker = request.args.get('ticker')
    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')
    patentRes = finnhub_client.stock_uspto_patent(ticker, _from=from_date, to=to_date)
    return jsonify(len(patentRes['data']))

@app.route('/getSentimentScore', methods=['GET'])
def get_sentiment_score():
    ticker = request.args.get('ticker')
    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')
    sentimentRes = finnhub_client.news_sentiment(ticker, from_date, to_date)
    dailyNegativeMentions = 0
    dailyPositiveMentions = 0
    averageScore = 0
    for hourlyData in sentimentRes['reddit']:
        dailyNegativeMentions += hourlyData['negativeMention']
        dailyPositiveMentions += hourlyData['positiveMention']
        averageScore += hourlyData['score']
    return jsonify({
        "dailyNegativeMentions": dailyNegativeMentions,
        "dailyPositiveMentions": dailyPositiveMentions,
        "averageScore": averageScore/24
    })

@app.route('/getInsiderSentimentScore', methods=['GET'])
def get_insider_sentiment_score():
    ticker = request.args.get('ticker')
    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')
    res = finnhub_client.stock_insider_sentiment(ticker, from_date, to_date)['data']
    avgInsiderSentiment = []
    for monthlyData in res:
        avgInsiderSentiment.append(monthlyData['mspr'])
    return jsonify(sum(avgInsiderSentiment)/len(avgInsiderSentiment))

@app.route('/')
def index():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(port=5000)
