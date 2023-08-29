# %%
# Step 0: Setup the environment 
!pip install finnhub-python
!pip install python-dotenv

# %%
import finnhub
import os
from dotenv import load_dotenv

load_dotenv()
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)

# %%
# Notes:
# There's a lot of data present, but its hardly digestable for the average user. 
# We assign scores such as innovation score, profitability score, social media presence, growth score, etc. to each company
# It's kind of like ranking universities, the data is not 100% accurate or transparent, but it gives a good idea of the company's performance
# We can use this data to rank companies and then use that to rank the stocks of those companies, and generate learning points for each companies
# I'll illustrate this with an example below

# Respective APIs for each of the scores:
# Innovation Score: USPTO patent count 
# Profitability Score: Earnings Calendar (revenue actual - revenue estimate) (Update: Not available)
# Social Media Presence: Sentiment 
# Growth Score: Financial reports
# Insider Trends: Insider Sentiment + Insider Trading

# Note: USPTO and earnings calendar aren't updated this year, may need other APIs.

# %%
startDate = "2022-02-01"
endDate = "2022-06-01"
patentRes = finnhub_client.stock_uspto_patent('NVDA', _from=startDate, to=endDate) 
print(len(patentRes['data'])) #169 patents applied by NVDA over the last year 

# Get number of patents registered by a company within a certain time period.
def get_patent_no(ticker, from_date, to_date):
    patentRes = finnhub_client.stock_uspto_patent(ticker, _from=from_date, to=to_date)
    return len(patentRes['data'])

# Get innovative score relative to peers in the same industry
peers = finnhub_client.company_peers('NVDA')
peerPatentCount = []
for peer in peers:
    peerPatentCount.append(get_patent_no(peer, startDate, endDate))
dictionary = dict(zip(peers, peerPatentCount))

# Sort by patents applied for, and you see why NVDA > AMD
sorted_dict = dict(sorted(dictionary.items(), key=lambda item: item[1], reverse=True))
print(sorted_dict)


# %%
# Now, we want to collate all these scores under the company name, and then pick the outstanding variables (> 2s.d.) to display the learning points (why they're trending).
# Step 1: Get the list of tickers from the S&P 500
# Step 2: Get the scores for each of the tickers (using a single function that takes in all the scores arguments needed)
# Step 3: Collate the scores under the company name
# Step 4: Identify outliers in scores and display the learning points
# Note: For industry analysis (which is a direction we can approach the education from,) we can use the 'Peers' API to compare scores between top dogs, and let users see the difference in scores.

# %%
# Get number of patents registered by a company within a certain time period.
def get_patent_no(ticker, from_date, to_date):
    patentRes = finnhub_client.stock_uspto_patent(ticker, _from=from_date, to=to_date)
    return len(patentRes['data'])

# Get the sentiment score of a company within a certain time period. (daily for now)
def get_sentiment_score(ticker, from_date, to_date):
    sentimentRes = finnhub_client.news_sentiment(ticker, from_date, to_date)
    dailyNegativeMentions = 0
    dailyPositiveMentions = 0
    averageScore = 0
    for hourlyData in sentimentRes['reddit']:
        dailyNegativeMentions += hourlyData['negativeMention']
        dailyPositiveMentions += hourlyData['positiveMention']
        averageScore += hourlyData['score']
    return dailyNegativeMentions, dailyPositiveMentions, averageScore/24

# Get the insider sentiment score of a company within a certain time period. (monthly) (from -100 to 100)
def get_insider_sentiment_score(ticker, from_date, to_date):
    res = finnhub_client.stock_insider_sentiment(ticker, from_date, to_date)['data']
    avgInsiderSentiment = []
    for monthlyData in res:
        avgInsiderSentiment.append(monthlyData['mspr'])
    return sum(avgInsiderSentiment)/len(avgInsiderSentiment)

# %%
print(get_insider_sentiment_score('NVDA', startDate, endDate))


