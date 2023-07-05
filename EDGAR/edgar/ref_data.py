import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import yfinance as yf

def get_sp100():
    #Get request and HTML parsing of S&P 100 tickers
    url = 'https://en.wikipedia.org/wiki/S%26P_100'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    table = soup.find('table',{'class':'wikitable sortable'})
    #Creation of ticker list
    tickers = []
    for row in table.find_all('tr')[1:]:
        ticker = row.find_all('td')[0].text.strip()
        tickers.append(ticker)

    return tickers


def get_yahoo_data(start_date, end_date, ticker):

    data = pd.DataFrame()
    #Download all financial data for the given ticker between two dates
    ticker_data = yf.download(ticker, start = start_date, end = end_date)
    ticker_data['ticker_symbol'] = ticker
    data = pd.concat([data, ticker_data], axis = 0)
    data.reset_index(inplace = True)
    data.rename(columns = {'Date':'date', 'High':'high', 'Low':'low','Close':'price', 'Volume':'volume'}, inplace = True)
    data.set_index('date', inplace = True)
    #Calculate % returns in investment across given intervals
    for days in [1,2,3,5,10]:
        data[f'{days}daily_return'] = data['price'].pct_change(days) 
    
    data.drop(columns = ['Adj Close', 'Open'], inplace = True)
    return data


def get_sentiment_word_dict():

    df = pd.read_csv(r'Loughran-McDonald_MasterDictionary_1993-2021.csv')
    #Create a list for each word type
    pos_list = []
    neg_list = []
    uncertain_list = []
    lit_list = []
    strong_list = []
    weak_list = []
    constraining_list = []
    #Iterate through the Loughran-Mcdonald Dictionary 
    for index,row in df.iterrows():
        #Append a word to a sentiment list if it is classed as such
        if row['Positive'] > 0:
            pos_list.append(row['Word'].lower())           
        if row['Negative'] > 0:
            neg_list.append(row['Word'].lower())
        if row['Uncertainty'] > 0:
            uncertain_list.append(row['Word'].lower())
        if row['Litigious'] > 0:
            lit_list.append(row['Word'].lower())
        if row['Strong_Modal'] > 0:
            strong_list.append(row['Word'].lower())
        if row['Weak_Modal'] > 0:
            weak_list.append(row['Word'].lower())
        if row['Constraining'] > 0:
            constraining_list.append(row['Word'].lower())
    
    #Create a sentiment dictionary using the list of words
    sentiment_dictionary = {'Positive':pos_list , 
                            'Negative':neg_list , 
                            'Uncertainty':uncertain_list,
                            'Litigious':lit_list,
                            'Strong_Modal':strong_list,
                            'Weak_Modal':weak_list,
                            'Constraining':constraining_list
                            }
    
    return sentiment_dictionary